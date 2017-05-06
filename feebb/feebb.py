# -*- coding: utf-8 -*-

import numpy as np


class Element:
    def __init__(self):
        self.length = 0
        self.E = 0
        self.I = 0
        self.loads = []
        self.nodal_loads = np.zeros((4))

    def local_stiffness(self):
        kfv = 12 * self.E * self.I / self.length ** 3
        kmv = 6 * self.E * self.I / self.length ** 2
        kft = kmv
        kmt = 4 * self.E * self.I / self.length
        kmth = 2 * self.E * self.I / self.length
        self.stiffness = np.array([[kfv, -kft, -kfv, -kft],
                                   [-kmv, kmt, kmv, kmth],
                                   [-kfv, kft, kfv, kft],
                                   [-kft, kmth, kft, kmt]])

    def fer_point(self, p, a):
        b = self.length - a
        v = [(p * b ** 2 * (3*a + b)) / self.length ** 3, (p * a ** 2 * (a + 3 * b))
             / self.length ** 3]
        m = [p * a * b ** 2 / self.length ** 2, p * a ** 2 * b / self.length ** 2]
        load_vector = np.array([v[0], -m[0], v[1], m[1]])
        return load_vector

    def fer_distrib(self, w):
        v = w * self.length / 2
        m = w * self.length ** 2 / 12
        load_vector = np.array([v, -m, v, m])
        return load_vector

    def fer_patch(self, w, start, end):
        d = end - start
        a = start + d / 2
        b = self.length - a
        v = [(w * d) / self.length ** 3 * ((2 * a + self.length) * b ** 2
                                           + (a - b) / 4 * d ** 2),
             (w * d) / self.length ** 3 * ((2 * b + self.length) * a ** 2
                                           + (a - b) / 4 * d ** 2)]
        m = [(w * d / self.length ** 2) * (a * b ** 2 + (a - 2 * b) * d ** 2 / 12),
             (w * d / self.length ** 2) * (a ** 2 * b + (b - 2 * a) * d ** 2 / 12)]
        load_vector = np.array([v[0], -m[0], v[1], m[1]])
        return load_vector

    def fer_moment():
        pass

    def load_vector(self):
        for load in self.loads:
            if load['type'] == 'udl':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_distrib(self.length, load['magnitude']))
            elif load['type'] == 'point':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_point(self.length, load['magnitude'],
                                                     load['location']))
            elif load['type'] == 'patch':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_patch(self.length, load['magnitude'],
                                                     load['start'], load['end']))
            elif load['type'] == 'moment':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_moment(self.length, load['magnitude'],
                                                      load['location']))
