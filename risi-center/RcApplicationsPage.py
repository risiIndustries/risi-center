# Stack for Applications Page
# Licensed Under GPL3
# By PizzaLovingNerd

import gi

import RcApplicationsFeatured
import RcApplicationsGames
import RcApplicationsCategories
import RcApplicationsSidebar
import RcStackPage

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk

class RcApplicationsStack(Gtk.Box):
    def __init__(self, apps):
        Gtk.Box.__init__(self)
        self.stack = Gtk.Stack()

        self.pages = [
            RcStackPage.RcStackPage(
                RcApplicationsFeatured.RcApplicationsFeatured,
                "featured",
                apps
            ),
            RcStackPage.RcStackPage(
                RcApplicationsGames.RcApplicationsGames,
                "games",
                apps
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategories.RcApplicationsCategories,
                "categories",
                apps
            )
        ]

        for page in self.pages:
            self.stack.add_named(page, page.id)

        self.stack.set_hexpand(True)
        self.stack.set_vexpand(True)
        self.stack_sidebar = RcApplicationsSidebar.RcApplicationsSidebar(self)
        self.stack.set_visible_child_name("featured")
        print(self.stack.get_visible_child_name())
        RcStackPage.generate_widgets(self.stack, self.pages)
        self.add(RcApplicationsSidebar.RcApplicationsSidebar(self))
        self.add(self.stack)

        # Needed Pages:
        #  Featured Applications
        #  Fun & Games
        #  Categories
        #  Search (on the bottom)
        #  Alternatives (on the bottom)