# Featured Applications Page in Applications Tab
# Licensed Under GPL3
# By PizzaLovingNerd

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


class RcApplicationsFeatured(Gtk.ScrolledWindow):
    def __init__(self, apps):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box.set_margin_start(30)
        self.box.set_margin_top(30)
        self.box.set_margin_bottom(30)
        self.box.set_spacing(20)
        self.box.add(RcBaseWidgets.Featured("Editor's Choice", test_apps))
        self.box.add(RcBaseWidgets.Featured("Used By The risiOS Team", test_apps))

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.add(self.box)
