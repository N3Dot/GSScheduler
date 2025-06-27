import os
from datetime import datetime, timedelta, date

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
from Backend import Code, UI, Popups

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem, MDSegmentButtonLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDTimePickerDialVertical

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
                                        text: "Kho Đồ:"
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
                                        text: f"[i]Chất lượng hoàng gia, phục vụ hiệp sĩ.[/i]"
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
                        on_release: navigation_drawer.set_state("toggle")
                # --- Trang Chủ End Section ---
                # --- Đấu Trường Start Section ---
                MDScreen:
                    name: "Arena"
                    
                    MenuButton:
                        on_release: navigation_drawer.set_state("toggle")
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
                                on_release: app.PopupManager.show_avatar_dialog()
                                MDListItemLeadingIcon:
                                    icon: "image-album"
                                MDListItemSupportingText:
                                    text: "Đổi Ảnh Nhân Vật"
                            MDListItem:
                                on_release: app.PopupManager.show_erase_dialog()
                                MDListItemLeadingIcon:
                                    id: trash_can_icon
                                    icon: "delete-outline"
                                    theme_text_color: "Custom"
                                    text_color: 1, 0, 0, 1
                                MDListItemSupportingText:
                                    text: "[color=ff4444]Xóa Dữ Liệu[/color]"
                    MenuButton:
                        on_release: navigation_drawer.set_state("toggle")
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
    
    MDScreen:
        name: "Edit"
        MDBoxLayout:
            orientation: 'vertical'
            MDBoxLayout:
                adaptive_height: True
                padding: "0dp", "60dp"
                md_bg_color: self.theme_cls.secondaryColor
                MDLabel:
                    text: "Điều Chỉnh Lịch Học"
                    font_style: "Title"
                    halign: 'center'
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "20dp"
                padding: "20dp"
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"
                    padding: "0dp", "10dp", "0dp", "0dp"
                    size_hint_x: 0.5
                    MDLabel:
                        text: "Chi Tiết:"
                        bold: True
                        adaptive_height: True
                    MDTextField:
                        id: description_field
                        hint_text: "Mô tả"
                        mode: "outlined"
                        max_height: "300dp"
                        multiline: True
                        MDTextFieldLeadingIcon:
                            icon: "tooltip-text-outline"
                        MDTextFieldHintText:
                            text: "Mô tả phiên học..."
                            font_style: "Label"
                    
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: "10dp"
                        MDIcon:
                            icon: "clock-start"
                            pos_hint: {"center_y": 0.5}
                        MDLabel:
                            id: start_time_label
                            text: "[b]Bắt Đầu: [/b] 08:00"
                            markup: True
                            font_style: "Label"
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                        MDButton:
                            pos_hint: {"center_y": 0.5}
                            style: "text"
                            on_release: app.show_time_picker("start_time")
                            MDButtonText:
                                text: "Chọn"
                        
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: "10dp"
                        MDIcon:
                            icon: "clock-end"
                            pos_hint: {"center_y": 0.5}
                        MDLabel:
                            id: end_time_label
                            text: "[b]Kết Thúc: [/b] 10:00"
                            markup: True
                            font_style: "Label"
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                        MDButton:
                            pos_hint: {"center_y": 0.5}
                            style: "text"
                            on_release: app.show_time_picker("end_time")
                            MDButtonText:
                                text: "Chọn"
                    Widget:

                MDDivider:
                    orientation: 'vertical'
                        
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"
                    size_hint_x: 0.5
                    MDBoxLayout:
                        adaptive_height: True
                        MDLabel:
                            text: "Nhiệm Vụ:"
                            bold: True
                            adaptive_height: True
                            pos_hint: {'center_y': 0.5}
                        MDButton:
                            style: "tonal"
                            on_release: app.add_quest()
                            pos_hint: {'center_y': 0.5}
                            MDButtonText:
                                text: "Thêm"
                    MDScrollView:
                        do_scroll_x: False
                        MDBoxLayout:
                            id: schedule_quest_grid
                            orientation: 'vertical'
                            spacing: "10dp"
                            adaptive_height: True
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp", "10dp", "20dp", "40dp"
                adaptive_height: True
                MDButton:
                    style: "outlined"
                    pos_hint: {"center_x": 0.5}
                    on_release: 
                        app.add_session()
                    MDButtonText:
                        text: "Hoàn Thành"
    
    MDScreen:
        name: "Lock"
        MDBoxLayout:
            orientation: 'vertical'
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "0dp", "40dp"
                md_bg_color: self.theme_cls.tertiaryColor
                MDLabel:
                    text: "Phiên Học Đang Diễn Ra"
                    bold: True
                    font_style: "Title"
                    halign: 'center'
                    adaptive_height: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                MDLabel:
                    text: "Hoàn thành nhiệm vụ để tiến bước!"
                    italic: True
                    font_style: "Label"
                    halign: 'center'
                    adaptive_height: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: "20dp"
                padding: "20dp"
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"
                    padding: "0dp", "10dp", "0dp", "0dp"
                    size_hint_x: 0.5
                    MDLabel:
                        text: "Chi Tiết:"
                        bold: True
                        adaptive_height: True
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: "10dp"
                        MDIcon:
                            icon: "clock"
                            pos_hint: {"center_y": 0.5}
                        MDLabel:
                            id: lock_schedule_label
                            text: "[b]Chặng: [/b] 08:00 - 10:00"
                            markup: True
                            font_style: "Label"
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                    MDBoxLayout:
                        orientation: 'horizontal'
                        adaptive_height: True
                        spacing: "10dp"
                        MDIcon:
                            icon: "notebook"
                            pos_hint: {"center_y": 0.5}
                        MDLabel:
                            id: lock_description_label
                            text: "[b]Mô tả: [/b] Phiên học mới!"
                            markup: True
                            font_style: "Label"
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                    MDBoxLayout:
                        orientation: 'vertical'
                        adaptive_height: True
                        spacing: "10dp"
                        padding: "10dp", "30dp"
                        MDIcon:
                            icon: "timer-sand"
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.tertiaryColor
                            theme_font_size: "Custom"
                            font_size: "64dp"
                        MDLabel:
                            text: "Thời Gian Còn Lại"
                            font_style: "Body"
                            halign: 'center'
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.tertiaryColor
                        MDLabel:
                            id: lock_time_label
                            text: "02:17:21"
                            bold: True
                            font_style: "Body"
                            halign: 'center'
                            pos_hint: {"center_y": 0.5}
                            adaptive_height: True
                            theme_text_color: "Custom"
                            text_color: app.theme_cls.tertiaryColor
                    Widget:

                MDDivider:
                    orientation: 'vertical'
                        
                MDBoxLayout:
                    orientation: 'vertical'
                    spacing: "15dp"
                    size_hint_x: 0.5
                    MDBoxLayout:
                        adaptive_height: True
                        padding: "0dp", "8dp", "0dp", "0dp"
                        MDLabel:
                            text: "Nhiệm Vụ:"
                            bold: True
                            adaptive_height: True
                            pos_hint: {'center_y': 0.5}
                    MDScrollView:
                        do_scroll_x: False
                        MDBoxLayout:
                            id: lock_quest_grid
                            orientation: 'vertical'
                            spacing: "10dp"
                            adaptive_height: True
            
            MDBoxLayout:
                orientation: "vertical"
                padding: "20dp", "10dp", "20dp", "40dp"
                adaptive_height: True
                MDButton:
                    style: "outlined"
                    pos_hint: {"center_x": 0.5}
                    on_release: 
                        print("Ayo...")
                    MDButtonText:
                        text: "Kết Thúc Phiên Học"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.tertiaryColor
    
    MDScreen:
        name: "Login"

    MDScreen:
        name: "Death"

'''


class GSS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Khởi tạo các objects theo kiến trúc gốc và truyền vào SessionManager
        self.character = Code.Character("Người Chơi")
        self.quest_system = Code.QuestSystem()
        self.reward_system = Code.RewardSystem()
        self.analytics = Code.StudyAnalytics(self.quest_system)
        self.session_manager = Code.SessionManager(character=self.character, reward_system=self.reward_system, analytics=self.analytics)
        self.active_card = None
        self.queued_cards = []
        self.EnableSave = True
        self.SessionStarted = False

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
        self.Sound_OnPurchase = SoundLoader.load('Sounds/On_Purchase.wav')
        self.Sound_Eat = SoundLoader.load('Sounds/Eat.wav')
        self.Sound_Equip = SoundLoader.load('Sounds/Equip.wav')

        self.session_manager.create_comprehensive_demo_data()
        self.character.name = "Anh Khôi"
        self.character.show_stats()
        self.shop = Code.Shop(self.character)
        self.load_tabs()
        # self.root.current = "Lock"
        quest1 = Code.Quest(description="Viết phần Mở đầu báo cáo.", difficulty=2)
        self.root.ids.lock_quest_grid.add_widget(UI.QuestLockCard(quest=quest1))
        self.root.ids.lock_quest_grid.add_widget(UI.QuestLockCard(quest=quest1))
        # self.updater = Clock.schedule_interval(self.update, 1)
        if platform == "android":
            from android.permissions import request_permissions, check_permission, Permission # type: ignore
            from jnius import autoclass # type: ignore
            SDK_INT = autoclass('android.os.Build$VERSION').SDK_INT
            permissions = [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]
            if SDK_INT >= 30:
                permissions.append('android.permission.MANAGE_EXTERNAL_STORAGE')
            permissions_to_request = [p for p in permissions if not check_permission(p)]
            if permissions_to_request:
                request_permissions(permissions_to_request, self.on_permissions_callback)

    def on_permissions_callback(self, permissions, grants):
        if all(grants):
            print("All permissions granted.")
        else:
            print("Some permissions were denied.")
    
    def on_pause(self): # on_stop() is not reliable on Android.
        if self.EnableSave:
            self.session_manager.ExportSave()
            self.session_manager.generate_qr_code()
            print("Game data saved and QR generated on app pause.")

    def on_stop(self):
        if self.EnableSave:
            self.session_manager.ExportSave()
            self.session_manager.generate_qr_code()
            print("Game data saved and QR generated on app close.")

    def on_resume(self):
        pass

    def update(self, dt):
        pass

    def load_tabs(self):
        # --- Load Saved Sessions ---
        for session in self.session_manager.sessions:
            self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
        # --- Load Character Tab ---
        self.update_inventories()
        self.update_achievements()
        self.reload_avatar()
        # --- Load Shop Tab ---
        for item in self.shop.current_stock:
            self.root.ids.shop_grid.add_widget(UI.ItemShopCard(item=item))
        self.switch_main()

    def update_inventories(self):
        self.root.ids.item_grid.clear_widgets()
        self.root.ids.equipment_grid.clear_widgets()
        for item in self.character.inventory:
            self.root.ids.item_grid.add_widget(UI.ItemCard(item=item))
        for item in self.character.equipment:
            self.root.ids.equipment_grid.add_widget(UI.ItemCard(item=item))
    
    def update_achievements(self):
        self.root.ids.achievement_grid.clear_widgets()
        for achievement in self.character.unlocked_achievements:
            self.root.ids.achievement_grid.add_widget(UI.ItemCard(item=Code.Achievements[achievement]))
    
    def reload_avatar(self):
        self.avatar_path = f"https://picsum.photos/600/600"
        avatar_dir = self.PopupManager.get_avatar_save_path()
        try:
            for filename in os.listdir(avatar_dir):
                file_path = os.path.join(avatar_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    self.avatar_path = file_path
            print("Loaded avatar from avatar directory.")
        except Exception as e:
            print(f"Failed to load avatar: {e}")
        print(self.avatar_path)
        self.root.ids.character_card.imagePath = self.avatar_path
        self.root.ids.schedule_character_card.imagePath = self.avatar_path

    def switch_main(self):
        if self.session_manager.sessions:
            self.root.ids.empty_schedule_hint_label.opacity = 0
        else:
            self.root.ids.empty_schedule_hint_label.opacity = 1
        self.root.current = "Main"
    
    def switch_edit(self, ScheduleCard = None):
        self.root.ids.schedule_quest_grid.clear_widgets() # Load Anew
        if self.PopupManager.instance:
            self.PopupManager.instance.dismiss()

        if ScheduleCard: # Edit Session
            self.active_card = ScheduleCard
            self.root.ids.description_field.text = self.active_card.session.goal_description
            self.root.ids.start_time_label.text = f"[b]Bắt Đầu: [/b] {self.active_card.session.start_time.strftime('%H:%M')}"
            self.root.ids.end_time_label.text = f"[b]Kết Thúc: [/b] {self.active_card.session.end_time.strftime('%H:%M')}"
            for quest in self.active_card.session.linked_quests:
                self.add_quest(quest)

        else: # Create Session
            self.active_card = None
            self.root.ids.start_time_label.text = f"[b]Bắt Đầu: [/b] {(datetime.now()+timedelta(minutes=30)).strftime('%H')}:00"
            self.root.ids.end_time_label.text = f"[b]Kết Thúc: [/b] {(datetime.now()+timedelta(minutes=90)).strftime('%H')}:00"
            self.add_quest()

        self.root.current = "Edit"

    def add_session(self):
        description_text = self.root.ids.description_field.text

        if not self.queued_cards:
            self.PopupManager.show_warning_dialog("Đừng quên thêm ít nhất 1 nhiệm vụ để khởi động phiên học!")
            return
        quests = []
        for quest_card in self.queued_cards:
            quests.append(quest_card.quest)
        
        start_date = datetime.strptime(self.root.ids.start_time_label.text.split()[-1], "%H:%M") # Dạng: 1900-01-01 H:M (Không phân biệt ngày!)
        end_date = datetime.strptime(self.root.ids.end_time_label.text.split()[-1], "%H:%M") # Dạng: 1900-01-01 H:M (Không phân biệt ngày!)
        if abs(start_date - end_date) < timedelta(minutes=5):
            self.PopupManager.show_warning_dialog("Nhanh quá! Hãy dành ít nhất 5 phút cho phiên học của mình nha!")
            return
        
        session = self.session_manager.schedule_session(goal_description=description_text, start_time=start_date, end_time=end_date, linked_quests=quests)
        if self.active_card: # Edit
            self.session_manager.sessions.remove(self.active_card.session)
            self.active_card.session = session
        else: # Create
            self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
        print(self.session_manager.sessions)
        self.queued_cards = []
        self.active_card = None
        self.switch_main()
        
    def remove_session(self, ScheduleCard):
        if self.PopupManager.instance:
            self.PopupManager.instance.dismiss()
        if ScheduleCard.parent:
            self.session_manager.sessions.remove(ScheduleCard.session)
            ScheduleCard.parent.remove_widget(ScheduleCard)
        else:
            print("Failed to remove session: Card with no parent.")

    def add_quest(self, Quest = None):
        if not Quest:
            Quest = self.quest_system.create_quest(difficulty=3, description="Hoàn thành... ")
        QuestCard = UI.QuestCard(quest=Quest)
        self.queued_cards.append(QuestCard)
        self.root.ids.schedule_quest_grid.add_widget(QuestCard)

    def remove_quest(self, QuestCard):
        self.quest_system.active_quests.pop(f"{QuestCard.quest.quest_id}", None)
        self.queued_cards.remove(QuestCard)
        self.root.ids.schedule_quest_grid.remove_widget(QuestCard)

    def edit_quest(self, QuestCard):
        segmented_button = MDSegmentedButton(
            MDSegmentedButtonItem(MDSegmentButtonLabel(text="1")),
            MDSegmentedButtonItem(MDSegmentButtonLabel(text="2")),
            MDSegmentedButtonItem(MDSegmentButtonLabel(text="3")),
            MDSegmentedButtonItem(MDSegmentButtonLabel(text="4")),
            MDSegmentedButtonItem(MDSegmentButtonLabel(text="5")),
        )
        description_field = MDTextField(
            MDTextFieldHintText(text="Mô tả nhiệm vụ...", font_style="Label"),
            mode="outlined", max_height="200dp", multiline=True
        )

        # --- Pre-Filling ---
        description_field.text = QuestCard.description
        for item in segmented_button.get_items():
            for child in item.walk(restrict=True):
                if isinstance(child, MDSegmentButtonLabel):
                    if child.text == QuestCard.difficulty:
                        segmented_button.mark_item(item)
                        break
            else:
                continue
            break
        
        # --- Dialog Creation ---
        self.QuestDialog = MDDialog(
            MDDialogHeadlineText(text="Cài Đặt Nhiệm Vụ"),
            MDDialogContentContainer(
                MDBoxLayout(
                    MDBoxLayout(
                        MDLabel(text="1 - Rất Dễ", font_style="Label", halign="left"),
                        MDLabel(text="5 - Rất Khó", font_style="Label", halign="right"),
                        orientation="horizontal", padding=["10dp", "0dp"],
                    ),
                    segmented_button,
                    description_field,
                    orientation="vertical", adaptive_height=True, spacing="15dp",
                ),
            ),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Hủy"), style="text",
                    on_release=lambda x: self.QuestDialog.dismiss(),
                ),
                MDButton(MDButtonText(text="Lưu"), style="filled",
                    on_release=lambda x: self.save_quest_changes(QuestCard, segmented_button, description_field),
                ),
                spacing="10dp",
            ),
        )
        self.QuestDialog.open()

    def save_quest_changes(self, QuestCard, segmented_button, description_field):
        selected_items = segmented_button.get_marked_items()
        if selected_items:
            for child in selected_items[0].walk(restrict=True):
                if isinstance(child, MDSegmentButtonLabel):
                    QuestCard.difficulty = child.text
                    QuestCard.quest.difficulty = int(child.text)
                    break

        QuestCard.description = description_field.text
        QuestCard.quest.description = description_field.text
        self.QuestDialog.dismiss()
    
    def get_schedule_options(self, instanceButton, ScheduleCard):
        menuItems = [
            {
                "text": f"Điều Chỉnh",
                "leading_icon": "wrench",
                "on_release": lambda Data=ScheduleCard: self.switch_edit(Data),
            },
            {
                "text": f"Xóa",
                "leading_icon": "trash-can",
                "on_release": lambda Data=ScheduleCard: self.remove_session(Data),
            },
        ]
        self.PopupManager.instance = MDDropdownMenu(caller=instanceButton, items=menuItems)
        self.PopupManager.instance.open()

    def show_time_picker(self, picker_type):
        time_picker = MDTimePickerDialVertical()
        time_picker.bind(on_ok=lambda instance, *args: self.on_time_picker_ok(instance, picker_type))
        time_picker.bind(on_cancel=lambda x: time_picker.dismiss())
        time_picker.open()

    def on_time_picker_ok(self, time_picker_vertical: MDTimePickerDialVertical, picker_type):
        HM_Format = time_picker_vertical.time.strftime("%H:%M")
        if picker_type == "start_time":
            self.root.ids.start_time_label.text = f"[b]Bắt Đầu: [/b] {HM_Format}"
        else:
            self.root.ids.end_time_label.text = f"[b]Kết Thúc: [/b] {HM_Format}"
        time_picker_vertical.dismiss()

    def walk_demo(self, instanceChip):
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

    def on_purchase_item(self, ItemShopCard):
        if self.character.gold >= ItemShopCard.item.price:
            self.character.gold -= ItemShopCard.item.price
            self.character.inventory.append(ItemShopCard.item)
            self.root.ids.item_grid.add_widget(UI.ItemCard(item=ItemShopCard.item))
            self.PopupManager.show_item_purchase(ItemShopCard)
            self.Sound_OnPurchase.play()
            self.root.ids.shop_grid.remove_widget(ItemShopCard)
        else:
            message = f"Bạn chưa đủ vàng! Cần thêm {ItemShopCard.item.price - self.character.gold}G để mua {ItemShopCard.item.name}."
            self.PopupManager.show_warning_dialog(message)

    def on_click_item(self, ItemCard):
        if ItemCard.item:
            self.PopupManager.show_item_dialog(ItemCard.item)
    
    def on_click_owned_item(self, ItemCard):
        if ItemCard.item:
            if ItemCard.item.category == "Thành Tích":
                self.PopupManager.show_item_dialog(ItemCard.item)
            else:
                self.PopupManager.show_owned_item_dialog(ItemCard.item)
    
    def on_use_item(self, item, ItemDialog):
        self.character.use_item(item)
        self.Sound_Eat.play()
        self.update_inventories()
        ItemDialog.dismiss()

    def on_unequip_item(self, item, ItemDialog):
        Flag = self.character.unequip(item)
        if isinstance(Flag, str):
            self.PopupManager.show_warning_dialog(Flag)
            return
        self.Sound_Equip.play()
        self.update_inventories()
        ItemDialog.dismiss()

    def on_equip_item(self, item, ItemDialog):
        Flag = self.character.equip(item)
        if isinstance(Flag, str):
            self.PopupManager.show_warning_dialog(Flag)
            return
        self.Sound_Equip.play()
        self.update_inventories()
        ItemDialog.dismiss()
    
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
        AppDict = self.root.ids
        if type == "name":
            AppDict.character_card.name = value
            AppDict.schedule_character_card.name = value
        elif type == "level":
            AppDict.character_card.level = value
            AppDict.schedule_character_card.level = value
        elif type == "xp":
            AppDict.character_card.xpCurrent = value
            AppDict.schedule_character_card.xpCurrent = value
        elif type == "xp_to_next_level":
            AppDict.character_card.xpMax = value
            AppDict.schedule_character_card.xpMax = value
        elif type == "hp":
            AppDict.character_card.hpCurrent = value
            AppDict.schedule_character_card.hpCurrent = value
            AppDict.hp_bar_shop.current = value
        elif type == "max_hp":
            AppDict.character_card.hpMax = value
            AppDict.schedule_character_card.hpMax = value
            AppDict.hp_bar_shop.max = value
        elif type == "dex":
            AppDict.character_card.dex = value
        elif type == "int":
            AppDict.character_card.int = value
        elif type == "luk":
            AppDict.character_card.luk = value
        elif type == "available_points":
            AppDict.character_card.available_points = value
        elif type == "gold":
            self.root.ids.gold_counter_card.goldAmount = value
            self.root.ids.schedule_character_card.goldAmount = value

    def show_analytics_dialog(self):
        ReportString = self.analytics.generate_report()
        self.PopupManager.show_analytics_dialog(ReportString)

    def on_home_switch_tab(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.root.ids.screen_manager_home.current = item_text

    def on_toggle_theme(self): # Switch to theme_cls.primary_palette
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    

GSS().run()