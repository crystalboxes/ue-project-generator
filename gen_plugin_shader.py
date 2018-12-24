from scripts.main_functions import *

if __name__ == "__main__":
    name = input("Plugin (with shaders) name: ")
    create(get_base_dir_from_settings(),
           plugin_generator.get_plugin_directory(name, True))
