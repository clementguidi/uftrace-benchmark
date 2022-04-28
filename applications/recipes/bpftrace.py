import os

from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        self.path_prefix_trim = "v"
        self.path_prefix_add  = "bpftrace-"
        super().__init__(name, archive_path)

        build_dir           = "build"
        configure_program   = "cmake"
        configure_arguments = ["-DCMAKE_BUILD_TYPE=Debug",
                               ".."]
        build_program       = "make"
        build_arguments     = [f"-j{os.cpu_count()}"]
