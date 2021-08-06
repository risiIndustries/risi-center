import gi

import RcBaseWidgets
import RcStackPage

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

categories = [
    ["Audio and Video", "AudioVideo"],
    ["Development", "Development"],
    ["Education", "Education"],
    ["Games", "Games"],
    ["Graphics", "Graphics"],
    ["Internet", "Network"],
    ["Productivity", "Office"],
    ["Science", "Science"],
    ["Utility", "Utility"],
]


class RcApplicationsSidebar(Gtk.ScrolledWindow):
    def __init__(self, stack):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.stack = stack
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)
        self.get_style_context().add_class("sidebar")

        self.top_list_case = {
            0: self.stack_page_featured,
            1: self.stack_page_games,
            2: self.reveal_category
        }
        self.category_case = {}
        self.bottom_list_case = {}

        self.top_list = Gtk.ListBox()
        self.top_list.add(RcBaseWidgets.ListBoxLabel("Featured Applications"))
        self.top_list.add(RcBaseWidgets.ListBoxLabel("Fun & Games"))
        self.categories = Gtk.ListBoxRow()
        self.categories.add(RcBaseWidgets.ListBoxLabelWithIcon("Categories", "pan-end-symbolic"))
        self.categories.set_selectable(False)
        self.top_list.add(self.categories)
        #self.top_list.set_vexpand(True)
        self.top_list.connect("row_activated", self.top_listbox_clicked)
        self.box.add(self.top_list)

        self.category_revealer = Gtk.Revealer()
        self.category_revealer.set_transition_type(Gtk.RevealerTransitionType.NONE)
        self.category_list = Gtk.ListBox()
        for category in categories:
            self.category_case[(len(self.category_case))] = category
            self.category_list.add(RcBaseWidgets.ListBoxLabel("   " + category[0]))
        self.category_revealer.add(self.category_list)
        self.category_list.connect("row_activated", self.category_clicked)
        self.category_list.unselect_all()
        self.box.add(self.category_revealer)

        self.bottom_list = Gtk.ListBox()
        self.bottom_list.add(RcBaseWidgets.ListBoxLabel("Alternatives"))
        self.bottom_list.add(RcBaseWidgets.ListBoxLabel("Search"))
        self.bottom_list.set_vexpand(True)
        self.bottom_list.set_valign(Gtk.Align.END)
        self.bottom_list.connect("row_activated", self.bottom_listbox_clicked)
        self.box.add(self.bottom_list)

    def top_listbox_clicked(self, listbox, listbox_row):
        self.top_list_case[listbox_row.get_index()]()
        self.category_list.unselect_all()
        self.bottom_list.unselect_all()

    def category_clicked(self, listbox, listbox_row):
        self.top_list.unselect_all()
        self.bottom_list.unselect_all()
        RcStackPage.set_child(
            self.stack.stack,
            self.stack.pages,
            categories[listbox_row.get_index()][0].lower().replace(" ", "_")
        )
        # print(categories[listbox_row.get_index()][0])

    def bottom_listbox_clicked(self, listbox, listbox_row):
        self.top_list.unselect_all()
        self.category_list.unselect_all()

    def reveal_category(self):
        self.category_revealer.set_reveal_child(not self.category_revealer.get_reveal_child())

    def stack_page_featured(self):
        RcStackPage.set_child(self.stack.stack, self.stack.pages, "featured")

    def stack_page_games(self):
        RcStackPage.set_child(self.stack.stack, self.stack.pages, "featured_games")


def change_stack(stack, page):
    pass