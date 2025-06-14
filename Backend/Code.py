import uuid
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional, Tuple, Callable
from enum import Enum
import random
import time

class Rarity(Enum):
    """Định nghĩa các cấp độ hiếm của vật phẩm."""
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

class Item:
    """
    Đại diện cho một vật phẩm trong trò chơi.
    Lớp này chứa tất cả thông tin chi tiết về một vật phẩm, từ tên, mô tả,
    đến các hiệu ứng khi sử dụng.
    """
    def __init__(self,
                 name: str,
                 description: str,
                 category: str,
                 rarity: Rarity,
                 price: int,
                 icon_path: str,
                 consumable: bool = False,
                 passive: bool = False,
                 on_use_effect: Optional[Callable[['Character', 'RewardSystem'], None]] = None):
        """
        Khởi tạo một đối tượng Item mới.

        Args:
            name (str): Tên của vật phẩm (duy nhất).
            description (str): Mô tả chi tiết về vật phẩm.
            category (str): Loại vật phẩm (ví dụ: 'Trang bị', 'Tiêu hao').
            rarity (Rarity): Độ hiếm của vật phẩm.
            price (int): Giá trị của vật phẩm bằng vàng.
            icon_path (str): Đường dẫn đến file icon của vật phẩm.
            consumable (bool): True nếu vật phẩm sẽ biến mất sau khi sử dụng.
            passive (bool): True nếu vật phẩm có hiệu ứng bị động khi trang bị.
            on_use_effect (Callable): Một hàm sẽ được gọi khi vật phẩm được sử dụng.
        """
        self.name: str = name
        self.description: str = description
        self.category: str = category
        self.rarity: Rarity = rarity
        self.price: int = price
        self.icon: str = icon_path
        self.consumable: bool = consumable
        self.passive: bool = passive
        self.on_use_effect = on_use_effect

    def get_details(self) -> Dict[str, Any]:
        """Trả về một từ điển chứa thông tin chi tiết của vật phẩm."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "rarity": self.rarity.name,
            "price": self.price,
            "icon": self.icon,
            "consumable": self.consumable,
            "passive": self.passive
        }

    def use_item(self, character: 'Character', reward_system: 'RewardSystem'):
        """
        Xử lý logic khi nhân vật sử dụng vật phẩm này.
        Chỉ có tác dụng với các vật phẩm 'consumable'.
        """
        if not self.consumable:
            print(f"Vật phẩm '{self.name}' không thể sử dụng theo cách này.")
            return

        print(f"{character.name} đã sử dụng {self.name}.")
        # Gọi hiệu ứng đặc biệt của vật phẩm nếu có
        if self.on_use_effect:
            self.on_use_effect(character, reward_system)

        # Xóa vật phẩm khỏi kho đồ của nhân vật nếu nó là loại tiêu hao
        if self in character.inventory:
            character.inventory.remove(self)
            print(f"'{self.name}' đã biến mất khỏi kho đồ.")

    def __repr__(self) -> str:
        """Biểu diễn đối tượng Item dưới dạng chuỗi để dễ gỡ lỗi."""
        return f"Item(name='{self.name}', rarity='{self.rarity.name}')"

class Character:
    """
    Đại diện cho người dùng trong ứng dụng.
    Lớp này quản lý tất cả các chỉ số, tài sản, trang bị, và tiến trình của nhân vật.
    """
    def __init__(self, name: str):
        self.name: str = name
        self.skin_visuals: str = "default_skin.png"  # Ngoại hình cơ bản
        self.equipment_visuals: List[Tuple[str, Tuple[int, int]]] = []  # Các lớp hình ảnh trang bị
        self.equipment: List[Item] = []  # Danh sách các vật phẩm đã trang bị
        self.inventory: List[Item] = []  # Kho đồ chứa các vật phẩm
        self.achievements: List[Item] = []  # Các thành tích dưới dạng vật phẩm (nếu có)
        self.unlocked_achievements = set()  # Tập hợp các ID thành tích đã mở khóa
        
        # Chỉ số cấp độ và kinh nghiệm
        self.level: int = 1
        self.xp: int = 0
        self.xp_to_next_level: int = 100
        
        # Chỉ số chiến đấu và thuộc tính
        self.hp: int = 50
        self.dex: int = 1  # Khéo léo -> Tăng XP nhận được
        self.int: int = 1  # Trí tuệ -> Giảm hình phạt
        self.luk: int = 1  # May mắn -> Tăng vàng nhận được
        self.available_points: int = 0  # Điểm cộng có sẵn để tăng chỉ số
        
        # Tài sản
        self.gold: int = 10
        print(f"Nhân vật '{self.name}' đã được tạo với {self.xp} XP và {self.gold} Vàng.")

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
            self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            
            print(f"🎉 CHÚC MỪNG! {self.name} đã lên cấp {self.level}!")
            print(f"   Bạn nhận được 1 điểm cộng. XP cần cho cấp tiếp theo: {self.xp_to_next_level}.")
        return leveled_up

    def add_achievement(self, achievement_id: str):
        """Thêm ID của một thành tích đã mở khóa vào danh sách."""
        if achievement_id not in self.unlocked_achievements:
            self.unlocked_achievements.add(achievement_id)
            print(f"🏆 THÀNH TÍCH MỚI ĐƯỢC MỞ KHÓA: {achievement_id}")

    def update_appearance(self):
        """(Mô phỏng) Cập nhật ngoại hình nhân vật dựa trên trang bị đang mặc."""
        print("Đang cập nhật ngoại hình nhân vật...")
        print(f"Ngoại hình đã được cập nhật dựa trên {len(self.equipment)} trang bị.")

    def show_stats(self):
        """Hiển thị các chỉ số hiện tại của nhân vật một cách trực quan."""
        print("\n--- TRẠNG THÁI NHÂN VẬT ---")
        print(f"Tên: {self.name}")
        print(f"Cấp độ: {self.level}")
        print(f"Kinh nghiệm: {self.xp}/{self.xp_to_next_level}")
        print(f"Vàng: {self.gold}")
        print(f"Điểm cộng có sẵn: {self.available_points}")
        print(f"Chỉ số: HP({self.hp}), DEX({self.dex}), INT({self.int}), LUK({self.luk})")
        print(f"Kho đồ: {[item.name for item in self.inventory] or ['Trống']}")
        print(f"Thành tích: {list(self.unlocked_achievements) or ['Chưa có']}")
        print("--------------------------\n")

class RewardSystem:
    """
    Quản lý việc tính toán và trao thưởng/phạt cho nhân vật.
    Lớp này tách biệt logic thưởng ra khỏi các hệ thống khác.
    """
    def __init__(self):
        self.reward_types: List[str] = ["xp", "gold", "item", "achievement"]

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
                print(f"   + {amount} XP.")
                character.check_level_up() # Tự động kiểm tra lên cấp
            elif reward_type == "gold":
                amount = int(reward["amount"])
                character.gold += amount
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
        if punishment_type == "gold":
            base_amount = punishment.get("amount", 0)
            # Mỗi điểm INT giảm 2% lượng vàng bị phạt, tối đa giảm 80%
            reduction_modifier = max(0.2, 1 - (character.int * 0.02))
            final_amount = int(base_amount * reduction_modifier)
            
            character.gold -= final_amount
            # Đảm bảo vàng không bị âm
            if character.gold < 0:
                character.gold = 0
            
            print(f"Nhân vật {character.name} bị phạt {final_amount} vàng vì không hoàn thành mục tiêu.")
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
    Quản lý một phiên học. Đã loại bỏ thuộc tính 'tags'.
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
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time
        #Thời gian kết thúc thật
        self.actual_end_time: Optional[datetime] = None
        self.status: str = 'Scheduled' #scheduled - running - finished
        self.rank: str = "N/A" #rank gồm a,b,c,d,f

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
        # Ghi lại thời gian kết thúc thực tế (dùng thời gian được truyền vào hoặc thời gian dự kiến)
        self.actual_end_time = end_time_override if end_time_override else self.end_time
        
        # Tính điểm hoàn thành nhiệm vụ (tỷ lệ từ 0.0 đến 1.0)
        quest_completion_score = self.quest_progress
        
        # Tính thời gian thực tế đã học (đơn vị: giây)
        time_spent_seconds = (self.actual_end_time - self.start_time).total_seconds()
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
        print(f"Phiên học '{self.goal_description}' đã kết thúc với Hạng: {self.rank} (Hoàn thành {progress_percent} nhiệm vụ, điểm: {final_performance_score:.2f}).")

    def get_session_data(self) -> Dict[str, Any]:
        """Trả về dữ liệu tóm tắt của phiên học, không có 'tags'."""
        # Tính thời lượng thực tế của phiên học (nếu đã kết thúc) hoặc 0 (nếu chưa kết thúc)
        duration = self.actual_end_time - self.start_time if self.actual_end_time else timedelta(0)
        # Trả về dictionary chứa tất cả thông tin quan trọng của phiên học
        return {
            "session_id": self.session_id,                           # ID duy nhất của phiên học
            "goal": self.goal_description,                           # Mô tả mục tiêu phiên học
            "status": self.status,                                   # Trạng thái hiện tại (Scheduled/Running/Finished)
            "start_time": self.start_time,                          # Thời gian bắt đầu dự kiến
            "end_time": self.end_time,                              # Thời gian kết thúc dự kiến
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
            'ChamChiCanCu': {'metric': 'total_study_hours', 'value': 0.01, 'name': 'Chăm Chỉ Cần Cù'},
            'BacThayNhiemVu': {'metric': 'quests_completed', 'value': 2, 'name': 'Bậc Thầy Nhiệm Vụ'},
            'Chuoi3Ngay': {'metric': 'focus_streak', 'value': 2, 'name': 'Chuỗi 2 Ngày'}
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
        self.session_history.append(session_data)
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
        self.focus_streak = self._calculate_focus_streak()

    def _calculate_focus_streak(self) -> int:
        """Tính số ngày học liên tiếp."""
        if not self.session_history: return 0
        
        # Lấy danh sách các ngày học duy nhất và sắp xếp chúng
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
            "📊======= BÁO CÁO HỌC TẬP CỦA BẠN =======📊",
            # ... các dòng báo cáo khác giữ nguyên ...
            f"   S: {stats['rank_counts']['S']} | A: {stats['rank_counts']['A']} | B: {stats['rank_counts']['B']} | C: {stats['rank_counts']['C']} | F: {stats['rank_counts']['F']}",
            "",
            "--- Nhiệm Vụ ---",
            f"🎯 Nhiệm Vụ Hoàn Thành: {stats['quests_completed']} / {len(self.quest_system.active_quests)}",
            f"   Tỷ Lệ Hoàn Thành: {stats['quest_completion_rate']:.1f}%",
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
        Thuộc tính 'tags' đã được loại bỏ khỏi phương thức này.

        Returns:
            Đối tượng StudySession vừa được tạo nếu thành công, ngược lại là None.
        """
        try:
            # (Có thể thêm logic kiểm tra trùng lặp thời gian ở đây nếu cần)
            session = StudySession(goal_description, start_time, end_time, linked_quests)
            self.sessions.append(session)
            print(f"🗓️  ĐÃ LÊN LỊCH: '{session.goal_description}' lúc {session.start_time.strftime('%H:%M:%S')}")
            return session
        except (ValueError, KeyError) as e:
            print(f"❌ LÊN LỊCH THẤT BẠI: {e}")
            return None

    def mark_quest_as_complete(self, session_id: str, quest_id: str):
        """
        Đánh dấu một nhiệm vụ là đã hoàn thành trong một phiên học đang chạy.
        Đây là "cầu nối" giữa giao diện người dùng và logic của StudySession.
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
                session.status = 'Running'
                print(f"▶️  BẮT ĐẦU: '{session.goal_description}'")
            
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
                self.reward_system.punish(self.character, {'type': 'gold', 'amount': total_difficulty_failed * 5})

# --- VÍ DỤ MÔ PHỎNG ---
# =============================================================================
if __name__ == "__main__":
    char = Character(name="Nhật Nam")
    rewards = RewardSystem()
    
    # SỬA ĐỔI Ở ĐÂY:
    # 1. Tạo một đối tượng QuestSystem.
    quests = QuestSystem() 
    # 2. Truyền đối tượng quests vào StudyAnalytics, không phải None.
    analytics = StudyAnalytics(quest_system=quests) 
    
    # 3. SessionManager không cần quest_system nữa, vì nó không tạo quest.
    # Nó chỉ nhận quest từ bên ngoài khi lên lịch.
    manager = SessionManager(character=char, reward_system=rewards, analytics=analytics)
    
    # 2. Tạo các đối tượng Quest riêng lẻ thông qua QuestSystem
    # Cách tạo quest không thay đổi, chỉ là giờ chúng được quản lý bởi `quests`.
    quest1 = quests.create_quest(description="Viết phần Mở đầu báo cáo", difficulty=2)
    quest2 = quests.create_quest(description="Thiết kế Class Diagram", difficulty=4)
    quest3 = quests.create_quest(description="Viết code cho 3 Class", difficulty=5)

    # 3. Lên lịch một phiên học và liên kết với các Quest đã tạo
    simulated_now = datetime.now()
    session1 = manager.schedule_session(
        goal_description="Làm báo cáo OOP - Giai đoạn 1",
        start_time=simulated_now + timedelta(seconds=2),
        end_time=simulated_now + timedelta(seconds=25), # Thời gian dự kiến là 23 giây
        linked_quests=[quest1, quest2, quest3] # Truyền danh sách các đối tượng Quest
    )

    # ... phần còn lại của vòng lặp mô phỏng giữ nguyên ...
    print("\n--- Bắt đầu Vòng lặp Mô phỏng ---")
    end_of_simulation = simulated_now + timedelta(seconds=30)
    current_sim_time = simulated_now
    
    session_has_started = False
    
    while current_sim_time < end_of_simulation:
        print(f"\n--- Tick lúc {current_sim_time.strftime('%H:%M:%S')} ---")
        manager.update(current_time=current_sim_time)
        
        # Mô phỏng người dùng hoàn thành các quest trong lúc học
        if session1 and session1.status == 'Running':
            if not session_has_started:
                session_has_started = True
                print(">>> Phiên học đang chạy. Người dùng bắt đầu làm việc...")

            time_in_session = (current_sim_time - session1.start_time).total_seconds()
            
            # Sau 5 giây, người dùng làm xong quest đầu tiên
            if 5 <= time_in_session < 6 and not quest1.is_completed:
                manager.mark_quest_as_complete(session1.session_id, quest1.quest_id)
            
            # Sau 12 giây, làm xong quest thứ hai
            if 12 <= time_in_session < 13 and not quest2.is_completed:
                manager.mark_quest_as_complete(session1.session_id, quest2.quest_id)
            
            # Người dùng quyết định kết thúc sớm sau 18 giây
            if 18 <= time_in_session < 19:
                manager.end_session_manually(session1.session_id)
                break

        time.sleep(1)
        current_sim_time += timedelta(seconds=1)
        
    print("\n\n--- MÔ PHỎNG KẾT THÚC ---")
    # In ra báo cáo cuối cùng nếu cần
    print(analytics.generate_report())
    char.show_stats()