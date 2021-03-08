import xonsh


__all__ = ()


with ${...}.swap(UPDATE_OS_ENVIRON=True):
    execx($(zoxide init xonsh), 'exec', __xonsh__.ctx, filename='zoxide')
