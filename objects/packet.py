from .constants import SOURCE_FILE

ERROR_TYPE = 'ERROR_TYPE'
CLOSE_SERVER_TYPE = 'CLOSE_SERVER_TYPE'   # when clients sends Packet to server to close it
SERVER_CLOSED_TYPE = 'SERVER_CLOSED_TYPE' # when server sends Packet back to clients to announce it closed
ID_TYPE = 'ID_TYPE'
ID_STATUS_TYPE = 'ID_STATUS_TYPE'


class Packet:
    def __init__(self, type: str, data: object = None) -> None:
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return f'<{self.type} | data={self.data}>'


if __name__ == '__main__':
    filename = __file__.split('\\')[-1]
    print(f'{filename} {SOURCE_FILE}')