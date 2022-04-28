import os
import importlib

from utils import *


class Builder():
    apps = {}
    recipes = {}

    def __init__(self, app_dir):
        self.source_dir = f"{app_dir}/source"
        self.recipe_dir = f"{app_dir}/recipes"
        self.app_list   = f"{app_dir}/apps.csv"
        self.import_url_list()

    def import_url_list(self):
        with open(self.app_list, "r") as file:
            for line in file:
                line = line.strip("\n")
                fields = line.split(",")
                name = fields[0]
                url = fields[1]
                self.apps[name] = url

    def import_recipes(self):
        for name in self.apps:
            try:
                module = importlib.import_module(f"recipes.{name}")
            except ImportError as err:
                print(f"Recipe not found: {err}")
                continue
            url = self.apps[name]
            file_name = os.path.basename(url)
            archive_path = f"{self.source_dir}/{file_name}"
            self.recipes[name] = module.Recipe(name, archive_path)

    def download(self, name, safe=True):
        url = self.apps[name]
        if safe:
            filename = url_parse_filename(url)
            path = f"{self.source_dir}/{filename}"
            if os.path.exists(path):
                return
        http_get(url)
        print(f"GET {url} to {path}")

    def download_all(self, safe=False):
        for name in self.apps:
            self.download(name, safe)

    def download_all_safe(self):
        self.download_all(True)

    def unpack(self, name, safe=True):
        recipe = self.recipes[name]
        recipe.unpack(safe)

    def unpack_all(self, safe=False):
        for name in self.recipes:
            self.unpack(name, safe)

    def unpack_all_safe(self):
        self.unpack_all(True)

    def preconfigure(self, name):
        recipe = self.recipes[name]
        recipe.preconfigure()

    def preconfigure_all(self):
        for name in self.apps:
            self.preconfigure(name)

    def configure(self, name):
        recipe = self.recipes[name]
        recipe.configure()

    def configure_all(self):
        for name in self.apps:
            self.configure(name)

    def build(self, name):
        recipe = self.recipes[name]
        recipe.build()

    def build_all(self):
        for name in self.apps:
            self.build(name)
