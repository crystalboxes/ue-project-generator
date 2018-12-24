from scripts.main_functions import *

if __name__ == "__main__":
    name = input("Module name: ")
    create(get_base_dir_from_settings(),
           module_generator.get_module_directory(name))
