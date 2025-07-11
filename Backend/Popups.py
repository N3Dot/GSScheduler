import os
import shutil
import random

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarText, MDSnackbarSupportingText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import platform
from kivy.graphics import Color, Rectangle


class Popup:
    """
    A dedicated class to manage creating and showing UI components
    like dialogs and snackbars.
    """
    def __init__(self, app):
        # Store a reference to the main app so we can access its properties
        self.app = app
        self.instance = None
        self.valid_image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        self.file_manager = MDFileManager(exit_manager=self.file_manager_exit, select_path=self.select_path)

    def show_item_purchase(self, ItemShopCardInstance):
        MDSnackbar(
            MDSnackbarText(text="Thanh toán thành công!"),
            MDSnackbarSupportingText(text=f"Bạn đã mua: {ItemShopCardInstance.name}"),
            duration=1, y=dp(90), orientation="horizontal", pos_hint={"center_x": 0.72}, size_hint_x=0.5,
            background_color=self.app.theme_cls.onPrimaryContainerColor,
        ).open()
    
    def show_reward(self, xp, gold):
        MDSnackbar(
            MDSnackbarText(text="Bạn đã được thưởng!"),
            MDSnackbarSupportingText(text=f"[b]XP:[/b] +{xp}\n[b]Vàng:[/b] +{gold}", markup=True),
            duration=1, y=dp(90), orientation="horizontal", pos_hint={"center_x": 0.77}, size_hint_x=0.4,
            background_color=self.app.theme_cls.onPrimaryContainerColor,
        ).open()
        
    def show_session_finish_dialog(self, rank: str, xp=0, gold=0):
        if rank == "F":
            PerfIcon = "emoticon-cry-outline"
            PerfHeadline = "Chưa Phải Là Ngày Của Bạn?"
            PerfSupport = "Đôi khi thất bại là một phần không thể thiếu trên con đường trở nên mạnh mẽ hơn. Đừng nản lòng, quay lại, rèn luyện, và chứng minh bản thân! Huyền thoại không được tạo ra trong một ngày!"
        elif rank == "S":
            PerfIcon = "party-popper"
            PerfHeadline = "Tuyệt Đỉnh!"
            PerfSupport = "Không một nhiệm vụ nào có thể ngăn cản bạn! Sự tập trung, kỹ năng và tinh thần bất khuất đã đưa bạn lên đỉnh vinh quang!"
        else:
            PerfIcon = "party-popper"
            PerfHeadline = "Chúc Mừng!"
            PerfSupport = "Sự nỗ lực của bạn đã đặt nền móng vững chắc cho những thành tựu lớn hơn. Đường vinh quang luôn mở rộng cho những ai không bỏ cuộc!"
        FinishDialog = MDDialog(
            MDDialogIcon(icon=PerfIcon),
            MDDialogHeadlineText(text=PerfHeadline, bold=True),
            MDDialogSupportingText(text=PerfSupport),
            MDDialogContentContainer(
                MDBoxLayout(
                    MDLabel(text="Phiên học của bạn đã kết thúc.", font_style="Label", halign='center', theme_text_color="Custom", text_color=self.app.theme_cls.primaryColor, adaptive_height=True),
                    MDLabel(text="Kết quả cuối cùng:", font_style="Label", halign='center', bold=True, theme_text_color="Custom", text_color=self.app.theme_cls.primaryColor, adaptive_height=True),
                    MDLabel(text=rank, font_style="Display", role="large", halign='center', theme_text_color="Custom", text_color=self.app.theme_cls.primaryColor, adaptive_height=True),
                    adaptive_height=True,
                    spacing="5dp",
                    orientation="vertical",
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: self.session_finish_follow_up(FinishDialog, rank, xp, gold),
                ),
                Widget(),
            ),
        )
        FinishDialog.open()
        if rank != "F":
            self.app.trigger_confetti()
    
    def session_finish_follow_up(self, FinishDialog, rank, xp=0, gold=0):
        FinishDialog.dismiss()
        if rank != "F":
            if xp != 0 or gold != 0:
                MDSnackbar(
                    MDSnackbarText(text="Bạn đã được thưởng!"),
                    MDSnackbarSupportingText(text=f"[b]XP:[/b] +{xp}\n[b]Vàng:[/b] +{gold}", markup=True),
                    duration=1, y=dp(90), orientation="horizontal", pos_hint={"center_x": 0.77}, size_hint_x=0.4,
                    background_color=self.app.theme_cls.onPrimaryContainerColor,
                ).open()

    def show_level_up_dialog(self):
        LevelUpDialog = MDDialog(
            MDDialogIcon(icon="progress-upload"),
            MDDialogHeadlineText(text=f"{self.app.character.name} Đã Lên Cấp {self.app.character.level}!", bold=True),
            MDDialogSupportingText(text=f"Từ một chiến binh không ngừng nỗ lực, bạn đã vượt qua mọi thử thách và vươn tới tầm cao mới!"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: LevelUpDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        LevelUpDialog.open()
        self.app.trigger_confetti()

    def show_item_dialog(self, item):
        rarity_types = [None, "Thường", "Nâng Cao", "Hiếm", "Sử Thi", "Huyền Thoại"]
        rarity_text = rarity_types[item.rarity.value]
        ItemDialog = MDDialog(
            MDDialogIcon(icon="list-box-outline"),
            MDDialogHeadlineText(text=item.name),
            MDDialogSupportingText(text=item.description),
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-four-points-circle-outline"),
                    MDListItemSupportingText(text=f"[b]Độ Hiếm:[/b] {rarity_text}", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="toolbox"),
                    MDListItemSupportingText(text=f"[b]Loại:[/b] {item.category}", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="arm-flex"),
                    MDListItemSupportingText(text=f"[b]DEX:[/b]  +{item.on_use_effect['dex']}   [b]INT:[/b]  +{item.on_use_effect['int']}   [b]LUK:[/b]  +{item.on_use_effect['luk']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="heart"),
                    MDListItemSupportingText(text=f"[b]HP:[/b]  +{item.on_use_effect['hp']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-box"),
                    MDListItemSupportingText(text=f"[b]XP:[/b]  +{item.on_use_effect['xp']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: ItemDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        ItemDialog.open()
    
    def show_owned_item_dialog(self, item):
        if item in self.app.character.equipment:
            ActionButton = MDButton(
                MDButtonText(text="Tháo Bỏ"), style="outlined", pos_hint={'center_x': 0.5},
                on_release=lambda x: self.app.on_unequip_item(item, ItemDialog),
            )
        elif item.category != "Tiêu Hao":
            ActionButton = MDButton(
                MDButtonText(text="Trang Bị"), style="outlined", pos_hint={'center_x': 0.5},
                on_release=lambda x: self.app.on_equip_item(item, ItemDialog),
            )
        else:
            ActionButton = MDButton(
                MDButtonText(text="Sử Dụng"), style="outlined", pos_hint={'center_x': 0.5},
                on_release=lambda x: self.app.on_use_item(item, ItemDialog),
            )
        rarity_types = [None, "Thường", "Nâng Cao", "Hiếm", "Sử Thi", "Huyền Thoại"]
        rarity_text = rarity_types[item.rarity.value]
        ItemDialog = MDDialog(
            MDDialogIcon(icon="list-box-outline"),
            MDDialogHeadlineText(text=item.name),
            MDDialogSupportingText(text=item.description),
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-four-points-circle-outline"),
                    MDListItemSupportingText(text=f"[b]Độ Hiếm:[/b] {rarity_text}", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="toolbox"),
                    MDListItemSupportingText(text=f"[b]Loại:[/b] {item.category}", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="arm-flex"),
                    MDListItemSupportingText(text=f"[b]DEX:[/b]  +{item.on_use_effect['dex']}   [b]INT:[/b]  +{item.on_use_effect['int']}   [b]LUK:[/b]  +{item.on_use_effect['luk']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="heart"),
                    MDListItemSupportingText(text=f"[b]HP:[/b]  +{item.on_use_effect['hp']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-box"),
                    MDListItemSupportingText(text=f"[b]XP:[/b]  +{item.on_use_effect['xp']}".replace("+-", "-"), markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                ActionButton,
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: ItemDialog.dismiss(),
                ),
                spacing="20dp",
            ),
        )
        ItemDialog.open()

    def show_character_dialog(self, qr_path: str):
        if qr_path and os.path.exists(qr_path):
            qr_source = qr_path
        else:
            qr_source = ""
            print(f"QR image file not found: {qr_path}")

        QRImageWidget = FitImage(
            source="",
            size_hint=(None, None),
            size=("240dp", "240dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[10, ],
        )
        QRImageWidget.source = qr_source
        QRImageWidget.reload()

        CharacterDialog = MDDialog(
            MDDialogIcon(icon="account-tie-hat-outline"),
            MDDialogHeadlineText(text=f"{self.app.character.name} (Cấp {self.app.character.level})", bold=True),
            MDDialogSupportingText(
                text="Quét mã QR để triệu hồi chiến binh huyền thoại này từ thế giới xa xăm...\nVinh quang chỉ dành cho người dám bước lên sàn đấu!",
                italic=True,
            ),
            MDDialogContentContainer(
                MDBoxLayout( # QR Code
                QRImageWidget,
                size_hint = (None, None),
                size = ("240dp", "240dp"),
                pos_hint = {"center_x": 0.5, "center_y": 0.5},
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: CharacterDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        CharacterDialog.open()

    def show_avatar_dialog(self):
        AvatarWidget = FitImage(
            source=f"{self.app.avatar_path}",
            size_hint=(None, None),
            size=("200dp", "200dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            radius=[10, ],
        )
        AvatarDialog = MDDialog(
            MDDialogIcon(icon="image-album"),
            MDDialogHeadlineText(text=f"Ảnh Của {self.app.character.name}", bold=True),
            MDDialogContentContainer(
                MDBoxLayout(
                AvatarWidget,
                size_hint = (None, None),
                size = ("240dp", "240dp"),
                pos_hint = {"center_x": 0.55, "center_y": 0.55},
                ),
                MDListItem(
                    MDListItemLeadingIcon(icon="folder-image"),
                    MDListItemSupportingText(text="Dùng Ảnh Trong Bộ Nhớ"),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor,
                    on_release=lambda x: self.use_local_avatar(AvatarDialog),
                ),
                MDListItem(
                    MDListItemLeadingIcon(icon="image-auto-adjust"),
                    MDListItemSupportingText(text="Dùng Ảnh Ngẫu Nhiên"),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor,
                    on_release=lambda x: self.use_random_avatar(AvatarDialog),
                ),
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: AvatarDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        AvatarDialog.open()

    def use_random_avatar(self, AvatarDialog):
        self.clear_avatar_save_path()
        self.app.reload_avatar()
        AvatarDialog.dismiss()

    def use_local_avatar(self, AvatarDialog):
        self.file_manager_open()
        AvatarDialog.dismiss()
    
    def show_analytics_dialog(self, ReportString: str):
        AnalyticsDialog = MDDialog(
            MDDialogIcon(icon="google-analytics"),
            MDDialogHeadlineText(text=f"Kết Quả Học Tập"),
            MDDialogSupportingText(text=ReportString),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: AnalyticsDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        AnalyticsDialog.open()
    
    def show_warning_dialog(self, warning_text: str = None):
        WarningDialog = MDDialog(
            MDDialogIcon(icon="exclamation-thick"),
            MDDialogHeadlineText(text=f"Khoan Đã...!?"),
            MDDialogSupportingText(text=warning_text),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: WarningDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        WarningDialog.open()

    def show_erase_dialog(self):
        EraseDialog = MDDialog(
            MDDialogIcon(icon="exclamation-thick", theme_text_color="Custom", text_color=(1, 0, 0, 1)),
            MDDialogHeadlineText(text=f"[color=ff4444]Xóa Dữ Liệu[/color]", bold=True),
            MDDialogSupportingText(text="[color=ff4444]Bạn có chắc rằng bạn muốn xóa tất cả dữ liệu nhân vật của mình? Ứng dụng sẽ đóng để khởi động lại![/color]"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Xóa"), style="filled", pos_hint={'center_x': 0.5},
                    on_release=lambda x: self.clear_save(EraseDialog),
                ),
                MDButton(MDButtonText(text="Hủy"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: EraseDialog.dismiss(),
                ),
                Widget(),
                spacing="20dp",
            ),
        )
        EraseDialog.open()
    
    def get_avatar_save_path(self, filename: str = None):
        '''
        Get the platform-specific base directory from the app's properties.
        Create the 'Avatar' directory if it doesn't already exist.
        '''
        if platform == 'android':
            from android.storage import app_storage_path # type: ignore
            user_data_dir = app_storage_path()
            avatar_dir = os.path.join(user_data_dir, 'Avatar')
        else:
            user_data_dir = os.path.dirname(os.path.abspath(__file__))
            avatar_dir = os.path.join(user_data_dir, 'Avatar')

        os.makedirs(avatar_dir, exist_ok=True)
        if filename:
            return os.path.join(avatar_dir, filename)
        else:
            return avatar_dir
    
    def clear_avatar_save_path(self):
        """
        Clears all files from the 'Avatar' subdirectory.
        """
        try:
            avatar_dir = self.get_avatar_save_path()
            if not os.path.exists(avatar_dir):
                print("Avatar directory does not exist, nothing to clear.")
                return

            for filename in os.listdir(avatar_dir):
                file_path = os.path.join(avatar_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            print("Avatar directory cleared.")
        except Exception as e:
            print(f"Failed to clear avatar directory: {e}")
    
    def clear_save(self, EraseDialog = None): # Clear save and quit.
        if EraseDialog:
            EraseDialog.dismiss()
        try:
            self.clear_avatar_save_path()
            save_file = self.app.session_manager.save_file_path
            if os.path.isfile(save_file) or os.path.islink(save_file):
                os.unlink(save_file)
            self.app.EnableSave = False
            self.app.get_running_app().stop()
        except Exception as e:
            print(f"Failed to clear save: {e}")
    
    def select_path(self, path: str):
        self.file_manager_exit()
        if not os.path.isfile(path):
            message = "Không tìm thấy tệp."
        else:
            file_ext = os.path.splitext(path)[1].lower()
            if file_ext in self.valid_image_extensions:
                try:
                    # 1. Clear the storage directory.
                    self.clear_avatar_save_path()

                    # 2. Copy the new file to the app's safe directory.
                    filename = os.path.basename(path)
                    destination_path = self.get_avatar_save_path(filename)
                    shutil.copy(path, destination_path)
                    message = "Thay đổi ảnh nhân vật thành công!"
                    print(f"Final image path: {destination_path}")
                    self.app.reload_avatar()

                except Exception as e:
                    message = f"Lỗi xử lý tệp: {e}"
            else:
                message = f"Tệp '{os.path.basename(path)}' không phải là hình ảnh hợp lệ."

        MDSnackbar(MDSnackbarText(text=message), y=dp(24), pos_hint={"center_x": 0.5}, size_hint_x=0.9).open()
    
    def file_manager_open(self):
        if platform == 'android':
            from android.storage import primary_external_storage_path # type: ignore
            self.file_manager.show(primary_external_storage_path())
        else:
            self.file_manager.show(os.path.expanduser("~"))
    
    def file_manager_exit(self, *args):
        self.file_manager.close()

    def show_long_dialog(self, HeadlineList: list, TextList: list, Index = 0):
        if len(TextList) <= 1:
            LongDialog = MDDialog(
                MDDialogIcon(icon="chat-question"),
                MDDialogHeadlineText(text=HeadlineList[Index], markup=True),
                MDDialogSupportingText(text=TextList[Index], markup=True),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(MDButtonText(text="Đóng"), style="text", pos_hint={'center_x': 0.5},
                        on_release=lambda x: LongDialog.dismiss(),
                    ),
                    Widget(),
                ),
            )
        else:
            if Index == 0:
                LongDialog = MDDialog(
                    MDDialogIcon(icon="chat-question"),
                    MDDialogHeadlineText(text=HeadlineList[Index], markup=True),
                    MDDialogSupportingText(text=TextList[Index], markup=True),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(MDButtonText(text="<<", bold=True), style="text", pos_hint={'center_x': 0.5}, disabled=True,
                            on_release=lambda x: LongDialog.dismiss(),
                        ),
                        MDButton(MDButtonText(text="Đóng"), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: LongDialog.dismiss(),
                        ),
                        MDButton(MDButtonText(text=">>", bold=True), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: self.show_long_dialog(HeadlineList, TextList, Index+1),
                        ),
                        Widget(),
                    ),
                )
            elif Index != (len(TextList) - 1):
                LongDialog = MDDialog(
                    MDDialogIcon(icon="chat-question"),
                    MDDialogHeadlineText(text=HeadlineList[Index]),
                    MDDialogSupportingText(text=TextList[Index]),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(MDButtonText(text="<<", bold=True), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: self.show_long_dialog(HeadlineList, TextList, Index-1),
                        ),
                        MDButton(MDButtonText(text="Đóng"), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: LongDialog.dismiss(),
                        ),
                        MDButton(MDButtonText(text=">>", bold=True), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: self.show_long_dialog(HeadlineList, TextList, Index+1),
                        ),
                        Widget(),
                    ),
                )
            else:
                LongDialog = MDDialog(
                    MDDialogIcon(icon="chat-question"),
                    MDDialogHeadlineText(text=HeadlineList[Index]),
                    MDDialogSupportingText(text=TextList[Index]),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(MDButtonText(text="<<", bold=True), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: self.show_long_dialog(HeadlineList, TextList, Index-1),
                        ),
                        MDButton(MDButtonText(text="Đóng"), style="text", pos_hint={'center_x': 0.5},
                            on_release=lambda x: LongDialog.dismiss(),
                        ),
                        MDButton(MDButtonText(text=">>", bold=True), style="text", pos_hint={'center_x': 0.5}, disabled=True,
                            on_release=lambda x: LongDialog.dismiss(),
                        ),
                        Widget(),
                    ),
                )
        LongDialog.open()
        if self.instance:
            self.instance.dismiss()
        self.instance = LongDialog

    def show_info_snackbar(self, message: str):
        """Hiển thị thông báo snackbar đơn giản"""
        MDSnackbar(
            MDSnackbarText(text=message),
            duration=2, 
            y=dp(90), 
            orientation="horizontal", 
            pos_hint={"center_x": 0.5}, 
            size_hint_x=0.8,
            background_color=self.app.theme_cls.primaryColor,
        ).open()

    def show_battle_message(self, message: str, message_type: str = "info"):
        """Hiển thị thông báo battle dạng popup với hiệu ứng"""
        from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
        
        # Chọn màu dựa trên loại thông báo
        if "thắng" in message.lower() or "chiến thắng" in message.lower():
            bg_color = [0.2, 0.7, 0.2, 1]  # Xanh lá
        elif "thua" in message.lower() or "thất bại" in message.lower():
            bg_color = [0.7, 0.2, 0.2, 1]  # Đỏ
        elif "sát thương" in message.lower():
            bg_color = [0.9, 0.5, 0.1, 1]  # Cam
        elif "thủ" in message.lower():
            bg_color = [0.2, 0.5, 0.9, 1]  # Xanh dương
        else:
            bg_color = self.app.theme_cls.primaryColor
        
        snackbar = MDSnackbar(
            MDSnackbarText(text=message),
            duration=2,
            y="200dp",
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
            background_color=bg_color,
        )
        snackbar.open()
    
    def show_battle_result_dialog(self, winner: str, messages: list, xp_reward: int = None, gold_reward: int = None):
        """Hiển thị dialog kết quả trận đấu với battle log đầy đủ"""
        from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
        from kivymd.uix.button import MDButton, MDButtonText
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivymd.uix.label import MDLabel
        from kivy.uix.widget import Widget
        
        # Tạo nội dung dialog
        content_box = MDBoxLayout(orientation="vertical", spacing="8dp", adaptive_height=True)
        
        # Hiển thị battle log đầy đủ từ arena
        if hasattr(self.app.session_manager, 'arena') and self.app.session_manager.arena.battle_log:
            battle_log = self.app.session_manager.arena.battle_log
            
            # Title cho battle log
            log_title = MDLabel(
                text="[b]Diễn biến trận đấu:[/b]",
                font_style="Title",
                role="small",
                adaptive_height=True,
                theme_text_color="Primary",
                markup=True
            )
            content_box.add_widget(log_title)
            
            # Hiển thị các lượt đánh (tối đa 8 lượt cuối)
            for log_entry in battle_log[-8:]:
                # Loại bỏ các icon và clean text
                clean_text = log_entry.replace("⚔️", "").replace("🛡️", "").replace("✨", "").strip()
                
                label = MDLabel(
                    text=clean_text,
                    font_style="Body",
                    role="small",
                    adaptive_height=True,
                    theme_text_color="Secondary"
                )
                content_box.add_widget(label)
        else:
            # Fallback: hiển thị messages nếu không có battle log
            for msg in messages[-5:]:
                # Clean text loại bỏ icons
                clean_text = msg.replace("⚔️", "").replace("🛡️", "").replace("✨", "").strip()
                
                label = MDLabel(
                    text=clean_text,
                    font_style="Body",
                    role="small",
                    adaptive_height=True,
                    theme_text_color="Secondary"
                )
                content_box.add_widget(label)
        
        # Hiển thị thưởng chính xác nếu thắng
        if winner == "player" and xp_reward is not None and gold_reward is not None:
            reward_label = MDLabel(
                text=f"[b]Thưởng:[/b] +{xp_reward} XP, +{gold_reward} Vàng!",
                font_style="Body",
                role="medium",
                adaptive_height=True,
                theme_text_color="Custom",
                text_color=(0.2, 0.6, 0.2, 1),
                markup=True
            )
            content_box.add_widget(reward_label)
        
        icon = "trophy" if winner == "player" else "emoticon-sad"
        title = "Chiến Thắng!" if winner == "player" else "Thất Bại"
        
        dialog = MDDialog(
            MDDialogIcon(icon=icon),
            MDDialogHeadlineText(text=title),
            MDDialogSupportingText(text="Kết quả trận đấu:"),
            MDDialogContentContainer(
                content_box,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Đóng"),
                    style="outlined",
                    on_release=lambda x: dialog.dismiss(),
                ),
                Widget(),
            ),
        )
        dialog.open()

    def show_arena_input_dialog(self, arena):
        """Hiển thị dialog nhập dữ liệu đối thủ với hint text"""
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
        from kivymd.uix.button import MDButton, MDButtonText
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.widget import Widget
        
        # Textfield với hint từ arena
        text_input = MDTextField(
            hint_text=arena.get_opponent_input_hint() if hasattr(arena, 'get_opponent_input_hint') else "Nhập mã QR hoặc base64 của đối thủ...",
            multiline=True,
            size_hint_y=None,
            height="100dp"
        )
        
        def validate_and_load():
            input_data = text_input.text.strip()
            if input_data:
                # Sử dụng validation từ arena nếu có
                if hasattr(arena, 'validate_opponent_data'):
                    validation = arena.validate_opponent_data(input_data)
                    if validation["valid"]:
                        arena.load_opponent(input_data)
                        self.show_info_snackbar(f"Đã load đối thủ: {validation['preview']['name']}")
                        dialog.dismiss()
                    else:
                        self.show_info_snackbar(validation["error"])
                else:
                    # Fallback nếu không có validation method
                    success = arena.load_opponent(input_data)
                    if success:
                        self.show_info_snackbar("Đã load đối thủ thành công!")
                        dialog.dismiss()
                    else:
                        self.show_info_snackbar("Không thể load đối thủ!")
            else:
                self.show_info_snackbar("Vui lòng nhập dữ liệu đối thủ")
        
        dialog = MDDialog(
            MDDialogIcon(icon="sword-cross"),
            MDDialogHeadlineText(text="Nhập Đối Thủ"),
            MDDialogSupportingText(text="Nhập mã QR hoặc dữ liệu base64 của đối thủ để bắt đầu trận đấu"),
            MDDialogContentContainer(
                text_input,
                orientation="vertical",
            ),
            MDDialogButtonContainer(
                MDButton(
                    MDButtonText(text="Load"),
                    style="filled",
                    on_release=lambda x: validate_and_load(),
                ),
                MDButton(
                    MDButtonText(text="Hủy"),
                    style="outlined",
                    on_release=lambda x: dialog.dismiss(),
                ),
                spacing="20dp",
            ),
        )
        dialog.open()
        
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
