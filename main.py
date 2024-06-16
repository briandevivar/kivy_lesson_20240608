# FULLSTACKDEVTUTORIALS.COM
# TOPIC: KIVYMD AND SQLITE3
# LECTURER: BRIAN DE VIVAR
# DATE: JUNE 08, 2024
# YT: https://www.youtube.com/channel/UC3veSIv6YTZ6rK6UEOFmFmg
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogContentContainer, MDDialogButtonContainer
from kivymd.uix.divider import MDDivider
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemLeadingIcon, MDListItemSupportingText, \
    MDListItemTertiaryText
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.widget import Widget

from datetime import datetime

from db import db
from model import ToysModel


class CustomIconButton(MDIconButton):
    def __init__(self, icon, style, theme_icon_color, icon_color, toy_item: ToysModel, btn_pressed, app_root, **kwargs):
        super(CustomIconButton, self).__init__(**kwargs)
        self.icon = icon
        self.style = style
        self.theme_icon_color = theme_icon_color
        self.icon_color = icon_color
        self.toy_item = toy_item
        self.btn_pressed = btn_pressed
        self.app_root = app_root

    def on_release(self):
        if self.btn_pressed == "update":
            self.on_update_btn_pressed()
        else:
            self.on_delete_btn_pressed()

    def on_update_btn_pressed(self):
        print(f"Update button pressed: {self.toy_item.id}")
        self.app_root.current = "update_screen"
        self.app_root.get_screen("update_screen").ids.u_toy_id.text = str(self.toy_item.id)
        self.app_root.get_screen("update_screen").ids.u_name.text = self.toy_item.name
        self.app_root.get_screen("update_screen").ids.u_description.text = self.toy_item.description
        self.app_root.get_screen("update_screen").ids.u_price.text = str(self.toy_item.price)
        self.app_root.get_screen("update_screen").ids.u_seller.text = self.toy_item.seller
        self.app_root.get_screen("update_screen").ids.u_created.text = self.toy_item.created

    def on_delete_btn_pressed(self):
        print(f"Delete button pressed: {self.toy_item.id}")
        md = MDDialog(
            MDDialogIcon(icon="trash"),
            MDDialogHeadlineText(
                text="Are you sure you want to delete this toy?",
            ),
            MDDialogSupportingText(
                text=f"This will delete {self.toy_item.name} to the database.",
            ),
            MDDialogContentContainer(
                MDDivider(),
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Yeah, I'm sure!",
                        theme_text_color="Custom",
                        text_color=(0, 0, 1, 1)
                    ),
                    style="text",
                    on_release=lambda instance: self.on_yes_btn(instance, md)
                ),
                MDButton(
                    MDButtonText(
                        text="Cancel",
                        theme_text_color="Custom",
                        text_color=(1, 0, 0, 1)
                    ),
                    style="text",
                    on_release=lambda instance: self.on_cancel_btn(instance, md)
                ),
                spacing="10"
            ),
            auto_dismiss=False,
        )

        md.open()

    def on_yes_btn(self, _, dialog):
        res = db.remove_toy_by_id(self.toy_item.id)
        if res:
            dialog.dismiss()
            self.app_root.load_toys()

    def on_cancel_btn(self, _, dialog):
        dialog.dismiss()


class HomeScreen(MDScreen):
    pass


class AddScreen(MDScreen):
    pass


class WindowManager(MDScreenManager):
    pass


class MainApp(MDApp):
    def build(self):
        return Builder.load_file("main.kv")

    def on_start(self):
        self.load_toys()

    def show_date_picker(self, focus):
        if not focus:
            return

        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_ok=self.on_ok, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_ok(self, instance):
        dt = str(instance.get_date()[0])
        self.root.get_screen("add_screen").ids.created.text = dt
        instance.dismiss()

    def on_cancel(self, instance):
        instance.dismiss()

    def add_toy(self):
        name = self.root.get_screen("add_screen").ids.name
        description = self.root.get_screen("add_screen").ids.description
        price = self.root.get_screen("add_screen").ids.price
        seller = self.root.get_screen("add_screen").ids.seller
        created = self.root.get_screen("add_screen").ids.created

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if name.text != "" and description.text != "" and price.text != "" and seller.text != "" and created.text != "":
            payload = {
                "name": name.text,
                "description": description.text,
                "price": price.text,
                "seller": seller.text,
                "created": created.text,
                "updated": today
            }

            res = db.insert_toy(list(payload.values()))

            if res:
                name.text = ""
                description.text = ""
                price.text = ""
                seller.text = ""
                created.text = ""

                self.load_toys()

                self.root.current = "home_screen"

    def update_toy(self):
        toy_id = self.root.get_screen("update_screen").ids.u_toy_id
        name = self.root.get_screen("update_screen").ids.u_name
        description = self.root.get_screen("update_screen").ids.u_description
        price = self.root.get_screen("update_screen").ids.u_price
        seller = self.root.get_screen("update_screen").ids.u_seller
        created = self.root.get_screen("update_screen").ids.u_created

        today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if toy_id.text != "" and name.text != "" and description.text != "" and price.text != "" and seller.text != "" and created.text != "":
            payload = {
                "name": name.text,
                "description": description.text,
                "price": float(price.text),
                "seller": seller.text,
                "created": created.text,
                "updated": today,
                "id": int(toy_id.text),
            }

            # UPDATE QUERY RETURNS A BOOLEAN VALUE
            res = db.update_toy_by_id(list(payload.values()))

            if res:
                toy_id.text = ""
                name.text = ""
                description.text = ""
                price.text = ""
                seller.text = ""
                created.text = ""

                self.load_toys()

                self.root.current = "home_screen"

    def load_toys(self):
        toys = db.select_all_toys()
        container = self.root.get_screen("home_screen").ids.container
        container.clear_widgets()

        if len(toys) > 0:
            for toy in toys:
                row: ToysModel = ToysModel(*toy)
                toy_item = MDListItem(
                    MDListItemLeadingIcon(
                        icon="teddy-bear"
                    ),
                    MDListItemHeadlineText(
                        text=f"Toy Name: {row.name} | ID: {row.id}",
                    ),
                    MDListItemSupportingText(
                        text=f"Description: {row.description}",
                    ),
                    MDListItemTertiaryText(
                        text=f"Price: {row.price} | Seller: {row.seller}",
                    )
                )

                update_btn = CustomIconButton(
                    icon="pencil",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(0, 0, 1, 1),
                    btn_pressed="update",
                    toy_item=row,
                    app_root=self.root
                )

                delete_btn = CustomIconButton(
                    icon="trash-can",
                    style="standard",
                    theme_icon_color="Custom",
                    icon_color=(1, 0, 0, 1),
                    btn_pressed="delete",
                    toy_item=row,
                    app_root=self
                )

                gl = MDGridLayout(
                    cols=2,
                    adaptive_width=True,
                )
                gl.add_widget(update_btn)
                gl.add_widget(delete_btn)
                toy_item.add_widget(gl)
                container.add_widget(toy_item)
        else:
            container.add_widget(
                MDListItem(
                    MDListItemHeadlineText(
                        text="No toys yet to sell. Add one now!"
                    )
                )
            )


if __name__ == '__main__':
    MainApp().run()
