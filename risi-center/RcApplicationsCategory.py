# Featured Categories Page in Applications Tab
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcBaseWidgets

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk

import RcApps

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
        # self.flow_box = Gtk.FlowBox()
        # self.flow_box.set_hexpand(True)
        # self.flow_box.set_vexpand(False)
        # self.flow_box.set_homogeneous(True)
        # self.flow_box.set_margin_start(5)
        # self.flow_box.set_margin_end(5)
        # self.flow_box.set_margin_bottom(20)
        # for category in categories:
        #     button = RcBaseWidgets.category_button(category[1], category[0])
        #     button.set_margin_start(5)
        #     button.set_margin_end(5)
        #     button.set_margin_top(10)
        #     button.set_margin_bottom(0)
        #     self.flow_box.add(button)
        # self.center_box.add(self.flow_box)

        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_hexpand(True)
        self.set_vexpand(True)

        self.items = RcBaseWidgets.ListView(RcApps.check_apps_for_category(apps, category))
        self.items.set_margin_top(10)
        self.items.set_margin_bottom(10)

        self.center_box.add(self.items)
        self.box.set_center_widget(self.center_box)
        self.add(self.box)
