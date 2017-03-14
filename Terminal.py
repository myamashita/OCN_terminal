import sublime
import sublime_plugin
import os
import sys
import subprocess
import locale

if os.name == 'nt':
    try:
        import _winreg
    except (ImportError):
        import winreg as _winreg
    from ctypes import windll, create_unicode_buffer

class NotFoundError(Exception):
    pass


if sys.version_info >= (3,):
    installed_dir, _ = __name__.split('.')
else:
    installed_dir = os.path.basename(os.getcwd())

def get_setting(key, default=None):
    settings = sublime.load_settings('Terminal.sublime-settings')
    os_specific_settings = {}
    return os_specific_settings.get(key, settings.get(key, default))


class TerminalSelector():
    default = None

    @staticmethod
    def get():
        package_dir = os.path.join(sublime.packages_path(), installed_dir)
        terminal = get_setting('terminal')
        if terminal:
            dir, executable = os.path.split(terminal)
            return terminal

        if TerminalSelector.default:
            return TerminalSelector.default

        default = None

        if os.name == 'nt':
            default = os.environ['SYSTEMROOT'] + '\\System32\\cmd.exe'
        TerminalSelector.default = default
        return default

class TerminalCommand():
    def get_path(self, paths):
        if paths:
            return paths[0]
        # DEV: On ST3, there is always an active view.
        #   Be sure to check that it's a file with a path (not temporary view)
        elif self.window.active_view() and self.window.active_view().file_name():
            return self.window.active_view().file_name()
        elif self.window.folders():
            return self.window.folders()[0]
        else:
            sublime.error_message('Terminal: No place to open terminal to')
            return False

    def run_terminal(self, dir_, parameters):
        try:
            if not dir_:
                raise NotFoundError('The file open in the selected view has ' +
                    'not yet been saved')
            for k, v in enumerate(parameters):
                parameters[k] = v.replace('%CWD%', dir_)
            args = [TerminalSelector.get()]
            args.extend(parameters)

            encoding = locale.getpreferredencoding(do_setlocale=True)
            if sys.version_info >= (3,):
                cwd = dir_
            else:
                cwd = dir_.encode(encoding)
            # Copy over environment settings onto parent environment
            env_setting = get_setting('env', {})
            env = os.environ.copy()
            for k in env_setting:
                if env_setting[k] is None:
                    env.pop(k, None)
                else:
                    env[k] = env_setting[k]

            # Normalize environment settings for ST2
            # https://github.com/wbond/sublime_terminal/issues/154
            # http://stackoverflow.com/a/4987414
            for k in env:
                if not isinstance(env[k], str):
                    if isinstance(env[k], unicode):
                        env[k] = env[k].encode('utf8')
                    else:
                        print('Unsupported environment variable type. Expected "str" or "unicode"', env[k])
            # Run our process
            subprocess.Popen(args, cwd=cwd, env=env)

        except (OSError) as exception:
            print(str(exception))
            sublime.error_message('Terminal: The terminal ' +
                TerminalSelector.get() + ' was not found')
        except (Exception) as exception:
            sublime.error_message('Terminal: ' + str(exception))


class OpenTerminalCommand(sublime_plugin.WindowCommand, TerminalCommand):
    def run(self, paths=[], parameters=None):
        path = self.get_path(paths)
        if not path:
            return

        if parameters is None:
            parameters = get_setting('parameters', [])

        if os.path.isfile(path):
            path = os.path.dirname(path)

        self.run_terminal(path, parameters)
        print(parameters)

