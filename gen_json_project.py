from scripts.main_functions import *

if __name__ == "__main__":
    create(get_base_dir_from_settings(),
           project_generator.get_project_directory_json(get_json("project.json")))
