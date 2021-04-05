import subprocess
import os

p = subprocess.Popen(
       'git show'.split(),
       stdout=subprocess.PIPE
)
commit = '\n'.join(p.stdout.read().decode().split('\n')[:3])
author_url = 'https://cdn.discordapp.com/avatars/420925923349495808/f65379464bfd12821bec3dc0293eaa29.png'
debug = os.environ.get('DEBUG', False)
