from kivy.config import Config
from kivy.lang import Builder
from kivy.utils import platform
from kivy.core.window import Window
if platform not in ('android', 'ios'):
    Window.size = (520, 780)

from kivymd.app import MDApp

# Simple test KV for Arena UI
KV = """
MDScreenManager:
    md_bg_color: self.theme_cls.backgroundColor
    MDScreen:
        name: "Arena"
        MDBoxLayout:
            orientation: "vertical"
            
            # Header với input code
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
                    
                MDButton:
                    text: "Load"
                    size_hint_x: 0.15
                    
                MDIconButton:
                    icon: "dice-6"
                    size_hint_x: 0.15
            
            # Arena Battle Area
            MDCard:
                elevation: 4
                radius: [12]
                md_bg_color: [0.1, 0.1, 0.2, 1]  # Dark arena background
                
                MDBoxLayout:
                    orientation: "vertical"
                    spacing: "8dp"
                    padding: "16dp"
                    
                    # Arena Title
                    MDLabel:
                        text: "⚔️ ĐẤUU TRƯỜNG ⚔️"
                        font_style: "Headline"
                        role: "medium"
                        halign: "center"
                        adaptive_height: True
                        theme_text_color: "Custom"
                        text_color: [1, 0.8, 0, 1]  # Gold color
                    
                    # Battle Field - Characters positioned in arena background
                    MDFloatLayout:
                        size_hint_y: 0.6
                        
                        # Arena Background Effect - The arena itself
                        MDCard:
                            md_bg_color: [0.15, 0.15, 0.3, 0.8]
                            radius: [8]
                            elevation: 2
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            size_hint: 0.95, 0.9
                            
                            # Arena floor pattern
                            MDBoxLayout:
                                orientation: "vertical"
                                padding: "8dp"
                                
                                MDLabel:
                                    text: "⚡ SÀN ĐẤU ⚡"
                                    font_style: "Title"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    pos_hint: {"center_x": 0.5}
                                    theme_text_color: "Custom"
                                    text_color: [0.5, 0.5, 0.5, 0.6]
                        
                        # Bot Character (Top Right) - Inside Arena
                        MDCard:
                            id: bot_character_card
                            size_hint: None, None
                            size: "140dp", "180dp"
                            pos_hint: {"x": 0.65, "y": 0.65}
                            elevation: 6
                            radius: [12]
                            md_bg_color: [0.8, 0.2, 0.2, 0.9]  # Red for enemy
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                padding: "8dp"
                                spacing: "4dp"
                                
                                # Bot Avatar
                                AsyncImage:
                                    id: bot_avatar
                                    source: "https://picsum.photos/100/100?random=2"
                                    size_hint: None, None
                                    size: "80dp", "80dp"
                                    pos_hint: {"center_x": 0.5}
                                
                                # Bot Info
                                MDLabel:
                                    id: bot_name_label
                                    text: "Bot - Lv.1"
                                    font_style: "Title"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                
                                # Bot HP Bar
                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "16dp"
                                    spacing: "4dp"
                                    
                                    MDLabel:
                                        text: "HP:"
                                        size_hint_x: None
                                        width: "24dp"
                                        font_style: "Body"
                                        role: "small"
                                        theme_text_color: "Custom"
                                        text_color: [1, 1, 1, 1]
                                    
                                    MDLinearProgressIndicator:
                                        id: bot_hp_bar
                                        value: 50
                                        max: 50
                                        size_hint_y: None
                                        height: "8dp"
                                    
                                MDLabel:
                                    id: bot_hp_label
                                    text: "50/50"
                                    font_style: "Body"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                
                                # Bot Stats
                                MDLabel:
                                    id: bot_stats_label
                                    text: "DEX:1 INT:1 LUK:1"
                                    font_style: "Body"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [0.9, 0.9, 0.9, 1]
                        
                        # Player Character (Bottom Left) - Inside Arena
                        MDCard:
                            id: player_character_card
                            size_hint: None, None
                            size: "140dp", "180dp"
                            pos_hint: {"x": 0.15, "y": 0.05}
                            elevation: 6
                            radius: [12]
                            md_bg_color: [0.2, 0.6, 0.9, 0.9]  # Blue for player
                            
                            MDBoxLayout:
                                orientation: "vertical"
                                padding: "8dp"
                                spacing: "4dp"
                                
                                # Player Avatar
                                AsyncImage:
                                    id: player_avatar
                                    source: "https://picsum.photos/100/100?random=1"
                                    size_hint: None, None
                                    size: "80dp", "80dp"
                                    pos_hint: {"center_x": 0.5}
                                
                                # Player Info
                                MDLabel:
                                    id: player_name_label
                                    text: "Player - Lv.1"
                                    font_style: "Title"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                
                                # Player HP Bar
                                MDBoxLayout:
                                    size_hint_y: None
                                    height: "16dp"
                                    spacing: "4dp"
                                    
                                    MDLabel:
                                        text: "HP:"
                                        size_hint_x: None
                                        width: "24dp"
                                        font_style: "Body"
                                        role: "small"
                                        theme_text_color: "Custom"
                                        text_color: [1, 1, 1, 1]
                                    
                                    MDLinearProgressIndicator:
                                        id: player_hp_bar
                                        value: 50
                                        max: 50
                                        size_hint_y: None
                                        height: "8dp"
                                    
                                MDLabel:
                                    id: player_hp_label
                                    text: "50/50"
                                    font_style: "Body"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [1, 1, 1, 1]
                                
                                # Player Stats
                                MDLabel:
                                    id: player_stats_label
                                    text: "DEX:1 INT:1 LUK:1"
                                    font_style: "Body"
                                    role: "small"
                                    halign: "center"
                                    adaptive_height: True
                                    theme_text_color: "Custom"
                                    text_color: [0.9, 0.9, 0.9, 1]
                        
                        # VS Label in center of arena
                        MDLabel:
                            text: "⚡ VS ⚡"
                            font_style: "Headline"
                            role: "large"
                            halign: "center"
                            pos_hint: {"center_x": 0.5, "center_y": 0.5}
                            theme_text_color: "Custom"
                            text_color: [1, 0.8, 0, 1]  # Gold
                    
                    # Skill Buttons
                    MDBoxLayout:
                        size_hint_y: None
                        height: "60dp"
                        spacing: "8dp"
                        
                        MDButton:
                            text: "⚔️ Đánh Thường"
                            style: "elevated"
                            theme_bg_color: "Custom"
                            md_bg_color: [0.8, 0.2, 0.2, 1]
                            
                        MDButton:
                            text: "🛡️ Thủ"
                            style: "elevated"
                            theme_bg_color: "Custom"
                            md_bg_color: [0.2, 0.6, 0.9, 1]
                            
                        MDButton:
                            text: "✨ Phép Thuật"
                            style: "elevated"
                            theme_bg_color: "Custom"
                            md_bg_color: [0.6, 0.2, 0.8, 1]
                    
                    # Battle Controls
                    MDBoxLayout:
                        size_hint_y: None
                        height: "60dp"
                        spacing: "8dp"
                        
                        MDButton:
                            id: start_battle_btn
                            text: "Bắt Đầu Trận Đấu"
                            style: "elevated"
                            
                        MDButton:
                            id: reset_battle_btn
                            text: "Reset"
                            style: "outlined"
"""

class TestArenaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Snow"
        return Builder.load_string(KV)

TestArenaApp().run()
