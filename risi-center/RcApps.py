# This file is used for managing listed apps
# Licensed Under GPL3
# By PizzaLovingNerd

# Temporary
standard_packages = True
flatpaks = True

import gi
import os
import RcUtils

gi.require_version('AppStreamGlib', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import AppStreamGlib, Gtk, GLib, Gio

# Only imports the flatpak library if "flatpaks" variable is set to true.
if flatpaks:
    gi.require_version('Flatpak', '1.0')
    from gi.repository import Flatpak

# Missing icon for packages.
missing_icon = Gtk.IconTheme.get_default().load_icon(
    "package-x-generic",
    64,
    Gtk.IconLookupFlags.GENERIC_FALLBACK
)

sources = []

# These are the commands a VTE will call when a action for a package is ran
class SourceCommands:
    def __init__(self):
        self.install = []
        self.remove = []
        self.upgrade = []
        self.upgrade_all = []

# This is used to setup new sources that apps may come from.
class AppSource:
    def __init__(self, **kwargs):
        self.queue = []
        self.package_type = RcUtils.set_if_key(kwargs, "package_type")
        self.origin = RcUtils.set_if_key(kwargs, "origin")
        self.origin_name = self.origin + " (" + self.package_type + ")"
        self.commands = get_source_commands(package_type=self.package_type, origin=self.origin)

        sources.append(self)

# Gets the source commands and returns them depending on the package manager.
def get_source_commands(*args, **kwargs):
    if RcUtils.set_if_key(kwargs, "package_type") == "dnf":
        commands = SourceCommands()
        commands.install = ["dnf", "install"]
        commands.remove = ["dnf", "remove"]
        commands.upgrade = ["dnf", "upgrade"]
        commands.upgrade_all = ["dnf", "upgrade"]
    elif RcUtils.set_if_key(kwargs, "package_type") == "flatpak":
        commands = SourceCommands()
        commands.install = ["flatpak", "install", RcUtils.set_if_key(kwargs, "origin")]
        commands.remove = ["flatpak", "uninstall"]
        commands.upgrade = ["flatpak", "update"]
        commands.upgrade_all = ["flatpak", "update"]

# Gets the source from origin (repo name)
def get_source_from_origin(origin):
    for source in sources:
        if origin == source.origin:
            return source
    return None


# Temporary, this is a test app used for testing the homepage
def test_app():
    return App(
        name="test_app",
        appid="com.test.app",
        package_name=["test", "test"],
        package_type=["dnf", "flatpak"],
        description="This is the description of my test app",
        comment="This is a comment",

        icon=Gtk.IconTheme.get_default().load_icon(
            "package-x-generic",
            64,
            Gtk.IconLookupFlags.GENERIC_FALLBACK
        ),

        origin=["archlinux-arch-core", "archlinux-arch-extra"]
    )


# This is a class that is used to define apps.
class App:
    def __init__(self, **kwargs):
        self.name = RcUtils.set_if_key(kwargs, "name")
        self.description = RcUtils.set_if_key(kwargs, "description")
        self.package_types = RcUtils.set_if_key(kwargs, "package_type")
        self.package_names = RcUtils.set_if_key(kwargs, "package_name")
        self.origins = RcUtils.set_if_key(kwargs, "origin")
        self.comment = RcUtils.set_if_key(kwargs, "comment")
        self.desktop = RcUtils.set_if_key(kwargs, "desktop")
        self.categories = RcUtils.set_if_key(kwargs, "categories")
        self.developer = RcUtils.set_if_key(kwargs, "developer")
        self.icon = RcUtils.set_if_key(kwargs, "icon")
        self.screenshots = RcUtils.set_if_key(kwargs, "screenshots")
        self.app_license = RcUtils.set_if_key(kwargs, "app_license")
        self.mimetypes = RcUtils.set_if_key(kwargs, "mimetypes")
        self.keywords = RcUtils.set_if_key(kwargs, "keywords")
        self.kind = RcUtils.set_if_key(kwargs, "kind")
        self.homepage = RcUtils.set_if_key(kwargs, "homepage")
        self.donation_page = RcUtils.set_if_key(kwargs, "donation_page")
        # source info needs package managers, package names, and source names


# This grabs the apps from AppStream
def get_apps():
    apps = {}

    if standard_packages:
        store = AppStreamGlib.Store()
        store.load(AppStreamGlib.StoreLoadFlags.APP_INFO_SYSTEM)

        # Converts a AppStream store to a dictionary.
        # This is used because of the fact that web apps won't share AppStream metadata.
        apps = store_to_dict(store, "dnf", False)

        # Checks to make sure that every repo has it's own app origin.
        for key in apps:
            if get_source_from_origin(apps[key].origins[0]) is None:
                AppSource(
                    origin=apps[key].origins[0],
                    package_type="dnf"
                )

    if flatpaks:
        flatpak_apps = []

        # Flatpaks aren't stored in the standard AppStream store
        # so it has to load custom ones from Flatpak appstream directories
        for remote in Flatpak.Installation.new_system(None).list_remotes():
            store = AppStreamGlib.Store()
            remote_path = remote.get_appstream_dir("x86_64").get_path()
            if os.path.exists(remote_path):
                for file in sorted(os.listdir(remote_path)):
                    if file.endswith(".xml") or file.endswith(".xml.gz") or \
                            file.endswith(".yml") or file.endswith(".yaml") or \
                            file.endswith(".yml.gz") or file.endswith(".yaml.gz"):
                        store.from_file(
                            Gio.File.new_for_path(remote_path + "/" + file)
                        )
                    AppSource(
                        origin=remote.get_name(),
                        package_type="flatpak"
                    )
                flatpak_apps = store_to_dict(store, remote, True)

            # This combines the dnf apps with the flatpak_apps in the
            # and makes sure that it combines the AppSource info.
            apps = dict_combine(apps, flatpak_apps)

    return apps


def store_to_dict(store, package, is_flatpak):
    apps = {}
    for app in store.get_apps():

        # Uses the app missing icon if there's no icon
        if app.get_icon_for_size(64, 64) is None:
            app_icon = missing_icon
        else:
            try:
                app.get_icon_for_size(64, 64).load(
                    AppStreamGlib.IconLoadFlags.SEARCH_SIZE
                )
                app_icon = app.get_icon_for_size(64, 64).get_pixbuf()
            except GLib.Error:
                app_icon = missing_icon

        # I can't remember how this code works and I'm worried it may cause a bug in the future.
        if is_flatpak is True:
            origin = package.get_name()
            package_name = app.get_id()
            package_type = "flatpak"
        else:
            if app.get_pkgname_default() is None or app.get_origin() == "": # Checks if app has DNF package
                continue
            origin = app.get_origin()
            package_name = app.get_pkgname_default()
            package_type = package

        # Sets all the info for an App class
        apps[app.get_id()] = App(
            name=app.get_name(),
            appid=app.get_id(),
            package_name=[package_name],
            package_type=[package_type],
            description=app.get_description(),
            comment=app.get_comment(),
            desktops=app.get_compulsory_for_desktops(),
            categories=app.get_categories(),
            developer=app.get_developer_name(),
            icon=app_icon,
            screenshots=app.get_screenshots(),
            app_license=app.get_project_license(),
            mimetypes=app.get_mimetypes(),
            keywords=app.get_keywords(),
            kind=app.get_kind(),
            origin=[origin],
            homepage=app.get_url_item(AppStreamGlib.UrlKind.HOMEPAGE),
            donation_page=app.get_url_item(AppStreamGlib.UrlKind.DONATION),
        )

    # Returns a dictionary full of apps.
    return apps


# Combines dictionaries and makes sure that apps with multiple packages has more than one.
def dict_combine(d1, d2):
    for key in d2:
        if key in d1:
            d1[key].package_types.extend(d2[key].package_types)
            d1[key].package_names.extend(d2[key].package_names)
            d1[key].origins.extend(d2[key].origins)
        else:
            d1[key] = d2[key]
    return d1

# Checks if apps are in a category (Can be moved to category page class)
def category_filter(app, category):
    if category in app.categories:
        return True
    False
