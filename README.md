# instance_script
 These script add support to c4d's instance function, which makes the scene with many instances more light weight.
## Installation
Option 1: copy the .py file to `C4D_installation_path\library\scripts`<br>
Option 2: make a environment variable named `C4D_SCRIPTS_DIR`, and points it to the path of your downloaded script folder<br>

The script is tested on C4D R26.107 and 2024.1, other versions may work.

## Change list
### v1.0.0
Features in initial release.<br>
1. Convert_to_Instance: Convert selected objects to instances, the last selected object (highlighted one) is the source object.
2. Pure_Instance: Convert selected object to instance, and move the source object to a null object for centralized management.
3. Convert_to_Multi_Instance: Convert selected objects to multi-instance (without the source object).
4. Instance_to_Cloner: Convert multi-instance to cloner.
5. Move_Source_Object: Move the source object to top of document without breaking the link of instance.