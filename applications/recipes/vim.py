from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        self.path_prefix_trim = "v"
        self.path_prefix_add  = "vim-"
        super().__init__(name, archive_path)
