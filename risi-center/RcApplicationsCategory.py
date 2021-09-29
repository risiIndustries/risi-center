# Featured Categories Page in Applications Tab
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

test_apps = {
    "app1": RcApps.test_app(),
    "app2": RcApps.test_app(),
    "app3": RcApps.test_app(),
    "app4": RcApps.test_app()
}


class RcApplicationsCategory(Gtk.ScrolledWindow):
    def __init__(self, apps, category, **kwargs):
        Gtk.ScrolledWindow.__init__(self)
        self.apps = apps
        self.category = category
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.items = Gtk.Box()
        self.items.set_margin_top(30)
        self.items.set_margin_bottom(30)
        self.items.set_margin_start(30)
        self.items.set_margin_end(30)

        self.listview = RcBaseWidgets.ListView(
            None
        )

        self.center_box.add(self.items)
        self.box.set_center_widget(self.center_box)
        self.add(self.box)

    def load_apps(self):
        apps = dict(
            filter(lambda app: self.category in app[1].categories, self.apps.items())
        )

        self.items.add(self.listview)

        thread = threading.Thread(target=self.app_thread, args=[apps])
        thread.daemon = True
        thread.start()

        del(self.apps)

    def app_thread(self, apps):
        for app in apps:
            GLib.idle_add(self.add_app, app, apps)
            time.sleep(0.01)

    def add_app(self, app, apps):
        self.listview.add_app(apps, app)
