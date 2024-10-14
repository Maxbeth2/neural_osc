import pygame as pg
import numpy as np
from cell import CellBundle
# from cell_batch import CellBatch as Cell
from network import Network
from render_cells import CellRenderer
import time as t
import math

np.random.seed(421)

pg.init()

w, h = 1200, 800

screen = pg.display.set_mode((w, h))
pg.display.set_caption('Oscillator')


# c3 = Cell(3, leak=0.2, beta=0.7, bs=3)
# c2 = Cell(2, leak=0.2, beta=0.7, bs=3)
# c1 = Cell(1, leak=0.2, beta=0.7, bs=3)
# c0 = Cell(1, leak=0.8, bs=3)
c3 = CellBundle(3, leak=0.2, beta=0.7)
c2 = CellBundle(3, leak=0.2, beta=0.7)
c1 = CellBundle(2, leak=0.2, beta=0.7)
c0 = CellBundle(1, leak=0.8)
# c3 = Cell(5, leak=0.2, beta=0.7)
# c2 = Cell(4, leak=0.2, beta=0.7)
# c1 = Cell(3, leak=0.2, beta=0.7)
# c0 = Cell(1, leak=0.8)

# c3.connect_b(c2)
# c2.connect_t(c3)
c2.connect_b(c1)
c1.connect_t(c2)
c1.connect_b(c0)
c0.connect_t(c1)

cells = [c2, c1, c0]

for c in cells:
    c.clip_theta()

nw = Network(cells)
nw.set_draw_data(w, h, 50, rad=60.)

renderer = CellRenderer(cells, screen)

rndW = True
rndE = True 
rndM = True 
rndU = True
rndV = True

pausing = False
feedback = False

t_elapsed = 0
dt = 1./60.

rad = 30


def read_slider():
    if rec.poll():
        data = rec.recv()
        b = data["B"]
        val = int(b)/1023.
        val -= 0.5
        val *= 2
        c0.inject(np.ones(c0.z.shape) * val)
    while rec.poll():
        rec.recv()

def broadcast_pred():
    pred = c0.extract_error()[0][0]
    snd_err.send(pred)

def write_error():
    command = f"1:{c0.extract_error()[0][0]*1000}&2:{0}"
    arduino.write(command.encode())

def connect_ardu():
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


# arduino = connect_ardu()
from processes.ardu_in_process import ArduInProcess
from multiprocessing.connection import Pipe
snd, rec = Pipe()
snd_err, rec_err = Pipe()
if __name__ == '__main__':
    # ardu_in = ArduInProcess(feed_network_pipe=snd, receive_from_nw=rec_err)
    # ardu_in.start()

    c0.inject((np.ones(c0.z.shape)) + np.random.normal(loc=0,scale=1,size=c0.z.shape)*0.02)


    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    # c0.inject(np.ones(c0.z.shape))
                    pulse = True
                if event.key == pg.K_w:
                    rndW = not rndW
                if event.key == pg.K_e:
                    rndE = not rndE
                if event.key == pg.K_m:
                    rndM = not rndM
                if event.key == pg.K_u:
                    rndU = not rndU
                if event.key == pg.K_v:
                    rndV = not rndV
                if event.key == pg.K_p:
                    pausing = not pausing
                if event.key == pg.K_f:
                    feedback = not feedback
        if not pausing:
            for c in cells:
                c.receive()
            for c in cells:
                c.integrate()

            if feedback:
                c0.inject(c0.extract_prediction())
            else:
                y = (math.sin(t_elapsed * 3))
                c0.inject((np.ones(c0.z.shape)) * y + np.random.normal(loc=0,scale=1,size=c0.z.shape)*0.02)
        
            # read_slider()
            
            for c in cells:
                c.predict()

            # broadcast_pred()

            # write_error()
            

            for c in cells:
                c.correct()
            if not feedback:
                for c in cells:
                    c.update_params(alpha=0.01)
            for c in cells:
                c.clip_theta()
            

        if rndW:
            renderer.render_W()
        if rndE:
            renderer.render_E()
        if rndM:
            renderer.render_M()
        if rndU:
            renderer.render_U()

        renderer.render_e()
        renderer.render_mu()
        renderer.render_z()
        renderer.render_y()
        if rndV:
            renderer.render_V()
        t.sleep(dt)
        t_elapsed += dt
        pg.display.flip()
        screen.fill((50,50,50))