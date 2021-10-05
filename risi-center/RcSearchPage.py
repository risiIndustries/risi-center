# Featured Search Page in Applications Tab
# Licensed Under GPL3
# By PizzaLovingNerd

import threading
import random
import time
import gi
import RcBaseWidgets
import RcApps

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk
from gi.repository import GLib

# This is used for the category pages in risiSoftware Center
class RcSearchpage(Gtk.ScrolledWindow):
    def __init__(self, apps, category, **kwargs):
        Gtk.ScrolledWindow.__init__(self)

        self.apps = apps
        self.category = category
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC) # Scrolls down
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.centered_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.centered_box.set_margin_top(30)
        self.centered_box.set_margin_bottom(30)
        self.centered_box.set_margin_start(30)
        self.centered_box.set_margin_end(30)

        # This is where the items are stored.
        self.listview = RcBaseWidgets.ListView(
            None # This is set to none because we are adding the apps async with load_apps()
        )

        self.centered_box.add(self.listview)
        self.box.set_center_widget(self.centered_box)
        self.add(self.box)

    def load_apps(self): # Function loads up thread
        apps = dict(
            filter(lambda app: self.category in app[1].categories, self.apps.items())
        ) # Finds apps that match the category for the page.

        thread = threading.Thread(target=self.app_thread, args=[apps])
        thread.daemon = True
        thread.start()

    def app_thread(self, apps): # The thread for loading apps to prevent freezing.
        for app in apps:
            GLib.idle_add(self.add_app, app, apps)
            time.sleep(0.001) # Sleep prevents GTK from trying to load all the apps at once

        del(self.apps)

    def add_app(self, app, apps): # Function needed for Glib.idle
        self.listview.add_app(apps, app)
