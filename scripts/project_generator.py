from scripts.common import *
from scripts import module_generator
from scripts import plugin_generator

ENGINE_VERSION = "4.23"

def get_uproject_source(name, modules):
    # todo expose engine version into settings
    uproject_source = ('{\n' +
                       '	"FileVersion": 3,\n' +
                       '	"EngineAssociation": "' + ENGINE_VERSION + '",\n' +
                       '	"Category": "",\n' +
                       '	"Description": "",\n' +
                       '	"Modules": [\n')

    uproject_source += ('		{\n' +
                        '			"Name": "'+name+'",\n' +
                        '			"Type": "Runtime",\n' +
                        '			"LoadingPhase": "Default"\n' +
                        '		}')

    for module in modules:
        uproject_source += ',\n'
        uproject_source += ('		 {\n' +
                            '			"Name": "'+module.name+'",\n' +
                            '			"Type": "Runtime",\n' +
                            '			"LoadingPhase": "Default"\n' +
                            '		 }')

    uproject_source += ('\n    ]\n' + '}\n')

    return Source(name+".uproject", uproject_source)


def get_source_directory(name, modules=[]):
    module_dir = module_generator.get_module_directory(
        name, False, is_primary=True, dependencies=[module.name for module in modules])
    module_dir.files.extend([
        Source(name+"GameModeBase.h", '#pragma once\n' +
               '#include "CoreMinimal.h"\n' +
               '#include "GameFramework/GameModeBase.h"\n' +
               '//\n' +
               '#include "'+name+'GameModeBase.generated.h"\n' +
               'UCLASS()\n' +
               'class '+name.upper()+'_API A'+name+'GameModeBase : public AGameModeBase\n' +
               '{\n' +
               '	GENERATED_BODY()\n' +
               '};\n'),
        Source(name+"GameModeBase.cpp", '#include "'+name+'GameModeBase.h"\n'),
    ])
    modules.append(module_dir)
    return Directory("Source", [
        Source(name+".Target.cs", 'using UnrealBuildTool;\n' +
               'using System.Collections.Generic;\n' +
               'public class '+name+'Target : TargetRules\n' +
               '{\n' +
               '	public '+name+'Target(TargetInfo Target) : base(Target)\n' +
               '	{\n' +
               '		Type = TargetType.Game;\n' +
               '		ExtraModuleNames.AddRange( new string[] { "'+name+'" } );\n' +
               '	}\n' +
               '}\n'),
        Source(name+'Editor.Target.cs', 'using UnrealBuildTool;\n' +
               'using System.Collections.Generic;\n' +
               'public class '+name+'EditorTarget : TargetRules\n' +
               '{\n' +
               '	public '+name+'EditorTarget(TargetInfo Target) : base(Target)\n' +
               '	{\n' +
               '		Type = TargetType.Editor;\n' +
               '		ExtraModuleNames.AddRange( new string[] { "'+name+'" } );\n' +
               '	}\n' +
               '}\n')
    ], modules)


def get_project_directory(name, modules=[], plugins=[]):
    uproject_source = get_uproject_source(name, modules)
    return Directory(name, [uproject_source, ], [
        Directory("Config"),
        Directory("Content"),
        Directory("Plugins", [], plugins),
        get_source_directory(name, modules)
    ])


def get_modules(items):
    modules = []
    for module_name in items:
        modules.append(module_generator.get_module_directory(module_name))
    return modules


def get_plugins(items, is_shader_plugin):
    plugins = []
    for plugin_item in items:
        if not isinstance(plugin_item, dict):
            plugins.append(
                plugin_generator.get_plugin_directory(plugin_item, is_shader_plugin, []))
        else:
            plugins.append(
                plugin_generator.get_plugin_directory_json(plugin_item))
    return plugins


def get_project_directory_json(json_data):
    modules = []
    project_name = json_data["name"]
    plugins = []
    print("PARSING MODULES")
    try:
        modules.extend(get_modules(json_data["modules"]))
    except Exception as e:
        print(e)

    print("PARSING PLUGINS")
    try:
        plugins.extend(get_plugins(json_data["plugins"], False))
    except Exception as e:
        print(e)

    print("PARSING SHADER PLUGINS")
    try:
        plugins.extend(get_plugins(json_data["shader_plugins"], True))
    except Exception as e:
        print(e)
    return get_project_directory(project_name, modules, plugins)
