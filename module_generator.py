from common import *


def get_csharp_source(module_name):
    return Source(module_name + '.Build.cs', 'using UnrealBuildTool;\n' +
                  'public class ' + module_name + ' : ModuleRules\n' +
                  '{\n' +
                  'public ' + module_name + '(ReadOnlyTargetRules Target) : base(Target)\n' +
                  '{\n' +
                  'PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;\n' +
                  'PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore" });\n' +
                  'PrivateDependencyModuleNames.AddRange(new string[] {  });\n' +
                  '}\n' +
                  '}\n')


def get_module_h_source(module_name):
    return Source(module_name + '.h', '#pragma once\n' +
                  '#include "CoreMinimal.h"\n')


def get_module_cpp_source(module_name):
    return Source(module_name + '.cpp', '#include "'+module_name+'.h"\n' +
                  '#include "Modules/ModuleManager.h"\n' +
                  'IMPLEMENT_PRIMARY_GAME_MODULE( FDefaultGameModuleImpl, '+module_name+', "'+module_name+'" );\n')


def get_module_directory(name, use_private_public_dirs=True):
    if use_private_public_dirs:
        return Directory(name, [
            get_csharp_source(name),
        ], [
            Directory("Private", [
                get_module_cpp_source(name),
            ]),
            Directory("Public", [
                get_module_h_source(name),
            ])
        ])
    return Directory(name, [
        get_csharp_source(name),
        get_module_cpp_source(name),
        get_module_h_source(name),
    ])


def get_csharp_source_shaders(name):
    return Source(module_name + '.Build.cs', 'using System.IO;\n' +
                  'namespace UnrealBuildTool.Rules\n' +
                  '{\n' +
                  '    public class '+name+' : ModuleRules\n' +
                  '    {\n' +
                  '        public '+name+'(ReadOnlyTargetRules Target) : base(Target)\n' +
                  '        {\n' +
                  '            PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;\n' +
                  '            var pluginName = Path.GetFileName(PluginDirectory);\n' +
                  '            var shadersFullPath = Path.Combine(PluginDirectory, "Shaders").Replace("\\", "/");\n' +
                  '            var shadersVirtualPath = "/Plugin/" + pluginName;\n' +
                  '            PublicDefinitions.Add(System.String.Format("'+name.upper()+'_SHADERS_FULL_PATH=\"{0}\"", shadersFullPath));\n' +
                  '            PublicDefinitions.Add(System.String.Format("'+name.upper()+'_SHADERS_VIRTUAL_PATH=\"{0}\"", shadersVirtualPath));\n' +
                  '\n' +
                  '            PublicDependencyModuleNames.AddRange(\n' +
                  '              new string[]\n' +
                  '                {"Core","CoreUObject","Engine","RenderCore","ShaderCore","RHI","GraphicsTools" }\n' +
                  '            );\n' +
                  '        }\n' +
                  '    }\n' +
                  '}\n')


def get_module_cpp_source_shaders(name):
    return Source(module_name + '.cpp', '#include "CoreMinimal.h"\n' +
                  '#include "Modules/ModuleManager.h"\n' +
                  '#include "Runtime/ShaderCore/Public/ShaderCore.h"\n' +
                  '\n' +
                  'class F'+name+'Module : public IModuleInterface {\n' +
                  'public:\n' +
                  '  virtual void StartupModule() override;\n' +
                  '  virtual void ShutdownModule() override;\n' +
                  '};\n' +
                  '\n' +
                  '#define PATH_AS_STRING(x) #x\n' +
                  'void F'+name+'Module::StartupModule() {\n' +
                  '  AddShaderSourceDirectoryMapping('+name.upper()+'_SHADERS_VIRTUAL_PATH, '+name.upper()+'_SHADERS_FULL_PATH);\n' +
                  '}\n' +
                  '\n' +
                  'void F'+name+'Module::ShutdownModule() {}\n' +
                  'IMPLEMENT_MODULE(F'+name+'Module, '+name+')\n')


def get_module_plugin_directory(name, add_shader_folder=True):
    csharp_source = ""
    if not add_shader_folder:
        csharp_source = get_csharp_source(name)
    else:
        get_csharp_source_shaders(name)

    cpp_source = ""
    if not add_shader_folder:
        cpp_source = get_module_cpp_source(name)
    else:
        cpp_source = get_module_cpp_source_shaders(name)

    return Directory(name, [
        csharp_source,
    ], [
        Directory("Private", [
            cpp_source,
        ]),
        Directory("Public", [
            get_module_h_source(name),
        ])
    ])
