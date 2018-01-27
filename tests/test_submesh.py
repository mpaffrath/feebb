# Modify for boundary "support" conditions
# Add "trapazodal" support when needed

element_dist_load = {'element': 1,
                     'length': 10,
                     'loads': [{'magnitude': 5, 'type': 'udl'}],
                     'moment_of_inertia': 1,
                     'youngs_mod': 1}
element_point_load = {'element': 1,
                      'length': 10,
                      'loads': [{'magnitude': 5, 'type': 'point', 'location': 3}],
                      'moment_of_inertia': 1,
                      'youngs_mod': 1}
element_patch_load1 = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'patch', 'location': [2, 5]}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}
element_patch_load2 = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'patch', 'location': [3, 6]}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}
element_patch_load3 = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'patch',
                                  'location': [2.5, 3.5]}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}
element_patch_load4 = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'patch', 'location': [2, 8]}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}
element_moment_load = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'moment', 'location': 3}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}


class Submesh():
    def __init__(self, element, size_mesh):
        self.size_mesh = size_mesh
        self.length = element['length'] / size_mesh
        self.lengths = [self.length] * size_mesh
        self.moi = [element['moment_of_inertia']] * size_mesh
        self.mod = [element['youngs_mod']] * size_mesh
        self.elements = [i for i in range(size_mesh)]
        self.loads = []
        self.sub_elements = []

        for i, load in enumerate(element['loads']):
            if load['type'] == 'udl':
                self.loads.append(self.__sub_udl(load))
            elif load['type'] == 'point' or load['type'] == 'moment':
                self.loads.append(self.__sub_point(load, load['type']))
            elif load['type'] == 'patch':
                self.loads.append(self.__sub_patch(load))
            else:
                self.loads.append([{'type': 'none'}])

        self.submesh = self.__repack()

        return

    def __sub_udl(self, load):
        sub_loads = []
        for _ in range(self.size_mesh):
            sub_loads.append({'magnitude': load['magnitude'],
                              'type': 'udl'
                              })

        return sub_loads

    def __sub_point(self, load, load_type):
        sub_loads = []
        start = 0
        end = self.length
        for _ in range(self.size_mesh):
            if load['location'] > end:
                sub_loads.append({'type': 'none'})
            elif load['location'] < start:
                sub_loads.append({'type': 'none'})
            else:
                sub_loads.append({'type': load_type,
                                  'magnitude': load['magnitude'],
                                  'location': (load['location'] - start)
                                  })

            start = start + self.length
            end = end + self.length

        return sub_loads

    def __sub_patch(self, load):
        sub_loads = []
        start = 0
        end = self.length
        load_start = load['location'][0]
        load_end = load['location'][1]
        for _ in range(self.size_mesh):
            if load_start >= end or load_end <= start:
                sub_loads.append({'type': 'none'})
            elif load_start <= end:
                if load_start <= start:
                    sub_start = 0
                    if load_end < end:
                        sub_end = load_end - start
                    else:
                        sub_end = self.length
                elif load_start > start:
                    sub_start = load_start - start
                    if load_end < end:
                        sub_end = load_end - start
                    else:
                        sub_end = self.length

                if sub_start == 0 and sub_end == self.length:
                    sub_loads.append({'type': 'udl',
                                      'magnitude': load['magnitude']
                                      })
                else:
                    sub_loads.append({'type': 'patch',
                                      'magnitude': load['magnitude'],
                                      'location': [sub_start, sub_end]
                                      })

            start = start + self.length
            end = end + self.length

        return sub_loads

    def __repack(self):
        loads = list(map(list, zip(*self.loads)))
        values = [[el, l, mod, moi, load] for el, l, mod, moi, load
                  in zip(self.elements, self.lengths, self.mod, self.moi, loads)]
        keys = ['element', 'length', 'youngs_mod', 'moment_of_inertia', 'loads']
        d_lists = {x: list(y) for x, y in zip(keys, zip(*values))}
        packed = [dict(zip(d_lists, t)) for t in zip(*d_lists.values())]

        return packed


def test_sub_dist():
    submesh = Submesh(element_dist_load, 5)
    for element in submesh.submesh:
        assert element['loads'][0]['magnitude'] == 5
        assert element['loads'][0]['type'] == 'udl'

    return


def test_sub_point():
    submesh = Submesh(element_point_load, 5)
    for i, element in enumerate(submesh.submesh):
        if i == 1:
            assert element['loads'][0]['magnitude'] == 5
            assert element['loads'][0]['location'] == 1
            assert element['loads'][0]['type'] == 'point'
        else:
            assert element['loads'][0]['type'] == 'none'

    return


def test_sub_moment():
    submesh = Submesh(element_moment_load, 5)
    for i, element in enumerate(submesh.submesh):
        if i == 1:
            assert element['loads'][0]['magnitude'] == 5
            assert element['loads'][0]['location'] == 1
            assert element['loads'][0]['type'] == 'moment'
        else:
            assert element['loads'][0]['type'] == 'none'

    return


def test_sub_patch():
    submesh = Submesh(element_patch_load1, 5)
    for i, element in enumerate(submesh.submesh):
        if i == 1:
            assert element['loads'][0]['magnitude'] == 5
            # assert element['loads'][0]['location'] == [0, 2]
            assert element['loads'][0]['type'] == 'udl'
        elif i == 2:
            assert element['loads'][0]['magnitude'] == 5
            assert element['loads'][0]['location'] == [0, 1]
            assert element['loads'][0]['type'] == 'patch'
        else:
            assert element['loads'][0]['type'] == 'none'

    submesh = Submesh(element_patch_load2, 5)
    for i, element in enumerate(submesh.submesh):
        if i == 1:
            assert element['loads'][0]['magnitude'] == 5
            assert element['loads'][0]['location'] == [1, 2]
            assert element['loads'][0]['type'] == 'patch'
        elif i == 2:
            assert element['loads'][0]['magnitude'] == 5
            # assert element['loads'][0]['location'] == [0, 2]
            assert element['loads'][0]['type'] == 'udl'
        else:
            assert element['loads'][0]['type'] == 'none'

    submesh = Submesh(element_patch_load3, 5)
    for i, element in enumerate(submesh.submesh):
        if i == 1:
            assert element['loads'][0]['magnitude'] == 5
            assert element['loads'][0]['location'] == [0.5, 1.5]
            assert element['loads'][0]['type'] == 'patch'
        else:
            assert element['loads'][0]['type'] == 'none'

    submesh = Submesh(element_patch_load4, 5)
    for i, element in enumerate(submesh.submesh):
        if 0 < i < 4:
            assert element['loads'][0]['magnitude'] == 5
            # assert element['loads'][0]['location'] == [0, 2]
            assert element['loads'][0]['type'] == 'udl'
        else:
            assert element['loads'][0]['type'] == 'none'
    return


def test_sub_support():
    return
