from . import recipe

class Recipe(recipe.BaseRecipe):
    def __init__(self, name, archive_path):
        self.path_prefix_trim = "blender-with-libraries"
        self.path_prefix_add  = "blender"
        super().__init__(name, archive_path)
