from ctypes import *
import os 
  
# locating the 'libsample.so' file in the 
# same directory as this file 
_file = 'libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file, ))) 
_mod = cdll.LoadLibrary(_path) 