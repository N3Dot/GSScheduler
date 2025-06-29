from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.fitimage import FitImage
from kivy.graphics import Color, RoundedRectangle

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
import random

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
    item = ObjectProperty()
    name = StringProperty()
    icon = StringProperty()
    rarity = StringProperty("Common")
    borderColor = ListProperty([0.65, 0.65, 0.65, 1])
    backgroundColor = ListProperty([0.65, 0.65, 0.65, 0.2])
    textColor = ListProperty([0.3, 0.3, 0.3, 1])

    def on_touch_down(self, touch):
        for child in self.children[::-1]:
            if child.collide_point(*touch.pos) and child.__class__.__name__ == "MDBoxLayout":
                MDApp.get_running_app().on_click_owned_item(self)
                return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_item(self, instance, value):
        if self.item:
            self.name = self.item.name
            self.icon = self.item.icon
            rarity_types = [None, "Common", "Uncommon", "Rare", "Epic", "Legendary"]
            self.rarity = rarity_types[self.item.rarity.value]

    def on_rarity(self, instance, value):
        colors = RARITY_COLORS[self.rarity]
        self.borderColor = colors["border"]
        self.backgroundColor = colors["background"]
        self.textColor = colors["text"]

Builder.load_file("Backend/KV/ItemShopCard.kv")
class ItemShopCard(MDCard):
    item = ObjectProperty()
    name = StringProperty()
    icon = StringProperty()
    price = StringProperty()
    rarity = StringProperty("Common")
    borderColor = ListProperty([0.65, 0.65, 0.65, 1])
    backgroundColor = ListProperty([0.65, 0.65, 0.65, 0.2])
    textColor = ListProperty([0.3, 0.3, 0.3, 1])

    def on_touch_down(self, touch):
        for child in self.children[::-1]:
            if child.collide_point(*touch.pos) and child.__class__.__name__ == "MDBoxLayout":
                MDApp.get_running_app().on_click_item(self)
                return super().on_touch_down(touch)
        return super().on_touch_down(touch)
    
    def on_item(self, instance, value):
        if self.item:
            self.name = self.item.name
            self.icon = self.item.icon
            self.price = str(self.item.price)
            rarity_types = [None, "Common", "Uncommon", "Rare", "Epic", "Legendary"]
            self.rarity = rarity_types[self.item.rarity.value]

    def on_rarity(self, instance, value):
        colors = RARITY_COLORS[self.rarity]
        self.borderColor = colors["border"]
        self.backgroundColor = colors["background"]
        self.textColor = colors["text"]

Builder.load_file("Backend/KV/ScheduleCard.kv")
class ScheduleCard(MDCard):
    session = ObjectProperty()
    startTime = StringProperty()
    endTime = StringProperty()
    description = StringProperty()
    expectedLoot = StringProperty()
    questTotal = NumericProperty()
    isOn = BooleanProperty()

    def toggle(self, value):
        if self.session:
            if value == False:
                self.session.status = "Finished"
                print(f"Current session is temporarily marked as Finished (Disabled)")
            else:
                self.session.status = "Scheduled"

    def on_session(self, instance, value):
        if self.session:
            self.startTime=self.session.start_time.strftime("%H:%M")
            self.endTime=self.session.end_time.strftime("%H:%M")
            self.description=self.session.goal_description
            if self.session.status == "Finished":
                self.isOn = False
            else:
                self.isOn = True
            self.questTotal = 0
            diffTotal = 0
            for quest in self.session.linked_quests:
                self.questTotal += 1
                diffTotal += quest.difficulty
            diffAvg = diffTotal/self.questTotal
            if diffAvg > 4:
                self.expectedLoot = "Khủng"
            elif diffAvg > 3:
                self.expectedLoot = "Khó"
            elif diffAvg > 2:
                self.expectedLoot = "Vừa"
            else:
                self.expectedLoot = "Dễ"

Builder.load_file("Backend/KV/QuestCard.kv")
class QuestCard(MDCard):
    quest = ObjectProperty()
    difficulty = StringProperty()
    description = StringProperty()

    def on_quest(self, instance, value):
        self.difficulty = str(self.quest.difficulty)
        self.description = self.quest.description

Builder.load_file("Backend/KV/QuestLockCard.kv")
class QuestLockCard(MDCard):
    difficulty = StringProperty()
    description = StringProperty()
    quest = ObjectProperty()

    def on_checkbox_active(self, checkbox, value):
        if self.quest:
            if value == False:
                self.quest.is_completed = False
            else:
                self.quest.is_completed = True
                print(f"   -> Nhiệm vụ '{self.quest.description}' đã được đánh dấu hoàn thành!")

    def on_quest(self, instance, value):
        self.difficulty = str(self.quest.difficulty)
        self.description = self.quest.description

Builder.load_file("Backend/KV/CharacterCard.kv")
class CharacterCard(MDBoxLayout):
    name = StringProperty("Nguyễn Văn A")
    title = StringProperty("Hạng Tân Binh")
    imagePath = StringProperty(f"")
    level = NumericProperty(1)
    hpCurrent = NumericProperty(50)
    hpMax = NumericProperty(50)
    xpCurrent = NumericProperty(0)
    xpMax = NumericProperty(10)
    dex = NumericProperty(1)
    int = NumericProperty(1)
    luk = NumericProperty(1)
    available_points = NumericProperty(0)

    def on_imagePath(self, instance, value):
        self.ids.character_image.source = self.imagePath
        self.ids.character_image.reload()

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
    imagePath = StringProperty(f"")
    level = NumericProperty(1)
    hpCurrent = NumericProperty(50)
    hpMax = NumericProperty(50)
    xpCurrent = NumericProperty(0)
    xpMax = NumericProperty(10)
    goldAmount = NumericProperty(10)

    def on_imagePath(self, instance, value):
        self.ids.character_image.source = self.imagePath
        self.ids.character_image.reload()

Builder.load_file("Backend/KV/BarWide.kv")
class BarWide(MDBoxLayout):
    statName = StringProperty("HP")
    current = NumericProperty(100)
    max = NumericProperty(100)
    isLight = BooleanProperty(False)

Builder.load_file("Backend/KV/GoldCounterCard.kv")
class GoldCounterCard(MDCard):
    goldAmount = NumericProperty(0)

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

class ArenaOpponentInput(MDBoxLayout):
    """Component cho việc nhập dữ liệu đối thủ với hint text"""
    hint_text = StringProperty("Nhập mã QR hoặc base64 của đối thủ...")
    input_text = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "8dp"
        self.adaptive_height = True
    
    def on_input_validate(self):
        """Callback khi người dùng nhập xong dữ liệu"""
        app = MDApp.get_running_app()
        if hasattr(app, 'on_arena_opponent_input'):
            app.on_arena_opponent_input(self.input_text)

# Effects và Animation Components
class ConfettiParticle(Widget):
    def __init__(self, pos, **kwargs):
        super().__init__(**kwargs)
        self.size = (10, 10)
        self.x, self.y = pos
        self.velocity = [
            random.uniform(-250, 250),
            random.uniform(450, 650)
        ]
        self.gravity = -300
        self.lifetime = 8
        self.age = 0

        r, g, b = random.random(), random.random(), random.random()
        with self.canvas:
            Color(r, g, b)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_graphics)
        Clock.schedule_interval(self.update, 1 / 60)

    def update_graphics(self, *args):
        self.rect.pos = self.pos

    def update(self, dt):
        self.age += dt
        if self.age > self.lifetime:
            if self.parent:
                self.parent.remove_widget(self)
            return False
        self.velocity[1] += self.gravity * dt
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        return True
