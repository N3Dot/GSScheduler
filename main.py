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
                                        on_release: app.switch_edit(None)
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
                                    text: "Kết Quả Học Tập"
                            MDListItem:
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
                        app.add_session() if app.mode == "Create" else print("yooo")
                        app.switch_main()
                    MDButtonText:
                        text: "Hoàn Thành"
    
    MDScreen:
        name: "Lock"

'''


class GSS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Khởi tạo các objects theo kiến trúc gốc và truyền vào SessionManager
        self.character = Code.Character("Người Chơi")
        self.quests = Code.QuestSystem()
        self.reward_system = Code.RewardSystem()
        self.analytics = Code.StudyAnalytics(Code.QuestSystem())
        self.session_manager = Code.SessionManager(character=self.character, reward_system=self.reward_system, analytics=self.analytics)
        self.mode = "Create"

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
        self.load_tabs()

        AppDict = self.root.ids
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

    def load_tabs(self):
        # --- Load Saved Sessions ---
        for session in self.session_manager.sessions:
            QuestNum = 0
            DifficultyNum = 0
            for quest in session.linked_quests:
                QuestNum += 1
                DifficultyNum += quest.difficulty
            DifficultyAvg = DifficultyNum/QuestNum
            if DifficultyAvg > 3:
                LootStr = "Cao"
            elif DifficultyAvg > 2:
                LootStr = "Vừa"
            else:
                LootStr = "Thấp"
            self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
        # --- Load Character Tab ---
        # --- Load Shop Tab ---

    def switch_main(self):
        self.root.current = "Main"
    
    def switch_edit(self, Data):
        if self.PopupManager.instance:
            self.PopupManager.instance.dismiss()
        if Data:
            self.mode = "Edit"
        else:
            self.mode = "Create"
        self.root.current = "Edit"

    def add_session(self):
        quests = Code.QuestSystem()
        quest1 = quests.create_quest(description="Viết phần Mở đầu báo cáo", difficulty=2)
        quest2 = quests.create_quest(description="Thiết kế Class Diagram", difficulty=4)
        quest3 = quests.create_quest(description="Viết code cho 3 Class", difficulty=5)
        session = self.session_manager.schedule_session(
        goal_description="Làm báo cáo OOP - Giai đoạn 1",
        start_time=datetime.now() + timedelta(seconds=100),
        end_time=datetime.now() + timedelta(seconds=200), # Thời gian dự kiến là 23 giây
        linked_quests=[quest1, quest2, quest3] # Truyền danh sách các đối tượng Quest
        )
        self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
        
    def remove_session(self, CardInstance):
        if self.PopupManager.instance:
            self.PopupManager.instance.dismiss()
        if CardInstance.parent:
            self.session_manager.sessions.remove(CardInstance.session)
            CardInstance.parent.remove_widget(CardInstance)
        else:
            print("Failed to remove session: Instance doesn't have parent.")

    def add_quest(self, SessionInstance = None): # ---> CurrentSession
        QuestCardInstance = UI.QuestCard(difficulty="3", description="Hoàn thành bài tập.")
        self.root.ids.schedule_quest_grid.add_widget(QuestCardInstance)

    def remove_quest(self, QuestCardInstance, QuestInstance = None, SessionInstance = None):
        self.root.ids.schedule_quest_grid.remove_widget(QuestCardInstance)

    def on_quest_edit(self, QuestCardInstance, QuestInstance = None, SessionInstance = None):
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
        description_field.text = QuestCardInstance.description
        for item in segmented_button.get_items():
            for child in item.walk(restrict=True):
                if isinstance(child, MDSegmentButtonLabel):
                    if child.text == QuestCardInstance.difficulty:
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
                    on_release=lambda x: self.save_quest_changes(QuestCardInstance, segmented_button, description_field),
                ),
                spacing="10dp",
            ),
        )
        self.QuestDialog.open()

    def save_quest_changes(self, QuestCardInstance, segmented_button, description_field, QuestInstance = None, SessionInstance = None):
        selected_items = segmented_button.get_marked_items()
        if selected_items:
            for child in selected_items[0].walk(restrict=True):
                if isinstance(child, MDSegmentButtonLabel):
                    new_difficulty = child.text
                    QuestCardInstance.difficulty = new_difficulty
                    break

        QuestCardInstance.description = description_field.text
        self.QuestDialog.dismiss()
    
    def spawn_schedule_options(self, instanceButton, CardInstance):
        menuItems = [
            {
                "text": f"Điều Chỉnh",
                "leading_icon": "wrench",
                "on_release": lambda Data=CardInstance: self.switch_edit(Data),
            },
            {
                "text": f"Xóa",
                "leading_icon": "trash-can",
                "on_release": lambda Data=CardInstance: self.remove_session(Data),
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