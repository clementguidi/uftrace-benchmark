import os

from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        self.path_prefix_trim = "v"
        self.path_prefix_add  = "git-"
        super().__init__(name, archive_path)

        self.conf_dir     = "."
        self.build_dir    = "."
        self.preconf_prog = "autoreconf"
        self.config_prog  = "./configure"
        self.config_args  = ["--prefix=/usr/local", "-C"]
        self.build_prog   = "make"
        self.build_args   = [f"-j{os.cpu_count()}"]
