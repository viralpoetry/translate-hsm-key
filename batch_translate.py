#!/usr/bin/python
import os
import hsm_serial
import hsm_socket


# read the scenario configuration
dir = os.path.dirname(os.path.realpath(__file__))
dir_keys = dir + "\\keys\\"
with open(dir + "\keys\config.csv", 'r') as f_config_r:
    # for every line in the scenario
    for config_line in f_config_r:
        # format: "COM1"; 9600; ik/ke; ZCMK; input_file; output_file
        l_setup = config_line.split(';')
        l_setup = [x.strip() for x in l_setup]
        print l_setup
        try:
            if l_setup[0] == 'COM':
                port, speed = l_setup[1], int(l_setup[2])
            elif l_setup[0] == 'TCP':
                ip, port = l_setup[1], int(l_setup[2])
            command, ZCMK = l_setup[3], l_setup[4]
            input_file, output_file = dir_keys + \
                l_setup[5], dir_keys + l_setup[6]
            print l_setup[5] + " ----> " + l_setup[6]
        except Exception as e:
            print "Failed to load config.csv\n", e
        try:
            f_input = open(input_file, 'r')
        except Exception as e:
            print "Failed to open import file\n", e
        try:
            f_output = open(output_file, 'w')
        except Exception as e:
            print "Failed to open export file\n", e

        # read the key line by line
        for input_line in f_input:
            result = None
            if l_setup[0] == 'COM':
                # connect to HSM via COM port
                hsm_connection = hsm_serial.HSM(port, speed, 0)
                result = hsm_connection.import_export_key_serial(
                    command, ZCMK, input_line)
            elif l_setup[0] == 'TCP':
                # connect to HSM via sockets
                hsm_connection = hsm_socket.HSM(ip, port)
                result = hsm_connection.import_export_key_tcp(
                    command, ZCMK, input_line)
            if result is not None:
                print "result: ", result
                # export to the file
                to_be_written = result[0] + '; '      # keytype
                to_be_written += result[1] + '; '     # key
                to_be_written += result[2] + '; '     # kcv
                to_be_written += result[3].strip(' ')  # comment
                f_output.write(to_be_written)

        if l_setup[0] == 'COM':
            # disconnect current Serial port session
            hsm_connection.close()
        f_input.close()
        f_output.close()
