import os

from flask import current_app, url_for

from CTFd.utils import _get_asset_json
from CTFd.utils.config import ctf_theme
from CTFd.utils.helpers import markup


class _AssetsWrapper:
    def manifest(self):
        theme = ctf_theme()
        manifest = os.path.join(
            current_app.root_path, "themes", theme, "static", "manifest.json"
        )
        return _get_asset_json(path=manifest)

    def manifest_css(self):
        theme = ctf_theme()
        manifest = os.path.join(
            current_app.root_path, "themes", theme, "static", "manifest-css.json"
        )
        return _get_asset_json(path=manifest)

    def js(self, asset_key):
        asset = self.manifest()[asset_key]
        entry = asset["file"]
        imports = asset.get("imports", [])
        html = ""
        for i in imports:
            # TODO: Needs a better recursive solution
            i = self.manifest()[i]["file"]
            url = url_for("views.themes_beta", path=i)
            html += f'<script defer type="module" src="{url}"></script>'
        url = url_for("views.themes_beta", path=entry)
        html += f'<script defer type="module" src="{url}"></script>'
        return markup(html)

    def css(self, asset_key):
        asset = self.manifest_css()[asset_key]
        entry = asset["file"]
        url = url_for("views.themes_beta", path=entry)
        return markup(f'<link rel="stylesheet" href="{url}">')

    def file(self, asset_key):
        asset = self.manifest()[asset_key]
        entry = asset["file"]
        return url_for("views.themes_beta", path=entry)


Assets = _AssetsWrapper()
