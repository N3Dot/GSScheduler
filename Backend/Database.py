from typing import List, Dict, Any, Optional, Tuple, Callable
from enum import Enum

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
                 on_use_effect: Optional[Dict[str, int]] = None):
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
            on_use_effect (Dict[str, int]): Các chỉ số cộng thêm khi trang bị.           
        """
        self.name: str = name
        self.description: str = description
        self.category: str = category
        self.rarity: Rarity = rarity
        self.price: int = price
        self.icon: str = icon_path
        self.consumable: bool = consumable
        self.passive: bool = passive
        # THAY ĐỔI: Đổi tên từ stat_bonuses thành on_use_effect, xóa on_use_effect function cũ
        self.on_use_effect: Dict[str, int] = on_use_effect or {}
    
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
            "passive": self.passive,
            "on_use_effect": self.on_use_effect  # THAY ĐỔI: đổi tên từ stat_bonuses
        }
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name == other.name

    def __repr__(self) -> str:
        """Biểu diễn đối tượng Item dưới dạng chuỗi để dễ gỡ lỗi."""
        return f"Item(name='{self.name}', rarity='{self.rarity.name}')"

Items = {
    "Kiem_Dau_Si": Item(
        name="Kiếm Đấu Sĩ",
        description="Một thanh kiếm cơ bản, sắc bén, rất đáng tin cậy và có thể mua ở mọi nơi trong thành phố.",
        category="Vũ Khí",
        rarity=Rarity.COMMON,
        price=20,
        icon_path="Art/Items/Kiem_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 1, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Bua_Dau_Si": Item(
        name="Búa Đấu Sĩ",
        description="Một cây búa chiến nặng, mạnh mẽ nhưng tự hại bản thân.",
        category="Vũ Khí",
        rarity=Rarity.COMMON,
        price=30,
        icon_path="Art/Items/Bua_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 5, 'int': 0, 'luk': 0, 'hp': -20, 'xp': 0}
    ),
    "Chuy_Dau_Si": Item(
        name="Chùy Đấu Sĩ",
        description="Một cây chùy đơn giản, lựa chọn tầm trung hàng đầu các chiến binh.",
        category="Vũ Khí",
        rarity=Rarity.UNCOMMON,
        price=25,
        icon_path="Art/Items/Chuy_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 2, 'hp': 0, 'xp': 0}
    ),
    "Dinh_Ba_Vang": Item(
        name="Đinh Ba Vàng",
        description="Một cây đinh ba vàng trứ danh của vua biển cả, nghe đồn còn có thể gọi cả nàng tiên cá.",
        category="Vũ Khí",
        rarity=Rarity.RARE,
        price=50,
        icon_path="Art/Items/Dinh_ba_vang.png",
        passive=True,
        on_use_effect={'dex': 2, 'int': 0, 'luk': 2, 'hp': 0, 'xp': 0}
    ),
    "Gang_Quy": Item(
        name="Găng Quỷ",
        description="Một chiếc găng tay được làm từ chính đôi bàn tay của Satan sau thất bại trong Ngày phán quyết, tuy đã không còn mạnh mẽ, nhưng vẫn rất tà thuật.",
        category="Vũ Khí",
        rarity=Rarity.EPIC,
        price=105,
        icon_path="Art/Items/Gang_quy.png",
        passive=True,
        on_use_effect={'dex': 5, 'int': 5, 'luk': -2, 'hp': -10, 'xp': 0}
    ),
    "Gay_Phap_Su": Item(
        name="Gậy Pháp Sư",
        description="Cây gậy phép thuật trứ danh của Merlin Toàn năng.",
        category="Vũ Khí",
        rarity=Rarity.COMMON,
        price=30,
        icon_path="Art/Items/Gay_Phap_su.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 2, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Gay_Thuat_Si": Item(
        name="Gậy Thuật Sĩ",
        description="Cây gậy phép thuật này là bạn đồng hành của Học giả Bruno trong chuyến hành trình của anh.",
        category="Vũ Khí",
        rarity=Rarity.UNCOMMON,
        price=27,
        icon_path="Art/Items/Gay_Thuat_si.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 2, 'hp': 0, 'xp': 0}
    ),
    "Kiem_Chien_Tuong": Item(
        name="Kiếm Chiến Tướng",
        description="Thanh kiếm từng được dùng bởi Chinh tướng Pantheon, mặc dù anh chỉ dùng giáo...",
        category="Vũ Khí",
        rarity=Rarity.RARE,
        price=60,
        icon_path="Art/Items/Kiem_Chien_tuong.png",
        passive=True,
        on_use_effect={'dex': 4, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Kiem_Vo_Su": Item(
        name="Kiếm Vũ Sư",
        description="Một thanh kiếm nhẹ nhàng, thanh thoát của các vũ sư tại các hội chợ.",
        category="Vũ Khí",
        rarity=Rarity.UNCOMMON,
        price=35,
        icon_path="Art/Items/Kiem_Vo_su.png",
        passive=True,
        on_use_effect={'dex': 2, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Riu_Dau_Si": Item(
        name="Rìu Đấu Sĩ",
        description="Một chiếc rìu chiến đấu, chuyên dùng tại Arena này.",
        category="Vũ Khí",
        rarity=Rarity.COMMON,
        price=20,
        icon_path="Art/Items/Riu_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 1, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Riu_Tho_San": Item(
        name="Rìu Thợ Săn",
        description="Chiếc rìu được sử dụng bởi các gã thợ săn hung bạo nhất.",
        category="Vũ Khí",
        rarity=Rarity.UNCOMMON,
        price=30,
        icon_path="Art/Items/Riu_Tho_san.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 20, 'xp': 0}
    ),
    "Sach_Phep_Tru_Ta": Item(
        name="Sách Phép Trừ Tà",
        description="Sách thánh được Thiên thần Michael sử dụng trong Ngày phán quyết để tung ra đòn chí mạng cho Satan.",
        category="Vũ Khí",
        rarity=Rarity.EPIC,
        price=120,
        icon_path="Art/Items/Sach_phep_tru_ta.png",
        passive=True,
        on_use_effect={'dex': 3, 'int': 3, 'luk': 3, 'hp': 30, 'xp': 0}
    ),
    "Sung_Dan_Chu": Item(
        name="Súng Dân Chủ",
        description="Một khẩu súng lục cơ bản, dùng đạn thông thường...",
        category="Vũ Khí",
        rarity=Rarity.LEGENDARY,
        price=1250,
        icon_path="Art/Items/Sung_Dan_chu.png",
        passive=True,
        on_use_effect={'dex': 999, 'int': -3, 'luk': -3, 'hp': 0, 'xp': 0}
    ),



    "Khau_Trang": Item(
        name="Khẩu Trang",
        description="Một chiếc khẩu trang y tế, dùng để bảo vệ khỏi bụi bẩn, vi khuẩn và virut.",
        category="Mũ",
        rarity=Rarity.COMMON,
        price=25,
        icon_path="Art/Items/Khau_trang.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 10, 'xp': 0}
    ),
    "Mat_Na_An_Danh": Item(
        name="Mặt Nạ Ẩn Danh",
        description="Một chiếc mặt nạ để che giấu danh tính, trông rất bí ẩn.",
        category="Mũ",
        rarity=Rarity.UNCOMMON,
        price=32,
        icon_path="Art/Items/Mat_na_an_danh.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 1, 'hp': 0, 'xp': 0}
    ),
    "Mu_Chien_Tuong": Item(
        name="Mũ Chiến Tướng",
        description="Chiếc mũ của Chinh tướng Hy Lạp cổ, trông rất oai phong phải không?",
        category="Mũ",
        rarity=Rarity.RARE,
        price=70,
        icon_path="Art/Items/Mu_Chien_tuong.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 40, 'xp': 0}
    ),
    "Mu_Dau_Si": Item(
        name="Mũ Đấu Sĩ",
        description="Chiếc mũ sắt đơn giản của đấu sĩ, bảo vệ đầu khỏi các đòn tấn công.",
        category="Mũ",
        rarity=Rarity.COMMON,
        price=25,
        icon_path="Art/Items/Mu_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 1, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Mu_May_Man": Item(
        name="Mũ May Mắn",
        description="Một chiếc mũ nhỏ may mắn, có thể mang lại vận may cho người đội.",
        category="Mũ",
        rarity=Rarity.UNCOMMON,
        price=35,
        icon_path="Art/Items/Mu_May_man.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 2, 'hp': 0, 'xp': 0}
    ),
    "Mu_Noel": Item(
        name="Mũ Noel",
        description="Chiếc mũ mà Santa đánh rơi lúc hắt xì.",
        category="Mũ",
        rarity=Rarity.UNCOMMON,
        price=40,
        icon_path="Art/Items/Mu_Noel.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 2, 'hp': 0, 'xp': 0}
    ),
    "Mu_Pub": Item(
        name="Mũ Pub",
        description="Chiếc mũ bảo hiểm của những chiến binh tương lai gan dạ.",
        category="Mũ",
        rarity=Rarity.EPIC,
        price=120,
        icon_path="Art/Items/Mu_Pub.png",
        passive=True,
        on_use_effect={'dex': 2, 'int': 5, 'luk': 0, 'hp': 30, 'xp': 0}
    ),
    "Mu_Phap_Su": Item(
        name="Mũ Pháp Sư",
        description="Chiếc mũ chóp nhọn của pháp sư, tăng cường sức mạnh phép thuật.",
        category="Mũ",
        rarity=Rarity.COMMON,
        price=30,
        icon_path="Art/Items/Mu_Phap_su.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 1, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Mu_Phu_Thuy": Item(
        name="Mũ Phù Thủy",
        description="Chiếc mũ ma thuật của phù thủy, chứa đựng sức mạnh huyền bí.",
        category="Mũ",
        rarity=Rarity.COMMON,
        price=30,
        icon_path="Art/Items/Mu_Phu_thuy.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 1, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Mu_Rom": Item(
        name="Mũ Rơm",
        description="Một chiếc mũ rơm đơn giản, dùng để che nắng.",
        category="Mũ",
        rarity=Rarity.RARE,
        price=75,
        icon_path="Art/Items/Mu_rom.png",
        passive=True,
        on_use_effect={'dex': 1, 'int': 0, 'luk': 2, 'hp': 10, 'xp': 0}
    ),
    "Mu_Sinh_Nhat": Item(
        name="Mũ Sinh Nhật",
        description="Chiếc mũ mà năm ấy nhờ nó Satan suýt thoát chết (ổng vẫn chết...)",
        category="Mũ",
        rarity=Rarity.EPIC,
        price=123,
        icon_path="Art/Items/Mu_Sinh_nhat.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 4, 'hp': 0, 'xp': 0}
    ),
    "Mu_Thiet_Giap": Item(
        name="Mũ Thiết Giáp",
        description="Chiếc mũ giáp nặng mà Pantheon hay đội lúc gội đầu",
        category="Mũ",
        rarity=Rarity.UNCOMMON,
        price=42,
        icon_path="Art/Items/Mu_Thiet_giap.png",
        passive=True,
        on_use_effect={'dex': 2, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),



    "Khien_Bang": Item(
        name="Khiên Băng",
        description="Một chiếc khiên được làm từ băng, có khả năng phòng thủ và gây sát thương lạnh.",
        category="Khiên",
        rarity=Rarity.RARE,
        price=80,
        icon_path="Art/Items/Khien_bang.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 30, 'xp': 0}
    ),
    "Khien_Chien_Tuong": Item(
        name="Khiên Chiến Tướng",
        description="Chiếc khiên của một chiến tướng, cực kỳ chắc chắn và đáng tin cậy.",
        category="Khiên",
        rarity=Rarity.RARE,
        price=80,
        icon_path="Art/Items/Khien_Chien_tuong.png",
        passive=True,
        on_use_effect={'dex': 1, 'int': 0, 'luk': 0, 'hp': 20, 'xp': 0}
    ),
    "Khien_Dau_Si": Item(
        name="Khiên Đấu Sĩ",
        description="Chiếc khiên cơ bản của đấu sĩ, dùng để chặn các đòn tấn công.",
        category="Khiên",
        rarity=Rarity.COMMON,
        price=30,
        icon_path="Art/Items/Khien_Dau_si.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Khien_Doi_Truong_Meo": Item(
        name="Khiên Đội Trưởng Mẽo",
        description="Một chiếc khiên huyền thoại, được làm từ vật liệu hiếm có, gần như không thể phá hủy.",
        category="Khiên",
        rarity=Rarity.EPIC,
        price=200,
        icon_path="Art/Items/Khien_Doi_truong.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 50, 'xp': 0}
    ),
    "Khien_Go": Item(
        name="Khiên Gỗ",
        description="Chiếc khiên được làm từ gỗ, nhẹ và dễ sử dụng.",
        category="Khiên",
        rarity=Rarity.COMMON,
        price=31,
        icon_path="Art/Items/Khien_go.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 10, 'xp': 0}
    ),
    "Khien_Mat_Troi": Item(
        name="Khiên Mặt Trời",
        description="Chiếc khiên tỏa sáng như mặt trời, có khả năng phản lại ánh sáng và gây choáng kẻ địch.",
        category="Khiên",
        rarity=Rarity.EPIC,
        price=201,
        icon_path="Art/Items/Khien_Mat_troi.png",
        passive=True,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 3, 'hp': 20, 'xp': 0}
    ),
    "Khien_Nokia": Item(
        name="Khiên Nokia",
        description="Một chiếc điện thoại Nokia cũ huyền thoại, nghe bảo có giai thoại rằng đây mới là thứ Michael ném đi làm Satan chết.",
        category="Khiên",
        rarity=Rarity.EPIC,
        price=203,
        icon_path="Art/Items/Khien_Nokia.png",
        passive=True,
        on_use_effect={'dex': 3, 'int': 0, 'luk': 0, 'hp': 20, 'xp': 0}
    ),



    "Banh_Quy_Tri_Tue": Item(
        name="Bánh Quy Trí Tuệ",
        description="Một chiếc bánh quy đặc biệt, khi ăn vào sẽ tăng trí tuệ trong một thời gian ngắn.",
        category="Tiêu Hao",
        rarity=Rarity.UNCOMMON,
        price=17,
        icon_path="Art/Items/Banh_Quy_Tri_Tue.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 2, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Ca_Phe": Item(
        name="Cà Phê",
        description="Còn gì tuyệt hơn một tách cà phê nóng hổi trong lúc bạn và đồng đội đang chiến đấu...",
        category="Tiêu Hao",
        rarity=Rarity.COMMON,
        price=10,
        icon_path="Art/Items/Ca_Phe.png",
        passive=False,
        on_use_effect={'dex': 1, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Sinh_To_Lua_Mach": Item(
        name="Sinh Tố Lúa Mạch",
        description="Một ly sinh tố lúa mạch, giúp bạn cảm thấy tràn niềm vui cùng bạn bè.",
        category="Tiêu Hao",
        rarity=Rarity.COMMON,
        price=10,
        icon_path="Art/Items/Sinh_To_Lua_Mach.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 3, 'xp': 3}
    ),
    "Tai_Loc": Item(
        name="Tài Lộc",
        description="Một loại dược phẩm huyền thoại mà dân gian truyền miệng có thể giúp người dùng mạnh mẽ hơn.",
        category="Tiêu Hao",
        rarity=Rarity.EPIC,
        price=40,
        icon_path="Art/Items/Tai_Loc.png",
        passive=False,
        on_use_effect={'dex': 2, 'int': 1, 'luk': 1, 'hp': 20, 'xp': 0}
    ),
    "Thit_Bo": Item(
        name="Thịt Bò",
        description="Một miếng thịt bò còn tươi còn của những con bò vừa thi THPT.",
        category="Tiêu Hao",
        rarity=Rarity.RARE,
        price=25,
        icon_path="Art/Items/Thit_Bo.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 3, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Thuoc_HP": Item(
        name="Thuốc Đỏ",
        description="Bình thuốc hồi máu cơ bản, giúp phục hồi một phần HP.",
        category="Tiêu Hao",
        rarity=Rarity.UNCOMMON,
        price=15,
        icon_path="Art/Items/Thuoc_HP.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 20, 'xp': 0}
    ),
    "Thuoc_Kinh_Nghiem": Item(
        name="Thuốc Kinh Nghiệm",
        description="Bình thuốc giúp tăng điểm kinh nghiệm nhận được trong một thời gian.",
        category="Tiêu Hao",
        rarity=Rarity.COMMON,
        price=10,
        icon_path="Art/Items/Thuoc_Kinh_Nghiem.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 6}
    ),
    "Thuoc_May_Man": Item(
        name="Thuốc May Mắn",
        description="Bình thuốc màu xanh lam, tăng chỉ số may mắn khi sử dụng.",
        category="Tiêu Hao",
        rarity=Rarity.COMMON,
        price=60,
        icon_path="Art/Items/Thuoc_May_Man.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 1, 'hp': 0, 'xp': 0}
    ),
    "Thuoc_Quy": Item(
        name="Thuốc Quỷ",
        description="Một lọ thuốc chứa giọt máu cuối cùng của Satan.",
        category="Tiêu Hao",
        rarity=Rarity.EPIC,
        price=57,
        icon_path="Art/Items/Thuoc_Quy.png",
        passive=False,
        on_use_effect={'dex': 3, 'int': 1, 'luk': -2, 'hp': 10, 'xp': 0}
    ),
    "Sau_Rieng": Item(
        name="Sầu Riêng",
        description="Một loại trái, có mùi hương có thể đẩy lùi cả quỷ, thiên hạ đồn ăn vào nhiều tác dụng lắm, nhưng mà chưa ai dám thử...",
        category="Tiêu Hao",
        rarity=Rarity.EPIC,
        price=60,
        icon_path="Art/Items/Sau_Rieng.png",
        passive=False,
        on_use_effect={'dex': 8, 'int': -2, 'luk': 0, 'hp': -20, 'xp': 5}
    )
}

Achievements = {
    "BuocDiDauTien": Item(
        name="Bước Đi Đầu Tiên",
        description="Chinh phục phiên học đầu tiên.",
        category="Thành Tích",
        rarity=Rarity.LEGENDARY,
        price=10,
        icon_path="Art/Items/Thanh_Tich.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "HocVienXuatSac": Item(
        name="Học Viên Xuất Sắc",
        description="Đạt kết quả S cho 1 phiên học. Quá xuất sắc!",
        category="Thành Tích",
        rarity=Rarity.LEGENDARY,
        price=10,
        icon_path="Art/Items/Thanh_Tich.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "ChamChiCanCu": Item(
        name="Chăm Chỉ Cần Cù",
        description="Dành ít nhất 1 tiếng cho phiên học cùa mình.",
        category="Thành Tích",
        rarity=Rarity.LEGENDARY,
        price=10,
        icon_path="Art/Items/Thanh_Tich.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "BacThayNhiemVu": Item(
        name="Bậc Thầy Nhiệm Vụ",
        description="Chinh phục ít nhất 3 nhiệm vụ trong quá trình học.",
        category="Thành Tích",
        rarity=Rarity.LEGENDARY,
        price=10,
        icon_path="Art/Items/Thanh_Tich.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    ),
    "Chuoi3Ngay": Item(
        name="Chuỗi 3 Ngày",
        description="Được điểm danh 3 lần liên tiếp. Một chiến sĩ gương mẫu!",
        category="Thành Tích",
        rarity=Rarity.LEGENDARY,
        price=10,
        icon_path="Art/Items/Thanh_Tich.png",
        passive=False,
        on_use_effect={'dex': 0, 'int': 0, 'luk': 0, 'hp': 0, 'xp': 0}
    )
}