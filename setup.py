"""
Mercier Wilfried - IRAP

Setting up the program at startup.
"""

import os
import os.path as     opath
from   yaml    import load, dump
from   yaml    import Loader, Dumper

def default(outname, *args, **kwargs):
   '''
   Utility function writing a default YAML setting file if none is found.

   Parameters
   ----------
      outname : str
         name of the output YAML file
   '''

   configuration = {'font'    : 'fixed,30,-1,5,75,0,0,0,0,0',
                    'color'   : '#ffdd1c'
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

   output         = dump(configuration, Dumper=Dumper)
   with open(outname, 'w') as f:
      f.write(output)
   return

def init(*args, **kwargs):
   '''
   Initialise code parameters at startup.
   Return the settings dictionnary and an error code (0 if ok, -1 if error).
   '''

   file           = 'settings.yaml'

   # If the file does not exist, a default one is created
   if not opath.isfile(file):
      default(file)

   # Load configuration option from setting file
   with open(file, 'r') as f:
      settings    = load(f, Loader=Loader)

   # If a key is missing, the setting file is saved and a new one is created with default values
   errCode        = 0
   for i in ['font', 'color']:
      if i not in settings.keys():
         print('Error in setting file %s. The key %s was missing. Generating a new default configuration file instead.' %(file, i))
         os.rename(r'%s' %file, r'~%s' %file)
         default(file)
         settings = load(file, Loader=Loader)
         errCode  = -1

   return settings, errCode
