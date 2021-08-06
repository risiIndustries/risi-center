# Featured Categories Page in Applications Tab
# Licensed Under GPL3
# By PizzaLovingNerd

import random
import gi
import RcBaseWidgets
import RcApps

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk

test_apps = {
    "app1": RcApps.test_app(),
    "app2": RcApps.test_app(),
    "app3": RcApps.test_app(),
    "app4": RcApps.test_app()
}


class RcApplicationsCategory(Gtk.ScrolledWindow):
    def __init__(self, apps, category, **kwargs):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.set_hexpand(True)
        self.set_vexpand(True)

        apps = dict(
            filter(lambda app: category in app[1].categories, apps.items())
        )
        self.items = RcBaseWidgets.ListView(
            dict(
                random.sample(
                    list(apps.items()),
                    len(apps)
                )
            )
        )
        self.items.set_margin_top(30)
        self.items.set_margin_bottom(30)
        self.items.set_margin_start(30)
        self.items.set_margin_end(30)

        self.center_box.add(self.items)
        self.box.set_center_widget(self.center_box)
        self.add(self.box)
