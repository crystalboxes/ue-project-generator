# Unreal Engine 4 Project Generator

Python scripts for generating Unreal Engine (4.21) C++ projects and plugins.

## Usage

Make sure you have [Python](https://www.python.org/) installed. 

### gen_project.py, gen_plugin.py, gen_plugin_shader.py, gen_module.py

This script will create an empty C++ project/plugin or module with the specified name. `gen_plugin_shader.py` generates a plugin with a custom **Global Shader** path specified. Useful for working on [custom shaders](https://www.unrealengine.com/en-US/tech-blog/how-to-add-global-shaders-to-ue4). 

### gen_json_project.py

Uses a special `.json` description to generate a project/plugin. Edit `project.json` or `plugin.json` before running those scripts.

#### project.json Example

```javascript
{
  "name": "NameOfYourProject",
  "modules": [
    "ModuleOne",
    "ModuleTwo"
  ],
  "plugins": [
    "PluginName", 
    {                           // Can be a plugin  
      "name": "PluginNameTwo",  // with modules inside.
      "modules": [
        "PluginModuleA",
        "PluginModuleB"
      ]
    }
  ],
  "shader_plugins": [           // Plugins with a custom 
    "TestShaderPlugin"          // "Shaders" folder
  ]
}
```
