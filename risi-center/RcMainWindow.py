# Loads up main window
# Licensed Under GPL3
# By PizzaLovingNerd

import RcApps
import RcApplicationsPage
import RcInstallationScreen
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk


# Launches main window of risiTweaks
class RcMainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app, title="risiCenter")
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
        self.window_stack.add(self.navigation_stack)
        self.window_stack.add(self.app_screen_page)
        self.header.set_custom_title(Gtk.StackSwitcher(stack=self.navigation_stack))

        # Application Stack
        self.application_stack = RcApplicationsPage.RcApplicationsStack(self.apps)
        self.navigation_stack.add_titled(self.application_stack, "applications", "Applications")

        self.add(self.window_stack)
        self.back_button.set_sensitive(False)

    def go_back(self, button): # Gos back to previous page.
        self.window_stack.set_visible_child(self.navigation_stack)
        button.set_sensitive(self.check_back())

    def check_back(self): # Checks if the back button should be active.
        return not self.window_stack.get_visible_child() == self.navigation_stack

    def load_app_page(self, app): # Loads an RcInstallationScreen page.
        self.app_screen_page.destroy()
        self.app_screen_page = Gtk.Box()
        self.app_screen_page.add(RcInstallationScreen.RcInstallationScreen(app))
        self.app_screen_page.show_all()

        self.window_stack.add(self.app_screen_page)
        self.window_stack.set_visible_child(self.app_screen_page)
        self.back_button.set_sensitive(self.check_back())
