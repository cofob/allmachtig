import os


def add(name):
    with open('env.sh', 'a') as file:
        file.write(f'export {name}="'+input(name+': ')+'"\n')


with open('env.sh', 'w') as file:
    file.write('#!/bin/bash\n')

add('API_ID')
add('API_HASH')
add('SECRET')
add('CHAT')
add('TOKEN')

os.system('chmod u+x env.sh')
