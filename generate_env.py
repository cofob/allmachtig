import os


def add(name):
    with open('env.sh', 'a') as file:
        file.write(f'export {name}="'+input(name+': ')+'"\n')


with open('env.sh', 'w') as file:
    file.write('#!/bin/bash\n')
    file.write(f'export LANG=en\n')
    file.write(f'export LOCALE=en\n')

add('API_ID')
add('API_HASH')
add('SECRET')
add('CHAT')
add('TOKEN')
add('PREFIX')

os.system('chmod u+x env.sh')
