from kivy.lang import Builder
from kivymd.app import MDApp
from Backend import UI
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogContentContainer,
    MDDialogButtonContainer,
)
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.segmentedbutton import MDSegmentedButton, MDSegmentedButtonItem, MDSegmentButtonLabel
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.pickers import MDTimePickerDialVertical
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText

KV = """
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    name = "Creation"
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
                size_hint_x: 0.5
                MDLabel:
                    text: "Chi Tiết:"
                    bold: True
                    adaptive_height: True

                MDTextField:
                    hint_text: "Mô tả"
                    mode: "outlined"
                    max_height: "200dp"
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
                        text: "[b]Bắt Đầu: [/b] 18:00"
                        markup: True
                        font_style: "Label"
                        pos_hint: {"center_y": 0.5}
                        adaptive_height: True
                    MDButton:
                        pos_hint: {"center_y": 0.5}
                        style: "text"
                        on_release: app.show_time_picker()
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
                        text: "[b]Kết Thúc: [/b] 20:00"
                        markup: True
                        font_style: "Label"
                        pos_hint: {"center_y": 0.5}
                        adaptive_height: True
                    MDButton:
                        pos_hint: {"center_y": 0.5}
                        style: "text"
                        on_release: app.show_time_picker()
                        MDButtonText:
                            text: "Chọn"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "20dp"
                    adaptive_height: True
                    MDButton:
                        style: "outlined"
                        pos_hint: {"center_x": 0.5}
                        MDButtonText:
                            text: "Hoàn Thành"
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
"""

from kivy.core.window import Window
Window.size = (520, 780) # Debug Note 8 View

class ScheduleApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Snow"
        return Builder.load_string(KV)

    def add_quest(self):
        QuestCardInstance = UI.QuestCard(difficulty="3", description="Hoàn thành bài tập.")
        self.root.ids.schedule_quest_grid.add_widget(QuestCardInstance)

    def remove_quest(self, QuestCardInstance):
        self.root.ids.schedule_quest_grid.remove_widget(QuestCardInstance)

    def on_quest_edit(self, QuestCardInstance):
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

    def save_quest_changes(self, QuestCardInstance, segmented_button, description_field):
        selected_items = segmented_button.get_marked_items()
        if selected_items:
            for child in selected_items[0].walk(restrict=True):
                if isinstance(child, MDSegmentButtonLabel):
                    new_difficulty = child.text
                    QuestCardInstance.difficulty = new_difficulty
                    break

        QuestCardInstance.description = description_field.text
        self.QuestDialog.dismiss()
    
    def show_time_picker(self):
        time_picker = MDTimePickerDialVertical()
        time_picker.bind(on_ok=self.on_ok)
        time_picker.open()

    def on_ok(self, time_picker_vertical: MDTimePickerDialVertical):
        print(f"{time_picker_vertical.time}")
        MDSnackbar(
            MDSnackbarSupportingText(
                text=f"Time is `{time_picker_vertical.time}`",
            ),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()


if __name__ == '__main__':
    ScheduleApp().run()