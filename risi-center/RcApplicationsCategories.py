# Featured Categories Page in Applications Tab
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcBaseWidgets

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk

import RcApps

categories = [
    ["Audio", "Audio"],
    ["Internet", "Network"],
    ["Video", "Video"],
    ["Development", "Development"],
    ["Education", "Education"],
    ["Games", "Games"],
    ["Graphics", "Graphics"],
    ["Network", "Network"],
    ["Productivity", "Office"],
    ["Science", "Science"],
    ["Utility", "Utility"]
]

test_apps = {
    "app1": RcApps.test_app(),
    "app2": RcApps.test_app(),
    "app3": RcApps.test_app(),
    "app4": RcApps.test_app()
}


class RcApplicationsCategories(Gtk.ScrolledWindow):
    def __init__(self, apps):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.center_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_hexpand(True)
        self.flowbox.set_vexpand(False)
        self.flowbox.set_homogeneous(True)
        self.flowbox.set_margin_start(5)
        self.flowbox.set_margin_end(5)
        self.flowbox.set_margin_bottom(20)
        for category in categories:
            button = RcBaseWidgets.category_button(category[1], category[0])
            button.set_margin_start(5)
            button.set_margin_end(5)
            button.set_margin_top(10)
            button.set_margin_bottom(0)
            self.flowbox.add(button)
        self.center_box.add(self.flowbox)
        self.center_box.add(RcBaseWidgets.ListView(test_apps))
        self.box.set_center_widget(self.center_box)
        self.add(self.box)
