#!/usr/bin/python
"""  timeme.py: Utility for timing activities
     For help use: python3 timeme.py -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.0'

'''
  TODOs:
  [X] Remove the need to specify wk_act in summary
  [X] Show week start when presenting summary
  [X] Print actName in summary
  [X] Improve TimeToWkNumber (* 100)
  [X] Improve ShowData()
  [ ] Support adding activities not based on current time
  [ ] Show week start date in summary
  [ ] Code is assuming that actNos are continuous
  [ ] Add support for summary based on time of day
  [ ] Readme
'''

import sys
import argparse
import yaml
from datetime import datetime, timedelta

YAML_FILE = 'timeme_data.yaml'
SUMMARY_WK_ACT = 'wk_act'
YEAR0 = 2019

def SaveToYaml(actData):
   stream = open(YAML_FILE, 'w')
   yaml.dump(actData, stream)

def LoadYaml():
   try:
      stream = open(YAML_FILE, 'r')
      actData = yaml.load(stream)
   except:
      print ("File \"%s\" not found. Create actvities with -add." % YAML_FILE)
      actData = None
   return actData

def ShowData(actData):
   for actNo, act in actData.items():
      print ('[%d]: %s' % (actNo, act['name']))
      times = act['times']
      if (times):
         for i in range(len(times)):
            print('start:%s  end:%s' % (times[i]['start'], times[i]['end']))

def FindUnusedActNo(actData):
   result = 0
   for actNo in actData.keys():
      if (actNo > result):
         break
      result += 1
   return result

def BuildActivity(name):
   return {'name': name, 'times': []}

def FindActivity(actData, actNo):
   try:
      act = actData[actNo]
      return act
   except:
      print ("Activity number \"%d\" not found." % actNo)
      sys.exit()

def FindMaxMinTime(actData):
   result = {'min': datetime.max, 'max': datetime.min}
   for actNo, act in actData.items():
      times = act['times']
      for i in range(len(times)):
         time = times[i]['start']
         if (time < result['min']):
            result['min'] = time
         if (time > result['max']):
            result['max'] = time
   return result
      
def GetWkNumber(dtime):
   yr = dtime.year
   yrNo = yr - YEAR0
   wk = dtime.isocalendar()[1] - 1 # Note: isocalendar()[1] gives us the week number
   wkNo = yrNo * 53 + wk # Note: There are max 53 weeks per year
   return wkNo

def BuildAndPrintAllWks(actData):
   actCount = len(actData.items())

   # Find wkCount and baseWk
   timeRange = FindMaxMinTime(actData)
   baseWk = GetWkNumber(timeRange['min'])
   wkCount = 1 + (GetWkNumber(timeRange['max']) - baseWk)
   '''
   Note: Example of how data could like:
   actData = {0: {'name': actName, 'times': [{'start': 01:00, 'end': 02:00}, {'start': 03:00, 'end': 04:00}],
              1: {'name': actName, 'times': [{'start': 01:00, 'end': 02:00}, {'start': 03:00, 'end': 04:00}]}

   allWks = [wk0, wk1, wk2]
   wk0 = [[00:00, 00:00, 00:00], [00:00, 00:00, 00:00], [00:00, 00:00, 00:00], [00:00, 00:00, 00:00], ...]
   '''
   print("actCount=%d wkCount=%d" % (actCount, wkCount))
   
   # Initialize allWks[]
   allWks = []
   for i in range(wkCount):  # Note: We assume that actNos in actData are continuous
      wk = []
      allWks.append(wk)
      for d in range(7):
         day = []
         wk.append(day)
         for k in range(actCount):
            day.append(timedelta(0))

   # Fill allWks[] with actData
   for actNo, act in actData.items():
      times = act['times']
      for i in range(len(times)):
         time = times[i]
         if (time['end']): # Only edit time in activities that have ended
            ellapsed = time['end'] - time['start']
            wkIdx = GetWkNumber(time['start']) - baseWk
            dIdx = time['start'].weekday()
            wk = allWks[wkIdx]
            wk[dIdx][actNo] += ellapsed

   # Print allWks[]
   for i in range(len(allWks)):
      print ("Wk: %d " % (baseWk + i)) # TODO: Use week start date instead
      PrintWk(allWks[i], actData)

def PrintWk(wkData, actData):
   #TODO: we arbitrarily use 20 as length for alignment- use instead len(longest(actName))
   print('{:<20s}{:<0s}'.format('', ' Mon     Tue     Wed     Thu     Fri     Sat     Sun     Total'))
   for actNo in actData.keys():
      sAct = '[%d] %s' % (actNo, actData[actNo]['name'])
      sTimes = ''
      total = timedelta(0)
      for d in range(7):
         time = wkData[d][actNo]
         total += time
         sTimes += ' %s' % str(time)[:7]
      sTimes += ' %s' % str(total)[:7]
      print('{:<20s}{:<0s}'.format(sAct, sTimes))
      
if __name__ == '__main__':

   argsAll = [(('--show'), {'required': False, 'help': 'Show activities', 'action': 'store_const', 'const': True}),
              (('--summary'), {'required': False, 'help': 'Summary of activities', 'action': 'store_const', 'const': True}),
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

   actData = LoadYaml()
   currentTime = datetime.now()
   act = None
   if (actData):
      if (args['start']):
         actNo = int(args['start'])
         act = FindActivity(actData, actNo)
         newtime = {'start': currentTime, 'end': None}
         times = act['times']
         if (len(times) == 0 or times[-1]['end']):
            act['times'].append(newtime) # append only if we have finished previous or is first
         else:
            times[-1] = newtime
      if (args['end']):
         actNo = int(args['end'])
         act = FindActivity(actData, actNo)
         times = act['times']
         if (len(times) == 0 or not times[-1]['start']):
            print ("Activity=%d: Not started." % actNo)
            print (act)
            sys.exit()
         time = times[-1]
         time['end'] = currentTime
         ellapsed = time['end'] - time['start']
         print("Ellapsed=%s" % str(ellapsed))
      if (args['cancel']):
         actNo = int(args['cancel'])
         act = FindActivity(actData, actNo)
         times = act['times']
         if (len(times) == 0):
            print ("Activity=%d: Nothing started" % actNo)
            print (act)
            sys.exit() 
         del times[-1]
      if (args['summary']):
         BuildAndPrintAllWks(actData)

   if (args['add']):
      act = BuildActivity(args['add'])
      if (actData):
         actNo = FindUnusedActNo(actData)
         actData[actNo] = act;
      else:
         actData = {0: None}
         actData[0] = act
         print ("First entry in actData: %s" % actData)
      showData = True

   if (act):
      print("Ok.")
      print("Activity=%s" % act['name'])
      
   if (showData):
      ShowData(actData)

   SaveToYaml(actData)
