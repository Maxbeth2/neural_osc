from cell import CellBundle
import pygame as pg
import math



class CellRenderer:
    def __init__(self, cells, screen):
        self.cells = cells
        self.screen = screen
        self.r = 30.

    def draw_activity(self, val, x, y, scaler=30.):
        if val > 0:
            pg.draw.circle(self.screen, (255,255,255), (x, y),  scaler*abs(val), width=0)
        else:
            pg.draw.circle(self.screen, (0,0,0), (x, y),  scaler*abs(val), width=0)


    def render_z(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            z = cell.z[0]
            phiz = cell.phi_z[0]
            for c in range(cell.dim):
                xy = cell.zxy[c]
                pg.draw.circle(self.screen, (100,100,100), xy,  30.)
                zval = z[c]
                if zval > 0:
                    pg.draw.circle(self.screen, (0,150,0), xy,  20.*abs(zval), width=10)
                else:
                    pg.draw.circle(self.screen, (150,0,0), xy,  20.*abs(zval), width=10)


                phizval = phiz[c]
                self.draw_activity(phizval, xy[0], xy[1])

    def render_mu(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if len(cell.muxy) > 0:
                mu = cell.mu_node[0]
                for c in range(cell.dim):
                    xy = cell.muxy[c]
                    val = mu[c]
                    # background circle
                    pg.draw.circle(self.screen, (0,0,255), xy,  30.)
                    self.draw_activity(val, xy[0], xy[1])

    def render_e(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if len(cell.exy) > 0:
                e = cell.e_node[0]
                for c in range(cell.dim):
                    xy = cell.exy[c]
                    val = e[c]
                    # background circle
                    pg.draw.circle(self.screen, (255,0,0), xy,  30.)
                    self.draw_activity(val, xy[0], xy[1])

    def render_y(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if len(cell.yxy) > 0:
                y = cell.y_node[0]
                for c in range(cell.dim):

                    xy = cell.yxy[c]
                    xyz = cell.zxy[c]
                    pg.draw.line(self.screen, (100,100,100),xy,xyz, width=10)
                    val = y[c]
                    # background circle
                    pg.draw.circle(self.screen, (40,40,100), xy,  30.)
                    self.draw_activity(val, xy[0], xy[1])

    def render_W(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if cell.b != None:
                W = cell.W
                rec = cell.b
                rec : CellBundle
                for m in range(cell.dim):
                    for n in range(rec.dim):
                        startc = cell.zxy[m]
                        endc = rec.muxy[n]
                        wval = W[m,n]
                        if wval > 0:
                            pg.draw.line(self.screen, (0,150,0), startc, endc, width=max(1,int(abs(wval)*15)))
                        else:
                            pg.draw.line(self.screen, (150,0,0), startc, endc, width=max(1,int(abs(wval)*15)))

    def render_E(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if cell.b != None:
                E = cell.E
                snd = cell.b
                snd : CellBundle
                for m in range(snd.dim):
                    for n in range(cell.dim):
                        startc = snd.exy[m]
                        endc = cell.yxy[n]
                        wval = E[m,n]
                        if wval > 0:
                            pg.draw.line(self.screen, (0,150,0), startc, endc, width=max(1,int(abs(wval)*15)))
                        else:
                            pg.draw.line(self.screen, (150,0,0), startc, endc, width=max(1,int(abs(wval)*15)))

    def render_M(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if cell.b != None:
                M = cell.M
                snd = cell.b
                for m in range(snd.dim):
                    for n in range(cell.dim):
                        if cell.b.b == None:
                            startc = snd.zxy[m]
                        else:
                            startc = snd.yxy[m]
                        startc = (startc[0] + 20, startc[1])
                        endc = cell.zxy[n]
                        wval = M[m,n]
                        if wval > 0:
                            pg.draw.line(self.screen, (0,150,0), startc, endc, width=max(1,int(abs(wval)*15)))
                        else:
                            pg.draw.line(self.screen, (150,0,0), startc, endc, width=max(1,int(abs(wval)*15)))

    def render_U(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if cell.t != None:
                snd = cell.t
                snd: CellBundle
                U = cell.U
                for m in range(snd.dim):
                    for n in range(cell.dim):
                        startc = snd.yxy[m]
                        endc = cell.zxy[n]
                        startc = (startc[0] - 20, startc[1])
                        wval = U[m,n]
                        if wval > 0:
                            pg.draw.line(self.screen, (0,150,0), startc, endc, width=max(1,int(abs(wval)*15)))
                        else:
                            pg.draw.line(self.screen, (150,0,0), startc, endc, width=max(1,int(abs(wval)*15)))
    def render_V(self):
        for c in range(len(self.cells)):
            cell = self.cells[c]
            cell : CellBundle
            if cell.b != None:
                V = cell.V
                for m in range(cell.dim):
                    for n in range(cell.dim):
                        startc = cell.yxy[m]
                        endc = cell.zxy[n]
                        endc = (endc[0], endc[1]+20)
                        wval = V[m,n]
                        if wval > 0:
                            pg.draw.line(self.screen, (0,150,0), startc, endc, width=max(1,int(abs(wval)*15)))
                        else:
                            pg.draw.line(self.screen, (150,0,0), startc, endc, width=max(1,int(abs(wval)*15)))
