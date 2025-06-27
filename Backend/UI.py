import os

from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.fitimage import FitImage
from kivy.graphics import Color, RoundedRectangle

RARITY_COLORS = {
    "Common": {
        "border": (0.65, 0.65, 0.65, 1),
        "background": (0.65, 0.65, 0.65, 0.2),
        "text": (0.3, 0.3, 0.3, 1),
    },
    "Uncommon": {
        "border": (0.24, 0.75, 0.33, 1),
        "background": (0.24, 0.75, 0.33, 0.2),
        "text": (0.1, 0.4, 0.15, 1),
    },
    "Rare": {
        "border": (0.26, 0.52, 0.96, 1),
        "background": (0.26, 0.52, 0.96, 0.2),
        "text": (0.12, 0.25, 0.5, 1),
    },
    "Epic": {
        "border": (0.63, 0.22, 0.89, 1),
        "background": (0.63, 0.22, 0.89, 0.2),
        "text": (0.35, 0.0, 0.5, 1),
    },
    "Legendary": {
        "border": (1.0, 0.69, 0.0, 1),
        "background": (1.0, 0.69, 0.0, 0.2),
        "text": (0.5, 0.35, 0.0, 1),
    },
}

Builder.load_file("Backend/KV/ItemCard.kv")
class ItemCard(MDCard):
    name = StringProperty()
    icon = StringProperty()
    rarity = StringProperty("Common")
    borderColor = ListProperty([0.65, 0.65, 0.65, 1])
    backgroundColor = ListProperty([0.65, 0.65, 0.65, 0.2])
    textColor = ListProperty([0.3, 0.3, 0.3, 1])
    ID = None

    def on_touch_down(self, touch):
        for child in self.children[::-1]:
            if child.collide_point(*touch.pos) and child.__class__.__name__ == "MDBoxLayout":
                MDApp.get_running_app().on_click_item()
                return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_rarity(self, instance, value):
        colors = RARITY_COLORS[self.rarity]
        self.borderColor = colors["border"]
        self.backgroundColor = colors["background"]
        self.textColor = colors["text"]

Builder.load_file("Backend/KV/ItemShopCard.kv")
class ItemShopCard(MDCard):
    name = StringProperty()
    icon = StringProperty()
    price = StringProperty()
    rarity = StringProperty("Common")
    borderColor = ListProperty([0.65, 0.65, 0.65, 1])
    backgroundColor = ListProperty([0.65, 0.65, 0.65, 0.2])
    textColor = ListProperty([0.3, 0.3, 0.3, 1])
    ID = None

    def on_touch_down(self, touch):
        for child in self.children[::-1]:
            if child.collide_point(*touch.pos) and child.__class__.__name__ == "MDBoxLayout":
                MDApp.get_running_app().on_click_item()
                return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_rarity(self, instance, value):
        colors = RARITY_COLORS[self.rarity]
        self.borderColor = colors["border"]
        self.backgroundColor = colors["background"]
        self.textColor = colors["text"]

Builder.load_file("Backend/KV/ScheduleCard.kv")
class ScheduleCard(MDCard):
    startTime = StringProperty()
    endTime = StringProperty()
    description = StringProperty()
    expectedLoot = StringProperty()
    questTotal = NumericProperty()
    ID = None

Builder.load_file("Backend/KV/CharacterCard.kv")
class CharacterCard(MDBoxLayout):
    name = StringProperty("Nguyễn Văn A")
    title = StringProperty("Hạng Tân Binh")
    imagePath = StringProperty(f"https://picsum.photos/600/600")
    level = NumericProperty(1)
    hpCurrent = NumericProperty(50)
    hpMax = NumericProperty(50)
    xpCurrent = NumericProperty(0)
    xpMax = NumericProperty(10)
    dex = NumericProperty(1)
    int = NumericProperty(1)
    luk = NumericProperty(1)
    available_points = NumericProperty(0)

    def on_level(self, instance, value):
        if value < 5:
            self.title = "Hạng Tân Binh"
        elif value < 10:
            self.title = "Hạng Chiến Binh"
        elif value < 15:
            self.title = "Hạng Cựu Binh"
        elif value < 20:
            self.title = "Hạng Ưu Tú"
        elif value < 25:
            self.title = "Hạng Tướng Quân"
        elif value < 35:
            self.title = "Hạng Anh Hùng"
        elif value < 50:
            self.title = "Hạng Huyền Thoại"
        elif value < 75:
            self.title = "Hạng Siêu Việt"
        else:
            self.title = "Hạng Thần Thoại"

Builder.load_file("Backend/KV/ScheduleCharacterCard.kv")
class ScheduleCharacterCard(MDBoxLayout):
    name = StringProperty("Nguyễn Văn A")
    imagePath = StringProperty(f"https://picsum.photos/600/600")
    level = NumericProperty(1)
    hpCurrent = NumericProperty(50)
    hpMax = NumericProperty(50)
    xpCurrent = NumericProperty(0)
    xpMax = NumericProperty(10)
    goldAmount = NumericProperty(10)

Builder.load_file("Backend/KV/BarWide.kv")
class BarWide(MDBoxLayout):
    statName = StringProperty("HP")
    current = NumericProperty(100)
    max = NumericProperty(100)
    isLight = BooleanProperty(False)

Builder.load_file("Backend/KV/GoldCounterCard.kv")
class GoldCounterCard(MDCard):
    goldAmount = NumericProperty(0)
   
Builder.load_file("Backend/KV/QuestCard.kv")
class QuestCard(MDCard):
    difficulty = StringProperty()
    description = StringProperty()

class QRCodeWidget(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("160dp", "160dp")
        self.pos_hint = {"right": 0.98, "top": 0.98}
        # White background with transparency
        with self.canvas.before:
            Color(1, 1, 1, 0.9)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
        # QR Image
        self.qr_image = FitImage(
            source=f"https://picsum.photos/150/150",
            size_hint=(None, None),
            size=("150dp", "150dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.add_widget(self.qr_image)
        # Refresh button
        self.refresh_btn = MDIconButton(
            icon="refresh",
            size_hint=(None, None),
            size=("20dp", "20dp"),
            pos_hint={"right": 1, "top": 1},
            theme_icon_color="Custom",
            icon_color=(0.5, 0.5, 0.5, 0.8),
            on_release=lambda x: MDApp.get_running_app().update_qr_code(),
        )
        self.add_widget(self.refresh_btn)
    
    def update_qr_image(self, image_path):
        """Cập nhật hình ảnh QR code"""
        if image_path and os.path.exists(image_path):
            self.qr_image.source = image_path
            self.qr_image.reload()
        else:
            self.qr_image.source = ""
            print(f"QR image file not found: {image_path}")

# Arena UI Components
class ArenaSkillButton(MDCard):
    skill_name = StringProperty()
    icon = StringProperty()
    icon_color = ListProperty([0.2, 0.6, 0.9, 1])
    skill_type = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = ("80dp", "80dp")
        self.elevation = 2
        self.radius = [8]
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = MDApp.get_running_app()
            if hasattr(app, 'on_arena_skill_selected'):
                app.on_arena_skill_selected(self.skill_type)
            return True
        return super().on_touch_down(touch)

class ArenaCharacterDisplay(MDBoxLayout):
    character_name = StringProperty("Player")
    level = NumericProperty(1)
    hp_current = NumericProperty(50)
    hp_max = NumericProperty(50)
    dex = NumericProperty(1)
    int_stat = NumericProperty(1)  # Tránh conflict với keyword 'int'
    luk_stat = NumericProperty(1)  # Đổi tên từ luk thành luk_stat
    avatar_path = StringProperty("https://picsum.photos/100/100")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "120dp"
        self.spacing = "8dp"
        self.padding = "8dp"
