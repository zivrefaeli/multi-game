class Type:
    ERROR = 'error'
    CLOSE_SERVER = 'close_server'   # when clients sends Packet to server to close it
    SERVER_CLOSED = 'server_closed' # when server sends Packet back to clients to announce it closed
    SEND_ID = 'send_id'
    ID_STATUS = 'id_status'
    DISCONNECT = 'disconnect'
    FULL_SERVER = 'full_server'


class Packet:
    def __init__(self, type: str, data = None) -> None:
        self.type = type
        self.data = data

    def __str__(self) -> str:
        return f'<{self.type} | data={self.data}>'