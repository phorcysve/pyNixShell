"""
plugins/__init__.py - Plugin system for the advanced Python shell.
"""
import os
import importlib
import importlib.util

class PluginBase:
    """Base class for shell plugins."""
    def activate(self, shell):
        """Activate the plugin with the shell context."""
        pass

def load_plugins(shell, plugins_dir='unix/plugins'):
    """Discover and load all plugins in the plugins directory."""
    plugins = []
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)
    for fname in os.listdir(plugins_dir):
        if fname.endswith('.py') and fname != '__init__.py':
            try:
                if plugins_dir == 'unix/plugins':
                    modname = f'unix.plugins.{fname[:-3]}'
                    mod = importlib.import_module(modname)
                else:
                    modname = fname[:-3]
                    spec = importlib.util.spec_from_file_location(modname, os.path.join(plugins_dir, fname))
                    if spec and spec.loader:
                        mod = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(mod)
                    else:
                        raise ImportError(f"Could not load spec for {fname}")
                if hasattr(mod, 'Plugin'):
                    plugin = mod.Plugin()
                    plugin.activate(shell)
                    plugins.append(plugin)
            except Exception as e:
                print(f"Failed to load plugin {fname}: {e}")
    return plugins 