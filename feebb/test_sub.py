from feebb import *
import matplotlib.pyplot as plt
import itertools

# Beam 1
pre = Preprocessor()
pre.load_json('ex_json/test2.json')
elems = [Element(elem) for elem in pre.elements]
print(pre.supports)
beam = Beam(elems, pre.supports)
post = Postprocessor(beam, 10)
print(max(post.interp('moment')))
print(min(post.interp('moment')))
plt.plot(post.interp('moment'))
plt.show()
print(max(post.interp('shear')))
print(min(post.interp('shear')))
plt.plot(post.interp('shear'))
plt.show()


# Beam 1 submeshed
pre = Preprocessor()
pre.load_json('ex_json/test2.json')
mesh = 100
meshed = [Submesh(elem, mesh).submesh for elem in pre.elements]
meshed_flat = list(itertools.chain.from_iterable(meshed))
elems = [Element(elem) for elem in meshed_flat]
meshed_supports = submesh_supports(pre.supports, mesh)
beam = Beam(elems, meshed_supports)
post = Postprocessor(beam, 2)
print(max(post.interp('moment')))
print(min(post.interp('moment')))
plt.plot(post.interp('moment'))
plt.show()
print(max(post.interp('shear')))
print(min(post.interp('shear')))
plt.plot(post.interp('shear'))
plt.show()

# Beam 2 submeshed
pre = Preprocessor()
pre.load_json('ex_json/test.json')
mesh = 100
meshed = [Submesh(elem, mesh).submesh for elem in pre.elements]
meshed_flat = list(itertools.chain.from_iterable(meshed))
elems = [Element(elem) for elem in meshed_flat]
meshed_supports = submesh_supports(pre.supports, mesh)
beam = Beam(elems, meshed_supports)
post = Postprocessor(beam, 2)
print(max(post.interp('moment')))
print(min(post.interp('moment')))
plt.plot(post.interp('moment'))
plt.show()
print(max(post.interp('shear')))
print(min(post.interp('shear')))
plt.plot(post.interp('shear'))
plt.show()

# Beam 3 submeshed
pre = Preprocessor()
pre.load_json('ex_json/test3.json')
mesh = 100
meshed = [Submesh(elem, mesh).submesh for elem in pre.elements]
meshed_flat = list(itertools.chain.from_iterable(meshed))
elems = [Element(elem) for elem in meshed_flat]
meshed_supports = submesh_supports(pre.supports, mesh)
beam = Beam(elems, meshed_supports)
post = Postprocessor(beam, 2)
print(max(post.interp('moment')))
print(min(post.interp('moment')))
plt.plot(post.interp('moment'))
plt.show()
print(max(post.interp('shear')))
print(min(post.interp('shear')))
plt.plot(post.interp('shear'))
plt.show()
