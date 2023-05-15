from PIL import Image
import numpy as np
import random

# 28 / 5 - wymiary budynku w oknach
# licze od lewego gornego okna

class WindowPatternGenerator:
  def poland_flag_arr(self,top_height,emulate = False):
    poland = [[255,255,255],[220,20,60]]
    out = self.make_flag(poland,top_height)
    return out.flatten()[11*3:] if not emulate else self.emulate(out)

  def ukraine_flag_arr(self,top_height,emulate = False):
    ukraine = [[0,87,183],[255,221,0]]
    out = self.make_flag(ukraine,top_height)
    return out.flatten()[11*3:] if not emulate else self.emulate(out)
  
  def rainbow_arr(self,emulate = False):
    out = self.make_random_colors()
    return out.flatten()[11*3:] if not emulate else self.emulate(out)
    
  def make_flag(self,country,top_height):
    rgb_arr = []
    # two - tone flag
    top_R_color = country[0][0]
    top_G_color = country[0][1]
    top_B_color = country[0][2]
    bottom_R_color = country[1][0]
    bottom_G_color = country[1][1]
    bottom_B_color = country[1][2]

    fifth_floor_non_exsitant_windows = 11
    fifth_floor_remaining_windows = 17
    normal_floor_window_count = 28
    row = []
    # R, G, B - rgb values for lights for one window

    # values for non-existant windows
    for i in range(fifth_floor_non_exsitant_windows):
      row.append(0) # R
      row.append(0) # G
      row.append(0) # B

    for i in range(fifth_floor_remaining_windows):
      row.append(top_R_color) # R
      row.append(top_G_color) # G
      row.append(top_B_color) # B

    rgb_arr.append(row)
    row = []

    # gorny pas flagi
    # i - wiersze
    for _ in range(top_height-1):
      # j - kolumny
      for _ in range(normal_floor_window_count):
        row.append(top_R_color) # R
        row.append(top_G_color) # G
        row.append(top_B_color) # B
      rgb_arr.append(row)
      row = []

    # dolny pas flagi
    for _ in range(5-top_height):
      for _ in range(normal_floor_window_count):
        row.append(bottom_R_color)
        row.append(bottom_G_color)
        row.append(bottom_B_color)
      rgb_arr.append(row)
      row = []

    return np.array(rgb_arr)
  
  def make_random_colors(self):
    rgb_arr = []
    fifth_floor_non_exsitant_windows = 11
    fifth_floor_remaining_windows = 17
    normal_floor_window_count = 28
    row = []

    for _ in range(fifth_floor_non_exsitant_windows*3):
      row.append(0)
    
    for _ in range(fifth_floor_remaining_windows):
      row.append(random.randint(0,255))
      row.append(random.randint(0,255))
      row.append(random.randint(0,255))

    rgb_arr.append(row)
    row = []
    for _ in range(4):
      for _ in range(normal_floor_window_count):
        row.append(random.randint(0,255)) # R
        row.append(random.randint(0,255)) # G
        row.append(random.randint(0,255)) # B
      rgb_arr.append(row)
      row = []

    return np.array(rgb_arr)

  def emulate(self,out):
    out_mod = out
    image_arr = out_mod.reshape(5,28,3).astype(np.uint8)
    windows = Image.fromarray(image_arr)
    windows.show()
    return out.flatten()[12*3:]


win = WindowPatternGenerator()

# win.poland_flag_arr(2,emulate=True)
# win.ukraine_flag_arr(2,emulate=True)
print(win.rainbow_arr())

# print(win.poland_flag_arr(2))
