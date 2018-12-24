import module_generator


def get_uplugin_source(name):
    return Source(name+".uplugin", '{\n'+
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
        '			"Type": "Runtime",\n' +
        '			"LoadingPhase": "Default"\n' +
        '		}\n' +
        '	]\n' +
        '}\n')

def get_plugin_directory(name, is_shader_plugin=False):
    return Directory(name, [get_uplugin_source(name), ], [
        Directory("Content"),
        Directory("Source", [], [
          module_generator.get_module_plugin_directory(name, is_shader_plugin)
        ])
    ])
