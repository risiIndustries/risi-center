# Main file, loads up main window class
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcMainWindow

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Loads up main window
class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="io.risi.center"
        )
        self.window = None

    def do_activate(self):  # Checks if window is already open before starting a new one
        if not self.window:
            self.window = RcMainWindow.RcMainWindow(self)
            self.add_window(self.window)
            self.window.show_all()
        self.window.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = Application()
    app.run()
