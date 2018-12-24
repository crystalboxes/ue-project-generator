import module_generator
import plugin_generator
import project_generator
import os
import sys


def create(path, directory):
    print("Creating dir: " + path + directory.name)
    os.mkdir(path + directory.name)
    for file_info in directory.files:
        print("Creating file: " + path +
              directory.name + "/" + file_info.filename)
        file = open(path + directory.name + "/" + file_info.filename, 'w')
        file.write(file_info.src)
        file.close()
    for i_dir in directory.directories:
        create(path + directory.name + "/", i_dir)


def main(args):
    if len(args) < 3:
        return

    name = args[2]
    item_type = args[1]

    directory = None

    if item_type == "project":
        directory = project_generator.get_project_directory(name)
    if item_type == "plugin":
        directory = plugin_generator.get_plugin_directory(name)
    if item_type == "plugin_with_shaders":
        directory = plugin_generator.get_plugin_directory(name, True)
    if item_type == "module":
        directory = module_generator.get_module_directory(name)

    if not directory:
        return

    create("", directory)


if __name__ == "__main__":
    main(sys.argv)
