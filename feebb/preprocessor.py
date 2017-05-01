import json

class Preprocessor:
    def __init__(self):
        self.number_elements = 0
        self.length_elements = []
        self.E_elements = []
        self.I_elements = []

    def read_json(self, infile):
        with open(infile) as json_model:
            model = json.load(json_model)

        self.number_elements = len(model['elements'])
        self.length_elements = [element['length'] for element in model['elements']]
        self.E_elements = [element['youngs_mod'] for element in model['elements']]
        self.I_elements = [element['moment_of_inertia'] for element in model['elements']]
