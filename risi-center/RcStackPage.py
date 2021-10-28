# Used to unload stack pages for memory management
# Licensed Under GPL3
# By PizzaLovingNerd

import gi, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import RcApplicationsCategory


class RcStackPage(Gtk.Box):
    def __init__(self, widget, page_id, *args, **kwargs):
        Gtk.Box.__init__(self)
        self.stack_widget = widget
        self.id = page_id
        self.stack_widget_args = args
        self.stack_widget_kwargs = kwargs


def generate_widgets(stack, pages):
    for page in pages:
        for child in page.get_children():
            child.destroy()
        if page == stack.get_visible_child():
            widget = page.stack_widget(*page.stack_widget_args, **page.stack_widget_kwargs)
            page.add(widget)
            widget.show_all()
            if hasattr(widget, "load_page"):
                widget.load_page()


def get_page_by_id(pages, page_id):
    for page in pages:
        if page_id == page.id:
            return page
    return None


def set_child(stack, pages, page_id):
    stack.set_visible_child(get_page_by_id(pages, page_id))
    generate_widgets(stack, pages)
