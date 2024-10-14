import numpy as np
import pygame as pg
import math
class CellBundle:
    def __init__(self, dim, leak=0.1, beta=1.):
        self.dim = dim
        self.z = np.zeros((1,dim))
        self.phi_z = np.zeros((1,dim))
        self.dz_td = np.zeros((1,dim))
        self.dz_bu = np.zeros((1,dim))
        self.y_node = np.zeros((1,self.dim))

        self.leak = leak
        self.beta = beta

        self.V = np.random.normal(loc=0, scale=1, size=(dim, dim))
        self.p_dict = {"W": None, "E": None, "M": None, "U": None, "V": self.V}
        # hierarchically superior node
        self.t = None
        # hierarchically inferior node
        self.b = None

        self.param = []
        self.param.append(self.V)

        self.zxy = None
        self.exy = None
        self.muxy = None
    
    def extract_prediction(self):
        return self.mu_node

    def extract_error(self):
        return self.e_node
        

    def clip_theta(self, threshold=1.2):
        for W in self.param:
            for c in range(W.shape[1]):
                col = W[:,c]
                norm = np.linalg.norm(col)
                if norm > threshold:
                    W[:,c] /= norm

    def connect_b(self, b):
        self.b : CellBundle
        self.b = b
        self.W = np.random.normal(loc=0, scale=1, size=(self.dim, self.b.dim))
        self.M = np.random.normal(loc=0, scale=1, size=(self.b.dim, self.dim))
        self.E = np.random.normal(loc=0, scale=1, size=(self.b.dim, self.dim))
        self.p_dict["W"] = self.W
        self.p_dict["E"] = self.E
        self.p_dict["M"] = self.M
        self.param.append(self.W)
        self.param.append(self.M)
        self.param.append(self.E)

        
        self.ev = np.zeros((1,self.dim)) 
        self.prev_ev = np.zeros((1,self.dim)) 
        

    def connect_t(self, t):
        self.t : CellBundle
        self.t = t
        self.U = np.random.normal(loc=0, scale=1, size=(self.t.dim, self.dim))
        self.p_dict["U"] = self.U
        self.param.append(self.U)

        self.e_node = np.zeros((1,self.dim))
        self.mu_node = np.zeros((1,self.dim))


    def receive(self):
        if self.t != None:
            self.dz_td = np.dot(self.t.y_node, self.U)
        if self.b != None:
            self.dz_bu = np.dot(self.b.y_node, self.M)
            self.dz_bu += np.dot(self.y_node, self.V)


    def integrate(self):
        """
        take in data from td and bu compartments and update state
        """
        temp = np.zeros((1, self.dim))
        if self.t != None:
            temp += self.dz_td * 0.5
        if self.b != None:
            temp += self.dz_bu * 0.5
        
        if self.b != None:
            self.phi_z = np.tanh(self.z)
            self.z += (-self.z * self.leak) + self.beta * temp
    

    def inject(self, val):
        self.z = val
        self.prev_phi_z = self.phi_z
        self.phi_z = val
        self.y_node = val
    

    def predict(self):
        if self.b != None:
            self.b.mu_node = (np.dot(self.phi_z, self.W))


    def correct(self):
        if self.t != None:
            self.e_node = self.phi_z - self.mu_node
        if self.b != None:
            if self.t == None:
                d = np.dot(self.b.e_node, self.E)
            else:
                d = np.dot(self.b.e_node, self.E) - (self.e_node * 0.001)

            d = d + (np.sign(self.z) * 0.002)
            # corr_signal = np.dot(self.b.e_node, self.E)
            # d = self.z - corr_signal * 0.1
            self.prev_y_node = self.y_node
            self.y_node = np.tanh(self.z - (d*0.2))
            new_ev = self.y_node - self.phi_z
            self.delta_ev = new_ev - self.ev
            self.ev = new_ev


    def update_params(self, alpha=0.075):
        dW = None
        if self.b != None:
            #W
            dW = np.outer(self.phi_z, self.b.e_node) * alpha
            self.W += dW
            #M
            if self.b.b != None:
                dW = np.outer(self.b.prev_y_node, self.ev) * alpha
                self.M += dW
            else:
                dW = np.outer(self.b.prev_phi_z, self.ev) * alpha
                self.M += dW
            #V 
            dW = np.outer(self.prev_y_node, self.ev) * alpha
            self.V += dW
            # E
            dW = np.outer(self.b.e_node, self.delta_ev) * -1
            self.E += dW
        if self.t != None and self.b != None:
            # U
            dW = np.outer(self.t.prev_y_node, self.ev) * alpha
            self.U += dW
    

    def set_coords(self, zxy, exy, muxy, yxy):
        self.zxy = zxy
        self.exy = exy
        self.muxy = muxy
        self.yxy = yxy


if __name__ == '__main__':
    c = CellBundle(1)
