#!/usr/bin/python
"""  timeme: Utility for timing activities
     For help use: python3 timeme -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.0'

import sys
import argparse
import yaml
from datetime import datetime      

YAML_FILE  = "timeme_data.yaml"
TIME_START = 0
TIME_END   = 1

#data = {0: {'name': 'Game dev', 'times': [('22.58', '23.18'), ('23.58', '00.18')]},
#        1: {'name': 'Open source', 'times': [('13.58', '14.18'), ('15.58', '16.18')]}}

def ShowData(data):
   print ("Data:")
#   print (data)
   for actNo, timeData in data.items():
      print ('[%d]: %s:' % (actNo, timeData['name']), end=' '),
      times = timeData['times']
      if (times):
         for i in range(len(times)):
            print ( '%s-%s' % (times[i]['start'], times[i]['end']), end=' ')
      print ()

def FindUnusedActNo(data):
   result = 0
   for actNo, timeData in data.items():
      if (actNo > result):
         break
      result += 1
   return result

def BuildActivity(name):
   return {'name': name, 'times': []}

def FindActivity(actNo):
   try:
      act = data[actNo]
      return act
   except:
      print ("Activity number \"%d\" not found." % actNo)
      sys.exit()

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
              (('-add'), {'required': False, 'help': 'Add activity', 'metavar': 'Activity name'}),
              (('-start'), {'required': False, 'help': 'Start activity', 'metavar': 'Activity number'}),
              (('-end'), {'required': False, 'help': 'End activity', 'metavar': 'Activity number'}),
              (('-cancel'), {'required': False, 'help': 'Cancel activity', 'metavar': 'Activity number'}),]
   parser = argparse.ArgumentParser(description='timeme: Utility for timing activities')
   for positional_args, keyword_args in argsAll:
      parser.add_argument(positional_args, **keyword_args)
   args = vars(parser.parse_args(sys.argv[1:]))
   #print(args)

   noArgs = len(sys.argv) <= 1
   if (noArgs):
      print ("Use -h for help")
   showData = args['show'] or noArgs

   data = LoadYaml()
   currentTime = datetime.now()

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

   if (data):
      if (args['start']):
         actNo = int(args['start'])
         act = FindActivity(actNo)
         htime = {'start': currentTime, 'end': None}
         act['times'].append(htime)
      if (args['end']):
         actNo = int(args['end'])
         act = FindActivity(actNo)
         times = act['times']
         if (len(times) == 0 or not times[-1]['start']):
            print ("Activity=%d: Not started." % actNo)
            print (act)
            sys.exit()
         time = times[-1]
         time['end'] = currentTime
         ellapsed = time['end'] - time['start']
         print("Ellapsed=%s" % ellapsed)
      if (args['cancel']):
         actNo = int(args['cancel'])
         act = FindActivity(actNo)
         times = act['times']
         if (len(times) == 0):
            print ("Activity=%d: Nothing started" % actNo)
            print (act)
            sys.exit()  
         times[-1]['start'] = None

      print("Ok.")
      
      if (showData):
            ShowData(data)

      SaveToYaml(data)
