from feebb import *
import matplotlib.pyplot as plt

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


pre = Preprocessor()
pre.load_json('ex_json/test2m.json')
elems = [Element(elem) for elem in pre.elements]
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


pre = Preprocessor()
pre.load_json('ex_json/test2mm.json')
elems = [Element(elem) for elem in pre.elements]
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

pre = Preprocessor()
pre.load_json('ex_json/test2mmm.json')
elems = [Element(elem) for elem in pre.elements]
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
