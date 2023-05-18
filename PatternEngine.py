from PIL import Image
import numpy as np
import random
import os

# 28 x 5 - resolution of the "window display"
# starting to count from the top-left corner

class PatternEngine:
  # returns ready-to-send array of pixels
  def arr_from_image(self,name,emulate = False):
    pixel_arr = self._load_image(name)
    # INNY WYMIAR NA TESTY!!!
    return self._RGB_to_RBG(pixel_arr).flatten()[10*3:] if not emulate else self.emulate(pixel_arr)

  # prints image on the terminal - big=True for single image display
  def print_on_terminal(self,name,big = False):
    pixel_arr = self._load_image(name)
    if big:
      for row in pixel_arr:
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
    else:
      for row in pixel_arr:
        for pixel in row:
          self._print_pixel(pixel)
        print()
  
  def print_color_on_terminal(self,pixel,big = False):
    pixel_arr = np.reshape([list(pixel) for _ in range(140)],(5,28,3))
    if big:
      for row in pixel_arr:
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
        for pixel in row:
          self._print_pixel(pixel)
          self._print_pixel(pixel)
          self._print_pixel(pixel)
        print()
    else:
      for row in pixel_arr:
        for pixel in row:
          self._print_pixel(pixel)
        print()
  # returns ready-to-send array of randomly colored pixels
  def random_colors_arr(self,emulate = False):
    out = self._make_random_colors()
    return out.flatten()[12*3:] if not emulate else self.emulate(out)
  
  # returns ready-to-send array of arrays with different frames of the animation
  # def animated_rainbow_arr(self,frames=10):
    # out = []
    # for _ in range(frames):
    #   out.append(self.make_random_colors().flatten()[11*3:])
    # return out
    # pass

  def print_all_patterns(self,path="Grafiki"):
    images = os.listdir(path)
    i = 1
    for image in images:
      if not image.startswith("."):
        print(f"{i}) {image}")
        self.print_on_terminal(image)
        print()
        i+=1

  # safe image loading
  def _load_image(self,name):
    extension = name.split(".")[-1]
    # dozwolone rozszerzenia
    if extension != "jpg" and extension != "png" and extension != "jpeg" and extension != "bmp":
      print("FORBIDDEN EXTENSION - only .bmp .jpg .jpeg .png allowed (bmp gives most accurate results)")
      return np.reshape(np.zeros(28*5*3),(5,28,3))
    image = np.array(Image.open(name))
    # dozwolony rozmiar tylko 5x28
    if np.shape(image)[0]!=5 or np.shape(image)[1]!=28:
      print("FORBIDDEN RESOLUTION - only 5x28 allowed")
      return np.reshape(np.zeros(28*5*3),(5,28,3))
    # konwersja z png na jpg
    if(np.shape(image)[2] == 4):
      image = np.array([[[val for val in pixel[:3]] for pixel in row] for row in image])
    return image

  # conversion from RGB to RBG for the window controller
  def _RGB_to_RBG(self,pixel_arr):
    return np.array([[[pixel[0],pixel[2],pixel[1]] for pixel in row] for row in pixel_arr])

  # prints single pixel on the terminal
  def _print_pixel(self,pixel):
    r,g,b = pixel[0],pixel[1],pixel[2]
    # we use the extended greyscale palette here, with the exception of
    # black and white. normal palette only has 4 greyscale shades.
    ansi = 0
    if r == g and g == b:
      if r < 8:
        ansi = 16
      elif r > 248:
        ansi = 231
      else:
        ansi = int(((r - 8) / 247) * 24) + 232
    else:
      ansi = 16 + (36 * int(r / 255 * 5)) + (6 * int(g / 255 * 5)) + int(b / 255 * 5)

    print(f"\033[38;5;{ansi}m█\033[0;00m",end='')
  
  # generates an array of random colors
  def _make_random_colors(self):
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
        row.append(random.randint(0,255)) # B
        row.append(random.randint(0,255)) # G
      rgb_arr.append(row)
      row = []

    return np.array(rgb_arr)

  # emulates with PIL
  def _emulate(self,out):
    image_arr = out.reshape(5,28,3).astype(np.uint8)
    windows = Image.fromarray(image_arr)
    windows.show()
    return out.flatten()[12*3:]