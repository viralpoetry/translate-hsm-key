#!/usr/bin/python
import socket
from struct import *


class HSM(object):
    def __init__(self, ip, port, buffer_size=1024):
        self.ip = ip
        self.port = int(port)
        self.buffer_size = buffer_size

    def __imp_exp_key(self, CMD, KEYTYPE, KEYSCHEME, ZCMK, KEY, KCV):
        HEADER = "RSM5"
        COMMAND = HEADER + CMD + KEYTYPE + ZCMK + KEY + KEYSCHEME
        # 1st two bytes must be command length
        SIZE = pack('>h', len(COMMAND))
        # join everything together
        MESSAGE = SIZE + COMMAND
        # Create socket and connect
        hsmSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hsmSocket.connect((self.ip, self.port))
        # send MESSAGE
        print 'MESSAGE: ', MESSAGE
        hsmSocket.send(MESSAGE)
        # receive
        data = hsmSocket.recv(self.buffer_size)
        # close socket
        hsmSocket.close()
        # parse response
        print 'RECEIVED:', data
        try:
            ret_key = data[len(HEADER) + len(CMD) + 2 + 2:len(data) - 6]
            ret_kcv = data[len(data) - 6:]
        except Exception as e:
            print e
            return None
        return (KEYTYPE, ret_key, ret_kcv)

    def import_export_key_tcp(self, command, ZCMK, import_line):
        l_import = import_line.split(';')
        l_import = [x.strip() for x in l_import]
        print l_import, len(l_import)
        KEYTYPE, KEY, KCV = l_import[0], l_import[1], l_import[2]
        NOTES = l_import[3]
        ret = None
        if len(KEY) > 16:
            if command == 'ik':
                KEYSCHEME = 'U'  # import under U scheme
            elif command == 'ke':
                KEYSCHEME = 'X'  # export under X scheme
        else:
            KEYSCHEME = 'Z'
        if command == 'ik':
            CMD = 'A6'  # import
        elif command == 'ke':
            CMD = 'A8'  # export
        else:
            print 'commant unsupported. Use ik/ke commands inside config file.'
            return
        ret = self.__imp_exp_key(CMD, KEYTYPE, KEYSCHEME, ZCMK, KEY, KCV)
        if ret is not None:
            # if KCVs did not match, warn user (and save new KCV)
            if (KCV != ret[2] and KCV != "XXXXXX"):
                NOTES = NOTES.rstrip('\r\n')
                NOTES += " WARNING: KCV is different!"
            # add user NOTES to the response
            ret += (NOTES + '\r\n',)
        else:
            ret = None
        return ret
