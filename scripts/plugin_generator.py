from scripts import module_generator
from scripts.common import *


def get_uplugin_source(name, is_shader_plugin):
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
    uplugin_source += ('		}\n' +
                       '	]\n' +
                       '}\n')
    return Source(name+".uplugin", uplugin_source)


def get_plugin_directory(name, is_shader_plugin=False):
    directory = Directory(name, [get_uplugin_source(name, is_shader_plugin), ], [
        Directory("Content"),
        Directory("Source", [], [
            module_generator.get_module_plugin_directory(
                name, is_shader_plugin)
        ])
    ])
    if is_shader_plugin:
        directory.directories.append(Directory("Shaders"))
    return directory
