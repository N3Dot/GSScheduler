from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional, Tuple, Callable
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from enum import Enum
from datetime import datetime
from kivy.utils import platform
from io import BytesIO
import uuid
import random
import time
import json
import os
import qrcode
import base64
import gzip
if __name__ == "__main__":
    from Database import Item, Rarity, Items
else:
    from Backend.Database import Item, Rarity, Items, Achievements

# Định nghĩa BASE_DATE và hàm tiện ích
BASE_DATE = datetime(1900, 1, 1)

def to_basedate_time(dt: datetime) -> datetime:
    """Chuyển mọi datetime về BASE_DATE, chỉ giữ lại giờ và phút."""
    return BASE_DATE.replace(hour=dt.hour, minute=dt.minute, second=0, microsecond=0)

class Character(EventDispatcher):
    """
    Đại diện cho người dùng trong ứng dụng.
    Lớp này quản lý tất cả các chỉ số, tài sản, trang bị, và tiến trình của nhân vật.
    """
    name = StringProperty("Nguyễn Văn A")
    level = NumericProperty(1)
    xp = NumericProperty(0)
    xp_to_next_level = NumericProperty(100)
    hp = NumericProperty(50)
    max_hp = NumericProperty(50)
    dex = NumericProperty(1)  # Khéo léo -> Tăng XP nhận được
    int = NumericProperty(1)  # Trí tuệ -> Giảm hình phạt
    luk = NumericProperty(1)  # May mắn -> Tăng vàng nhận được
    available_points = NumericProperty(0)  # Điểm cộng có sẵn để tăng chỉ số
    gold = NumericProperty(10)

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.equipment: List[Item] = []  # Danh sách các vật phẩm đã trang bị
        self.inventory: List[Item] = []  # Kho đồ chứa các vật phẩm
        self.unlocked_achievements = set()  # Tập hợp các ID thành tích đã mở khóa
        
        # Chỉ số cấp độ và kinh nghiệm
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100
        
        # Chỉ số chiến đấu và thuộc tính
        self.hp: int = 50
        self.max_hp: int = 50
        self.dex: int = 1  # Khéo léo -> Tăng XP nhận được
        self.int: int = 1  # Trí tuệ -> Giảm hình phạt
        self.luk: int = 1  # May mắn -> Tăng vàng nhận được
        self.available_points: int = 0 # Điểm cộng có sẵn để tăng chỉ số
        
        # Tài sản
        self.gold: int = 10
        print(f"Nhân vật '{self.name}' đã được tạo với {self.xp} XP và {self.gold} Vàng.")

    def check_negative_stats(self):
        """
        Kiểm tra các chỉ số nếu bị âm thì đặt lại thành 0.
        """
        for stat in ['hp','max_hp','dex', 'int', 'luk', 'gold', 'xp']:
            value = getattr(self, stat, 0)
            if value < 0:
                setattr(self, stat, 0)

    def check_level_up(self):
        """
        Kiểm tra nếu nhân vật đủ XP để lên cấp.
        Lặp cho đến khi không đủ XP để lên cấp nữa.
        """
        leveled_up = False
        while self.xp >= self.xp_to_next_level:
            leveled_up = True
            self.xp -= self.xp_to_next_level
            self.level += 1
            self.available_points += 1
            # Lượng XP cần cho cấp tiếp theo tăng theo cấp số nhân
            self.xp_to_next_level = int(self.xp_to_next_level * 1.25)
            
            print(f"{self.name} đã lên cấp {self.level}!")
        return leveled_up

    def add_achievement(self, achievement_id: str):
        """Thêm ID của một thành tích đã mở khóa vào danh sách."""
        if achievement_id not in self.unlocked_achievements:
            self.unlocked_achievements.add(achievement_id)
            print(f"🏆 THÀNH TÍCH MỚI ĐƯỢC MỞ KHÓA: {achievement_id}")

    def show_stats(self):
        """Hiển thị các chỉ số hiện tại của nhân vật một cách trực quan."""
        print("\n--- TRẠNG THÁI NHÂN VẬT ---")
        print(f"Tên: {self.name}")
        print(f"Cơ bản: HP({self.hp}/{self.max_hp}), DEX({self.dex}), INT({self.int}), LUK({self.luk})")
        print(f"Trang bị: {[item.name for item in self.equipment] or ['Không có']}")
        print(f"Kho đồ: {[item.name for item in self.inventory] or ['Trống']}")
        print(f"Thành tích: {list(self.unlocked_achievements) or ['Chưa có']}")
        print("--------------------------\n")
    
    def use_item(self, item: Item):
        """
        Xử lý logic khi nhân vật sử dụng vật phẩm này.
        """
        print(f"{self.name} đã sử dụng {item.name}.")
        # Áp dụng stat bonuses từ on_use_effect
        if item.on_use_effect:
            for stat, bonus in item.on_use_effect.items():
                if hasattr(self, stat):
                    current_value = getattr(self, stat)
                    setattr(self, stat, current_value + bonus)

        # Xóa vật phẩm khỏi kho đồ của nhân vật nếu nó là loại tiêu hao
        if item in self.inventory:
            self.inventory.remove(item)
    
    def equip(self, item: Item):
        # Kiểm tra item có trong inventory không
        if item not in self.inventory:
            return f"Không tìm thấy '{item.name}' trong kho đồ."

        # Nếu đã có trang bị cùng category thì unequip nó trước
        existing_equipped = next((i for i in self.equipment if i.category == item.category), None)
        if existing_equipped:
            print(f"Đang có trang bị '{existing_equipped.name}' cùng loại. Gỡ ra trước khi trang bị '{item.name}'.")
            Flag = self.unequip(existing_equipped)
            if isinstance(Flag, str):
                return Flag

        # Trang bị item mới
        self.equipment.append(item)
        self.inventory.remove(item)

        # Tăng chỉ số
        for stat, bonus in item.on_use_effect.items():
            if stat == 'hp':
                self.max_hp += bonus
            elif hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + bonus)

        print(f"Đã trang bị '{item.name}'.")
        self.validate_health()
        return True

    def unequip(self, item: Item):
        # Kiểm tra item có trong equipment không
        if item not in self.equipment:
            return f"'{item.name}' không có trong trang bị."

        # Ước lượng tác động của việc gỡ bỏ item
        simulated_max_hp = self.max_hp
        simulated_hp = self.hp

        for stat, bonus in item.on_use_effect.items():
            if stat == 'hp':
                simulated_hp -= bonus
            elif stat == 'max_hp':
                simulated_max_hp -= bonus  # Trong trường hợp bạn dùng 'max_hp' riêng biệt

        # Kiểm tra nếu max_hp hoặc hp sau khi gỡ <= 0
        if simulated_max_hp <= 0 or simulated_hp <= 0:
            return f"Không thể gỡ '{item.name}' vì sẽ khiến HP bị âm hoặc bằng 0!"

        # Gỡ trang bị
        self.equipment.remove(item)
        self.inventory.append(item)

        # Giảm chỉ số
        for stat, bonus in item.on_use_effect.items():
            if stat == 'hp':
                self.max_hp -= bonus
            elif hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) - bonus)

        print(f"Đã gỡ trang bị '{item.name}'.")
        self.check_negative_stats()
        self.validate_health()
        return True

    def validate_health(self):
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class Shop:
    def __init__(self, Character: Character):
        self.current_stock: List[Item] = []
        for key in Items:
            item_to_add = Items[key]
            if (item_to_add.category == "Tiêu Hao") or (item_to_add not in Character.inventory and item_to_add not in Character.equipment):
                self.current_stock.append(Items[key])
            else:
                print(f"Item not added: {item_to_add}")
        self.current_stock.sort(key=lambda x: x.rarity.value, reverse=True)

class RewardSystem:
    """
    Quản lý việc tính toán và trao thưởng/phạt cho nhân vật.
    Lớp này tách biệt logic thưởng ra khỏi các hệ thống khác.
    """
    def __init__(self):
        self.reward_types: List[str] = ["xp", "gold", "item", "achievement"]
        self.public_messages = {'xp': 0, 'gold': 0}

    def calculate_xp(self, character: Character, difficulty: int) -> int:
        """Tính toán lượng XP nhận được dựa trên độ khó và chỉ số DEX."""
        base_xp = difficulty * 20
        modifier = 1 + (character.dex * 0.02)  # Mỗi điểm DEX tăng 2% XP
        final_xp = int(base_xp * modifier)
        return final_xp

    def calculate_currency(self, character: Character, difficulty: int) -> int:
        """Tính toán lượng vàng nhận được dựa trên độ khó và chỉ số LUK."""
        base_gold = difficulty * 10
        modifier = 1 + (character.luk * 0.02)  # Mỗi điểm LUK tăng 2% vàng
        final_gold = int(base_gold * modifier)
        return final_gold

    def grant_reward(self, character: Character, reward: Dict[str, Any]):
        """
        Trao một phần thưởng cụ thể cho nhân vật dựa trên một dictionary.

        Args:
            character (Character): Nhân vật nhận thưởng.
            reward (Dict): Từ điển chứa thông tin phần thưởng, ví dụ:
                           {"type": "xp", "amount": 100}
                           {"type": "item", "item_object": <Item object>}
        """
        reward_type = reward.get("type")
        if not reward_type or reward_type not in self.reward_types:
            print(f"Cảnh báo: Loại phần thưởng '{reward_type}' không hợp lệ.")
            return

        try:
            if reward_type == "xp":
                amount = int(reward["amount"])
                character.xp += amount
                self.public_messages['xp'] += amount
                print(f"   + {amount} XP.")
                character.check_level_up() # Tự động kiểm tra lên cấp
            elif reward_type == "gold":
                amount = int(reward["amount"])
                character.gold += amount
                self.public_messages['gold'] += amount
                print(f"   + {amount} Vàng.")
            elif reward_type == "item":
                item = reward.get("item_object")
                if isinstance(item, Item):
                    character.inventory.append(item)
                    print(f"   + Vật phẩm: {item.name}.")
                else:
                    print("Cảnh báo: 'item_object' trong phần thưởng không phải là một Item hợp lệ.")
        except (KeyError, TypeError, ValueError) as e:
            print(f"Lỗi dữ liệu phần thưởng: {e}. Dữ liệu nhận được: {reward}")

    def grant_quest_completion_reward(self, character: Character, quest: Dict[str, Any]):
        """
        Tính toán và trao thưởng toàn bộ khi hoàn thành một nhiệm vụ.
        """
        difficulty = quest.get('difficulty', 1)
        print(f"\n--- Trao thưởng cho nhiệm vụ: '{quest['description']}' (Độ khó: {difficulty}) ---")
        
        # Thưởng XP
        xp_reward_amount = self.calculate_xp(character, difficulty)
        self.grant_reward(character, {"type": "xp", "amount": xp_reward_amount})

        # Thưởng Vàng
        gold_reward_amount = self.calculate_currency(character, difficulty)
        self.grant_reward(character, {"type": "gold", "amount": gold_reward_amount})

        # Thưởng vật phẩm (nếu có)
        if quest.get('item_reward'):
            self.grant_reward(character, {"type": "item", "item_object": quest['item_reward']})
            
        print("--------------------------------" + "-"*len(quest['description']))

    def punish(self, character: Character, punishment: Dict[str, Any]):
        """
        Trừng phạt nhân vật khi không hoàn thành mục tiêu.
        Chỉ số INT giúp giảm thiểu hình phạt.
        """
        punishment_type = punishment.get("type")
        if punishment_type == "hp":
            base_amount = punishment.get("amount", 0)
            # Mỗi điểm INT giảm 2% lượng máu bị phạt, tối đa giảm 80%
            reduction_modifier = max(0.2, 1 - (character.int * 0.02))
            final_amount = int(base_amount * reduction_modifier)
            
            character.hp -= final_amount
            # Đảm bảo máu không bị âm
            if character.hp < 0:
                character.hp = 0
            
            print(f"Nhân vật {character.name} bị phạt {final_amount} máu vì không hoàn thành mục tiêu.")
        else:
            print(f"Loại hình phạt '{punishment_type}' không hợp lệ.")


class Quest:
    """Đại diện cho MỘT nhiệm vụ duy nhất. Đơn giản và tập trung."""
    def __init__(self, description: str, difficulty: int):
        self.quest_id: str = "quest_" + str(uuid.uuid4())
        self.description: str = description
        self.difficulty: int = difficulty
        self.is_completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi đối tượng Quest thành dictionary."""
        return {
            "quest_id": self.quest_id, "description": self.description,
            "difficulty": self.difficulty, "is_completed": self.is_completed
        }


class StudySession:
    """
    Quản lý một phiên học. Đã thêm theo dõi thời gian bắt đầu thực tế.
    """
    def __init__(
        self,
        goal_description: str,
        start_time: datetime,
        end_time: datetime,
        linked_quests: List[Quest]
    ):
        if start_time >= end_time: print("Thời gian kết thúc phải sau thời gian bắt đầu.")
        if not goal_description: print("Mô tả phiên học không được để trống.")
        if not linked_quests: print("Phiên học phải có ít nhất một nhiệm vụ liên kết.")

        self.session_id: str = str(uuid.uuid4())
        self.goal_description: str = goal_description
        self.linked_quests: List[Quest] = linked_quests
        # Chỉ giữ giờ và phút, bỏ ngày
        self.start_time: datetime = to_basedate_time(start_time)
        self.end_time: datetime = to_basedate_time(end_time)      # Thời gian dự kiến kết thúc
        
        # Thời gian thực tế
        self.actual_start_time: Optional[datetime] = None  # Thời gian bắt đầu thực tế
        self.actual_end_time: Optional[datetime] = None    # Thời gian kết thúc thực tế
        
        self.status: str = 'Scheduled' #scheduled - running - finished
        self.rank: str = "N/A" #rank gồm a,b,c,d,f
        self.active: bool = True #TODO

    def mark_quest_as_complete(self, quest_id: str):
        """Tìm và đánh dấu một quest trong các quest liên kết là đã hoàn thành."""
        quest_found = next((q for q in self.linked_quests if q.quest_id == quest_id), None)
        if quest_found and not quest_found.is_completed:
            quest_found.is_completed = True
            print(f"   -> Nhiệm vụ '{quest_found.description}' trong phiên học đã được đánh dấu hoàn thành!")
        elif not quest_found:
            print(f"Lỗi: Không tìm thấy nhiệm vụ với ID {quest_id} trong phiên học này.")
    
    @property
    def quest_progress(self) -> float:
        """Trả về tỷ lệ hoàn thành quest (0.0 đến 1.0). Đây là tỉ lệ số quest đã làm so chia với tổng số quest dự tính phải làm"""
        completed_count = sum(1 for q in self.linked_quests if q.is_completed)
        total_count = len(self.linked_quests)
        return completed_count / total_count if total_count > 0 else 0.0

    def get_completed_quests(self) -> List[Quest]:
        """Trả về danh sách các quest đã hoàn thành trong phiên này."""
        return [q for q in self.linked_quests if q.is_completed]

    def finish(self, end_time_override: Optional[datetime] = None):
        """Hoàn tất phiên học. Hạng được quyết định bởi điểm số kết hợp."""
        # Kiểm tra xem phiên học có đang chạy không, nếu không thì thoát
        if self.status != 'Running': return
        
        # Đánh dấu phiên học đã kết thúc
        self.status = 'Finished'
        # Ghi lại thời gian kết thúc thực tế (dùng thời gian được truyền vào hoặc thời gian hiện tại)
        self.actual_end_time = end_time_override if end_time_override else datetime.now()
        
        # Tính điểm hoàn thành nhiệm vụ (tỷ lệ từ 0.0 đến 1.0)
        quest_completion_score = self.quest_progress
        
        # Tính thời gian thực tế đã học - sử dụng actual_start_time nếu có
        start_time_for_calc = self.actual_start_time if self.actual_start_time else self.start_time
        time_spent_seconds = (self.actual_end_time - start_time_for_calc).total_seconds()
        
        # Tính thời gian dự kiến ban đầu (đơn vị: giây)
        time_planned_seconds = (self.end_time - self.start_time).total_seconds()
        # Tính tỷ lệ thời gian thực tế so với dự kiến
        time_ratio = time_spent_seconds / time_planned_seconds if time_planned_seconds > 0 else 1.0
        # Tính điểm thưởng hiệu quả thời gian (càng học ít thời gian càng được thưởng)
        time_efficiency_bonus = max(0, 1 - time_ratio)

        # Đặt trọng số cho hai yếu tố chấm điểm
        quest_weight = 0.5  # Hoàn thành nhiệm vụ chiếm 50%
        time_weight = 0.5   # Hiệu quả thời gian chiếm 50%
        # Tính điểm tổng kết dựa trên trọng số
        final_performance_score = (quest_completion_score * quest_weight) + (time_efficiency_bonus * time_weight)
        
        # Xếp hạng dựa trên điểm tổng kết
        if final_performance_score >= 0.85: self.rank = 'S'      # Xuất sắc (≥85%)
        elif final_performance_score >= 0.70: self.rank = 'A'    # Giỏi (70-84%)
        elif final_performance_score >= 0.55: self.rank = 'B'    # Khá (55-69%)
        elif final_performance_score >= 0.40: self.rank = 'C'    # Trung bình (40-54%)
        else: self.rank = 'F'                                    # Yếu (<40%)

        # Chuyển đổi tỷ lệ hoàn thành thành phần trăm để hiển thị
        progress_percent = f"{int(quest_completion_score * 100)}%"
        # In thông báo kết quả phiên học
        actual_duration = f"{time_spent_seconds/60:.1f} phút"
        print(f"Phiên học '{self.goal_description}' đã kết thúc với Hạng: {self.rank} (Hoàn thành {progress_percent} nhiệm vụ, thời gian thực: {actual_duration}).")

    def start_session(self, actual_start_time: Optional[datetime] = None):
        """Bắt đầu phiên học và ghi lại thời gian bắt đầu thực tế."""
        if self.status != 'Scheduled':
            print(f"Không thể bắt đầu phiên học '{self.goal_description}' - trạng thái hiện tại: {self.status}")
            return False        
        self.status = 'Running'
        self.actual_start_time = actual_start_time if actual_start_time else datetime.now()
        print(f"▶️  BẮT ĐẦU THỰC TẾ: '{self.goal_description}' lúc {self.actual_start_time.strftime('%H:%M:%S')}")
        return True

    def get_session_data(self) -> Dict[str, Any]:
        """Trả về dữ liệu tóm tắt của phiên học, không có 'tags'."""
        # Tính thời lượng thực tế của phiên học
        if self.actual_end_time and self.actual_start_time:
            # Nếu có cả thời gian bắt đầu và kết thúc thực tế
            duration = self.actual_end_time - self.actual_start_time
        elif self.actual_end_time:
            # Nếu chỉ có thời gian kết thúc thực tế, dùng thời gian bắt đầu dự kiến
            duration = self.actual_end_time - self.start_time
        else:
            # Nếu chưa kết thúc hoặc chưa có thời gian thực tế
            duration = timedelta(0)
            
        # Trả về dictionary chứa tất cả thông tin quan trọng của phiên học
        return {
            "session_id": self.session_id,                           # ID duy nhất của phiên học
            "goal": self.goal_description,                           # Mô tả mục tiêu phiên học
            "status": self.status,                                   # Trạng thái hiện tại (Scheduled/Running/Finished)
            "start_time": self.start_time,                          # Thời gian bắt đầu dự kiến
            "end_time": self.end_time,                              # Thời gian kết thúc dự kiến
            "actual_start_time": self.actual_start_time,            # Thời gian bắt đầu thực tế
            "actual_end_time": self.actual_end_time,                # Thời gian kết thúc thực tế
            "rank": self.rank,                                      # Hạng đạt được (S/A/B/C/F)
            "duration_seconds": duration.total_seconds(),           # Thời lượng thực tế tính bằng giây
            "linked_quests_data": [q.to_dict() for q in self.linked_quests]  # Danh sách dữ liệu các nhiệm vụ liên kết
        }


class QuestSystem:
    """Quản lý tất cả các đối tượng Quest."""
    def __init__(self):
        self.active_quests: Dict[str, Quest] = {}

    def create_quest(self, description: str, difficulty: int) -> Quest:
        """Tạo một đối tượng Quest mới, lưu trữ và trả về nó."""
        quest = Quest(description, difficulty)
        self.active_quests[quest.quest_id] = quest
        return quest

    def get_completed_quests_count(self) -> int:
        """Đếm số lượng quest đã được đánh dấu là hoàn thành."""
        return sum(1 for quest in self.active_quests.values() if quest.is_completed)


class StudyAnalytics:
    """
    Cung cấp các phân tích và thống kê chi tiết về hiệu suất học tập của người dùng.
    """
    def __init__(self, quest_system: QuestSystem):
        self.session_history: List[Dict[str, Any]] = []
        self.quest_system = quest_system
        self.aggregated_stats: Dict[str, Any] = self._get_initial_stats()
        self.focus_streak: int = 0
        self.quest_system = quest_system
        self.unlockable_achievements = {
            'BuocDiDauTien': {'metric': 'total_sessions', 'value': 1, 'name': 'Bước Đi Đầu Tiên'},
            'HocVienXuatSac': {'metric': 'rank_counts.S', 'value': 1, 'name': 'Học Viên Xuất Sắc'},
            'ChamChiCanCu': {'metric': 'total_study_hours', 'value': 1, 'name': 'Chăm Chỉ Cần Cù'},
            'BacThayNhiemVu': {'metric': 'quests_completed', 'value': 3, 'name': 'Bậc Thầy Nhiệm Vụ'},
            'Chuoi3Ngay': {'metric': 'focus_streak', 'value': 3, 'name': 'Chuỗi 3 Ngày'}
        }

    def _get_initial_stats(self) -> Dict[str, Any]:
        """Khởi tạo dictionary thống kê, không có 'time_by_tag'."""
        return {
            'total_study_seconds': 0, 'total_study_hours': 0, 'total_sessions': 0,
            'rank_counts': {'S': 0, 'A': 0, 'B': 0, 'C': 0, 'F': 0},
            'average_session_duration_minutes': 0, 'average_rank_score': 0,
            'quests_completed': 0, 'quest_completion_rate': 0
        }

    def log_session(self, session_data: Dict[str, Any]):
        """Ghi lại một phiên học đã kết thúc và gọi hàm cập nhật thống kê."""
        # !!!
        # Gây lỗi khi ImportSave()
        # !!!
        # self.session_history.append(session_data)
        self._update_stats()

    def _update_stats(self):
        """Tính toán lại thống kê, không xử lý 'tags'."""
        stats = self._get_initial_stats()
        rank_map = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'F': 0}
        total_rank_score = 0
        
        for session in self.session_history:
            stats['total_sessions'] += 1
            stats['total_study_seconds'] += session.get('duration_seconds', 0)
            
            rank = session.get('rank', 'N/A')
            if rank in stats['rank_counts']:
                stats['rank_counts'][rank] += 1
                total_rank_score += rank_map.get(rank, 0)
        # Tính toán các chỉ số cuối cùng
        stats['total_study_hours'] = stats['total_study_seconds'] / 3600
        if stats['total_sessions'] > 0:
            stats['average_session_duration_minutes'] = (stats['total_study_seconds'] / stats['total_sessions']) / 60
            stats['average_rank_score'] = total_rank_score / stats['total_sessions']

        # Lấy dữ liệu từ hệ thống nhiệm vụ
        stats['quests_completed'] = self.quest_system.get_completed_quests_count()
        total_quests = len(self.quest_system.active_quests)
        if total_quests > 0:
            stats['quest_completion_rate'] = (stats['quests_completed'] / total_quests) * 100

        self.aggregated_stats = stats
        # !!!
        # !!! Gây lỗi nếu chạy !!!
        # !!!
        # self.focus_streak = self._calculate_focus_streak()

    def _calculate_focus_streak(self) -> int:
        """Tính số ngày học liên tiếp."""
        if not self.session_history: return 0
        
        study_dates = sorted(list(set(s['end_time'].date() for s in self.session_history)))
        if not study_dates: return 0
        
        streak = 0
        # Chỉ bắt đầu tính chuỗi nếu ngày học cuối cùng là hôm nay hoặc hôm qua
        if study_dates[-1] >= date.today() - timedelta(days=1):
            streak = 1
            # Lặp ngược từ cuối danh sách để kiểm tra tính liên tục
            for i in range(len(study_dates) - 1, 0, -1):
                if study_dates[i] - study_dates[i-1] == timedelta(days=1):
                    streak += 1
                else:
                    break  # Ngắt chuỗi nếu có khoảng trống
        return streak

    def check_unlockable_achievements(self, character: Character):
        """Kiểm tra và mở khóa thành tích cho nhân vật."""
        for ach_id, criteria in self.unlockable_achievements.items():
            if ach_id in character.unlocked_achievements: continue

            # Lấy giá trị thống kê cần kiểm tra
            metric_path = criteria['metric'].split('.')
            value_to_check = self.aggregated_stats
            try:
                for key in metric_path: value_to_check = value_to_check[key]
            except KeyError: continue

            # So sánh với giá trị yêu cầu và mở khóa
            if value_to_check >= criteria['value']:
                character.add_achievement(ach_id)
                
    def generate_report(self) -> str:
        """Tạo báo cáo chi tiết, không có phần 'Time Breakdown by Tag'."""
        stats = self.aggregated_stats
        report_lines = [
            "==========================================",
            # ... các dòng báo cáo khác giữ nguyên ...
            "--- Đánh Giá ---",
            f"S: {stats['rank_counts']['S']} | A: {stats['rank_counts']['A']} | B: {stats['rank_counts']['B']} | C: {stats['rank_counts']['C']} | F: {stats['rank_counts']['F']}",
            "",
            "--- Ngày Học Liên Tiếp ---",
            f"{self.focus_streak}",
            "",
            "--- Nhiệm Vụ ---",
            f"Nhiệm Vụ Hoàn Thành: {stats['quests_completed']} / {len(self.quest_system.active_quests)}",
            f"Tỷ Lệ Hoàn Thành: {stats['quest_completion_rate']:.1f}%",
            "=========================================="
        ]
        return "\n".join(report_lines)


class SessionManager:
    """
    Bộ điều khiển trung tâm cho tất cả các phiên học.
    Đây là class điều phối hoạt động của các hệ thống khác như
    StudySession, RewardSystem, và StudyAnalytics.
    """
    def __init__(self, character: Character, reward_system: RewardSystem, analytics: StudyAnalytics):
        # Lưu trữ tham chiếu đến các hệ thống cốt lõi khác
        self.sessions: List[StudySession] = []
        self.character = character
        self.reward_system = reward_system
        self.analytics = analytics
        self.arena = Arena(character)  # Thêm hệ thống đấu trường
        self.save_file_path = self._get_save_path()
        self.qr_image_path = self._get_qr_path()
        self.public_rewards = [0, 0]
        self.public_rank = ''
    
    def _get_save_path(self):
        """Xác định đường dẫn lưu file tùy theo platform"""
        if platform == 'android':
            from android.storage import app_storage_path # type: ignore
            save_dir = app_storage_path()
            print(os.path.join(save_dir, "save_data.json"))
            return os.path.join(save_dir, "save_data.json")
        else:
            save_dir = os.path.dirname(os.path.abspath(__file__))
            print(os.path.join(save_dir, "save_data.json"))
            return os.path.join(save_dir, "save_data.json")

    def _get_qr_path(self):
        """Xác định đường dẫn lưu QR code"""
        if platform == 'android':
            from android.storage import app_storage_path # type: ignore
            save_dir = app_storage_path()
            return os.path.join(save_dir, "save_qr.png")
        else:
            save_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(save_dir, "save_qr.png")
    
    def generate_qr_code(self):
        """
        Tạo QR code từ dữ liệu save game với compression tối ưu
        Returns: đường dẫn file QR code hoặc None nếu lỗi
        """
        try:
            # Lấy dữ liệu save game đã được tối ưu cho QR
            save_data = self._get_optimized_qr_data()
            # Chuyển đổi thành JSON string compact
            json_string = json.dumps(save_data, ensure_ascii=False, separators=(',', ':'))
            
            # Nén dữ liệu bằng base64
            compressed_bytes = gzip.compress(json_string.encode('utf-8'))
            compressed_data = base64.b64encode(compressed_bytes).decode('ascii')
            
            # Kiểm tra kích thước dữ liệu
            print(f"QR data size: {len(compressed_data)} characters")
            
            # Nếu dữ liệu quá lớn, sử dụng phiên bản rút gọn hơn
            if len(compressed_data) > 2000:  # Giới hạn an toàn cho QR code
                print("Data too large, using minimal version...")
                save_data = self._get_minimal_qr_data()
                json_string = json.dumps(save_data, ensure_ascii=False, separators=(',', ':'))
                compressed_bytes = gzip.compress(json_string.encode('utf-8'))
                compressed_data = base64.b64encode(compressed_bytes).decode('ascii')
                print(f"Minimal QR data size: {len(compressed_data)} characters")
            
            # Tạo QR code với error correction thấp hơn để chứa nhiều dữ liệu hơn
            qr = qrcode.QRCode(
                version=None,  # Tự động điều chỉnh
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Thấp nhất
                box_size=8,  # Giảm kích thước box
                border=2,    # Giảm border
            )
            
            # Thêm prefix để nhận biết
            qr_data = f"GSS:{compressed_data}"
            qr.add_data(qr_data)
            qr.make(fit=True)
            # Tạo hình ảnh QR
            qr_image = qr.make_image(fill_color="black", back_color="white")
            # Lưu file
            qr_image.save(self.qr_image_path)
            
            print(f"QR code đã được tạo: {self.qr_image_path}")
            return self.qr_image_path
            
        except Exception as e:
            print(f"Lỗi khi tạo QR code: {str(e)}")
            return None

    def import_from_qr_data(self, qr_data):
        """
        Import dữ liệu từ QR code data với hỗ trợ gzip
        """
        try:
            # Kiểm tra prefix
            if not qr_data.startswith("GSS:"):
                print("QR code không phải của GSScheduler")
                return False
            
            # Lấy dữ liệu đã nén
            compressed_data = qr_data[4:]  # Bỏ prefix "GSS:"
            
            # Giải nén base64 và gzip
            compressed_bytes = base64.b64decode(compressed_data.encode('ascii'))
            json_string = gzip.decompress(compressed_bytes).decode('utf-8')
            
            # Parse JSON
            save_data = json.loads(json_string)
            
            # Import dữ liệu
            return self._load_save_data(save_data)
            
        except Exception as e:
            print(f"Lỗi khi import từ QR: {str(e)}")
            return False

    def ExportSave(self):
        """
        Xuất dữ liệu game ra file JSON
        Lưu chỉ số nhân vật, thành tích, sessions
        """
        try:
            save_data = self._get_save_data()
            
            with open(self.save_file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            print(f"Dữ liệu đã được lưu thành công vào {self.save_file_path}")
            return True
            
        except Exception as e:
            print(f"Lỗi khi lưu dữ liệu: {str(e)}")
            return False

    def ImportSave(self):
        """
        Nhập dữ liệu game từ file JSON
        Tải chỉ số nhân vật, thành tích, sessions
        """
        try:
            if not os.path.exists(self.save_file_path):
                print(f"File save không tồn tại: {self.save_file_path}")
                return False
            
            with open(self.save_file_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            return self._load_save_data(save_data)
            
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu: {str(e)}")
            return False
    
    def create_comprehensive_demo_data(self):
        """
        Tạo data đầy đủ với stats phong phú để demo
        """
        # Set comprehensive character info
        self.character.name = "Demo Hero"
        self.character.level = 15
        self.character.xp = 450
        self.character.xp_to_next_level = 800
        self.character.hp = 120
        self.character.max_hp = 150
        self.character.gold = 350
        self.character.dex = 25
        self.character.int = 18
        self.character.luk = 22
        self.character.available_points = 3
        
        # Add some achievements
        self.character.unlocked_achievements.add('BuocDiDauTien')
        self.character.unlocked_achievements.add('HocVienXuatSac')
        self.character.unlocked_achievements.add('ChamChiCanCu')        # Create demo items for inventory
        
        self.character.inventory.extend([Items['Khien_Doi_Truong_Meo'], Items['Sach_Phep_Tru_Ta']])
        self.character.equipment.append(Items['Riu_Tho_San'])
        
        # Create demo quests
        for i in range(8):
            quest = self.analytics.quest_system.create_quest(
                description=f"Demo Quest {i+1}: Study Session Task",
                difficulty=random.randint(1, 5)
            )
            if i < 6:  # Mark some as completed
                quest.is_completed = True
        
        # Create demo session history
        base_time = datetime.now() - timedelta(days=10)
        for day in range(10):
            session_start = base_time + timedelta(days=day, hours=14)
            session_end = session_start + timedelta(hours=2, minutes=random.randint(0, 60))
            
            # Create quests for this session
            session_quests = []
            for j in range(random.randint(2, 4)):
                quest = Quest(f"Task {j+1} for Day {day+1}", random.randint(1, 3))
                if random.random() > 0.3:  # 70% completion rate
                    quest.is_completed = True
                session_quests.append(quest)
            
            # Create session data
            session_data = {
                "session_id": f"demo_session_{day}",
                "goal": f"Study Session Day {day+1}",
                "status": "Finished",
                "start_time": session_start,
                "end_time": session_end,
                "rank": random.choice(['S', 'A', 'A', 'B', 'B', 'C']),  # Weighted towards good grades
                "duration_seconds": (session_end - session_start).total_seconds(),
                "linked_quests_data": [q.to_dict() for q in session_quests]
            }
            
            self.analytics.session_history.append(session_data)
        
        # Update analytics stats
        self.analytics._update_stats()
        self.analytics.focus_streak = 5  # 5-day streak
        
        print("Comprehensive demo data created with full stats, achievements, and session history")

    def _get_optimized_qr_data(self):
        """Tạo dữ liệu tối ưu cho QR code, bỏ bớt thông tin không cần thiết"""
        try:
            # Chỉ lấy những thông tin quan trọng nhất
            save_data = {
                "c": {  # character (viết tắt để tiết kiệm)
                    "n": self.character.name,
                    "l": self.character.level,
                    "x": self.character.xp,
                    "h": self.character.hp,
                    "m": self.character.max_hp,
                    "g": self.character.gold,
                    "d": self.character.dex,
                    "i": self.character.int,
                    "k": self.character.luk,
                    "p": self.character.available_points,
                    "a": list(self.character.unlocked_achievements)[:5],  # Chỉ lấy 5 achievement đầu
                },
                "s": {  # stats (rút gọn)
                    "ts": self.analytics.aggregated_stats.get('total_sessions', 0),
                    "th": round(self.analytics.aggregated_stats.get('total_study_hours', 0), 2),
                    "qc": self.analytics.aggregated_stats.get('quests_completed', 0),
                    "fs": self.analytics.focus_streak,
                    "rc": self.analytics.aggregated_stats.get('rank_counts', {})
                },
                "t": datetime.now().strftime("%Y%m%d%H%M"),  # timestamp ngắn gọn
                "v": "2.0"  # version
            }
            
            print(f"Optimized save data for character: {self.character.name}")
            return save_data
        except Exception as e:
            print(f"Error generating optimized data: {e}")
    
    def _get_save_data(self):
        """Lấy dữ liệu save game đầy đủ cho file JSON"""
        try:
            save_data = {
                "character": {
                    "name": self.character.name,
                    "level": self.character.level,
                    "xp": self.character.xp,
                    "xp_to_next_level": self.character.xp_to_next_level,
                    "hp": self.character.hp,
                    "max_hp": self.character.max_hp,
                    "gold": self.character.gold,
                    "dex": self.character.dex,
                    "int": self.character.int,
                    "luk": self.character.luk,
                    "available_points": self.character.available_points,
                    "unlocked_achievements": list(self.character.unlocked_achievements),
                    "inventory": [
                        {
                            "name": item.name,
                            "description": item.description,
                            "category": item.category,
                            "rarity": item.rarity.name,                            "price": item.price,
                            "icon": item.icon,
                            "consumable": item.consumable,
                            "passive": item.passive,
                            "on_use_effect": item.on_use_effect  # THAY ĐỔI: đổi tên từ stat_bonuses
                        } for item in self.character.inventory
                    ],
                    "equipment": [
                        {
                            "name": item.name,
                            "description": item.description,
                            "category": item.category,
                            "rarity": item.rarity.name,                            "price": item.price,
                            "icon": item.icon,
                            "consumable": item.consumable,
                            "passive": item.passive,
                            "on_use_effect": item.on_use_effect  # THAY ĐỔI: đổi tên từ stat_bonuses
                        } for item in self.character.equipment
                    ]
                },
                "analytics": {
                    "session_history": [
                        {
                            **session,
                            "start_time": session["start_time"].isoformat() if isinstance(session["start_time"], datetime) else session["start_time"],
                            "end_time": session["end_time"].isoformat() if isinstance(session["end_time"], datetime) else session["end_time"]
                        } for session in self.analytics.session_history
                    ],
                    "aggregated_stats": self.analytics.aggregated_stats,
                    "focus_streak": self.analytics.focus_streak
                },
                "sessions": [
                    {
                        "session_id": session.session_id,
                        "goal_description": session.goal_description,
                        "start_time": session.start_time.isoformat(),
                        "end_time": session.end_time.isoformat(),
                        "actual_end_time": session.actual_end_time.isoformat() if session.actual_end_time else None,
                        "status": session.status,
                        "rank": session.rank,
                        "linked_quests": [
                            {
                                "quest_id": quest.quest_id,
                                "description": quest.description,
                                "difficulty": quest.difficulty,
                                "is_completed": quest.is_completed
                            } for quest in session.linked_quests
                        ]
                    } for session in self.sessions
                ],
                "quest_system": {
                    "active_quests": [
                        {
                            "quest_id": quest.quest_id,
                            "description": quest.description,
                            "difficulty": quest.difficulty,
                            "is_completed": quest.is_completed
                        } for quest in self.analytics.quest_system.active_quests.values()
                    ]
                },
                "save_timestamp": datetime.now().isoformat(),
                "version": "1.0"
            }
            print(f"Generated comprehensive save data for character: {self.character.name}")
            return save_data
        except Exception as e:
            print(f"Error generating save data: {e}")
            import traceback
            traceback.print_exc()
            return {"error": "failed_to_generate", "timestamp": datetime.now().isoformat()}

    def _load_save_data(self, save_data):
        """Load dữ liệu save game - sửa lại cho phù hợp với structure thực tế"""
        try:
            # Khôi phục character data
            char_data = save_data.get("character", {})
            self.character.name = char_data.get("name", "Hero")
            self.character.level = char_data.get("level", 1)
            self.character.xp = char_data.get("xp", 0)
            self.character.xp_to_next_level = char_data.get("xp_to_next_level", 100)
            self.character.hp = char_data.get("hp", 50)
            self.character.max_hp = char_data.get("max_hp", 50)
            self.character.gold = char_data.get("gold", 10)
            self.character.dex = char_data.get("dex", 1)
            self.character.int = char_data.get("int", 1)
            self.character.luk = char_data.get("luk", 1)
            self.character.available_points = char_data.get("available_points", 0)
            self.character.unlocked_achievements = set(char_data.get("unlocked_achievements", []))
            
            # Khôi phục inventory
            self.character.inventory = []
            for item_data in char_data.get("inventory", []):
                try:
                    rarity_enum = Rarity[item_data.get("rarity", "COMMON")]
                    item = Item(
                        name=item_data.get("name", "Unknown Item"),
                        description=item_data.get("description", ""),
                        category=item_data.get("category", "misc"),
                        rarity=rarity_enum,                        price=item_data.get("price", 0),
                        icon_path=item_data.get("icon", ""),
                        consumable=item_data.get("consumable", False),
                        passive=item_data.get("passive", False),
                        on_use_effect=item_data.get("on_use_effect", {})  # THAY ĐỔI: đổi tên từ stat_bonuses
                    )
                    self.character.inventory.append(item)
                except (KeyError, ValueError) as e:
                    print(f"Error loading inventory item: {e}")
            
            # Khôi phục equipment
            self.character.equipment = []
            for item_data in char_data.get("equipment", []):
                try:
                    rarity_enum = Rarity[item_data.get("rarity", "COMMON")]
                    item = Item(
                        name=item_data.get("name", "Unknown Equipment"),
                        description=item_data.get("description", ""),
                        category=item_data.get("category", "equipment"),
                        rarity=rarity_enum,                        price=item_data.get("price", 0),
                        icon_path=item_data.get("icon", ""),
                        consumable=item_data.get("consumable", False),
                        passive=item_data.get("passive", True),
                        on_use_effect=item_data.get("on_use_effect", {})  # THAY ĐỔI: đổi tên từ stat_bonuses
                    )
                    self.character.equipment.append(item)
                except (KeyError, ValueError) as e:
                    print(f"Error loading equipment item: {e}")
            
            # Khôi phục analytics
            analytics_data = save_data.get("analytics", {})
            self.analytics.session_history = analytics_data.get("session_history", [])
            self.analytics.aggregated_stats = analytics_data.get("aggregated_stats", self.analytics._get_initial_stats())
            self.analytics.focus_streak = analytics_data.get("focus_streak", 0)
            
            # Khôi phục quest system
            quest_data = save_data.get("quest_system", {})
            self.analytics.quest_system.active_quests = {}
            for quest_info in quest_data.get("active_quests", []):
                quest = Quest(
                    description=quest_info.get("description", "Unknown Quest"),
                    difficulty=quest_info.get("difficulty", 1)
                )
                quest.quest_id = quest_info.get("quest_id", quest.quest_id)
                quest.is_completed = quest_info.get("is_completed", False)
                self.analytics.quest_system.active_quests[quest.quest_id] = quest
            
            # Khôi phục sessions
            self.sessions = []
            for session_data in save_data.get("sessions", []):
                try:
                    # Tái tạo quests cho session
                    linked_quests = []
                    for quest_info in session_data.get("linked_quests", []):
                        quest = Quest(
                            description=quest_info.get("description", "Unknown Quest"),
                            difficulty=quest_info.get("difficulty", 1)
                        )
                        quest.quest_id = quest_info.get("quest_id", quest.quest_id)
                        quest.is_completed = quest_info.get("is_completed", False)
                        linked_quests.append(quest)
                    
                    # Tái tạo session
                    session = StudySession(
                        goal_description=session_data.get("goal_description", "Unknown Session"),
                        start_time=datetime.fromisoformat(session_data["start_time"]),
                        end_time=datetime.fromisoformat(session_data["end_time"]),
                        linked_quests=linked_quests
                    )
                    session.session_id = session_data.get("session_id", session.session_id)
                    session.status = session_data.get("status", "Scheduled")
                    session.rank = session_data.get("rank", "N/A")
                    if session_data.get("actual_end_time"):
                        session.actual_end_time = datetime.fromisoformat(session_data["actual_end_time"])
                    
                    self.sessions.append(session)
                except (KeyError, ValueError) as e:
                    print(f"Error loading session: {e}")
            
            save_timestamp = save_data.get("save_timestamp", "Unknown")
            print(f"Dữ liệu đã được load thành công - Time: {save_timestamp}")
            print(f"Character: {self.character.name} (Level {self.character.level})")
            return True
            
        except Exception as e:
            print(f"Lỗi khi load dữ liệu: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _find_session_by_id(self, session_id: str) -> Optional[StudySession]:
        """
        Hàm trợ giúp nội bộ để tìm một phiên học trong danh sách theo ID.
        
        Returns:
            StudySession hoặc None nếu không tìm thấy.
        """
        for s in self.sessions:
            if s.session_id == session_id:
                return s
        return None

    def schedule_session(
        self,
        goal_description: str,
        start_time: datetime,
        end_time: datetime,
        linked_quests: List[Quest]
    ) -> Optional[StudySession]:
        """
        Xác thực và lên lịch một phiên học mới.
        Kiểm tra trùng lặp thời gian với các session đã có.

        Returns:
            Đối tượng StudySession vừa được tạo nếu thành công, ngược lại là None.
        """
        try:
            # Chỉ giữ giờ và phút
            start_time = to_basedate_time(start_time)
            end_time = to_basedate_time(end_time)

            # Kiểm tra trùng lặp thời gian với các session đã có
            session = StudySession(goal_description, start_time, end_time, linked_quests)
            conflicting_session = self._check_time_conflict(start_time, end_time)
            if conflicting_session:
                print(f"Xung đột thời gian: Phiên học mới trùng với '{conflicting_session.goal_description}'")
                return [conflicting_session, session]
            
            self.sessions.append(session)
            print(f"🗓️  ĐÃ LÊN LỊCH: '{session.goal_description}' lúc {session.start_time.strftime('%H:%M:%S')}")
            return session
        except (ValueError, KeyError) as e:
            print(f"❌ LÊN LỊCH THẤT BẠI: {e}")
            return None

    def _check_time_conflict(self, new_start: datetime, new_end: datetime) -> Optional[StudySession]:
        """
        Kiểm tra xem thời gian mới có xung đột với session nào đã có không.
        Chỉ so sánh giờ:phút, bỏ qua ngày (theo comment trong main.py).
        
        Returns:
            StudySession bị xung đột nếu có, None nếu không có xung đột.
        """
        # Chuyển đổi về cùng ngày để so sánh chỉ thời gian
        base_date = datetime(1900, 1, 1)  # Sử dụng ngày cơ sở như trong main.py
        
        new_start_time_only = to_basedate_time(new_start)
        new_end_time_only = to_basedate_time(new_end)
        
        # Xử lý trường hợp qua ngày (ví dụ: 23:00 - 01:00)
        if new_end_time_only <= new_start_time_only:
            new_end_time_only += timedelta(days=1)
        
        for existing_session in self.sessions:
            # if existing_session.status == 'Finished': Không bỏ qua các session đã kết thúc. Đây là trạng thái bật tắt.
            
            # Chuyển session hiện có về cùng định dạng
            existing_start = to_basedate_time(existing_session.start_time)
            existing_end = to_basedate_time(existing_session.end_time)
            
            # Xử lý trường hợp session hiện có qua ngày
            if existing_end <= existing_start:
                existing_end += timedelta(days=1)
            
            # Kiểm tra xung đột: hai khoảng thời gian overlap
            if (new_start_time_only <= existing_end and new_end_time_only >= existing_start):
                return existing_session
        
        return None
    
    def mark_quest_as_complete(self, session_id: str, quest_id: str):
        """
        Đánh dấu một nhiệm vụ là đã hoàn thành trong một phiên học đang chạy. Đây là "cầu nối" giữa giao diện người dùng và logic của StudySession.
        """
        session = self._find_session_by_id(session_id)
        if session and session.status == 'Running':
            session.mark_quest_as_complete(quest_id)
        else:
            print("Lỗi: Không thể đánh dấu nhiệm vụ. Phiên học không đang chạy hoặc không tồn tại.")

    def update(self, current_time: datetime):
        """
        'Tick' chính của ứng dụng, được gọi định kỳ để cập nhật trạng thái.
        Tự động bắt đầu và kết thúc các phiên học khi đến giờ.
        """
        for session in self.sessions[:]: # Lặp trên bản sao để xóa an toàn
            if session.status == 'Scheduled' and current_time >= session.start_time:
                session.start_session(current_time)  # Sử dụng method mới với thời gian thực tế
            
            if session.status == 'Running' and current_time >= session.end_time:
                # Gọi finish() không có tham số -> kết thúc tự động khi hết giờ
                session.finish()
                self._finalize_session(session)

    def end_session_manually(self, session_id: str):
        """
        Xử lý yêu cầu kết thúc một phiên học thủ công từ người dùng.
        """
        session = self._find_session_by_id(session_id)
        if session and session.status == 'Running':
            print(f"Người dùng yêu cầu kết thúc sớm phiên '{session.goal_description}'.")
            # Gọi finish() với thời gian hiện tại làm tham số
            session.finish(end_time_override=datetime.now())
            self._finalize_session(session)
        else:
            print(f"Lỗi: Không tìm thấy phiên học đang chạy với ID {session_id}.")

    def _finalize_session(self, session: StudySession):
        """
        Xử lý tất cả logic sau khi một phiên học kết thúc.
        Đây là nơi tập trung các bước xử lý cuối cùng.
        """
        if session.status != 'Finished': return
        
        # 1. Ghi lại dữ liệu phân tích
        self.analytics.log_session(session.get_session_data())
        # 2. Áp dụng thưởng/phạt
        self._apply_session_consequences(session)
        # 3. Kiểm tra thành tích mới (sau khi đã có thưởng/phạt và cập nhật stats)
        self.analytics.check_unlockable_achievements(self.character)
        # 4. Xóa phiên học đã kết thúc khỏi danh sách đang hoạt động
        self.sessions.remove(session)

    def _apply_session_consequences(self, session: StudySession):
        """
        Áp dụng thưởng cho các nhiệm vụ đã hoàn thành và thưởng/phạt dựa trên hạng.
        """
        completed_quests_in_session = session.get_completed_quests()

        # Phần thưởng chính từ việc hoàn thành các quest
        if completed_quests_in_session:
            print("\n--- Bắt đầu trao thưởng cho các nhiệm vụ đã hoàn thành ---")
            for quest in completed_quests_in_session:
                # Gọi hàm trao thưởng từ RewardSystem cho từng quest
                self.reward_system.grant_quest_completion_reward(self.character, quest.to_dict())
            print("------------------------------------------------------")
        
        # THAY ĐỔI MỚI: Thêm phần thưởng nhỏ dựa trên hạng của phiên học
        # Đây là phần thưởng khuyến khích cho việc nỗ lực và đạt kết quả tốt
        rank_bonuses = {
            'S': {'type': 'gold', 'amount': 15}, # Thưởng nhiều nhất
            'A': {'type': 'gold', 'amount': 10},
            'B': {'type': 'gold', 'amount': 5},
            'C': {'type': 'gold', 'amount': 2}   # Thưởng khuyến khích
        }

        # Nếu hạng của phiên học nằm trong danh sách thưởng, hãy trao thưởng
        if session.rank in rank_bonuses:
            print(f"Thưởng thêm cho việc đạt Hạng {session.rank}:")
            self.reward_system.grant_reward(self.character, rank_bonuses[session.rank])

        # Áp dụng hình phạt nếu hạng thấp
        if session.rank == 'F':
            # Phạt dựa trên tổng độ khó của các quest CHƯA hoàn thành
            total_difficulty_failed = sum(q.difficulty for q in session.linked_quests if not q.is_completed)
            if total_difficulty_failed > 0:
                print(f"Phiên học kết thúc với hạng F, áp dụng hình phạt.")
                self.reward_system.punish(self.character, {'type': 'hp', 'amount': total_difficulty_failed * 4})


class SkillType(Enum):
    """Các loại skill trong đấu trường"""
    ATTACK = "attack"  # Đánh thường
    DEFEND = "defend"  # Thủ
    MAGIC = "magic"    # Dùng phép


class ArenaBot:
    """Bot đấu trường được tạo từ dữ liệu base64 của người chơi khác"""
    def __init__(self, name: str = "Bot", level: int = 1, hp: int = 50, 
                 max_hp: int = 50, dex: int = 1, int_stat: int = 1, luk: int = 1):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = max_hp
        self.dex = dex
        self.int_stat = int_stat  # Tránh conflict với keyword 'int'
        self.luk = luk
        self.is_alive = True
    
    @classmethod
    def from_base64(cls, base64_data: str):
        """Tạo bot từ dữ liệu base64"""
        try:
            # Decode base64 và parse JSON
            json_data = base64.b64decode(base64_data).decode('utf-8')
            data = json.loads(json_data)
            
            # Lấy thông tin từ dữ liệu (có thể là format rút gọn hoặc đầy đủ)
            if 'c' in data:  # Format rút gọn
                char_data = data['c']
                return cls(
                    name=char_data.get('n', 'Unknown Player'),
                    level=char_data.get('l', 1),
                    hp=char_data.get('h', 50),
                    max_hp=char_data.get('m', 50),
                    dex=char_data.get('d', 1),
                    int_stat=char_data.get('i', 1),
                    luk=char_data.get('k', 1)
                )
            else:  # Format đầy đủ
                char_data = data.get('character', {})
                return cls(
                    name=char_data.get('name', 'Unknown Player'),
                    level=char_data.get('level', 1),
                    hp=char_data.get('hp', 50),
                    max_hp=char_data.get('max_hp', 50),
                    dex=char_data.get('dex', 1),
                    int_stat=char_data.get('int', 1),
                    luk=char_data.get('luk', 1)
                )
        except Exception as e:
            print(f"Error parsing base64 data: {e}")
            # Trả về bot mặc định nếu lỗi
            return cls(name="Error Bot")
    
    def choose_skill(self) -> SkillType:
        """Bot chọn skill ngẫu nhiên với tỷ lệ"""
        choices = [SkillType.ATTACK, SkillType.DEFEND, SkillType.MAGIC]
        weights = [0.5, 0.3, 0.2]  # 50% attack, 30% defend, 20% magic
        return random.choices(choices, weights=weights)[0]


class Arena:
    """Hệ thống đấu trường"""
    def __init__(self, character: 'Character'):
        self.player = character
        self.bot: Optional[ArenaBot] = None
        self.battle_log: List[str] = []
        self.turn_count = 0
        self.player_defended = False
        self.bot_defended = False
        self.battle_active = False
    
    def load_opponent(self, base64_data: str) -> bool:
        """Load đối thủ từ dữ liệu base64"""
        try:
            self.bot = ArenaBot.from_base64(base64_data)
            return True
        except Exception as e:
            print(f"Error loading opponent: {e}")
            return False
    
    def generate_demo_opponent(self) -> str:
        """Tạo đối thủ demo và trả về mã base64"""
        demo_names = ["Mom", "Nhật Nam", "Natsu", "Luffy", "Goku", "Vegeta", "Saitama"]
        demo_data = {
            "c": {
                "n": random.choice(demo_names),
                "l": random.randint(1, 10),
                "h": random.randint(40, 100),
                "m": random.randint(50, 120),
                "d": random.randint(1, 15),
                "i": random.randint(1, 15),
                "k": random.randint(1, 15)
            }
        }
        
        json_str = json.dumps(demo_data)
        base64_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        return base64_data
    
    def start_battle(self) -> bool:
        """Bắt đầu trận đấu"""
        if not self.bot:
            return False
        
        self.battle_active = True
        self.turn_count = 0
        self.battle_log = []
        self.player_defended = False
        self.bot_defended = False
        
        # Reset HP về max
        self.player.hp = self.player.max_hp
        self.bot.hp = self.bot.max_hp
        self.bot.is_alive = True
        
        self.battle_log.append(f"Trận đấu bắt đầu! {self.player.name} vs {self.bot.name}")
        return True
    
    def calculate_damage(self, attacker_stats: Dict[str, int], defender_stats: Dict[str, int], 
                        skill_type: SkillType, defender_defended: bool = False) -> int:
        """Tính toán sát thương dựa trên chỉ số và loại skill"""
        base_damage = 0
        
        if skill_type == SkillType.ATTACK:
            # Đánh thường: phụ thuộc vào DEX và LUK
            base_damage = 10 + (attacker_stats['dex'] * 2) + (attacker_stats['luk'] * 1.5)
        elif skill_type == SkillType.MAGIC:
            # Phép thuật: phụ thuộc vào INT và LUK
            base_damage = 15 + (attacker_stats['int'] * 3) + (attacker_stats['luk'] * 1)
        elif skill_type == SkillType.DEFEND:
            # Thủ không gây sát thương
            return 0
        
        # Thêm yếu tố ngẫu nhiên
        damage_variance = random.uniform(0.8, 1.2)
        base_damage *= damage_variance
        
        # Giảm sát thương nếu đối thủ đang thủ
        if defender_defended:
            defense_reduction = 0.3 + (defender_stats['dex'] * 0.02)  # 30% + 2% per DEX
            base_damage *= (1 - min(defense_reduction, 0.8))  # Tối đa giảm 80%
        
        return max(1, int(base_damage))  # Tối thiểu 1 damage
    
    def execute_turn(self, player_skill: SkillType) -> Dict[str, Any]:
        """Thực hiện một lượt đấu"""
        if not self.battle_active or not self.bot:
            return {"error": "Battle not active"}
        
        self.turn_count += 1
        bot_skill = self.bot.choose_skill()
        
        turn_result = {
            "turn": self.turn_count,
            "player_skill": player_skill.value,
            "bot_skill": bot_skill.value,
            "player_damage": 0,
            "bot_damage": 0,
            "messages": [],
            "battle_ended": False,
            "winner": None
        }
        
        # Chuẩn bị stats
        player_stats = {
            'dex': self.player.dex,
            'int': self.player.int,
            'luk': self.player.luk
        }
        bot_stats = {
            'dex': self.bot.dex,
            'int': self.bot.int_stat,
            'luk': self.bot.luk
        }
        
        # Xử lý skill của người chơi
        if player_skill == SkillType.DEFEND:
            self.player_defended = True
            turn_result["messages"].append(f"{self.player.name} đang thủ!")
        else:
            self.player_defended = False
            damage = self.calculate_damage(player_stats, bot_stats, player_skill, self.bot_defended)
            self.bot.hp -= damage
            turn_result["player_damage"] = damage
            
            skill_name = "đánh thường" if player_skill == SkillType.ATTACK else "dùng phép"
            turn_result["messages"].append(f"{self.player.name} {skill_name} gây {damage} sát thương!")
        
        # Xử lý skill của bot
        if bot_skill == SkillType.DEFEND:
            self.bot_defended = True
            turn_result["messages"].append(f"{self.bot.name} đang thủ!")
        else:
            self.bot_defended = False
            damage = self.calculate_damage(bot_stats, player_stats, bot_skill, self.player_defended)
            self.player.hp -= damage
            turn_result["bot_damage"] = damage
            
            skill_name = "đánh thường" if bot_skill == SkillType.ATTACK else "dùng phép"
            turn_result["messages"].append(f"{self.bot.name} {skill_name} gây {damage} sát thương!")
        
        # Kiểm tra kết thúc trận đấu
        if self.player.hp <= 0:
            self.battle_active = False
            turn_result["battle_ended"] = True
            turn_result["winner"] = "bot"
            turn_result["messages"].append(f"{self.bot.name} thắng!")
        elif self.bot.hp <= 0:
            self.battle_active = False
            turn_result["battle_ended"] = True
            turn_result["winner"] = "player"
            turn_result["messages"].append(f"{self.player.name} thắng!")
            
            # Thưởng cho người chơi khi thắng
            xp_reward = 50 + (self.bot.level * 10)
            gold_reward = 25 + (self.bot.level * 5)
            self.player.xp += xp_reward
            self.player.gold += gold_reward
            turn_result["messages"].append(f"Thưởng: +{xp_reward} XP, +{gold_reward} Vàng!")
            self.player.check_level_up()
        
        # Lưu vào battle log
        for message in turn_result["messages"]:
            self.battle_log.append(message)
        
        return turn_result
    
    def get_battle_state(self) -> Dict[str, Any]:
        """Lấy trạng thái hiện tại của trận đấu"""
        return {
            "battle_active": self.battle_active,
            "turn_count": self.turn_count,
            "player": {
                "name": self.player.name,
                "hp": self.player.hp,
                "max_hp": self.player.max_hp,
                "level": self.player.level,
                "dex": self.player.dex,
                "int": self.player.int,
                "luk": self.player.luk
            },
            "bot": {
                "name": self.bot.name if self.bot else "No Bot",
                "hp": self.bot.hp if self.bot else 0,
                "max_hp": self.bot.max_hp if self.bot else 0,
                "level": self.bot.level if self.bot else 0,
                "dex": self.bot.dex if self.bot else 0,
                "int": self.bot.int_stat if self.bot else 0,
                "luk": self.bot.luk if self.bot else 0
            } if self.bot else None,
            "battle_log": self.battle_log
        }


# Utility function để tạo demo data
def generate_demo_base64_codes(count: int = 5) -> List[str]:
    """Tạo nhiều mã base64 demo cho test"""
    demo_names = ["Kirito", "Asuna", "Natsu", "Luffy", "Goku", "Vegeta", "Saitama", "Ichigo", "Naruto", "Sasuke"]
    codes = []
    
    for i in range(count):
        demo_data = {
            "c": {
                "n": demo_names[i % len(demo_names)],
                "l": random.randint(1, 10),
                "h": random.randint(40, 100),
                "m": random.randint(50, 120),
                "d": random.randint(1, 15),
                "i": random.randint(1, 15),
                "k": random.randint(1, 15)
            }
        }
        
        json_str = json.dumps(demo_data)
        base64_data = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        codes.append(base64_data)
    
    return codes

if __name__ == "__main__":
    print("\n=== DEMO BASE_DATE: So sánh giờ và phút, bỏ qua ngày ===")
    # Tạo SessionManager và các session demo
    char = Character(name="Demo")
    rewards = RewardSystem()
    quests = QuestSystem()
    analytics = StudyAnalytics(quest_system=quests)
    manager = SessionManager(character=char, reward_system=rewards, analytics=analytics)

    # Tạo 2 session trùng giờ (dù khác ngày)
    s1 = manager.schedule_session(
        "Session Sáng",
        datetime(2025, 6, 27, 8, 0),
        datetime(2025, 6, 27, 9, 0),
        [quests.create_quest("Toán", 2)]
    )
    s2 = manager.schedule_session(
        "Session Trùng Giờ (khác ngày)",
        datetime(2025, 7, 1, 8, 0),
        datetime(2025, 7, 1, 9, 0),
        [quests.create_quest("Lý", 2)]
    )
    if not s2:
        print("❌ Đã phát hiện trùng giờ dù khác ngày (ĐÚNG)")
    else:
        print("⚠️ Không phát hiện trùng giờ (SAI)")

    # Tạo session không trùng giờ
    s3 = manager.schedule_session(
        "Session Chiều",
        datetime(2025, 6, 27, 14, 0),
        datetime(2025, 6, 27, 15, 0),
        [quests.create_quest("Hóa", 2)]
    )
    if s3:
        print("✅ Session chiều tạo thành công (không trùng)")

    # Tạo session qua ngày (23:00-01:00)
    s4 = manager.schedule_session(
        "Session Đêm",
        datetime(2025, 6, 27, 23, 0),
        datetime(2025, 6, 28, 1, 0),
        [quests.create_quest("Anh", 2)]
    )
    if s4:
        print("✅ Session đêm tạo thành công (qua ngày)")

    print("\n=== Kết thúc demo BASE_DATE ===\n")