import sys
sys.path.append('..')
from client import cmain
from server import smain

FILE_NAME = __file__.split('\\')[-1]
VALID_COMMANDS = ['s', 'server', 'c', 'client']
VALID_STARTS = ['--', '-', '']


def main() -> None:
    length = len(sys.argv)

    if length <= 1:
        print(f'Usage: python ./{FILE_NAME} <command>')
    if length > 2:
        print('Expected only one command')
    if length != 2:
        print('Valid commands are:', ', '.join(VALID_COMMANDS))
        return

    command = sys.argv[1].lower()
    valid = False
    
    for start in VALID_STARTS:
        if command.startswith(start):
            valid = command[len(start):] in VALID_COMMANDS
            break
    
    if not valid:
        print(f'{sys.argv[1]} is an invalid command')
        return
    
    if VALID_COMMANDS[0] in command:
        smain()
    else:
        cmain()


if __name__ == '__main__':
    main()