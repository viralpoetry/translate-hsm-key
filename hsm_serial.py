#!/usr/bin/python
import hsm_serial_connect


class HSM(hsm_serial_connect.HSM):

    def collect_config(self):
        '''
        l_commands = [
            'vr', 'v', 'vt', 'va', 'qs',
            'qc', 'qh', 'qm', 'qp', 'qa', 'ql',
            'getcmds', 'configpb',
            'errlog', 'auditlog'
        ]
        '''
        # TODO
        l_commands = ['vr']

        for command in l_commands:
            self.to_hsm(command + '\r\n' + '\r\n')
            result = self.from_hsm()
            print result

    def __imp_exp_key(self, CMD, KEYTYPE, SCHEME, ZCMK, VARIANT, KEY, KCV):
        exec_data = ""
        exec_data += CMD + '\r\n'
        exec_data += '\r\n'  # LMK id
        exec_data += KEYTYPE + '\r\n'
        exec_data += SCHEME + '\r\n'
        exec_data += ZCMK + '\r\n'
        #exec_data += VARIANT + '\r\n'
        exec_data += KEY + '\r\n'
        self.to_hsm(exec_data)
        result = self.from_hsm()
        # parse the response and return KEY, KCV
        ret_key, ret_kcv = self.parse_hsm_response(result)
        return (KEYTYPE, ret_key, ret_kcv)

    def import_export_key_serial(self, hsm, command, ZCMK, import_line):
        l_import = import_line.split(';')
        l_import = [x.strip() for x in l_import]
        KEYTYPE, KEY, KCV = l_import[0], l_import[1], l_import[2]
        NOTES = l_import[3]
        ret = None
        if command == 'ik':
            # import key - returns (KEYTYPE, ret_key, ret_kcv)
            ret = self.ser.import_key(KEYTYPE, ZCMK, KEY, KCV)
        elif command == 'ke':
            # export key - returns (KEYTYPE, ret_key, ret_kcv)
            ret = self.ser.export_key(KEYTYPE, ZCMK, KEY, KCV)
        if ret is not None:
            # if KCVs did not match, warn user (and save new KCV)
            if (KCV != ret[2] and KCV != "XXXXXX"):
                NOTES = NOTES.rstrip('\r\n')
                NOTES += " WARNING: KCV is different!"
            # add user NOTES to the response
            ret += (NOTES + '\r\n',)
        return ret

    def parse_hsm_response(self, data):
        ret_key = None
        ret_kcv = None
        # split lines
        lines = data.splitlines()
        for line in lines:
            if line.startswith("Encrypted key:"):
                ret_key = line[14:].replace(" ", "")
            elif line.startswith("Key under ZMK:"):
                ret_key = line[14:].replace(" ", "")
            elif line.startswith("Key check value:"):
                ret_kcv = line[16:].replace(" ", "")
        return (ret_key, ret_kcv)

    def import_key(self, KEYTYPE, ZCMK, KEY, KCV):
        if (KEY[0] == 'Z' or len(KEY) is 16):
            return self.__imp_exp_key("ik", KEYTYPE, "Z", ZCMK, "0", KEY, KCV)
        else:
            return self.__imp_exp_key("ik", KEYTYPE, "U", ZCMK, "0", KEY, KCV)

    def export_key(self, KEYTYPE, ZCMK, KEY, KCV):
        if (KEY[0] == 'Z' or len(KEY) is 16):
            return self.__imp_exp_key("ke", KEYTYPE, "Z", ZCMK, "0", KEY, KCV)
        else:
            return self.__imp_exp_key("ke", KEYTYPE, "X", ZCMK, "0", KEY, KCV)
