from scripts.main_functions import *

if __name__ == "__main__":
    create(get_base_dir_from_settings(),
           plugin_generator.get_plugin_directory_json(get_json("plugin.json")))
           