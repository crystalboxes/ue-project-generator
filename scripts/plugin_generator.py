from scripts import module_generator
from scripts.common import *


def get_uplugin_source(name, is_shader_plugin, modules):
    uplugin_source = ('{\n' +
                      '	"FileVersion": 3,\n' +
                      '	"Version": 1,\n' +
                      '	"VersionName": "1.0",\n' +
                      '	"FriendlyName": "'+name+'",\n' +
                      '	"Description": "",\n' +
                      '	"Category": "Other",\n' +
                      '	"CreatedBy": "crystalboxes",\n' +
                      '	"CreatedByURL": "",\n' +
                      '	"DocsURL": "",\n' +
                      '	"MarketplaceURL": "",\n' +
                      '	"SupportURL": "",\n' +
                      '	"CanContainContent": true,\n' +
                      '	"IsBetaVersion": false,\n' +
                      '	"Installed": false,\n' +
                      '	"Modules": [\n' +
                      '		{\n' +
                      '			"Name": "'+name+'",\n' +
                      '			"Type": "Runtime",\n')

    if is_shader_plugin:
        uplugin_source += '			"LoadingPhase": "PostConfigInit"\n'
    else:
        uplugin_source += '			"LoadingPhase": "Default"\n'
    uplugin_source += '		}'

    for module in modules:
        uplugin_source += ',\n'
        uplugin_source += ('		{\n' +
                           '			"Name": "'+module.name+'",\n' +
                           '			"Type": "Runtime",\n' +
                           '			"LoadingPhase": "Default"\n' +
                           '		}')

    uplugin_source += '\n'
    uplugin_source += ('	]\n' +
                       '}\n')
    return Source(name+".uplugin", uplugin_source)


def get_plugin_directory(name, is_shader_plugin, modules=[]):
    uplugin_source = get_uplugin_source(name, is_shader_plugin, modules)
    modules.append(module_generator.get_module_plugin_directory(
        name, is_shader_plugin))
    directory = Directory(name, [uplugin_source, ], [
        Directory("Content"),
        Directory("Source", [], modules)
    ])
    if is_shader_plugin:
        directory.directories.append(Directory("Shaders"))
    return directory


def get_plugin_directory_json(json_data):
    is_shader_plugin = True
    modules = []
    plugin_name = json_data["name"]
    try:
        is_shader_plugin = json_data["is_shader_plugin"] == "true"
    except:
        pass

    try:
        for module_name in json_data["modules"]:
            modules.append(
                module_generator.get_module_directory(module_name))
    except Exception as e:
        print(e)

    return get_plugin_directory(plugin_name, is_shader_plugin, modules)
