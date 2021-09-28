import gi
import RcApps
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class RcInstallationScreen(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.add(Top(app))

class Top(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.left = TopLeft(app)
        self.right = TopRight(app)
        self.left.set_halign(Gtk.Align.START)
        self.add(self.left)
        self.add(self.right)


class TopLeft(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.image = Gtk.Image.new_from_pixbuf(app.icon)
        # self.image.set_margin_start(0)
        self.image.set_margin_end(3)
        self.add(self.image)
        self.add(NameAndDescription(app.name, app.comment))
        self.set_halign(Gtk.Align.FILL)
        self.set_hexpand(True)

class NameAndDescription(Gtk.Box):
    def __init__(self, name, comment):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.name = Gtk.Label(label=name, xalign=0)
        self.name.set_markup("<b>" + name + "</b>")
        self.add(self.name)
        self.add(Gtk.Label(label=comment, xalign=0))
        self.set_valign(Gtk.Align.CENTER)
        # self.set_halign(Gtk.Align.EXPAND)

class TopRight(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.combobox = Gtk.ComboBoxText()

        for origin in app.origins:
            print(origin)
            self.combobox.append_text(
                RcApps.get_source_from_origin(origin).origin_name
            )

        self.combobox.set_active(0)

        self.button = Gtk.Button(label="Install")
        self.button.set_margin_end(5)

        self.add(self.combobox)
        self.add(self.button)
        self.set_valign(Gtk.Align.CENTER)
