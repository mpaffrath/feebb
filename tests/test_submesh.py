# Modify for multiple elements and multiple loads.
# Modify for boundary "support" conditions
# Add "patch" and "trapazodal" support when needed

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
element_patch_load = {'element': 1,
                      'length': 10,
                      'loads': [{'magnitude': 5, 'type': 'patch'}],
                      'moment_of_inertia': 1,
                      'youngs_mod': 1}
element_moment_load = {'element': 1,
                       'length': 10,
                       'loads': [{'magnitude': 5, 'type': 'moment', 'location': 3}],
                       'moment_of_inertia': 1,
                       'youngs_mod': 1}


def sub_dist(element, num_divs):
    # sub_length = element['length'] / num_divs
    magnitude = element['loads'][0]['magnitude']
    sub_loads = []
    for _ in range(num_divs):
        sub_loads.append({'magnitude': magnitude,
                          'type': 'udl'})

    return sub_loads


def sub_point(element, num_divs):
    sub_length = element['length'] / num_divs
    location = element['loads'][0]['location']
    magnitude = element['loads'][0]['magnitude']
    sub_loads = []
    start = 0
    end = sub_length
    for _ in range(num_divs):
        if location > end:
            sub_loads.append({'type': 'none'})
        elif location < start:
            sub_loads.append({'type': 'none'})
        else:
            sub_loads.append({'type': 'point',
                              'magnitude': magnitude,
                              'location': (location - start)})
        start = start + sub_length
        end = end + sub_length

    return sub_loads


def sub_patch(element, num_divs):

    return


def test_sub_dist():
    sub_loads = sub_dist(element_dist_load, 5)
    for load in sub_loads:
        assert load['magnitude'] == 5
        assert load['type'] == 'udl'

    return


def test_sub_point():
    sub_loads = sub_point(element_point_load, 5)
    for i, load in enumerate(sub_loads):
        if i == 1:
            assert load['magnitude'] == 5
            assert load['location'] == 1
            assert load['type'] == 'point'
        else:
            assert load['type'] == 'none'

    return

