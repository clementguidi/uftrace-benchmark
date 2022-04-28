from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        self.path_prefix_add  = "lxc-"
        super().__init__(name, archive_path)
