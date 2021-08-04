# Loads up main window
# Licensed Under GPL3
# By PizzaLovingNerd

import RcApps
import RcApplicationsPage
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk


# Launches main window of risiTweaks
class RcMainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="Risi Center")
        self.apps = RcApps.get_apps()
        self.set_default_size(-1, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("io.risi.center")

        # Creating the Header Bar and the 2 views for the window.
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.set_titlebar(self.header)

        # Back Button
        self.back_button = Gtk.Button()
        self.back_button.set_image(Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.BUTTON))
        self.back_button.set_relief(Gtk.ReliefStyle.NONE)
        self.back_button.get_style_context().add_class("circular")
        self.back_button.connect("clicked", self.go_back)
        self.header.add(self.back_button)

        # Window Stacks
        self.window_stack = Gtk.Stack()
        self.navigation_stack = Gtk.Stack()
        self.app_screen_page = Gtk.Box()
        self.window_stack.add_named(self.navigation_stack, "navigation")
        self.window_stack.add_named(self.app_screen_page, "app_screen")
        self.header.set_custom_title(Gtk.StackSwitcher(stack=self.navigation_stack))

        # Application Stack
        self.application_stack = RcApplicationsPage.RcApplicationsStack(self.apps)
        self.navigation_stack.add_titled(self.application_stack, "applications", "Applications")

        self.add(self.window_stack)

    def go_back(self, button):
        pass

    def check_back(self, button):
        pass

    def load_app_page(self, app):
        pass