# This is the screen you get with info about the app when you click on an app.
# This app is coded in different parts with a Top(Left/Right) and Bottom
# Licensed Under GPL3
# By PizzaLovingNerd

import gi
import RcApps
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class RcInstallationScreen(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.set_margin_top(10)
        self.set_margin_right(10)
        self.set_margin_left(10)
        self.add(Top(app))

# Top part which combines the TopLeft and TopRight
class Top(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        self.left = TopLeft(app)
        self.right = TopRight(app)
        self.left.set_halign(Gtk.Align.START)
        self.add(self.left)
        self.add(self.right)

# Top Left with the Name, Description, and Icon for an app.
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

# Vertical Name and Description
class NameAndDescription(Gtk.Box):
    def __init__(self, name, comment):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)
        self.name = Gtk.Label(label=name, xalign=0)
        self.name.set_markup("<b>" + name + "</b>")
        self.add(self.name)
        self.add(Gtk.Label(label=comment, xalign=0))
        self.set_valign(Gtk.Align.CENTER)
        # self.set_halign(Gtk.Align.EXPAND)

# Top Right with Install Button and Package Sources.
class TopRight(Gtk.Box):
    def __init__(self, app):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)

        # Creates dropdown for package sources and adds sources to the dropdown.
        self.combobox = Gtk.ComboBoxText()
        for origin in app.origins:
            self.combobox.append_text(
                RcApps.get_source_from_origin(origin).origin_name
            )
        self.combobox.set_active(0)

        # Install button
        self.button = Gtk.Button(label="Install")
        self.button.set_margin_end(5)

        self.add(self.combobox)
        self.add(self.button)
        self.set_valign(Gtk.Align.CENTER) # Makes sure the button and combo box isn't thicc.
