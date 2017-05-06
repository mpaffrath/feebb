# -*- coding: utf-8 -*-

import numpy as np


class Element:
    def __init__(self, preprocessed=None):
        self.stiffness = np.array([])
        self.nodal_loads = np.zeros((4))
        if preprocessed is None:
            self.length = 0
            self.E = 0
            self.I = 0
            self.loads = []
        else:
            self.length = preprocessed.length
            self.E = preprocessed.E
            self.I = preprocessed.I
            self.loads = preprocessed.loads
            self.local_stiffness()
            self.load_vector()

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


class Beam():
    def __init__(self, elements, supports):
        self.num_elements = len(elements)
        self.num_nodes = self.num_elements + 1
        self.num_dof = self.num_nodes * 2
        self.supports = supports
        self.stiffness = np.zeros((self.num_dof, self.num_dof))
        self.load = np.zeros((self.num_dof))
        for i, element in enumerate(elements):
            a = i * 2
            b = a + 4
            stiffness_element = np.zeros_like(self.stiffness)
            stiffness_element[a:b, a:b] = element.stiffness
            self.stiffness = self.stiffness + stiffness_element
            load_element = np.zeros_like(self.load)
            load_element[a:b] = element.nodal_loads
            self.load = self.load - load_element

        for i in range(self.num_dof):
            if self.supports[i] < 0:
                self.stiffness[i, :] = 0
                self.stiffness[:, i] = 0
                self.stiffness[i, i] = 1
                self.load[i] = 0

        self.displacement = np.linalg.solve(self.stiffness, self.load)
