from kivy.config import Config
from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock # Clock.schedule_once()
from kivy.metrics import dp
if platform not in ('android', 'ios'):
    Config.set('graphics', 'resizable', False)
    from kivy.core.window import Window
    Window.size = (370, 740) # Note 8 Vertical View
    # Window.always_on_top = True

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivymd.uix.chip import MDChip, MDChipText, MDChipLeadingIcon
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarSupportingText
from Backend import Code, UI

KV = '''
<MenuButton@MDFabButton>:
    pos_hint: {"x": 0.02, "top": 0.99}
    icon: "menu"
    style: "small"

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager_menu

            MDScreen:
                name: "Home"

                MDScreenManager:
                    id: screen_manager_home

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
                                        text: "2 Phiên Học"
                                        halign: "center"
                                        pos_hint: {"center_y": 0.15}
                                        font_style: "Title"
                                        theme_text_color: "Custom"
                                        text_color: 1, 1, 1, 1
                                ScheduleCharacterCard:
                                    name: "Nguyễn Văn A"
                                    level: 15
                                    hpCurrent: 50
                                    hpMax: 100
                                    xpCurrent: 145
                                    xpMax: 145
                                    goldAmount: 500
                            
                            MDBoxLayout:
                                size_hint_y: None
                                height: "25dp"
                                md_bg_color: app.theme_cls.primaryColor

                            MDBoxLayout:
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
                        
                        MDFabButton:
                            icon: "plus"
                            pos_hint: {'x': 0.41, 'y': 0.69}
                    # --- Schedules End Section ---

                    # --- Character Start Section ---
                    MDScreen:
                        name: "Anh Hùng"
                        MDBoxLayout:
                            orientation: "vertical"
                            CharacterCard:
                                name: "Nguyễn Văn A"
                                title: "Hạng Tân Binh"
                                level: 15
                                hpCurrent: 50
                                hpMax: 100
                                xpCurrent: 145
                                xpMax: 145
                                dex: 10
                                int: 15
                                luk: 25
                            MDBoxLayout:
                                orientation: "vertical"
                                Widget:
                                MDButton:
                                    style: "elevated"
                                    pos_hint: {"center_x": 0.5}
                                    MDButtonText:
                                        text: "Đang Thi Công..."
                                    MDButtonIcon:
                                        icon: "progress-wrench"
                                Widget:
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
                                        current: 100
                                        max: 125
                                MDBoxLayout:
                                    size_hint_x: 1
                                    orientation: "vertical"
                                    GoldCounterCard:
                                        goldAmount: 500
                                        pos_hint: {'center_x': 0.55}
                            
                            Widget:
                                size_hint_y: None
                                height: "24dp"
                                
                            MDScrollView:
                                do_scroll_x: False
                                MDGridLayout:
                                    id: shop_grid
                                    cols: 3
                                    padding: dp(12), dp(0), dp(0), dp(90)
                                    spacing: dp(12)
                                    adaptive_height: True
                                    size_hint: None, None
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
                            text: "Anh Hùng"
                    MDNavigationItem:
                        MDNavigationItemIcon:
                            icon: "shopping-outline"
                        MDNavigationItemLabel:
                            text: "Cửa Hàng"
                MenuButton:
                    on_release: navigation_drawer.set_state("toggle")
            
            # --- Đấu Trường Start Section ---
            MDScreen:
                name: "Arena"
                
                MenuButton:
                    on_release: navigation_drawer.set_state("toggle")
            # --- Đấu Trường End Section ---

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
                            MDListItemLeadingIcon:
                                icon: "help-circle-outline"
                            MDListItemSupportingText:
                                text: "Instructions"

                        MDListItem:
                            MDListItemLeadingIcon:
                                id: trash_can_icon
                                icon: "delete-outline"
                                theme_text_color: "Custom"
                                text_color: 1, 0, 0, 1
                            MDListItemSupportingText:
                                text: "[color=ff4444]Reset All[/color]"
                MenuButton:
                    on_release: navigation_drawer.set_state("toggle")

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
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Snow"
        return Builder.load_string(KV)
    
    def on_start(self):
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

    def menu_callback(self, textItem):
        print(textItem, self.root.ids.shop_gold_counter.goldAmount)

    def on_home_switch_tab(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.root.ids.screen_manager_home.current = item_text

    def on_toggle_theme(self): # Switch to theme_cls.primary_palette
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
    
    def on_stop(self):
        pass # Save .json settings

GSS().run()