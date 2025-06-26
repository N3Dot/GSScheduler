import os
import shutil

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarText, MDSnackbarSupportingText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.fitimage import FitImage
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.widget import Widget
from kivy.metrics import dp

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
    
    def show_reward_snackbar(self, XP=0, Gold=0):
        MDSnackbar(
            MDSnackbarText(text="Bạn đã được thưởng!"),
            MDSnackbarSupportingText(text=f"[b]XP:[/b] +{XP}\n[b]Vàng:[/b] +{Gold}", markup=True),
            duration=1, y=dp(90), orientation="horizontal", pos_hint={"center_x": 0.77}, size_hint_x=0.4,
            background_color=self.app.theme_cls.onPrimaryContainerColor,
            ).open()

    def show_item_dialog(self):
        ItemDialog = MDDialog(
            MDDialogIcon(icon="list-box-outline"),
            MDDialogHeadlineText(text="Kiếm Rỉ Sét"),
            MDDialogSupportingText(
                text="Một thanh kiếm cũ kỹ, lưỡi kiếm phủ đầy lớp rỉ sét do bị bỏ quên trong thời gian dài. Tay cầm lỏng lẻo, lưỡi kiếm sứt mẻ, nhưng vẫn có thể dùng để tự vệ trong trường hợp khẩn cấp. Được những nhà thám hiểm mới bắt đầu sử dụng như một phương án tạm thời.",
            ),
            MDDialogContentContainer(
                MDDivider(),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-four-points-circle-outline"),
                    MDListItemSupportingText(text="[b]Độ Hiếm:[/b] Thường", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="toolbox"),
                    MDListItemSupportingText(text="[b]Loại:[/b] Vũ Khí", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="arm-flex"),
                    MDListItemSupportingText(text="[b]DEX:[/b] +5   [b]INT:[/b] +5   [b]LUK:[/b] +5", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="heart"),
                    MDListItemSupportingText(text="[b]HP:[/b]  +10", markup=True),
                    theme_bg_color="Custom",
                    md_bg_color=self.app.theme_cls.transparentColor),
                MDListItem(
                    MDListItemLeadingIcon(icon="star-box"),
                    MDListItemSupportingText(text="[b]XP:[/b]  +5", markup=True),
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
        self.clear_user_data_dir()
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
    
    def clear_user_data_dir(self):
        try:
            for filename in os.listdir(self.app.user_data_dir):
                file_path = os.path.join(self.app.user_data_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            print("user_data_dir cleared.")
        except Exception as e:
            print(f"Failed to clear user data directory: {e}")
    
    def file_manager_open(self):
        self.file_manager.show(os.path.expanduser("~"))
    
    def file_manager_exit(self, *args):
        self.file_manager.close()
    
    def select_path(self, path: str):
        self.file_manager_exit()
        if not os.path.isfile(path):
            message = "Không tìm thấy tệp."
        else:
            file_ext = os.path.splitext(path)[1].lower()
            if file_ext in self.valid_image_extensions:
                try:
                    # 1. Clear the storage directory.
                    self.clear_user_data_dir()

                    # 2. Copy the new file to the app's safe directory.
                    destination_path = os.path.join(self.app.user_data_dir, os.path.basename(path))
                    shutil.copy(path, destination_path)
                    message = "Thay đổi ảnh nhân vật thành công!"
                    print(f"Final image path: {destination_path}")
                    self.app.reload_avatar()

                except Exception as e:
                    message = f"Lỗi xử lý tệp: {e}"
            else:
                message = f"Tệp '{os.path.basename(path)}' không phải là hình ảnh hợp lệ."

        MDSnackbar(MDSnackbarText(text=message), y=dp(24), pos_hint={"center_x": 0.5}, size_hint_x=0.9).open()
