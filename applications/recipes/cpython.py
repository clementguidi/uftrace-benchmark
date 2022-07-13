import os

from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        super().__init__(name, archive_path)

        self.build_dir           = "debug"
        self.configure_program   = "../configure"
        self.configure_arguments = ["--with-pydebug", "-C"]
        self.build_program       = "make"
        self.build_arguments     = [f"-j{os.cpu_count()}"]
