from feebb import *
import matplotlib.pyplot as plt

pre = Preprocessor()
pre.load_json('ex_json/ex77.json')
elems = [Element(elem) for elem in pre.elements]
beam = Beam(elems, pre.supports)
post = Postprocessor(beam, 3)
print(post.interp('moment'))
plt.plot(post.interp('moment'))
plt.show()
print(post.interp('shear'))
plt.plot(post.interp('shear'))
plt.show()
