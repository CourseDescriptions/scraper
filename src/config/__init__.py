import os
import importlib
import pkgutil

SITES = {}

package_name = "config"
package = importlib.import_module(package_name)
package_path = os.path.dirname(package.__file__)

for _, module_name, _ in pkgutil.iter_modules([package_path]):
        module = importlib.import_module(f"{package_name}.{module_name}")
        
        # Call get_config() to get the dictionary
        if hasattr(module, "get_config"):
            config_data = module.get_config()

            if config_data:
                # print(f"CONFIG DATA FOR {module_name}: {type(config_data)}")
                SITES[module_name] = config_data