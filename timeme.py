#!/usr/bin/python
"""  timeme: Utility for timing activities
     For help use: python3 timeme -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.0'

import sys
import argparse

TIME_START = 0
TIME_END   = 1

data = {0: {'name': 'Game dev', 'times': [('22.58', '23.18'), ('23.58', '00.18')]},
        1: {'name': 'Open source', 'times': [('13.58', '14.18'), ('15.58', '16.18')]}}

      
def ShowData(data):
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
   
if __name__ == '__main__':
   argsAll = [(('--show'), {'required': False, 'help': 'Show activities', 'action': 'store_const', 'const': True}),
              (('-add'), {'required': False, 'help': 'Add activity', 'metavar': 'Activity'})]
   parser = argparse.ArgumentParser(description='timeme: Utility for timing activities')
   for positional_args, keyword_args in argsAll:
      parser.add_argument(positional_args, **keyword_args)
   args = vars(parser.parse_args(sys.argv[1:]))

   print(args)

   if (args['add']):
      act = BuildActivity(args['add'])
      actNo = FindUnusedActNo(data)
      data[actNo] = act;
         
   ShowData(data)

