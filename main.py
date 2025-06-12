from kivy.lang import Builder
from kivy.utils import platform
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarSupportingText

if platform not in ('android', 'ios'):
    from kivy.core.window import Window
    Window.size = (370, 740) # Note 8 Vertical View

class HomeMenuItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

KV = '''
<HomeMenuItem>
    MDNavigationItemIcon:
        icon: root.icon
    MDNavigationItemLabel:
        text: root.text

MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager_menu

            MDScreen:
                name: "Home"

                MDScreenManager:
                    id: screen_manager_home

                    MDScreen:
                        name: "Phiên Học"
                        MDBoxLayout:
                            md_bg_color: self.theme_cls.backgroundColor
                            pos_hint: {"center_y": 0.5}
                            FitImage:
                                source: f"https://picsum.photos/600/400"

                                size_hint_y: .35
                                pos_hint: {"top": 1}

                        MDBoxLayout:
                            MDLabel:
                                text: "Subscreen 1 - Schedules"
                                halign: "center"

                    MDScreen:
                        name: "Anh Hùng"
                        MDLabel:
                            text: "Subscreen 2 - Character"
                            halign: "center"
                    
                    MDScreen:
                        name: "Cửa Hàng"
                        MDLabel:
                            text: "Subscreen 3 - Shop"
                            halign: "center"
                
                MDNavigationBar:
                    on_switch_tabs: app.on_home_switch_tab(*args)
                    HomeMenuItem
                        icon: "av-timer"
                        text: "Phiên Học"
                        active: True
                    HomeMenuItem
                        icon: "account-tie-hat"
                        text: "Anh Hùng"
                    HomeMenuItem
                        icon: "shopping-outline"
                        text: "Cửa Hàng"
                
                MDFabButton:
                    pos_hint: {"x": 0.02, "top": 0.99}
                    on_release: navigation_drawer.set_state("toggle")
                    icon: "menu"
                    style: "small"
            
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
                            on_release: app.on_toggle_theme()
                            MDListItemLeadingIcon:
                                icon: "weather-sunny" if app.theme_cls.theme_style == "Light" else "weather-night"
                            MDListItemSupportingText:
                                text: "Current Theme:  Light Mode" if app.theme_cls.theme_style == "Light" else "Current Theme:  Dark Mode"
                        
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
                
                MDFabButton:
                    pos_hint: {"x": 0.02, "top": 0.99}
                    on_release: navigation_drawer.set_state("toggle")
                    icon: "menu"
                    style: "small"

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
    
    def on_home_switch_tab(self, bar: MDNavigationBar, item: MDNavigationItem, item_icon: str, item_text: str):
        self.root.ids.screen_manager_home.current = item_text

    def on_toggle_theme(self):
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        self.root.ids.trash_can_icon.theme_text_color = "Custom"
        self.root.ids.trash_can_icon.text_color = (1, 0, 0, 1)

GSS().run()