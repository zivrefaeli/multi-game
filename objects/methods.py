from socket import socket
from math import degrees, atan
from random import randint
from pickle import loads, dumps
from .packet import Packet, Type


class Methods:
    @staticmethod
    def get_angle_by_delta(dx: float, dy: float) -> int:
        if dy == 0:
            if dx >= 0:
                return 0
            return 180
        
        if dx == 0:
            if dy > 0:
                return 90
            return 270
        
        alpha = int(degrees(atan(dy / dx)))
        if dx > 0:
            if dy > 0:
                return alpha
            return 360 + alpha
        return 180 + alpha

    @staticmethod
    def random_color() -> tuple:
        return randint(0, 255), randint(0, 255), randint(0, 255)


class App:
    BUFFER = 1024 # 1KB

    @staticmethod
    def send(socket: socket, packet: Packet) -> None:
        try:
            socket.send(dumps(packet))
        except Exception as e:
            print(f'Exception: {e} ({type(e).__name__})')

    @staticmethod
    def receive(socket: socket) -> Packet:
        try:
            message = b''
            while True:
                data = socket.recv(App.BUFFER)
                message += data
                if len(data) < App.BUFFER:
                    break
            return loads(message)
        except Exception as e:
            print(f'Exception: {e} ({type(e).__name__})')
            return Packet(Type.ERROR)


class Validate:
    VALID = 'valid'
    MESSAGE = 'message'

    @staticmethod
    def ip(ip: str) -> dict:
        result = {Validate.VALID: False, Validate.MESSAGE: ''}

        if len(ip) == 0:
            result[Validate.MESSAGE] = 'Enter IP address'
            return result

        if ip.count('.') != 3:
            result[Validate.MESSAGE] = 'IP address should contain 3 dots'
            return result

        sections = ip.split('.')
        for section in sections:
            if len(section) == 0:
                result[Validate.MESSAGE] = 'Empty IP section'
                return result
            
            if not section.isnumeric():
                result[Validate.MESSAGE] = 'IP section should contain only digits'
                return result

            value = int(section)
            if value < 0 or value > 255:
                result[Validate.MESSAGE] = 'IP section should be in range [0, 255]'
                return result

        result[Validate.VALID] = True
        return result

    @staticmethod
    def port(port: str) -> dict:
        length = len(port)
        result = {Validate.VALID: False, Validate.MESSAGE: ''}

        if length == 0:
            result[Validate.MESSAGE] = 'Enter port'
            return result

        if length < 4 or length > 5:
            result[Validate.MESSAGE] = 'Port length should be in range [4, 5]'
            return result

        if not port.isnumeric():
            result[Validate.MESSAGE] = 'Port should contain only digits'
            return result
        
        result[Validate.VALID] = True
        return result

    @staticmethod
    def id(id: str) -> dict:
        result = {Validate.VALID: False, Validate.MESSAGE: ''}

        if len(id) < 3:
            result[Validate.MESSAGE] = 'Id name should be at least 3 characters'
            return result

        result[Validate.VALID] = True
        return result