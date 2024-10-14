from cell import CellBundle
class Network:
    def __init__(self, layers):
        self.layers = layers
        self.maxwidth = 0
        self.depth = len(layers)
        self.maxwidths = []
        for layer in layers:
            layer : CellBundle
            self.maxwidths.append(layer.dim)
            if layer.dim > self.maxwidth:
                self.maxwidth = layer.dim

        self.y_spacing = 1. / float(self.depth)
        print(f"Ysp: {self.y_spacing}")
        self.x_spacing = 1. / float(self.maxwidth)
        print(f"Xsp: {self.x_spacing}")
        

    
    def return_info(self):
        print(f"\nmaxwidth: {self.maxwidth}, depth: {self.depth}\n")
        for w in self.maxwidths:
            s = "o"
            for _ in range(w-1):
                s += "-o"
            print(s)
        print()

    def set_draw_data(self, sc_w, sc_h, padding, rad=30.):
        c_x = sc_w / 2.
        c_y = sc_h / 2.

        padded_x = (sc_w - padding)
        padded_y = (sc_h - padding)
        start_x = c_x - (padded_x/2.)
        start_y = c_y - (padded_y/2.)
        bounds_x = (c_x - padded_x/2., c_x + padded_x/2.)
        bounds_y = (c_y - padded_y/2., c_x + padded_y/2.)
        print(f"startx: {start_x}")

        y_space = padded_y * self.y_spacing
        x_space = padded_x * self.x_spacing
        print(f"xspace: {x_space}")


        for l in range(len(self.layers)):
            lr = self.layers[l]
            lr : CellBundle
            xyzl = []
            xyel = []
            xymul = []
            xyyl = []
            for i in range(lr.dim):
                # xyzl.append((start_x, start_y))
                xyzl.append((start_x + (x_space*i + x_space/2), start_y + (y_space*l + y_space/2)))
                if lr.t != None:
                    xyel.append((start_x + (x_space*i + x_space/2), start_y + (y_space*l + y_space/2) - rad))
                    xymul.append((start_x + (x_space*i + x_space/2) + rad, start_y + (y_space*l + y_space/2) - rad))
                if lr.b != None:
                    xyyl.append((start_x + (x_space*i + x_space/2) - rad/1.2, start_y + (y_space*l + y_space/2) + rad/1.2 ))
            lr.set_coords(xyzl, xyel, xymul, xyyl)


if __name__ == '__main__':
    c2 = CellBundle(2)
    c1 = CellBundle(2)
    c0 = CellBundle(1)
    L = [c2, c1, c0]
    nw = Network(L)
    nw.return_info()