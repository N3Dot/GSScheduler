from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock # Clock.schedule_once()
from kivy.metrics import dp
from kivy.uix.widget import Widget
# Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
if platform not in ('android', 'ios'):
    # Window.always_on_top = True
    Window.size = (520, 780) # Debug Note 8 View With Original (720, 1480)
else:
    Window.keep_screen_on = True

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.chip import MDChip, MDChipText, MDChipLeadingIcon
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.floatlayout import MDFloatLayout
from Backend import Code, UI, Popups

KV = '''
<MenuButton@MDFabButton>:
    pos_hint: {"x": 0.02, "top": 0.99}
    icon: "menu"
    style: "small"

MDScreenManager:
    md_bg_color: self.theme_cls.backgroundColor
    MDScreen:
        name: "Main"
        MDNavigationLayout:
            MDScreenManager:
                id: screen_manager_menu
                # --- Trang Chủ Start Section ---
                MDScreen:
                    name: "Home"
                    MDScreenManager:
                        id: screen_manager_home
                        # on_pre_enter: app.abc()
                        # --- Schedules Start Section ---
                        MDScreen:
                            name: "Phiên Học"
                            MDBoxLayout:
                                padding: "40dp"
                                MDLabel:
                                    id: empty_schedule_hint_label
                                    text: "Hiện tại không có phiên học. Bắt đầu hành trình bằng cách nhấn nút phía trên để tạo phiên học mới nhé!"
                                    disabled: 1
                                    halign: 'center'
                                    pos_hint: {"center_x": 0.5, "center_y": 0.5}

                            MDBoxLayout:
                                orientation: "vertical"
                                MDBoxLayout:
                                    size_hint_y: None  # CRUCIAL: Disables vertical size scaling.
                                    height: "175dp"    # CRUCIAL: Sets a fixed height.
                                    md_bg_color: app.theme_cls.primaryColor
                                    spacing: "10dp"
                                    orientation: 'vertical'
                                    MDBoxLayout:
                                        MDLabel:
                                            text: f"Lịch Học Hôm Nay"
                                            halign: "center"
                                            pos_hint: {"center_y": 0.15}
                                            font_style: "Title"
                                            theme_text_color: "Custom"
                                            text_color: 1, 1, 1, 1
                                    ScheduleCharacterCard:
                                        id: schedule_character_card
                                        imagePath: f"https://picsum.photos/600/600"
                                
                                MDBoxLayout:  # Fixed height padding.
                                    size_hint_y: None
                                    height: "25dp"
                                    md_bg_color: app.theme_cls.primaryColor
                                MDBoxLayout:  # Fixed height padding.
                                    orientation: "vertical"
                                    size_hint_y: None
                                    height: "50dp"
                                MDScrollView:
                                    do_scroll_x: False
                                    MDBoxLayout:
                                        id: schedule_grid
                                        orientation: "vertical"
                                        adaptive_height: True
                                        padding: dp(15), dp(0), dp(15), dp(90)
                                        spacing: dp(10)

                            MDBoxLayout:
                                orientation: "vertical"
                                MDBoxLayout: # Fixed height padding.
                                    size_hint_y: None
                                    height: "175dp"
                                MDAnchorLayout:
                                    anchor_x: "center"
                                    anchor_y: "top"
                                    MDFabButton:
                                        icon: "plus"
                                        on_release: app.switch_edit()
                        # --- Schedules End Section ---

                        # --- Character Start Section ---
                        MDScreen:
                            name: "Nhân Vật"
                            MDBoxLayout:
                                orientation: "vertical"
                                CharacterCard:
                                    id: character_card
                                    imagePath: f"https://picsum.photos/600/600"

                                MDBoxLayout:
                                    orientation: "vertical"
                                    padding: "12dp"
                                    spacing: "4dp"
                                    MDLabel:
                                        text: "Trang Bị:"
                                        adaptive_height: True
                                        font_style: "Body"
                                        role: "large"
                                    MDDivider:
                                    MDScrollView:
                                        do_scroll_y: False
                                        MDGridLayout:
                                            id: equipment_grid
                                            cols: 100
                                            spacing: dp(12)
                                            adaptive_width: True

                                    MDLabel:
                                        text: "Vật Phẩm:"
                                        adaptive_height: True
                                        font_style: "Body"
                                        role: "large"
                                    MDDivider:
                                    MDScrollView:
                                        do_scroll_y: False
                                        MDGridLayout:
                                            id: item_grid
                                            cols: 100
                                            spacing: dp(12)
                                            adaptive_width: True

                                    MDLabel:
                                        text: "Thành Tích:"
                                        adaptive_height: True
                                        font_style: "Body"
                                        role: "large"
                                    MDDivider:
                                    MDScrollView:
                                        do_scroll_y: False
                                        MDGridLayout:
                                            id: achievement_grid
                                            cols: 100
                                            spacing: dp(12)
                                            adaptive_width: True
                                    
                                    MDBoxLayout:
                                        size_hint_y: None
                                        height: "75dp"
                        # --- Character End Section ---
                        
                        # --- Shop Start Section ---
                        MDScreen:
                            name: "Cửa Hàng"
                            MDBoxLayout:
                                orientation: "vertical"
                                MDBoxLayout:
                                    size_hint_y: None  # CRUCIAL: Disables vertical size scaling.
                                    height: "120dp"    # CRUCIAL: Sets a fixed height.
                                    md_bg_color: app.theme_cls.primaryColor
                                    padding: "10dp"
                                    orientation: 'vertical'
                                    MDLabel:
                                        text: "Gian Hàng"
                                        halign: "center"
                                        font_style: "Title"
                                        role: "large"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1
                                    MDLabel:
                                        text: f"[i]Gian hàng tiếp theo sẽ đến trong: 12:39:42[/i]"
                                        halign: "center"
                                        markup: "True"
                                        font_style: "Label"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1
                                
                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "30dp"
                                    padding: "12dp", "0dp", "12dp", "0dp"
                                    orientation: "horizontal"
                                    MDBoxLayout:
                                        size_hint_x: 2
                                        BarWide:
                                            id: hp_bar_shop
                                            current: 100
                                            max: 125
                                    MDBoxLayout:
                                        size_hint_x: 1
                                        orientation: "vertical"
                                        GoldCounterCard:
                                            id: gold_counter_card
                                            pos_hint: {'center_x': 0.55}
                                
                                Widget:
                                    size_hint_y: None
                                    height: "24dp"
                                    
                                MDScrollView:
                                    do_scroll_x: False
                                    MDGridLayout:
                                        id: shop_grid
                                        cols: 4
                                        padding: dp(12), dp(0), dp(12), dp(90)
                                        spacing: dp(12)
                                        adaptive_height: True
                        # --- Shop End Section ---
                    
                    MDNavigationBar:
                        on_switch_tabs: app.on_home_switch_tab(*args)
                        MDNavigationItem:
                            active: True
                            MDNavigationItemIcon:
                                icon: "av-timer"
                            MDNavigationItemLabel:
                                text: "Phiên Học"
                        MDNavigationItem:
                            MDNavigationItemIcon:
                                icon: "account-tie-hat"
                            MDNavigationItemLabel:
                                text: "Nhân Vật"
                        MDNavigationItem:
                            MDNavigationItemIcon:
                                icon: "shopping-outline"
                            MDNavigationItemLabel:
                                text: "Cửa Hàng"
                    MenuButton:
                        on_release: app.root.ids.navigation_drawer.set_state("toggle")
                # --- Trang Chủ End Section ---
                # --- Đấu Trường Start Section ---
                MDScreen:
                    name: "Arena"
                    MDBoxLayout:
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y: None
                            height: "60dp"
                            padding: "12dp"
                            spacing: "8dp"
                            MDTextField:
                                id: opponent_code_input
                                hint_text: "Nhập mã đối thủ (Base64)"
                                size_hint_x: 0.7
                                mode: "outlined"
                            Button:
                                text: "Load"
                                size_hint_x: 0.15
                                on_press: app.load_arena_opponent()
                            MDIconButton:
                                icon: "dice-6"
                                size_hint_x: 0.15
                                on_press: app.load_demo_opponent()
                        MDCard:
                            elevation: 4
                            radius: [12]
                            md_bg_color: [0.1, 0.1, 0.2, 1]
                            MDBoxLayout:
                                orientation: "vertical"
                                spacing: "8dp"
                                padding: "16dp"
                                MDLabel:
                                    text: " ĐẤU TRƯỜNG "
                                    font_style: "Headline"
                                    role: "medium"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [0, 0, 0, 1]  # Đen
                                MDFloatLayout:
                                    size_hint_y: 0.6
                                    # Background image for arena
                                    canvas.before:
                                        Rectangle:
                                            source: "Art/Backgrounds/arena_bg.jpg"
                                            size: self.size
                                            pos: self.pos
                                    MDCard:
                                        id: bot_character_card
                                        size_hint: None, None
                                        size: "140dp", "180dp"
                                        pos_hint: {"x": 0.65, "y": 0.65}
                                        elevation: 6
                                        radius: [12]
                                        md_bg_color: [0.8, 0.2, 0.2, 0.9]
                                        on_release: app.show_bot_stats_dialog()
                                        MDBoxLayout:
                                            orientation: "vertical"
                                            padding: "8dp"
                                            spacing: "4dp"
                                            AsyncImage:
                                                id: bot_avatar
                                                source: "https://picsum.photos/100/100?random=2"
                                                size_hint: None, None
                                                size: "80dp", "80dp"
                                                pos_hint: {"center_x": 0.5}
                                            MDLabel:
                                                id: bot_name_label
                                                text: "Bot - Lv.1"
                                                font_style: "Title"
                                                role: "small"
                                                halign: "center"
                                                adaptive_height: True
                                                theme_text_color: "Custom"
                                                text_color: [0, 0, 0, 1]  # Đen
                                            MDBoxLayout:
                                                size_hint_y: None
                                                height: "16dp"
                                                spacing: "1dp"
                                                MDLabel:
                                                    text: "HP:"
                                                    size_hint_x: None
                                                    width: "24dp"
                                                    font_style: "Body"
                                                    role: "small"
                                                    theme_text_color: "Custom"
                                                    text_color: [0, 0, 0, 1]  # Đen
                                                    halign: "center"
                                                MDLabel:
                                                    id: bot_hp_label
                                                    text: "50/50"
                                                    font_style: "Body"
                                                    role: "small"
                                                    halign: "center"
                                                    adaptive_height: True
                                                    theme_text_color: "Custom"
                                                    text_color: [0, 0, 0, 1]  # Đen
                                            # Xóa các label chỉ số khác khỏi card bot, chỉ giữ HP và LV
                                    MDCard:
                                        id: player_character_card
                                        size_hint: None, None
                                        size: "140dp", "180dp"
                                        pos_hint: {"x": 0.15, "y": 0.05}
                                        on_release: app.show_character_stats_dialog()
                                        elevation: 6
                                        radius: [12]
                                        md_bg_color: [0.2, 0.6, 0.9, 0.9]
                                        MDBoxLayout:
                                            orientation: "vertical"
                                            padding: "8dp"
                                            spacing: "4dp"
                                            AsyncImage:
                                                id: player_avatar
                                                source: "https://picsum.photos/100/100?random=1"
                                                size_hint: None, None
                                                size: "80dp", "80dp"
                                                pos_hint: {"center_x": 0.5}
                                            MDLabel:
                                                id: player_name_label
                                                text: "Player - Lv.1"
                                                font_style: "Title"
                                                role: "small"
                                                halign: "center"
                                                adaptive_height: True
                                                theme_text_color: "Primary"
                                            MDBoxLayout:
                                                size_hint_y: None
                                                height: "16dp"
                                                spacing: "1dp"
                                                MDLabel:
                                                    text: "HP:"
                                                    size_hint_x: None
                                                    width: "24dp"
                                                    font_style: "Body"
                                                    role: "small"
                                                    theme_text_color: "Primary"
                                                    halign: "center"
                                                MDLabel:
                                                    id: player_hp_label
                                                    text: "50/50"
                                                    font_style: "Body"
                                                    role: "small"
                                                    halign: "center"
                                                    adaptive_height: True
                                                    theme_text_color: "Primary"
                                            # Xóa các label chỉ số khác khỏi card, chỉ giữ HP và LV
                                        
                                    MDLabel:
                                        text: " VS "
                                        font_style: "Headline"
                                        role: "large"
                                        halign: "center"
                                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                        theme_text_color: "Custom"
                                        text_color: [0, 0, 0, 1]  # Đen
                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: "8dp"
                                    Button:
                                        text: "Attack"
                                        background_normal: ""
                                        background_color: 0.95, 0.95, 0.95, 1
                                        color: 0, 0, 0, 1
                                        font_size: "18sp"
                                        bold: True
                                        on_release: app.on_arena_skill_selected("attack")
                                    Button:
                                        text: "Defend"
                                        background_normal: ""
                                        background_color: 0.92, 0.95, 1, 1
                                        color: 0, 0, 0, 1
                                        font_size: "18sp"
                                        bold: True
                                        on_release: app.on_arena_skill_selected("defend")
                                    Button:
                                        text: "Magic"
                                        background_normal: ""
                                        background_color: 0.95, 0.92, 1, 1
                                        color: 0, 0, 0, 1
                                        font_size: "18sp"
                                        bold: True
                                        on_release: app.on_arena_skill_selected("magic")
                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "60dp"
                                    spacing: "8dp"
                                    Button:
                                        id: start_battle_btn
                                        text: "Bắt Đầu Trận Đấu"
                                        background_normal: ""
                                        background_color: 0.92, 1, 0.92, 1
                                        color: 0, 0, 0, 1
                                        font_size: "18sp"
                                        bold: True
                                        on_press: app.start_arena_battle()
                                    Button:
                                        id: reset_battle_btn
                                        text: "Reset"
                                        background_normal: ""
                                        background_color: 1, 0.92, 0.92, 1
                                        color: 0, 0, 0, 1
                                        font_size: "18sp"
                                        bold: True
                                        on_press: app.reset_arena_battle()
                                    
                    MenuButton:
                        on_release: app.root.ids.navigation_drawer.set_state("toggle")
                # --- Đấu Trường End Section ---
                # --- Cài Đặt Start Section ---
                MDScreen:
                    name: "Settings"
                    MDScrollView:
                        do_scroll_x: False
                        MDList:
                            MDLabel:
                                text: "Cài Đặt"
                                font_style: "Title"
                                theme_text_color: "Secondary"
                                halign: "center"
                                size_hint_y: None
                            MDListItem:
                                on_release: app.show_analytics_dialog()
                                MDListItemLeadingIcon:
                                    icon: "google-analytics"
                                MDListItemSupportingText:
                                    text: "Xem Kết Quả"
                            MDListItem:
                                on_release: app.show_avatar_dialog()
                                MDListItemLeadingIcon:
                                    icon: "image-album"
                                MDListItemSupportingText:
                                    text: "Đổi Ảnh Nhân Vật"
                            MDListItem:
                                MDListItemLeadingIcon:
                                    id: trash_can_icon
                                    icon: "delete-outline"
                                    theme_text_color: "Custom"
                                    text_color: 1, 0, 0, 1
                                MDListItemSupportingText:
                                    text: "[color=ff4444]Xóa Dữ Liệu[/color]"
                    MenuButton:
                        on_release: app.root.ids.navigation_drawer.set_state("toggle")
                # --- Cài Đặt End Section ---

            MDNavigationDrawer:
                id: navigation_drawer
                radius: 0, dp(16), dp(16), 0
                MDNavigationDrawerMenu:
                    MDNavigationDrawerHeader:
                        orientation: "vertical"
                        padding: 0, 0, 0, "12dp"
                        adaptive_height: True
                        MDIcon:
                            icon: "nintendo-game-boy"
                            padding_x: "16dp"
                            theme_font_size: "Custom"
                            font_size: "32dp"
                        MDLabel:
                            theme_line_height: "Custom"
                            line_height: 0
                            text: "GS Scheduler"
                            padding: "16dp", "0dp"
                            adaptive_height: True
                            font_style: "Display"
                            role: "small"
                        MDLabel:
                            text: "Version: 06-25"
                            padding: "20dp", "0dp"
                            adaptive_height: True
                            font_style: "Title"
                            role: "small"

                    MDNavigationDrawerDivider:
                    MDNavigationDrawerItem:
                        on_release:
                            app.root.ids.navigation_drawer.set_state("toggle")
                            app.root.ids.screen_manager_menu.current = "Home"
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "home"
                        MDNavigationDrawerItemText:
                            text: "Trang Chủ"
                    MDNavigationDrawerItem:
                        on_release:
                            app.root.ids.navigation_drawer.set_state("toggle")
                            app.root.ids.screen_manager_menu.current = "Arena"
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "sword-cross"
                        MDNavigationDrawerItemText:
                            text: "Đấu Trường"
                    MDNavigationDrawerItem:
                        on_release:
                            app.root.ids.navigation_drawer.set_state("toggle")
                            app.root.ids.screen_manager_menu.current = "Settings"
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "cog"
                        MDNavigationDrawerItemText:
                            text: "Cài Đặt"
                    MDNavigationDrawerItem:
                        on_release: app.get_running_app().stop() # Does not stop background services started by pyjnius or android.service
                        MDNavigationDrawerItemLeadingIcon:
                            icon: "exit-to-app"
                        MDNavigationDrawerItemText:
                            text: "Thoát"

'''


class GSS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Khởi tạo các objects theo kiến trúc gốc và truyền vào SessionManager
        self.character = Code.Character("Người Chơi")
        self.reward_system = Code.RewardSystem()
        self.analytics = Code.StudyAnalytics(Code.QuestSystem())
        self.session_manager = Code.SessionManager(character=self.character, reward_system=self.reward_system, analytics=self.analytics)
        
        # Đảm bảo Arena được khởi tạo
        if not hasattr(self.session_manager, 'arena') or self.session_manager.arena is None:
            self.session_manager.arena = Code.Arena(player=self.character)

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Snow"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.PopupManager = Popups.Popup(self)
        self.character.bind(name=lambda instance, value: self.update_player_labels(value, "name"))
        self.character.bind(level=lambda instance, value: self.update_player_labels(value, "level"))
        self.character.bind(xp=lambda instance, value: self.update_player_labels(value, "xp"))
        self.character.bind(xp_to_next_level=lambda instance, value: self.update_player_labels(value, "xp_to_next_level"))
        self.character.bind(hp=lambda instance, value: self.update_player_labels(value, "hp"))
        self.character.bind(max_hp=lambda instance, value: self.update_player_labels(value, "max_hp"))
        self.character.bind(dex=lambda instance, value: self.update_player_labels(value, "dex"))
        self.character.bind(int=lambda instance, value: self.update_player_labels(value, "int"))
        self.character.bind(luk=lambda instance, value: self.update_player_labels(value, "luk"))
        self.character.bind(available_points=lambda instance, value: self.update_player_labels(value, "available_points"))
        self.character.bind(gold=lambda instance, value: self.update_player_labels(value, "gold"))

        self.session_manager.create_comprehensive_demo_data()
        self.character.name = "Anh Khôi"
        self.character.show_stats()

        AppDict = self.root.ids
        AppDict.schedule_grid.add_widget(UI.ScheduleCard(startTime="08:00", endTime="11:00", description="Ôn tập buổi cuối đề XSTK.", questTotal=3, expectedLoot="Cao"))
        AppDict.schedule_grid.add_widget(UI.ScheduleCard(startTime="15:00", endTime="17:00", description="Ôn tập buổi cuối đề CTTR.", questTotal=2, expectedLoot="Vừa"))
        AppDict.schedule_grid.add_widget(UI.ScheduleCard(startTime="15:00", endTime="17:00", description="Ôn tập buổi cuối đề CTTR.", questTotal=2, expectedLoot="Vừa"))
        AppDict.schedule_grid.add_widget(UI.ScheduleCard(startTime="15:00", endTime="17:00", description="Ôn tập buổi cuối đề CTTR.", questTotal=2, expectedLoot="Vừa"))
        AppDict.schedule_grid.add_widget(UI.ScheduleCard(startTime="15:00", endTime="17:00", description="Ôn tập buổi cuối đề CTTR.", questTotal=2, expectedLoot="Vừa"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Vàng", icon="Art/Items/TEST.png", price="1000", rarity="Legendary"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Xịn", icon="Art/Items/TEST.png", price="250", rarity="Epic"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Xịn", icon="Art/Items/TEST.png", price="250", rarity="Epic"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Bạc", icon="Art/Items/TEST.png", price="75", rarity="Rare"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Bạc", icon="Art/Items/TEST.png", price="75", rarity="Rare"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Bạc", icon="Art/Items/TEST.png", price="75", rarity="Rare"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Thường", icon="Art/Items/TEST.png", price="25", rarity="Uncommon"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Thường", icon="Art/Items/TEST.png", price="25", rarity="Uncommon"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Thường", icon="Art/Items/TEST.png", price="25", rarity="Uncommon"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Thường", icon="Art/Items/TEST.png", price="25", rarity="Uncommon"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.shop_grid.add_widget(UI.ItemShopCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", price="10", rarity="Common"))
        AppDict.equipment_grid.add_widget(UI.ItemCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", rarity="Common"))
        AppDict.item_grid.add_widget(UI.ItemCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", rarity="Common"))
        AppDict.item_grid.add_widget(UI.ItemCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", rarity="Common"))
        AppDict.achievement_grid.add_widget(UI.ItemCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", rarity="Common"))
        AppDict.achievement_grid.add_widget(UI.ItemCard(name="Kiếm Rỉ Sét", icon="Art/Items/TEST.png", rarity="Common"))
        
        # Initialize Arena display
        self.update_arena_display()
        
        # Generate and print demo codes for testing
    
    def on_pause(self): # on_stop() is not reliable on Android.
        self.session_manager.ExportSave()
        self.session_manager.generate_qr_code()
        print("Game data saved and QR generated on app pause.")

    def on_stop(self):
        self.session_manager.ExportSave()
        self.session_manager.generate_qr_code()
        print("Game data saved and QR generated on app close.")

    def on_resume(self):
        pass

    def spawn_schedule_options(self, instanceButton):
        menuItems = [
            {
                "text": f"Điều Chỉnh",
                "leading_icon": "wrench",
                "on_release": lambda id=f"Yo...": self.menu_callback(id),
            },
            {
                "text": f"Xóa",
                "leading_icon": "trash-can",
                "on_release": lambda id=f"Ayo!": self.menu_callback(id),
            },
        ]
        MDDropdownMenu(caller=instanceButton, items=menuItems).open()
    
    def menu_callback(self, textItem):
        print(textItem)

    def on_enable_schedule(self, instanceChip):
        chip_text_widget = None
        chip_icon_widget = None

        for child in instanceChip.walk(restrict=True):
            if isinstance(child, MDChipText):
                chip_text_widget = child
            elif isinstance(child, MDChipLeadingIcon):
                chip_icon_widget = child
        
        if not chip_text_widget or not chip_icon_widget:
            print("Widget Error: Could not find text or icon inside the chip.")
            return
        
        if chip_text_widget.text == "Tắt":
            instanceChip.md_bg_color = (0.82, 0.86, 0.82, 1)  # Set Enabled Color
            chip_text_widget.text = "Bật"
            chip_icon_widget.icon = "check"
        else:
            instanceChip.md_bg_color = (0.95, 0.95, 0.95, 1)  # Set Disabled Color
            chip_text_widget.text = "Tắt"
            chip_icon_widget.icon = "sleep"

    def on_click_character(self):
        try:
            qr_path = self.session_manager.generate_qr_code()
            if qr_path:
                self.PopupManager.show_character_dialog(qr_path)
                print(f"QR code updated successfully at {qr_path}")
            else:
                print("Failed to update QR code - no path or widget not found!")
        except Exception as e:
            print(f"Error updating QR code: {e}")

    def debug_function(self):
        self.character.gold += 5
        self.character.hp -= 2
        self.character.dex += 1
        self.character.int += 2
        self.character.luk += 3
        self.character.available_points += 1
        self.character.level += 1
        self.on_reward()

    def on_purchase_item(self, ItemShopCardInstance):
        self.PopupManager.show_item_purchase(ItemShopCardInstance)

    def on_click_item(self):
        self.PopupManager.show_item_dialog()
        self.debug_function()
    
    def on_reward(self, XP=0, Gold=0):
        self.PopupManager.show_reward_snackbar(XP, Gold)
    
    def handle_attribute_upgrade(self, type: str):
        self.character.available_points -= 1
        if type == "max_hp":
            self.character.max_hp += 10
        elif type == "dex":
            self.character.dex += 1
        elif type == "int":
            self.character.int += 1
        elif type == "luk":
            self.character.luk += 1

    def update_player_labels(self, value, type: str):
        try:
            AppDict = self.root.ids
            if type == "name":
                # Update character screen
                AppDict.character_name_label.text = value
                # Update schedule screen  
                AppDict.schedule_character_name.text = value
            elif type == "level":
                # Update character screen
                AppDict.character_level_label.text = f"Cấp độ: {value}"
                # Update schedule screen
                AppDict.schedule_character_level.text = f"Cấp độ: {value}"
            elif type == "xp":
                # Update XP progress
                if hasattr(self.character, 'xp_to_next_level') and self.character.xp_to_next_level > 0:
                    xp_progress = value / self.character.xp_to_next_level
                    AppDict.character_xp_bar.value = xp_progress
                    AppDict.character_xp_label.text = f"{value}/{self.character.xp_to_next_level} XP"
            elif type == "xp_to_next_level":
                # Update XP progress when max changes
                if hasattr(self.character, 'xp') and value > 0:
                    xp_progress = self.character.xp / value
                    AppDict.character_xp_bar.value = xp_progress
                    AppDict.character_xp_label.text = f"{self.character.xp}/{value} XP"
            elif type == "hp":
                # Update HP displays
                if hasattr(self.character, 'max_hp') and self.character.max_hp > 0:
                    hp_progress = value / self.character.max_hp
                    # Character screen
                    AppDict.character_hp_bar.value = hp_progress
                    AppDict.character_hp_label.text = f"{value}/{self.character.max_hp}"
                    # Schedule screen
                    AppDict.schedule_character_hp_bar.value = hp_progress
                    AppDict.schedule_character_hp_text.text = f"{value}/{self.character.max_hp}"
                    # Shop screen
                    AppDict.hp_bar_shop.value = hp_progress
                    AppDict.hp_bar_shop_label.text = f"{value}/{self.character.max_hp}"
            elif type == "max_hp":
                # Update HP displays when max changes
                if hasattr(self.character, 'hp') and value > 0:
                    hp_progress = self.character.hp / value
                    # Character screen
                    AppDict.character_hp_bar.value = hp_progress
                    AppDict.character_hp_label.text = f"{self.character.hp}/{value}"
                    # Schedule screen
                    AppDict.schedule_character_hp_bar.value = hp_progress
                    AppDict.schedule_character_hp_text.text = f"{self.character.hp}/{value}"
                    # Shop screen
                    AppDict.hp_bar_shop.value = hp_progress
                    AppDict.hp_bar_shop_label.text = f"{self.character.hp}/{value}"
            elif type == "dex":
                AppDict.character_dex_label.text = str(value)
            elif type == "int":
                AppDict.character_int_label.text = str(value)
            elif type == "luk":
                AppDict.character_luk_label.text = str(value)
            elif type == "available_points":
                AppDict.character_available_points_label.text = str(value)
            elif type == "gold":
                # Update gold displays
                AppDict.character_gold_label.text = f"💰 {value}"
                AppDict.schedule_character_gold.text = f"💰 {value} Vàng"
                AppDict.gold_counter_label.text = str(value)
        except Exception as e:
            print(f"Error updating player labels: {e}")

    def on_home_switch_tab(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.root.ids.screen_manager_home.current = item_text

    def on_toggle_theme(self): # Switch to theme_cls.primary_palette
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    # Arena Methods
    def load_arena_opponent(self):
        """Load đối thủ từ mã base64"""
        code_input = self.root.ids.opponent_code_input
        base64_code = code_input.text.strip()
        
        if not base64_code:
            self.PopupManager.show_info_snackbar("Vui lòng nhập mã đối thủ!")
            return
        
        try:
            success = self.session_manager.arena.load_opponent(base64_code)
            if success:
                self.update_arena_display()
                self.PopupManager.show_info_snackbar(f"Đã load đối thủ: {self.session_manager.arena.bot.name}")
                code_input.text = ""
            else:
                self.PopupManager.show_info_snackbar("Không thể load đối thủ từ mã này!")
        except Exception as e:
            self.PopupManager.show_info_snackbar(f"Lỗi: {str(e)}")
    
    def load_demo_opponent(self):
        """Load đối thủ demo ngẫu nhiên"""
        demo_code = self.session_manager.arena.generate_demo_opponent()
        success = self.session_manager.arena.load_opponent(demo_code)
        if success:
            self.update_arena_display()
            self.PopupManager.show_info_snackbar(f"Đã load đối thủ demo: {self.session_manager.arena.bot.name}")
    
    def start_arena_battle(self):
        """Bắt đầu trận đấu"""
        if not self.session_manager.arena.bot:
            self.PopupManager.show_info_snackbar("Vui lòng load đối thủ trước!")
            return
        
        success = self.session_manager.arena.start_battle()
        if success:
            self.update_arena_display()
            self.update_arena_ui_state(True)
            self.PopupManager.show_battle_message("⚔️ Trận đấu bắt đầu! Chọn skill để chiến đấu!")
            Clock.schedule_once(lambda dt: self.PopupManager.show_info_snackbar("Trận đấu đã bắt đầu! Chọn skill để tấn công!"), 0.5)
    
    def reset_arena_battle(self):
        """Reset trận đấu"""
        self.session_manager.arena.battle_active = False
        self.session_manager.arena.battle_log = []
        self.session_manager.arena.turn_count = 0
        self.update_arena_display()
        self.update_arena_ui_state(False)
        self.PopupManager.show_info_snackbar("Đã reset trận đấu!")
    
    def on_arena_skill_selected(self, skill_type):
        """Xử lý khi người chơi chọn skill"""
        if not self.session_manager.arena.battle_active:
            self.PopupManager.show_info_snackbar("Trận đấu chưa bắt đầu!")
            return
        
        # Import enum
        from Backend.Code import SkillType
        skill_map = {
            "attack": SkillType.ATTACK,
            "defend": SkillType.DEFEND, 
            "magic": SkillType.MAGIC
        }
        
        if skill_type not in skill_map:
            return
        
        # Hiệu ứng rung cho player khi thực hiện skill tấn công hoặc phép
        if skill_type in ["attack", "magic"]:
            self.shake_character(is_player=True)
        
        # Thực hiện lượt đấu
        result = self.session_manager.arena.execute_turn(skill_map[skill_type])
        
        # Hiển thị kết quả bằng popup messages với delay
        messages = result.get("messages", [])
        for i, message in enumerate(messages):
            Clock.schedule_once(
                lambda dt, msg=message: self.PopupManager.show_battle_message(msg), 
                i * 0.8  # Delay 0.8s giữa các message
            )
            
            # Hiệu ứng rung cho bot khi bot tấn công
            if "dùng phép" in message or "đánh thường" in message:
                if self.session_manager.arena.bot and self.session_manager.arena.bot.name in message:
                    Clock.schedule_once(lambda dt: self.shake_character(is_player=False), i * 0.8 + 0.3)
        
        # Cập nhật hiển thị
        self.update_arena_display()
        
        # Kiểm tra kết thúc trận đấu
        if result.get("battle_ended", False):
            winner = result.get("winner")
            delay_time = len(messages) * 0.8 + 1.0  # Đợi tất cả messages hiển thị xong
            
            if winner == "player":
                Clock.schedule_once(
                    lambda dt: self.PopupManager.show_battle_result_dialog("player", result.get("messages", [])), 
                    delay_time
                )
                # Tính thưởng
                if "messages" in result:
                    for msg in result["messages"]:
                        if "Thưởng:" in msg:
                            try:
                                parts = msg.split("Thưởng: +")[1].split(" XP, +")
                                if len(parts) == 2:
                                    xp = int(parts[0])
                                    gold = int(parts[1].split(" Vàng!")[0])
                                    Clock.schedule_once(lambda dt: self.on_reward(xp, gold), delay_time + 2.0)
                            except:
                                pass
            else:
                Clock.schedule_once(
                    lambda dt: self.PopupManager.show_battle_result_dialog("bot", result.get("messages", [])), 
                    delay_time
                )
            
            Clock.schedule_once(lambda dt: self.update_arena_ui_state(False), delay_time + 1.0)
    
    def update_arena_display(self):
        """Cập nhật hiển thị thông tin nhân vật trong arena"""
        try:
            AppDict = self.root.ids
            # Player - luôn cập nhật
            AppDict.player_name_label.text = f"{self.character.name} - Lv.{self.character.level}"
            AppDict.player_hp_label.text = f"{self.character.hp}/{self.character.max_hp}"
            
            # Bot - cập nhật khi có dữ liệu, giữ nguyên default nếu chưa load
            if self.session_manager.arena.bot:
                bot = self.session_manager.arena.bot
                AppDict.bot_name_label.text = f"{bot.name} - Lv.{bot.level}"
                AppDict.bot_hp_label.text = f"{bot.hp}/{bot.max_hp}"
            else:
                # Hiển thị default khi chưa có bot
                AppDict.bot_name_label.text = "??? - Lv.?"
                AppDict.bot_hp_label.text = "?/?"
        except Exception as e:
            print(f"Error updating arena display: {e}")
GSS().run()