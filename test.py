
import hsm

# connect to HSM COM port
hsm = hsm.HSM("COM2", 9600, 0)

#collect HSM config
hsm.collect_config()
