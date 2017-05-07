# -*- coding: utf-8 -*-
"""
feebb - Finite Element Euler-Bernoulli Beams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Feebb is a library for analysing beams using Euler-Bernoulli beam theory. It includes
a preprocessor to aid in building the model as well as a postprocessor for obtaining
forces and displacemnts at no-nodal locations.
"""
import json
import numpy as np


class Preprocessor:
    """Class for reading in preformatted input data for building the FEA model.

    Attributes:
        number_elements (int): Total number of elemnts in the model.
        elements (:obj:`list` of :obj:`dict`): A list of dictionaries. Each dictionary
            contains the defnition of a single beam element.
        supports (:obj:`list' of :obj:`int`): A list of the degrees of freedom at each
            node.

   """

    def __init__(self):
        """The Preprocessor class is initialized with all attributes as `None`."""

        self.reset()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ': '))

    def reset(self):
        """Sets all attributes to `None`."""

        self.number_elements = None
        # self.loads = []
        self.elements = None
        self.supports = None

    def load_json(self, infile):
        """Reads on formatted input data from a .json file

        Args:
            infile (str): Name of the .json file to parse.

        """

        self.reset()
        with open(infile) as json_model:
            model = json.load(json_model)

        self.number_elements = len(model['elements'])
        # self.loads = [element['loads'] for element in model['elements']]
        self.elements = model['elements']
        self.supports = model['supports']


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
            self.length = preprocessed['length']
            self.E = preprocessed['youngs_mod']
            self.I = preprocessed['moment_of_inertia']
            self.loads = preprocessed['loads']
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
                                    + self.fer_distrib(load['magnitude']))
            elif load['type'] == 'point':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_point(load['magnitude'],
                                                     load['location']))
            elif load['type'] == 'patch':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_patch(load['magnitude'],
                                                     load['start'], load['end']))
            elif load['type'] == 'moment':
                self.nodal_loads = (self.nodal_loads
                                    + self.fer_moment(load['magnitude'],
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
