from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty

from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

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

Builder.load_file("Backend/KV/ItemShopCard.kv")
class ItemShopCard(MDCard):
    name = StringProperty()
    icon = StringProperty()
    price = StringProperty()
    rarity = StringProperty("Common")
    borderColor = ListProperty([0.65, 0.65, 0.65, 1])
    backgroundColor = ListProperty([0.65, 0.65, 0.65, 0.2])
    textColor = ListProperty([0.3, 0.3, 0.3, 1])

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

Builder.load_file("Backend/KV/CharacterCard.kv")
class CharacterCard(MDBoxLayout):
    name = StringProperty()
    title = StringProperty()
    imagePath = StringProperty(f"https://picsum.photos/600/600")
    level = NumericProperty()
    hpCurrent = NumericProperty()
    hpMax = NumericProperty()
    xpCurrent = NumericProperty()
    xpMax = NumericProperty()
    dex = NumericProperty()
    int = NumericProperty()
    luk = NumericProperty()

Builder.load_file("Backend/KV/ScheduleCharacterCard.kv")
class ScheduleCharacterCard(MDBoxLayout):
    name = StringProperty()
    imagePath = StringProperty(f"https://picsum.photos/600/600")
    level = NumericProperty()
    hpCurrent = NumericProperty()
    hpMax = NumericProperty()
    xpCurrent = NumericProperty()
    xpMax = NumericProperty()
    goldAmount = NumericProperty()

Builder.load_file("Backend/KV/BarWide.kv")
class BarWide(MDBoxLayout):
    statName = StringProperty("HP")
    current = NumericProperty(100)
    max = NumericProperty(100)
    isLight = BooleanProperty(False)

Builder.load_file("Backend/KV/GoldCounterCard.kv")
class GoldCounterCard(MDCard):
    goldAmount = NumericProperty(0)