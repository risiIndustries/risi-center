standard_packages = True
flatpaks = True

import gi
import os
import RcUtils

gi.require_version('AppStreamGlib', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import AppStreamGlib, Gtk, GLib, Gio

if flatpaks:
    gi.require_version('Flatpak', '1.0')
    from gi.repository import Flatpak

missing_icon = Gtk.IconTheme.get_default().load_icon(
    "package-x-generic",
    64,
    Gtk.IconLookupFlags.GENERIC_FALLBACK
)

sources = []


class AppSource:
    def __init__(self, **kwargs):
        self.package_type = RcUtils.set_if_key(kwargs, "package_type")
        self.origin = RcUtils.set_if_key(kwargs, "origin")
        self.origin_name = self.origin + " (" + self.package_type + ")"

        sources.append(self)


def get_source_from_origin(origin):
    for source in sources:
        if origin == source.origin:
            return source
    return None


def test_app():
    return App(
        name="Test App",
        comment="This is a test app for testing labels on a stupid project that doesn't work.",
        icon=missing_icon
    )


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


def get_apps():
    apps = {}

    if standard_packages:
        store = AppStreamGlib.Store()
        store.load(AppStreamGlib.StoreLoadFlags.APP_INFO_SYSTEM)
        apps = store_to_dict(store, "dnf", False)
        for key in apps:
            if get_source_from_origin(apps[key].origins[0]) is None:
                AppSource(
                    origin=apps[key].origins[0],
                    package_type="dnf"
                )

    if flatpaks:
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
                        origin=remote.get_name() + " (flatpak)",
                        package_type="flatpak"
                    )
                flatpak_apps = store_to_dict(store, remote, True)
            apps = dict_combine(apps, flatpak_apps)

    # for key in apps:
        # print(key, apps[key].name, [apps[key].package_names, apps[key].package_types, apps[key].origins])

    return apps


def store_to_dict(store, package, is_flatpak):
    apps = {}
    for app in store.get_apps():
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

        if is_flatpak is True:
            origin = package.get_name() + " (flatpak)"
            package_name = app.get_id()
            package_type = "flatpak"
        else:
            if app.get_pkgname_default() is None or app.get_origin() == "":
                continue
            origin = app.get_origin() + " (" + package + ")"
            package_name = app.get_pkgname_default()
            package_type = package

        apps[app.get_id()] = App(
            name=app.get_name(),
            id=app.get_id(),
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

    return apps


def dict_combine(d1, d2):
    for key in d2:
        if key in d1:
            d1[key].package_types.extend(d2[key].package_types)
            d1[key].package_names.extend(d2[key].package_names)
            d1[key].origins.extend(d2[key].origins)
        else:
            d1[key] = d2[key]
    return d1


def category_filter(app, category):
    if category in app.categories:
        return True
    False