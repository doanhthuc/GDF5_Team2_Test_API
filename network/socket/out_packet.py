from network.socket.packet_header_analyze import *


class OutPacket:

    def __init__(self):
        self.__capacity = None
        self.__data = None
        self.__controller_id = 1  # default controller id
        self.__cmd_id = None
        self.__is_packed_header = False
        self.__length = None
        self.__pos = None

    def init_data(self, capacity):
        self.__capacity = capacity
        self.__pos = 0
        self.__data = bytearray(0)

    def get_data(self):
        return self.__data

    def set_controller_id(self, controller_id):
        self.__controller_id = controller_id

    def set_cmd_id(self, cmd_id):
        self.__cmd_id = cmd_id

    def pack_header(self):
        if self.__is_packed_header:
            return

        self.__is_packed_header = True
        header = gen_header(False, False)
        self.put_byte(header)
        self.put_unsigned_short(self.__length)
        self.put_byte(self.__controller_id)
        self.put_short(self.__cmd_id)

    def put_data(self):
        pass

    def update_size(self):
        size = len(self.__data) - 3
        self.__data[INDEX_SIZE_PACKET] = size >> 8
        self.__data[INDEX_SIZE_PACKET + 1] = (size & 255) >> 0

    def put_byte(self, b):
        self.__data.append(b)
        self.__pos = self.__pos + 1
        self.__length = self.__pos

    def put_unsigned_short(self, v):
        self.put_byte(v >> 8)
        self.put_byte(v >> 0)

    def put_short(self, v):
        self.put_byte((v >> 8) & 0xFF)
        self.put_byte((v >> 0) & 0xFF)

    def put_bytes(self, byte_array, size):
        for i in range(size):
            self.put_byte(byte_array[i])

    def put_byte_array(self, byte_array, size):
        self.put_short(size)
        self.put_bytes(byte_array, size)

    def put_string(self, i_str):
        b = bytearray(i_str.encode())
        self.put_byte_array(b, len(b))

    def put_int(self, v):
        self.put_byte((v >> 24) & 0xff)
        self.put_byte((v >> 16) & 0xff)
        self.put_byte((v >> 8) & 0xff)
        self.put_byte((v >> 0) & 0xff)

    def put_long(self, v):
        self.put_byte((v >> 56) & 0xff)
        self.put_byte((v >> 48) & 0xff)
        self.put_byte((v >> 40) & 0xff)
        self.put_byte((v >> 32) & 0xff)
        self.put_byte((v >> 24) & 0xff)
        self.put_byte((v >> 16) & 0xff)
        self.put_byte((v >> 8) & 0xff)
        self.put_byte((v >> 0) & 0xff)
