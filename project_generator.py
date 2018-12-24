from common import *
import module_generator


def get_uproject_source(name):
    return Source(name+".uproject", '{\n' +
                  '	"FileVersion": 3,\n' +
                  '	"EngineAssociation": "4.21",\n' +
                  '	"Category": "",\n' +
                  '	"Description": "",\n' +
                  '	"Modules": [\n' +
                  '		{\n' +
                  '			"Name": "'+name+'",\n' +
                  '			"Type": "Runtime",\n' +
                  '			"LoadingPhase": "Default"\n' +
                  '		}\n' +
                  '	]\n' +
                  '}\n')


def get_source_directory(name):
    module_dir = module_generator.get_module_directory(name, False)
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
    ], [module_dir, ])


def get_project_directory(name):
    return Directory(name, [get_uproject_source(name), ], [
        Directory("Config"),
        Directory("Content"),
        Directory("Plugins"),
        get_source_directory(name)
    ])
