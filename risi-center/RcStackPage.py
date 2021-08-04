import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class RcStackPage(Gtk.Box):
    def __init__(self, widget, page_id, *args, **kwargs):
        Gtk.Box.__init__(self)
        self.stack_widget = widget
        self.id = page_id
        self.stack_widget_args = args
        self.stack_widget_kwargs = kwargs


def generate_widgets(stack, pages):
    for page in pages:
        if page == stack.get_visible_child():
            page.add(page.widget())
        elif page.get_children() == [] or not page.get_children():
            for child in page.get_children():
                child.destroy()
