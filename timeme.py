#!/usr/bin/python
"""  timeme: Utility for timing activities
     For help use: python3 timeme -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.0'

import sys
import argparse
import yaml

YAML_FILE  = "timeme_data.yaml"
TIME_START = 0
TIME_END   = 1

#data = {0: {'name': 'Game dev', 'times': [('22.58', '23.18'), ('23.58', '00.18')]},
#        1: {'name': 'Open source', 'times': [('13.58', '14.18'), ('15.58', '16.18')]}}

      
def ShowData(data):
   print ("Data:")
   for actNo, timeData in data.items():
      print ('[%d]: %s:' % (actNo, timeData['name']), end=' '),
      times = timeData['times']
      if (times):
         for i in range(len(times)):
            print ( '%s-%s' % (times[i][TIME_START], times[i][TIME_END]), end=' ')
      print ()

def FindUnusedActNo(data):
   result = 0
   for actNo, timeData in data.items():
      if (actNo > result):
         break
      result += 1
   return result

def BuildActivity(name):
   return {'name': name, 'times': None}

def SaveToYaml(data):
   stream = open(YAML_FILE, 'w')
   yaml.dump(data, stream)
   # print (yaml.dump(data))  # Output the document to the screen.

def LoadYaml():
   try:
      stream = open(YAML_FILE, 'r')
      data = yaml.load(stream)
   except:
      print ("Data file \"%s\" not found. Create actvities with -add." % YAML_FILE)
      data = None
   return data
   
if __name__ == '__main__':

   # Parsing arguments
   argsAll = [(('--show'), {'required': False, 'help': 'Show activities', 'action': 'store_const', 'const': True}),
              (('-add'), {'required': False, 'help': 'Add activity', 'metavar': 'Activity'})]
   parser = argparse.ArgumentParser(description='timeme: Utility for timing activities')
   for positional_args, keyword_args in argsAll:
      parser.add_argument(positional_args, **keyword_args)
   args = vars(parser.parse_args(sys.argv[1:]))
   # print(args)

   noArgs = len(sys.argv) <= 1
   if (noArgs):
      print ("Use -h for help")
   showData = args['show'] or noArgs

   data = LoadYaml()

   if (args['add']):
      act = BuildActivity(args['add'])
      if (data):
         actNo = FindUnusedActNo(data)
         data[actNo] = act;
      else:
         data = {0: None}
         data[0] = act
         print ("First entry in data: %s" % data)
      showData = True

   if (showData and data):
      ShowData(data)

   if (data):
      SaveToYaml(data)
