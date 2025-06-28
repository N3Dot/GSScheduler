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
        else:
            MDSnackbar(
                MDSnackbarText(text="Bạn đã mất máu..."),
                MDSnackbarSupportingText(text="Máu có thể mất, nhưng ý chí vẫn còn nguyên vẹn. Hãy tiếp tục, chiến binh dũng cảm!"),
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

    def show_welcome_dialog(self):
        WelcomeDialog = MDDialog(
            MDDialogIcon(icon="gamepad-up"),
            MDDialogHeadlineText(text=f"Chào Mừng Đến Với Học Tập Kiểu RPG!"),
            MDDialogSupportingText(text="Bắt đầu bằng cách tạo một phiên học, đặt thời gian bắt đầu và kết thúc. Tạo các nhiệm vụ với độ khó tùy chọn - chúng chính là “quái vật” bạn cần tiêu diệt để nhận XP!\n\nKhi đến giờ, ứng dụng sẽ tự động kích hoạt phiên học và đếm giờ. Trong suốt thời gian đó, hãy tập trung hoàn thành nhiệm vụ, đánh dấu tiến độ và đạt hạng cao nhất.\n\nKết thúc phiên học, hệ thống sẽ trao thưởng nếu bạn làm tốt... hoặc trừ HP nếu bạn lười biếng!\n\nĐừng quên ghé qua Shop để tiêu vàng, nâng cấp nhân vật và chuẩn bị cho những phiên học tiếp theo!"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="outlined", pos_hint={'center_x': 0.5},
                    on_release=lambda x: WelcomeDialog.dismiss(),
                ),
                Widget(),
            ),
        )
        WelcomeDialog.open()
    
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
