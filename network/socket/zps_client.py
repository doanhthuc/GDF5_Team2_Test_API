from logging import NullHandler
import socket
import threading
import json
import time

from cmd import Cmd
from common.logger import logger

from network.socket.out_packet import OutPacket
from network.socket.in_packet import InPacket
from network.socket.raw_packet import RawPacket
from network.socket.packet_header_analyze import *

from modules.connection.connection_send import *

# HOST = "127.0.0.1"
PORT = 10072
HOST = "120.138.65.108"
# PORT = 10072

class ZPSClient(Cmd):
    prompt = ''
    intro = ''

    def __init__(self):
        super().__init__()

        #AF_INET: domain, [AF_IPX, AF_IOS, AF_NS]
        #SOCKET_STREAM: type, [SOCK_DGRAM: udp, SOCK_STREAM: tcp]
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None
        self.__isLogin = False
        self.__is_connected = False

        self.__module_registered = []

        self.__sessionToken =""

    def __receive_message_thread(self):
        while self.__is_connected:
            #try:
            raw_data = self.__read_data()
            if (raw_data is None):
                continue

            cmd_id = get_cmd_id_from_data(raw_data.get_data())
            #logger.info("zps_client::__receive_message_thread receive CMD ID: {}".format(cmd_id))

            #in_packet = InPacket()
            #in_packet.init(raw_data)
            #print("check error {}".format(in_packet.get_error()))
            #in_packet.read_data()

            # for all module
            for module in self.__module_registered:
               if module.is_in_range_listener(cmd_id):
                   module.on_listener(cmd_id, raw_data)
                   break

            #logger.info("zps_client::__receive_message_thread - receive done")
            #except Exception as e:
            #    logger.error("zps_client::__receive_message_thread - error")

    def add_module(self, modules):
        self.__module_registered.append(modules)

    def __send_message_thread(self, message):
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())

    def __read_data(self):
        buffer_size = 1024
        buffer = self.__socket.recv(buffer_size)

        if (len(buffer) <= 0):
            return None

        valid_size = get_valid_size(buffer, buffer_size)
        if valid_size < 0 or valid_size > buffer_size:
            logger.error("zps_client::__read_data - error read data")
            return

        raw_packet = RawPacket()
        raw_packet.process(buffer, buffer_size)

        return raw_packet

    def start(self):
        logger.info("gsn_client::start")

        #try:
        self.__socket.connect((HOST, PORT))
        self.__is_connected = True
        #self.cmdloop() # for run command line, user input

        # # create thread listener
        thread = threading.Thread(target=self.__receive_message_thread)
        thread.daemon = True
        thread.start()
        #except Exception as e:
        #   logger.error("something's wrong with %s:%d. Exception is %s" % (HOST, PORT, e))
        #finally:
        #    self.__is_connected = False
        #    self.__socket.close()

    def do_send(self, args):
        print("[gsn_client]::[do_send] - OK")
        message = args
        print('[' + str(self.__nickname) + '(' + str(self.__id) + ')' + ']', message)

        thread = threading.Thread(target=self.__send_message_thread, args=(message,))
        thread.daemon = True
        thread.start()

    def do_logout(self, args=None):
        self.__socket.send(json.dumps({
            'type': 'logout',
            'sender_id': self.__id
        }).encode())
        self.__isLogin = False
        return True

    def send_data(self, data):
        self.__socket.send(data)

    def get_session_token(self):
        return self.__sessionToken

    def send(self, pk):
        if self.__is_connected:
            pk.pack_header()
            pk.put_data()
            pk.update_size()

            self.__socket.send(pk.get_data())
            #time.sleep(0.5)
        else:
            logger.error("client is not connected")
