import json
import numpy as np

class Preprocessor:
    def __init__(self):
        self.reset()

    def reset(self):
        self.number_elements = 0
        self.length_elements = []
        self.E_elements = []
        self.I_elements = []
        self.loads = []
        self.supports = []

    def load_json(self, infile):
        self.reset()
        with open(infile) as json_model:
            model = json.load(json_model)

        self.number_elements = len(model['elements'])
        self.length_elements = [element['length'] for element in model['elements']]
        self.E_elements = [element['youngs_mod'] for element in model['elements']]
        self.I_elements = [element['moment_of_inertia'] for element in model['elements']]
        for element in model['elements']:
            for load in element['loads']:
                load["element"] = element["element"]
                self.loads.append(load)

        self.supports = model['supports']


class Element:
    def __init___(self):
        self.length = 0
        self.E = 0
        self.I = 0
        self.loads = []

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
        v = [(p * b ** 2 * (3*a + b)) / l** 3,
             (p * a ** 2 * (a + 3 * b)) / l ** 3]
        m = [p * a * b ** 2 /  l ** 2,
             p * a ** 2 * b / l** 2]
        load_vector = np.array([v[0], -m[0], v[1], m[1]])
        return  load_vector

    def fer_distrib(self, w):
        v = w * self.length / 2
        m = w * self.length ** 2 / 12
        load_vector = np.array([v, -m, v, m])
        return load_vector

    def fer_patch(self, w, start, end):
        d = end - start
        a = start + d / 2
        b = self.length - a
        v = [(w * d) / self.length ** 3 * ((2 * a + self.length) * b ** 2 +
                                           (a - b) / 4 * d ** 2),
             (w * d) / self.length ** 3 * ((2 * b + self.length) * a ** 2 +
                                           (a - b) / 4 * d ** 2)]
        m = [(w * d / self.length ** 2) * (a * b ** 2 + (a - 2 * b) * d ** 2 / 12),
             (w * d / self.length ** 2) * (a ** 2 * b + (b - 2 * a) * d ** 2 / 12)]
        load_vector = np.array([v[0], -m[0], v[1], m[1]])
        return load_vector

    def fer_moment():
        pass
