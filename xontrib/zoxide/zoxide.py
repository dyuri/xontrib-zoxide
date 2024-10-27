import subprocess
import sys, os
import hashlib
from xonsh.built_ins	import XSH
from pathlib        	import Path

_cache_name	= "zoxide_init_cache.py"

__all__ = ()

def _cache_zoxide_init(zoxide_init, z_cache_path):
  if not (z_cache_name := z_cache_path.name) == _cache_name:
    print(f"xontrib-zoxide: error: cache file should be '{_cache_name}', got {z_cache_name}")
    return
  print("xontrib-zoxide: creating a zoxide init cache file too speed up subsequent loads")
  with z_cache_path.open('wb') as f:
    f.write(zoxide_init)

def  _initZoxide():
  if cache_home := os.environ.get("XDG_CACHE_HOME"):
    z_cache_path = Path(cache_home).expanduser() / "zoxide" / _cache_name
    z_cache_path.parent.mkdir(exist_ok=True, parents=True)
  else:
    z_cache_path	= Path(os.path.dirname(__file__)).parent / _cache_name
  sys.path.append(str(z_cache_path.parent))

  zoxide_init_proc	= subprocess.run(["zoxide",'init','xonsh'],capture_output=True)
  zoxide_init     	= zoxide_init_proc.stdout
  zoxide_init_err 	= zoxide_init_proc.stderr

  if zoxide_init_err:
    print("xontrib-zoxide:error: 'zoxide init xonsh' failed with:")
    print(zoxide_init_err.decode())
    return

  if not z_cache_path.exists(): # Cache & Load (slow)
    _cache_zoxide_init(zoxide_init, z_cache_path)
    execx(zoxide_init.decode(), 'exec', XSH.ctx, filename='zoxide')
  else:                               # Hash & Load
    hash_init  = hashlib.md5(     zoxide_init         ).hexdigest()
    hash_cache = hashlib.md5(z_cache_path.read_bytes()).hexdigest()

    if hash_init == hash_cache:       # Load fast from cache
      import zoxide_init_cache
    else:                             # Cache & Load (slow)
      _cache_zoxide_init(zoxide_init, z_cache_path)
      execx(zoxide_init.decode(), 'exec', XSH.ctx, filename='zoxide')
