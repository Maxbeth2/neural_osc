import multiprocessing as mp
import multiprocessing.connection as mpc
from pynput import keyboard
import serial
from pythonosc import udp_client
import time


class ArduInProcess(mp.Process):
    """
    Starts a synth on a running SCServer. Looks for OSC messages containing pitch information on serial and updates the pitch of the synth accordingly.
    """
    def __init__(self, 
                 feed_network_pipe : mpc.Connection,
                 receive_from_nw : mpc.Connection,
                 OSC_PORT=7771):
        mp.Process.__init__(self)
        self.OSC_PORT = OSC_PORT
        self.feed_network_pipe = feed_network_pipe
        self.receive_from_nw = receive_from_nw


    def run(self):
        def get_ardu():
            import serial
            import serial.tools
            import serial.tools.list_ports
            port = None
            for p in serial.tools.list_ports.comports():
                in_description = any(x in p.description for x in ["Arduino", "IOUSBHostDevice"])
                if in_description:
                    port = p
            try:
                arduino = serial.Serial(port=port.device, baudrate=38400, timeout=.1)
                arduino.flush()
                for _ in range(100):
                    arduino.readline()
                return arduino
            except:
                return None

        arduino = get_ardu()
        if arduino == None:
            self.close()

        OSC_IP = "127.0.0.1"
        OSC_PORT = self.OSC_PORT

        client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)


        while True:
            try:    
                serialdata = arduino.readline()
                received_string = serialdata.decode("utf-8").strip()
                if received_string != "" and ":" in received_string:
                    address, value = received_string.split(":")
                    a, b = value.split(",")
                    # print(a)
                    self.feed_network_pipe.send({"A":a, "B": b})
                    if self.receive_from_nw.poll():
                        data = self.receive_from_nw.recv()
                        while self.receive_from_nw.poll():
                            self.receive_from_nw.recv()
                        client.send_message("/chA", data)
                        client.send_message("/chB", b)

            except KeyboardInterrupt:
                pass