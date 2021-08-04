# All of the commonly used widgets we need for risiCenter are in this file.
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcUtils

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango, AppStreamGlib


class ListView(Gtk.FlowBox):
    def __init__(self, apps):
        Gtk.FlowBox.__init__(self)
        self.set_max_children_per_line(2)
        self.set_min_children_per_line(1)
        self.set_homogeneous(True)
        for app in apps:
            frame = Gtk.Frame()
            frame.get_style_context().add_class('view')
            frame.add(ListApp(apps[app]))
            frame.set_size_request(350, -1)
            self.add(frame)


class ListApp(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self)
        self.add(Gtk.Image.new_from_pixbuf(app.icon))
        self.label_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.label_box.set_margin_start(5)
        self.title = Gtk.Label(xalign=0)
        self.title.set_max_width_chars(30)
        self.title.set_label(app.name)
        self.title.get_style_context().add_class('heading')
        self.title.set_ellipsize(Pango.EllipsizeMode.END)
        self.label_box.add(self.title)
        if app.comment is not None:
            self.comment = Gtk.Label(xalign=0)
            self.comment.get_style_context().add_class('dim-label')
            self.comment.set_line_wrap(True)
            self.comment.set_lines(1)
            self.comment.set_max_width_chars(80)
            self.comment.set_label(
                RcUtils.one_line_wrap(
                    AppStreamGlib.markup_convert(
                        app.comment,
                        AppStreamGlib.MarkupConvertFormat.SIMPLE
                    ), 80
                ),

                # app.comment

                # textwrap.shorten(
                #     app.comment,
                #     80,
                #     placeholder="..."
                # )
            )
            self.comment.set_ellipsize(Pango.EllipsizeMode.END)
            self.label_box.add(self.comment)
        self.add(self.label_box)


class GridView(Gtk.ScrolledWindow):
    def __init__(self, apps):
        Gtk.ScrolledWindow.__init__(self)
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.NEVER)
        self.box = Gtk.Box()
        self.box.set_spacing(10)
        for app in apps:
            self.box.add(GridApp(apps[app]))
        self.add(self.box)


class GridApp(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.icon = Gtk.Image.new_from_pixbuf(app.icon)
        self.icon.set_margin_start(10)
        self.icon.set_margin_end(10)
        self.add(self.icon)
        self.title = Gtk.Label(label=app.name)
        self.title.set_ellipsize(Pango.EllipsizeMode.END)
        self.title.get_style_context().add_class('heading')
        self.title.set_line_wrap(True)
        self.add(self.title)


class Featured(Gtk.Box):
    def __init__(self, label, apps):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        self.label = Gtk.Label(label="Editor's Choice", xalign=0)
        self.label.set_margin_start(10)
        self.label.set_markup("<big><b>" + label + "</b></big>")
        self.grid = GridView(apps)
        self.add(self.label)
        self.add(self.grid)


class ListBoxLabel(Gtk.Label):
    def __init__(self, text):
        Gtk.Label.__init__(self, label=text, xalign=0)
        self.set_margin_start(26)
        self.set_margin_end(26)
        self.set_margin_top(10)
        self.set_margin_bottom(10)


class ListBoxLabelWithIcon(Gtk.Box):
    def __init__(self, text, icon):
        Gtk.Box.__init__(self)

        self.icon = Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.MENU)
        self.icon.set_margin_end(5)
        self.label = Gtk.Label(label=text, xalign=0)
        self.add(self.icon)
        self.add(self.label)

        self.set_margin_start(5)
        self.set_margin_end(5)
        self.set_margin_top(10)
        self.set_margin_bottom(10)


class category_button(Gtk.Button):
    def __init__(self, category, category_name):
        self.category = category
        self.category_name = category_name
        Gtk.Button.__init__(self, label=self.category_name)