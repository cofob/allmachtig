import subprocess
import os

p = subprocess.Popen(
    'git show'.split(),
    stdout=subprocess.PIPE
)
commit = '\n'.join(p.stdout.read().decode().split('\n')[:3])
author_url = 'https://i.imgur.com/jGec7RB.jpg'
debug = os.environ.get('DEBUG', False)

colors = {
    'black':      0x000000,
    'white':      0xffffff,
    'red':        0xff0000,
    'green':      0x00ff00,
    'blue':       0x0000ff,
    'yellow':     0xffff00,
    'brown':      0xa52a2a,
    'pink':       0xffc0cb,
    'cyan':       0x00ffff,
    'grey':       0x808080,
    'darkgrey':   0x202225,
}

# для команды set
# типы проверок: minmax, None
settings = {
    'schema': {
        'delete_error_messages': {
            'min': 0,
            'max': 30,
            'check_type': 'minmax',
            'type': int,
            'default': 10
        },
        'error_on_non_existent_command': {
            'min': 0,
            'max': 1,
            'check_type': 'minmax',
            'type': int,
            'default': 1
        }
    }
}

base_settings = {
    'user': {
        'delete_error_messages': 10,
        'error_on_non_existent_command': 0
    }
}

base_user_settings = {
    'rank_color': '000000'
}

settings_schema_default = {
    'check_type': None,
    'type': int,
    'default': 0
}

# применяем дефолтные настройки для схем
for i in list(settings['schema']):
    t = settings_schema_default | settings['schema'][i]
    settings['schema'][i] = t
