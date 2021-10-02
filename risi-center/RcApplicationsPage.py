# Stack for Applications Page
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcApplicationsFeatured
import RcApplicationsGames
import RcApplicationsCategory
import RcApplicationsSidebar
import RcStackPage

gi.require_version('Gtk', '3.0')
gi.require_version('AppStreamGlib', '1.0')
from gi.repository import Gtk


# This is the stack that is used for the "Applications" tab on the top of the window
class RcApplicationsStack(Gtk.Box):
    def __init__(self, apps):
        Gtk.Box.__init__(self)
        self.stack = Gtk.Stack()

        # I'm adding all the pages recursively using a list.
        self.pages = [
            RcStackPage.RcStackPage(
                RcApplicationsFeatured.RcApplicationsFeatured,
                "featured",
                apps
            ),
            RcStackPage.RcStackPage(
                RcApplicationsGames.RcApplicationsGames,
                "featured_games",
                apps
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "audio_and_video",
                apps,
                "AudioVideo"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "development",
                apps,
                "Development"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "education",
                apps,
                "Education"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "games",
                apps,
                "Game"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "graphics",
                apps,
                "Graphics"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "internet",
                apps,
                "Network"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "productivity",
                apps,
                "Office"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "science",
                apps,
                "Science"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "utility",
                apps,
                "Utility"
            ),
            RcStackPage.RcStackPage(
                RcApplicationsCategory.RcApplicationsCategory,
                "video",
                apps,
                "Video"
            )
        ]

        # Adds each page to the stack
        for page in self.pages:
            self.stack.add(page)

        # Adds sidebar
        self.stack_sidebar = RcApplicationsSidebar.RcApplicationsSidebar(self)
        self.stack.set_visible_child(self.pages[0])

        self.add(RcApplicationsSidebar.RcApplicationsSidebar(self))
        self.add(self.stack)
        self.connect("show", shown)

        # Needed Pages:
        #  Featured Applications
        #  Fun & Games
        #  Categories
        #  Search (on the bottom)
        #  Alternatives (on the bottom)

def shown(widget):
    RcStackPage.generate_widgets(widget.stack, widget.pages)
