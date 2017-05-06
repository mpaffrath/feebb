import json


class Preprocessor:
    def __init__(self):
        self.reset()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2, separators=(',', ': '))

    def reset(self):
        self.number_elements = None
        # self.length_elements = []
        # self.E_elements = []
        # self.I_elements = []
        # self.loads = []
        self.elements = None
        self.supports = None

    def load_json(self, infile):
        self.reset()
        with open(infile) as json_model:
            model = json.load(json_model)

        self.number_elements = len(model['elements'])
        # self.length_elements = [element['length'] for element in model['elements']]
        # self.E_elements = [element['youngs_mod'] for element in model['elements']]
        # self.I_elements = [element['moment_of_inertia'] for element in model['elements']]
        #  for element in model['elements']:
        #      for load in element['loads']:
        #          load["element"] = element["element"]
        #          self.loads.append(load)
        # self.loads = [element['loads'] for element in model['elements']]
        self.elements = model['elements']
        self.supports = model['supports']
