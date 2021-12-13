from __future__ import print_function, unicode_literals

import sys

# import inquirer
from PyInquirer import prompt
import os

# import re

from main import main

if __name__ == '__main__':
    working_dir = os.getcwd()

    map_dir = os.path.join(working_dir, 'maps')
    maps = os.listdir(map_dir)
    maps = [m.replace('.txt', '') for m in maps]

    agent_dir = os.path.join(working_dir, 'agents')
    agents = os.listdir(agent_dir)
    agents = [a.replace('.png', '') for a in agents if a[0].isupper()]

    questions = [
        {
            'type': 'list',
            'message': 'Select map to use',
            'name': 'map',
            'choices': maps,
        }, {
            'type': 'list',
            'message': 'Select agent to use',
            'name': 'agent',
            'choices': agents
        }, {
            'type': 'input',
            'message': 'Thinking time',
            'default': '1',
            'name': 'time',
            'validate': lambda x: int(x) >= 1
        }, {
            'type': 'input',
            'message': 'Max depth level',
            'default': '-1',
            'name': 'lvl',
            'validate': lambda x: int(x) >= -1
        }
    ]

    ans = prompt(questions)
    print(ans)

    # questions = [
    #     # inquirer.List(name='map', message='Select map to use', choices=maps),
    #     # inquirer.List(name='agent', message='Select agent to use', choices=agents),
    #     inquirer.Text(name='time_to_think', message='Enter think time', validate=lambda _, x: re.match('[0-9]+', x),
    #                   default=1),
    #     inquirer.Text(name='max_lvl', message='Enter max depth level', validate=lambda _, x: re.match('[-]?[0-9]+', x),
    #                   default=-1)
    # ]
    #
    # ans = inquirer.prompt(questions)
    # print(ans)

    sys.argv.append(os.path.join(map_dir, ans.get('map') + '.txt'))
    sys.argv.append(ans.get('agent'))
    sys.argv.append(ans.get('time'))
    sys.argv.append(ans.get('lvl'))

    main()
