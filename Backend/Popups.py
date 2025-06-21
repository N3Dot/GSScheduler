from kivymd.uix.snackbar import MDSnackbar, MDSnackbarButtonContainer, MDSnackbarCloseButton, MDSnackbarText, MDSnackbarSupportingText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivy.metrics import dp

class Popup:
    """
    A dedicated class to manage creating and showing UI components
    like dialogs and snackbars.
    """
    def __init__(self, app):
        # Store a reference to the main app so we can access its properties
        self.app = app

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
                    MDListItemSupportingText(text="[b]Loại:[/b] Trang bị", markup=True),
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
                MDButton(MDButtonText(text="Đóng"), style="text", pos_hint={'center_x': 0.5},
                    on_release=lambda x: ItemDialog.dismiss(),
                ),
            ),
        )
        ItemDialog.open()