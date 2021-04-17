"""
Mercier Wilfried - IRAP

Setting up the program at startup.
"""

import os
import os.path      as     opath
from   PyQt5.QtCore import QTime
from   yaml         import load, dump, Loader, Dumper

def default(outname, *args, **kwargs):
   '''
   Utility function writing a default YAML setting file if none is found.

   Parameters
   ----------
      outname : str
         name of the output YAML file
   '''

   configuration = {'font'        : 'fixed,30,-1,5,75,0,0,0,0,0',
                    'color'       : '#ffdd1c',
                    'x'           : 0,
                    'y'           : 0,
                    'opacity'     : 1,
                    'blinkPeriod' : '00:00:01',
                    'blinkFreq'   : 100,
                    'blinkNb'     : 3
                   }

   writeConfiguration(outname, configuration)
   return

def writeConfiguration(outname, configuration, *args, **kwargs):
   '''
   Utility function to write the YAML configuration file with the given parameters.

   Parameters
   ----------
      configuration : dict
         dictionnary to be converted into a YAML file
      outname : str
         name of the output YAML file
   '''

   output = dump(configuration, Dumper=Dumper)
   with open(outname, 'w') as f:
      f.write(output)
   return

def init(scriptDir, *args, **kwargs):
   '''
   Initialise code parameters at startup.

   Parameters
   ---------
      sriptDir : str
         location of the code and the yaml file(s)

   Return the settings dictionnary and an error code (0 if ok, -1 if error).
   '''

   file           = opath.join(scriptDir, 'settings.yaml')

   # If the file does not exist, a default one is created
   if not opath.isfile(file):
      default(file)

   # Load configuration option from setting file
   with open(file, 'r') as f:
      settings    = load(f, Loader=Loader)

   # If a key is missing, the setting file is saved and a new one is created with default value
   errCode        = 0
   for i in ['font', 'color', 'x', 'y', 'opacity', 'blinkPeriod', 'blinkFreq', 'blinkNb']:
      if i not in settings.keys():
         print('Error in setting file %s. The key %s was missing. Generating a new default configuration file instead.' %(file, i))

         # Save copy
         path, newname = opath.split(file)
         newname       = opath.join(path, r'~%s' %newname)
         os.rename(file, newname)

         # Generate and load new default settings
         default(file)
         settings = load(file, Loader=Loader)
         errCode  = -1

   ################################################
   #               Check parameters               #
   ################################################

   # X coordinate
   if not isinstance(settings['x'], int) or settings['x'] < 0:
      print('Given x coordinate is < 0 or is not an int. Using 0 as default value instead.')
      settings['x'] = 0
   else:
      settings['x'] = int(settings['x'])

   # Y coordinate
   if not isinstance(settings['y'], int) or settings['y'] < 0:
      print('Given y coordinate is < 0 or is not an int. Using 0 as default value instead.')
      settings['y'] = 0
   else:
      settings['y'] = int(settings['y'])

   # Opacity
   if not isinstance(settings['opacity'], (int, float)) or settings['opacity'] < 0 or settings['opacity'] > 1:
      print('Given opacity is not in the range [0, 1] or is not an int/float. Using 1 as default value instead.')
      settings['opacity']      = 1

   # Period is changed from a string to a PyQt Qtime object
   period = QTime().fromString(settings['blinkPeriod'])
   if period.isNull():
      print('Given blinking period could not be broadcasted to a valid PyQt QTime object. Using 1s as default value instead.')
      settings['blinkPeriod']  = Qtime(0, 0, 1)
   else:
      settings['blinkPeriod']  = period

   # Blinking frequency
   if not isinstance(settings['blinkFreq'], (int, float)):
      print('Given bliking frequency is not an int/float. Using 100ms as default value instead.')
      settings['blinkFreq']    = 100
   else:
      if settings['blinkFreq'] < 50:
         print('Given blinking frequency is below minimum value. Clipping to 50ms as default value instead.')
         settings['blinkFreq'] = 50
      elif settings['blinkFreq'] > 10000:
         print('Given bliking frequency is above maximum value. Clipping to 10s as default value instead.')
         settings['blinkFreq'] = 10000
      else:
         settings['blinkFreq'] = int(settings['blinkFreq'])

   # Blinking number
   if not isinstance(settings['blinkNb'], int) or settings['blinkNb'] <= 0:
      print('Given blinking number is <= 0 or is not an int. Using 3 as default value instead.')
      settings['blinkNb']      = 3

   return settings, errCode
