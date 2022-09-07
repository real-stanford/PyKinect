# %%
import os
os.environ['DISPLAY'] = ':0'

# %%
from pyk4a import PyK4A

# Load camera with the default config
k4a = PyK4A()
k4a.start()

# %%
k4a.exposure_mode_auto = (True, 100)

# %%
k4a.exposure_mode_auto = False
k4a.exposure = 8330
# k4a.brightness = 1000

# %%
# Get the next capture (blocking function)
capture = k4a.get_capture()
img_color = capture.color

# Display with pyplot
from matplotlib import pyplot as plt
plt.imshow(img_color[:, :, 2::-1]) # BGRA to RGB
plt.show()
# %%
