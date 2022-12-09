import sys
sys.path.append('..')
from client import cmain
from server import smain

FILE_NAME = __file__.split('\\')[-1]
VALID_COMMANDS = ['s', 'server', 'c', 'client']
COMMAND_START = '-'


def main() -> None:
    length = len(sys.argv)

    if length <= 1:
        print(f'Usage: python {FILE_NAME} -<command>')
    elif length > 2:
        print('Expected only one command')
    if length != 2:
        print('Valid commands are:', ', '.join(VALID_COMMANDS))
        return

    command = sys.argv[1].lower()
    if command[0] != COMMAND_START or command[1:] not in VALID_COMMANDS:
        print(f'{sys.argv[1]} is an invalid command')
        return
    
    if VALID_COMMANDS[0] in command:
        smain()
    else:
        cmain()


if __name__ == '__main__':
    main()