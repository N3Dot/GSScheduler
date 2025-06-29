import os
from datetime import datetime, timedelta, date

from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.widget import Widget
# Config.set('graphics', 'resizable', False)
from kivy.core.window import Window
if platform not in ('android', 'ios'):
    Window.always_on_top = True
    Window.size = (520, 780) # Debug Note 8 View With Original (720, 1480)
else:
    Window.keep_screen_on = True

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.floatlayout import MDFloatLayout
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
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer, MDDialogContentContainer
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
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
                        on_release: app.root.ids.navigation_drawer.set_state("toggle")
                # --- Trang Chủ End Section ---
                # --- Đấu Trường Start Section ---
                MDScreen:
                    name: "Arena"
                    MDBoxLayout:
                        orientation: "vertical"
                        MDBoxLayout:
                            size_hint_y: None
                            height: "50dp"
                            padding: "50dp", "8dp", "8dp", "8dp"  # Thêm padding left 50dp để tránh nút menu
                            spacing: "8dp"
                            MDButton:
                                style: "elevated"
                                size_hint_x: 0.7
                                size_hint_y: None
                                height: "36dp"
                                on_press: app.load_arena_opponent()
                                MDButtonText:
                                    text: "Nhập Mã Đối Thủ"
                            MDButton:
                                style: "filled"
                                size_hint_x: 0.3
                                size_hint_y: None
                                height: "36dp"
                                on_press: app.load_demo_opponent()
                                MDButtonText:
                                    text: "Demo"
                        FloatLayout:
                            # Modern background image approach: Image widget as first child
                            Image:
                                source: "Art/Backgrounds/arena_bg.jpg" if app.check_background_exists() else ""
                                allow_stretch: True
                                keep_ratio: False
                                fit_mode: "cover"
                                size_hint: 1, 1
                                pos_hint: {"x": 0, "y": 0}
                                z: 0
                            # Arena widgets above background
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
                                        text_color: [0, 0, 0, 1]
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
                                            text_color: [0, 0, 0, 1]
                                        MDLabel:
                                            id: bot_hp_label
                                            text: "50/50"
                                            font_style: "Body"
                                            role: "small"
                                            halign: "center"
                                            adaptive_height: True
                                            theme_text_color: "Custom"
                                            text_color: [0, 0, 0, 1]
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
                            MDLabel:
                                text: " VS "
                                font_style: "Headline"
                                role: "large"
                                halign: "center"
                                bold: True
                                pos_hint: {"center_x": 0.5, "center_y": 0.5}
                                theme_text_color: "Custom"
                                text_color: [1, 1, 1, 1]
                        BoxLayout:
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
                                italic: True
                                on_release: app.on_arena_skill_selected("attack")
                            Button:
                                text: "Defend"
                                background_normal: ""
                                background_color: 0.92, 0.95, 1, 1
                                color: 0, 0, 0, 1
                                font_size: "18sp"
                                bold: True
                                italic: True
                                on_release: app.on_arena_skill_selected("defend")
                            Button:
                                text: "Magic"
                                background_normal: ""
                                background_color: 0.95, 0.92, 1, 1
                                color: 0, 0, 0, 1
                                font_size: "18sp"
                                bold: True
                                italic: True
                                on_release: app.on_arena_skill_selected("magic")
                        BoxLayout:
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
                                on_release: app.show_analytics_from_code_dialog()
                                MDListItemLeadingIcon:
                                    icon: "qrcode-scan"
                                MDListItemSupportingText:
                                    text: "Load Dữ Liệu Từ QR"
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
        MDFloatLayout:
            id: effect_layer                  

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
                orientation: "horizontal"
                padding: "10dp", "10dp", "10dp", "40dp"
                spacing: "20dp"
                adaptive_height: True
                Widget:
                MDButton:
                    style: "filled"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.add_session()
                    MDButtonText:
                        text: "Hoàn Thành"
                MDButton:
                    style: "outlined"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.cancel_session()
                    MDButtonText:
                        text: "Hủy"
                Widget:
                
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
                            text: ""
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
                    on_release: app.on_end_session()
                    MDButtonText:
                        text: "Kết Thúc Phiên Học"
                        theme_text_color: "Custom"
                        text_color: app.theme_cls.tertiaryColor
    
    MDScreen:
        name: "Login"
        MDBoxLayout:
            orientation: 'vertical'
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "40dp", "40dp"
                spacing: "10dp"
                md_bg_color: self.theme_cls.primaryColor
                MDLabel:
                    text: "Tạo Nhân Vật"
                    bold: True
                    font_style: "Title"
                    halign: 'center'
                    adaptive_height: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                MDLabel:
                    text: "Vận mệnh lặng lẽ gọi tên bạn. Nhưng trước khi hành trình bắt đầu, bạn phải trả lời một câu hỏi đơn giản..."
                    font_style: 'Label'
                    halign: 'center'
                    italic: True
                    adaptive_height: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
            MDBoxLayout:
                orientation: 'vertical'
                spacing: "20dp"
                padding: "20dp"
                MDLabel:
                    text: "Tên của bạn là gì?"
                    halign: 'center'
                    bold: True
                    adaptive_height: True
                MDTextField:
                    id: login_name_field
                    hint_text: "Mô tả"
                    mode: "outlined"
                    MDTextFieldLeadingIcon:
                        icon: "account"
                    MDTextFieldHintText:
                        text: "Nhập tên nhân vật..."
                        font_style: "Label"
                Widget:
                MDLabel:
                    text: "Ngoại hình của nhân vật bạn là gì?"
                    halign: 'center'
                    bold: True
                MDBoxLayout:
                    size_hint: None, None
                    size: "125dp", "125dp"
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    MDCard:
                        style: "filled"
                        radius: [10, ]
                        padding: "8dp"
                        size_hint_x: 0.45
                        FitImage:
                            id: login_avatar_image
                            source: app.avatar_path
                            radius: [10, ]
                MDListItem:
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.PopupManager.show_avatar_dialog()
                    MDListItemLeadingIcon:
                        icon: "file-image"
                    MDListItemSupportingText:
                        text: "Chọn Ảnh Chân Dung"
                        font_style: "Body"
                MDButton:
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    style: "outlined"
                    on_release: app.confirm_login()
                    MDButtonText:
                        text: "Hoàn Tất"
                Widget:
            MDBoxLayout:
                orientation: 'vertical'
                adaptive_height: True
                padding: "0dp", "60dp"
                md_bg_color: self.theme_cls.primaryColor

    MDScreen:
        name: "Death"
        md_bg_color: self.theme_cls.primaryColor
        MDBoxLayout:
            orientation: 'vertical'
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            adaptive_height: True
            spacing: "15dp"
            padding: "50dp"
            MDIcon:
                icon: "emoticon-sad-outline"
                pos_hint: {"center_x": 0.5}
                theme_icon_color: "Custom"
                icon_color: 1, 1, 1, 1
                theme_font_size: "Custom"
                font_size: "64dp"
            MDLabel:
                text: "Ôi Không..."
                bold: True
                font_style: "Title"
                halign: 'center'
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDLabel:
                text: "Bạn đã gục ngã... Nhưng chưa kết thúc!"
                bold: True
                font_style: "Body"
                halign: 'center'
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDLabel:
                text: "Bạn đã mất toàn bộ HP. Nhưng một anh hùng không được định nghĩa bởi số lần chiến thắng, mà bởi số lần họ đứng dậy sau khi ngã xuống."
                font_style: "Label"
                halign: 'center'
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDLabel:
                text: "Vận mệnh của bạn vẫn chưa khép lại. Hãy hồi sinh và viết tiếp câu chuyện còn dang dở của mình."
                font_style: "Label"
                halign: 'center'
                adaptive_height: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
            MDButton:
                style: "elevated"
                pos_hint: {"center_x": 0.5}
                on_release: app.revive_character()
                MDButtonText:
                    text: "Hồi Sinh"
                    theme_text_color: "Custom"
                    text_color: self.theme_cls.primaryColor
'''

class GSS(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Khởi tạo các objects theo kiến trúc gốc và truyền vào SessionManager
        self.character = Code.Character("Người Chơi")
        self.quest_system = Code.QuestSystem()
        self.reward_system = Code.RewardSystem()
        
        # Make sure analytics has access to session manager
        self.analytics = Code.StudyAnalytics(self.quest_system)
        self.session_manager = Code.SessionManager(character=self.character, reward_system=self.reward_system, analytics=self.analytics)
        
        # Ensure analytics knows about session manager
        if hasattr(self.analytics, 'set_session_manager'):
            self.analytics.set_session_manager(self.session_manager)
        
        self.avatar_path = f"https://picsum.photos/600/600"
        self.active_card = None
        self.queued_cards = []
        self.EnableSave = True
        self.HeroKilled = False
        self.FullyLoaded = False
        self.SessionStarted = None
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
        self.Sound_OnPurchase = SoundLoader.load('Sounds/On_Purchase.wav')
        self.Sound_Eat = SoundLoader.load('Sounds/Eat.wav')
        self.Sound_Equip = SoundLoader.load('Sounds/Equip.wav')
        self.Sound_Hurt = SoundLoader.load('Sounds/Hurt.wav')
        self.Sound_Pop = SoundLoader.load('Sounds/Pop.wav')
        self.Sound_Ding = SoundLoader.load('Sounds/Ding.wav')
        self.Sound_LevelUp = SoundLoader.load('Sounds/Level_Up.wav')

        SavePresent = self.session_manager.ImportSave()

        self.character.show_stats()
        self.shop = Code.Shop(self.character)
        self.load_tabs(SavePresent)
        self.updater = Clock.schedule_interval(self.update, 1)
        self.FullyLoaded = True
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
        if self.HeroKilled == False and self.character.hp <= 0 and self.SessionStarted is None:
            self.HeroKilled = True
            self.root.current = "Death"
            self.Sound_Hurt.play()
        else:
            cur = datetime.now()
            time_now = datetime(1900, 1, 1).replace(hour=cur.hour, minute=cur.minute, second=cur.second)
            if self.SessionStarted is None:
                for session in self.session_manager.sessions[:]: # Lặp trên bản sao để xóa an toàn
                    if (time_now <= session.end_time and time_now >= session.start_time) and session.status != "Finished":
                        self.SessionStarted = session
                        self.root.ids.lock_description_label.text = f"[b]Mô tả: [/b] {self.SessionStarted.goal_description}"
                        self.root.ids.lock_schedule_label.text = f"[b]Chặng: [/b] {self.SessionStarted.start_time.strftime('%H:%M')} - {self.SessionStarted.end_time.strftime('%H:%M')}"
                        self.root.ids.lock_quest_grid.clear_widgets()
                        for quest in self.SessionStarted.linked_quests:
                            QuestLockCard = UI.QuestLockCard(quest=quest)
                            self.root.ids.lock_quest_grid.add_widget(QuestLockCard)
                        self.SessionStarted.start_session()
                        self.reward_system.public_messages = {'xp': 0, 'gold': 0}
                        self.Sound_Ding.play()
                        self.root.current = "Lock"
                        return
            else:
                self.root.ids.lock_time_label.text = str(self.SessionStarted.end_time - time_now)
                if self.root.current != "Lock":
                    self.root.current = "Lock"
                if time_now > self.SessionStarted.end_time and self.SessionStarted.status == "Running":
                    self.on_end_session()
    
    def on_end_session(self):
        if self.SessionStarted:
            # Ensure analytics is updated before ending session
            completed_session = self.session_manager.end_session_manually(self.SessionStarted.session_id)
            
            # Manually update analytics if needed
            if completed_session and hasattr(self.analytics, 'add_session_data'):
                self.analytics.add_session_data(completed_session)
            
            self.root.ids.schedule_grid.clear_widgets()
            for session in self.session_manager.sessions:
                self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
            
            self.update_achievements()
            self.switch_main()
            self.Sound_Ding.play()
            self.PopupManager.show_session_finish_dialog(self.SessionStarted.rank, self.reward_system.public_messages['xp'], self.reward_system.public_messages['gold'])
            self.SessionStarted = None
        else:
            print("Chưa có phiên học nào bắt đầu!")
            self.switch_main()

    def load_tabs(self, SavePresent: bool):
        # --- Load Shop Tab ---
        for item in self.shop.current_stock:
            self.root.ids.shop_grid.add_widget(UI.ItemShopCard(item=item))
        if SavePresent:
            # --- Load Saved Sessions ---
            for session in self.session_manager.sessions:
                self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
            # --- Load Character Tab ---
            self.update_inventories()
            self.update_achievements()
            self.reload_avatar()
            self.switch_main()
        else:
            self.root.current = "Login"

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
            print(f"Loaded avatar from avatar directory {self.avatar_path}")
        except Exception as e:
            print(f"Failed to load avatar: {e}")
        self.root.ids.character_card.imagePath = self.avatar_path
        self.root.ids.schedule_character_card.imagePath = self.avatar_path
        self.root.ids.login_avatar_image.source = self.avatar_path
        self.root.ids.login_avatar_image.reload()

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
            self.root.ids.description_field.text = ""
            self.root.ids.start_time_label.text = f"[b]Bắt Đầu: [/b] {(datetime.now()+timedelta(minutes=10)).strftime('%H:%M')}"
            self.root.ids.end_time_label.text = f"[b]Kết Thúc: [/b] {(datetime.now()+timedelta(minutes=70)).strftime('%H:%M')}"
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
        if abs(start_date - end_date) < timedelta(minutes=1):
            self.PopupManager.show_warning_dialog("Nhanh quá! Hãy dành ít nhất 1 phút cho phiên học của mình nha!")
            return
        
        if (end_date - start_date).total_seconds() < 0:
            self.PopupManager.show_warning_dialog("Thời gian kết thúc không được trước thời gian bắt đầu!")
            return
        
        session = self.session_manager.schedule_session(goal_description=description_text, start_time=start_date, end_time=end_date, linked_quests=quests)
        if isinstance(session, list):
            if self.active_card is None: # Handle time conflicts when there is no sessions being edited.
                conflicting_session = session[0]
                self.PopupManager.show_warning_dialog(f"Xung đột thời gian! Phiên học này mới trùng với chặng {conflicting_session.start_time.strftime('%H:%M')} - {conflicting_session.end_time.strftime('%H:%M')}.")
                return
            else:
                session = session[1]
                self.session_manager.sessions.append(session)
        
        if self.active_card: # Edit
            session.status = self.active_card.session.status
            self.session_manager.sessions.remove(self.active_card.session)
            self.active_card.session = session
        else: # Create
            self.root.ids.schedule_grid.add_widget(UI.ScheduleCard(session=session))
        print(self.session_manager.sessions)
        self.queued_cards = []
        self.active_card = None
        self.switch_main()
    
    def cancel_session(self):
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

    def on_click_character(self):
        try:
            qr_path = self.session_manager.generate_qr_code()
            if qr_path:
                self.PopupManager.show_character_dialog(qr_path)
            else:
                print("Failed to update QR code - no path or widget not found!")
        except Exception as e:
            print(f"Error updating QR code: {e}")

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
        self.character.check_level_up()
        self.character.validate_health()
        self.character.check_negative_stats()

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
              AppDict.character_card.name = value
              AppDict.schedule_character_card.name = value
          elif type == "level":
              AppDict.character_card.level = value
              AppDict.schedule_character_card.level = value
              if self.FullyLoaded:
                  self.Sound_LevelUp.play()
                  self.PopupManager.show_level_up_dialog()
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
        except Exception as e:
            print(f"Error updating player labels: {e}")
    
    def confirm_login(self):
        self.character.name = self.root.ids.login_name_field.text
        self.switch_main()
        self.PopupManager.show_welcome_dialog()
    
    def revive_character(self):
        self.character.equipment = []
        self.character.inventory = []
        self.character.level = 1
        self.character.xp = 0
        self.character.xp_to_next_level = 100
        self.character.hp = 50
        self.character.max_hp = 50
        self.character.dex = 1
        self.character.int = 1 
        self.character.luk = 1
        self.character.available_points = 0
        self.character.gold = 10

        self.HeroKilled = False
        self.update_inventories()
        self.switch_main()

    def show_analytics_dialog(self):
        # Debug: Print analytics data before generating report
        print(f"Analytics sessions count: {len(getattr(self.analytics, 'completed_sessions', []))}")
        print(f"Quest system active quests: {len(self.quest_system.active_quests)}")
        print(f"Session manager sessions: {len(self.session_manager.sessions)}")
        
        ReportString = self.analytics.generate_report()
        print(f"Generated report: {ReportString[:100]}...")  # Print first 100 chars for debugging
        self.PopupManager.show_analytics_dialog(ReportString)

    def show_analytics_from_code_dialog(self):
       

        text_field = MDTextField(
            MDTextFieldHintText(text="Mã QR hoặc mã base64...", font_style="Label"),
            id="analytics_code_field",
            mode="outlined",
            size_hint_x=0.85,
            size_hint_y=None,
            height="56dp",
        )

        def on_load_code(*_):
            code = text_field.text.strip()
            if not code:
                self.PopupManager.show_warning_dialog("Vui lòng nhập mã QR/Base64!")
                return
            try:
                # Tạo session manager tạm để import dữ liệu QR, KHÔNG ghi đè dữ liệu hiện tại
                temp_session_manager = Code.SessionManager(
                    character=Code.Character("Temp"),
                    reward_system=Code.RewardSystem(),
                    analytics=Code.StudyAnalytics(Code.QuestSystem())
                )
                success = temp_session_manager.import_from_qr_data(code)
                if not success:
                    self.PopupManager.show_warning_dialog("Mã QR không hợp lệ hoặc không đúng định dạng!")
                    return

                imported_character = temp_session_manager.character
                imported_analytics = temp_session_manager.analytics

                # Tạo report từ dữ liệu đã import
                report = imported_analytics.generate_report()
                character_info = f"""
=== THÔNG TIN NHÂN VẬT ĐÃ IMPORT ===
Tên: {imported_character.name}
Level: {imported_character.level}
HP: {imported_character.hp}/{imported_character.max_hp}
Stats: DEX:{imported_character.dex} | INT:{imported_character.int} | LUK:{imported_character.luk}
Vàng: {imported_character.gold}
Thành tích: {len(imported_character.unlocked_achievements)}
Trang bị: {len(imported_character.equipment)}
Kho đồ: {len(imported_character.inventory)}

"""
                full_report = character_info + report

                self.PopupManager.show_analytics_dialog(full_report)
                self.analytics_code_dialog.dismiss()
                self.PopupManager.show_info_snackbar(f"Đã xem dữ liệu của: {imported_character.name}")

            except Exception as e:
                self.PopupManager.show_warning_dialog(f"Lỗi khi đọc mã: {e}")

        content = MDBoxLayout(
            text_field,
            MDButton(
                MDButtonText(text="Xem"),
                style="filled",
                size_hint_x=0.15,
                size_hint_y=None,
                height="56dp",
                on_release=on_load_code,
            ),
            orientation="horizontal",
            spacing="8dp",
            adaptive_height=True,
        )

        self.analytics_code_dialog = MDDialog(
            MDDialogHeadlineText(text="Xem Dữ Liệu Từ Mã QR"),
            MDDialogContentContainer(content),
            MDDialogButtonContainer(
                MDButton(MDButtonText(text="Đóng"), style="outlined", on_release=lambda x: self.analytics_code_dialog.dismiss()),
            ),
        )
        self.analytics_code_dialog.open()

    def on_home_switch_tab(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.root.ids.screen_manager_home.current = item_text
    
    def trigger_confetti(self, amount: int = 40):
        if self.root.current != "Main":
            return
        self.Sound_Pop.play()
        for _ in range(amount):
            particle = UI.ConfettiParticle(pos=(Window.width/2, 0))  # Đổi từ Popups.ConfettiParticle
            self.root.ids.effect_layer.add_widget(particle)

    def on_toggle_theme(self): # Switch to theme_cls.primary_palette
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    # Arena Methods
    def load_arena_opponent(self):
        """Mở dialog để nhập mã QR hoặc base64 của đối thủ"""
        def on_confirm_opponent_code(text_input):
            base64_code = text_input.text.strip()
            if not base64_code:
                self.PopupManager.show_info_snackbar("Vui lòng nhập mã đối thủ!")
                return
            
            try:
                success = self.session_manager.arena.load_opponent(base64_code)
                if success:
                    self.update_arena_display()
                    self.PopupManager.show_info_snackbar(f"Đã load đối thủ: {self.session_manager.arena.bot.name}")
                    dialog.dismiss()
                else:
                    self.PopupManager.show_info_snackbar("Không thể load đối thủ từ mã này!")
            except Exception as e:
                self.PopupManager.show_info_snackbar(f"Lỗi: {str(e)}")
        
        # Tạo text input cho mã QR/base64
        text_input = MDTextField(
            mode="outlined",
            size_hint_y=None,
            height="56dp"
        )
        text_input.add_widget(MDTextFieldHintText(text="Mã QR hoặc mã base64"))
        
        # Tạo dialog
        dialog = MDDialog(
            MDDialogHeadlineText(text="Nhập Mã Đối Thủ"),
            MDDialogContentContainer(
                text_input,
                orientation="vertical",
                spacing="16dp",
                size_hint_y=None,
                height="100dp"
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Hủy"),
                    style="text",
                    on_release=lambda x: dialog.dismiss()
                ),
                MDButton(
                    MDButtonText(text="Xác Nhận"),
                    style="elevated",
                    on_release=lambda x: on_confirm_opponent_code(text_input)
                ),
                spacing="8dp"
            )
        )
        dialog.open()
    
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
        
        # Lưu HP ban đầu trước khi bắt đầu trận đấu
        self.session_manager.arena.original_player_hp = self.character.hp
        self.session_manager.arena.original_bot_hp = self.session_manager.arena.bot.hp
        
        success = self.session_manager.arena.start_battle(self.character)
        if success:
            self.update_arena_display()
            self.update_arena_ui_state(True)
            self.PopupManager.show_battle_message("Trận đấu bắt đầu! Chọn skill để chiến đấu!")
            Clock.schedule_once(lambda dt: self.PopupManager.show_info_snackbar("Trận đấu đã bắt đầu! Chọn skill để tấn công!"), 0.5)
    
    def reset_arena_battle(self):
        """Reset trận đấu và khôi phục HP về trạng thái ban đầu"""
        # Khôi phục HP của character từ original_hp nếu có
        if hasattr(self.session_manager.arena, 'original_player_hp'):
            self.character.hp = self.session_manager.arena.original_player_hp
        
        # Reset arena state
        self.session_manager.arena.battle_active = False
        self.session_manager.arena.battle_log = []
        self.session_manager.arena.turn_count = 0
        self.session_manager.arena.player_copy = None
        
        # Reset bot HP nếu có
        if self.session_manager.arena.bot and hasattr(self.session_manager.arena, 'original_bot_hp'):
            self.session_manager.arena.bot.hp = self.session_manager.arena.original_bot_hp
        
        self.update_arena_display()
        self.update_arena_ui_state(False)
        self.PopupManager.show_info_snackbar("Đã reset trận đấu và khôi phục HP!")
    
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
            
            # Hiệu ứng rung cho bot khi bot tấn công/phép thuật (tìm trong message)
            if "đánh thường" in message or "dùng phép" in message:
                # Kiểm tra nếu là bot tấn công (tên bot xuất hiện trước "đánh thường" hoặc "dùng phép")
                if self.session_manager.arena.bot and self.session_manager.arena.bot.name in message:
                    Clock.schedule_once(lambda dt: self.shake_character(is_player=False), i * 0.8 + 0.2)
                # Nếu là player tấn công (tên player xuất hiện trước)
                elif self.session_manager.arena.player_copy and self.session_manager.arena.player_copy.name in message:
                    Clock.schedule_once(lambda dt: self.shake_character(is_player=True), i * 0.8 + 0.2)
        
        # Cập nhật hiển thị
        self.update_arena_display()
        
        # Kiểm tra kết thúc trận đấu
        if result.get("battle_ended", False):
            winner = result.get("winner")
            delay_time = len(messages) * 0.8 + 1.0  # Đợi tất cả messages hiển thị xong
            
            if winner == "player":
                # Lấy thưởng từ result (đã được tính trong backend)
                arena_xp = result.get("xp_reward", 0)
                arena_gold = result.get("gold_reward", 0)
                
                Clock.schedule_once(
                    lambda dt: self.PopupManager.show_battle_result_dialog("player", result.get("messages", []), arena_xp, arena_gold),
                    delay_time
                )
                # Không cộng thêm XP/Gold ở đây vì backend đã cộng rồi
                Clock.schedule_once(lambda dt: self.PopupManager.show_reward(arena_xp, arena_gold), delay_time + 1.5)
            else:
                Clock.schedule_once(
                    lambda dt: self.PopupManager.show_battle_result_dialog("bot", result.get("messages", [])),
                    delay_time
                )
            
            # Chỉ cập nhật UI state, KHÔNG reset HP
            Clock.schedule_once(lambda dt: self.update_arena_ui_state(False), delay_time + 1.0)
            # Không gọi end_battle để không reset HP về trạng thái ban đầu
    
    def show_character_stats_dialog(self):
        """Show player character stats in a snackbar popup"""
        stats_text = (f"{self.character.name} (Lv.{self.character.level})\n"
                     f"HP: {self.character.hp}/{self.character.max_hp}\n"
                     f"DEX: {self.character.dex} | INT: {self.character.int} | LUK: {self.character.luk}")
        
        self.PopupManager.show_info_snackbar(stats_text)
    
    def show_bot_stats_dialog(self):
        """Show bot character stats in a snackbar popup"""
        if not self.session_manager.arena.bot:
            self.PopupManager.show_info_snackbar("Chưa có đối thủ!")
            return
        
        bot = self.session_manager.arena.bot
        stats_text = (f"{bot.name} (Lv.{bot.level})\n"
                     f"HP: {bot.hp}/{bot.max_hp}\n"
                     f"DEX: {bot.dex} | INT: {bot.int_stat} | LUK: {bot.luk}")
        
        self.PopupManager.show_info_snackbar(stats_text)
    
    def update_arena_ui_state(self, battle_active):
        """Update arena UI buttons based on battle state"""
        try:
            start_btn = self.root.ids.start_battle_btn
            reset_btn = self.root.ids.reset_battle_btn
            
            if battle_active:
                start_btn.disabled = True
                start_btn.text = "Trận đấu đang diễn ra..."
                reset_btn.disabled = False
            else:
                start_btn.disabled = False
                start_btn.text = "Bắt Đầu Trận Đấu"
                reset_btn.disabled = False
        except Exception as e:
            print(f"Error updating arena UI state: {e}")
    
    def shake_character(self, is_player=True):
        """Add shake animation effect to character cards"""
        try:
            from kivy.animation import Animation
            
            if is_player:
                card = self.root.ids.player_character_card
            else:
                card = self.root.ids.bot_character_card
            
            # Lưu vị trí gốc
            original_x = card.x
            original_y = card.y
            
            # Tạo chuỗi animation lắc mạnh hơn với cả x và y
            shake_anim = (
                Animation(x=original_x + 15, y=original_y + 5, duration=0.08) + 
                Animation(x=original_x - 15, y=original_y - 5, duration=0.08) +
                Animation(x=original_x + 10, y=original_y + 3, duration=0.08) +
                Animation(x=original_x - 10, y=original_y - 3, duration=0.08) +
                Animation(x=original_x + 5, y=original_y + 2, duration=0.08) +
                Animation(x=original_x, y=original_y, duration=0.08)
            )
            
            shake_anim.start(card)
        except Exception as e:
            print(f"Error creating shake animation: {e}")
    
    def update_arena_display_from_demo(self):
        """Load a random demo bot from Code.generate_demo_base64_codes and update arena display."""
        try:
            from Backend.Code import generate_demo_base64_codes
            demo_codes = generate_demo_base64_codes()
            if not demo_codes:
                self.PopupManager.show_info_snackbar("Không có dữ liệu demo!")
                return
            import random
            demo_code = random.choice(demo_codes)
            success = self.session_manager.arena.load_opponent(demo_code)
            if success:
                self.update_arena_display()
                bot = self.session_manager.arena.bot
                self.PopupManager.show_info_snackbar(f"Đã load demo bot: {bot.name}")
            else:
                self.PopupManager.show_info_snackbar("Không thể load bot demo!")
        except Exception as e:
            self.PopupManager.show_info_snackbar(f"Lỗi demo: {e}")
    
    def update_arena_display(self):
        """Cập nhật hiển thị thông tin nhân vật trong arena với stats battle"""
        try:
            AppDict = self.root.ids
            
            # Player - ưu tiên hiển thị HP từ battle copy nếu có
            if (self.session_manager.arena.player_copy):
                # Có battle copy: hiển thị HP từ copy (trong và sau trận đấu)
                player_name = f"{self.session_manager.arena.player_copy.name} - Lv.{self.session_manager.arena.player_copy.level}"
                player_hp = f"{self.session_manager.arena.player_copy.hp}/{self.session_manager.arena.player_copy.max_hp}"
                AppDict.player_name_label.text = player_name
                AppDict.player_hp_label.text = player_hp
                
                # Đổi màu HP thành đỏ nếu HP <= 0
                if self.session_manager.arena.player_copy.hp <= 0:
                    AppDict.player_hp_label.text_color = [1, 0, 0, 1]  # Đỏ
                else:
                    AppDict.player_hp_label.text_color = [0, 0.7, 0, 1]  # Xanh lá
            else:
                # Chưa có battle copy: hiển thị HP thật của character
                AppDict.player_name_label.text = f"{self.character.name} - Lv.{self.character.level}"
                AppDict.player_hp_label.text = f"{self.character.hp}/{self.character.max_hp}"
                
                # Đổi màu HP thành đỏ nếu HP <= 0
                if self.character.hp <= 0:
                    AppDict.player_hp_label.text_color = [1, 0, 0, 1]  # Đỏ
                else:
                    AppDict.player_hp_label.text_color = [0, 0.7, 0, 1]  # Xanh lá
            
            # Cập nhật avatar player với avatar thật
            if hasattr(self, 'avatar_path'):
                AppDict.player_avatar.source = self.avatar_path
            
            # Bot - cập nhật khi có dữ liệu, giữ nguyên default nếu chưa load
            if self.session_manager.arena.bot:
                bot = self.session_manager.arena.bot
                AppDict.bot_name_label.text = f"{bot.name} - Lv.{bot.level}"
                AppDict.bot_hp_label.text = f"{bot.hp}/{bot.max_hp}"
                
                # Đổi màu HP thành đỏ nếu HP <= 0
                if bot.hp <= 0:
                    AppDict.bot_hp_label.text_color = [1, 0, 0, 1]  # Đỏ
                else:
                    AppDict.bot_hp_label.text_color = [0, 0.7, 0, 1]  # Xanh lá
            else:
                # Hiển thị default khi chưa có bot
                AppDict.bot_name_label.text = "??? - Lv.?"
                AppDict.bot_hp_label.text = "?/?"
                AppDict.bot_hp_label.text_color = [0, 0, 0, 1]  # Đen
        except Exception as e:
            print(f"Error updating arena display: {e}")

    def check_background_exists(self):
        import os
        return os.path.exists("Art/Backgrounds/arena_bg.jpg")

GSS().run()