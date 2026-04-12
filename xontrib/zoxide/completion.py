_zoxide_z_prefix = 'z#'


def _init_zoxide_completion():
    """Set up z command completion with two modes:

    - ``z <TAB>`` or ``z foo<TAB>`` completes directories (like cd)
    - ``z foo <TAB>`` launches zoxide interactive selection
    """
    import subprocess
    import sys

    from xonsh.built_ins import XSH
    from xonsh.completers.tools import contextual_command_completer_for, RichCompletion
    from xonsh.completers.path import complete_dir
    from xonsh.completers._aliases import add_one_completer

    # Wrap the z alias to handle the special prefix argument
    # added by interactive completion
    z_orig = XSH.aliases['z']

    def zoxide_z_with_completion_trick(args):
        if args and args[-1].startswith(_zoxide_z_prefix):
            return z_orig([args[-1][len(_zoxide_z_prefix):]])
        return z_orig(args)

    XSH.aliases['z'] = zoxide_z_with_completion_trick

    def zoxide_fn(name):
        """Look up a zoxide helper function regardless of how the init was loaded.

        When zoxide init was loaded from cache (import zoxide_init_cache), the
        functions live in that module. When loaded via execx, they live in XSH.ctx.
        """
        mod = sys.modules.get('zoxide_init_cache')
        if mod is not None:
            return getattr(mod, name)
        return XSH.ctx[name]

    @contextual_command_completer_for('z')
    def _zoxide_complete_z(command):
        if command.suffix:
            return None
        if command.arg_index == 1:
            return complete_dir(command)
        if command.prefix != '':
            return None

        query = [arg.value for arg in command.args[1:]]
        if query and query[-1].startswith(_zoxide_z_prefix):
            return None

        result = subprocess.run(
            [zoxide_fn('__zoxide_bin')(), 'query', '--exclude', zoxide_fn('__zoxide_pwd')(), '--interactive', '--', *query],
            check=False,
            env=zoxide_fn('__zoxide_env')(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        selected = result.stdout.rstrip('\n')
        if result.returncode != 0 or not selected:
            return set()

        return {RichCompletion(f'{_zoxide_z_prefix}{selected}/')}

    add_one_completer('z', _zoxide_complete_z, 'start')
