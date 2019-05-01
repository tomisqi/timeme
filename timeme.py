#!/usr/bin/python
"""  timeme.py: Utility to time weekly activities
     For help use: python3 timeme.py -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.1'

'''
  TODOs:
  [ ] Support adding activities not based on current time
  [ ] Add support for summary based on time of day > export this data
'''
import sys
import argparse
import yaml
from datetime import datetime, timedelta, date

YAML_FILE = 'timeme_data.yaml'
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
      
def GetWkNumber(dt):
   yr = dt.year
   yrNo = yr - YEAR0
   wk = dt.isocalendar()[1] - 1 # Note: isocalendar()[1] gives us the week number
   wkNo = yrNo * 53 + wk # Note: There are max 53 weeks per year
   
   return wkNo

def GetMondayDateTime(dt):
   tmp = dt - timedelta(days=dt.weekday()) # This gives us Monday for any datetime
   return datetime(tmp.year, tmp.month, tmp.day) # New datetime object w/ time=00:00

def DumpActivityData(actData):
   for actNo, act in actData.items():
      print ('[%d]: %s' % (actNo, act['name']))
      times = act['times']
      if (times):
         for i in range(len(times)):
            print('start:%s  end:%s' % (times[i]['start'], times[i]['end']))

def StartActivity(actData, actNo):
   act = FindActivity(actData, actNo)
   newtime = {'start': currentTime, 'end': None}
   times = act['times']
   if (len(times) == 0 or times[-1]['end']):
      act['times'].append(newtime) # Append only if we have finished previous or is first
   else:
      times[-1] = newtime
      
   return act

def EndActivity(actData, actNo):
   act = FindActivity(actData, actNo)
   times = act['times']
   if (len(times) == 0 or not times[-1]['start']):
      print ("Activity=%d: Nothing started." % actNo)
      print (act)
      sys.exit()
   time = times[-1]
   time['end'] = currentTime
   ellapsed = time['end'] - time['start']
   print("Ellapsed=%s" % str(ellapsed))
   
   return act

def CancelActivity(actData, actNo):
   act = FindActivity(actData, actNo)
   times = act['times']
   if (len(times) == 0 or times[-1]['end']):
      print ("Activity=%d: Nothing started" % actNo)
      sys.exit()
   del times[-1]

   return act

def RenameActivity(actData, actNo, newName):
   act = FindActivity(actData, actNo)
   oldName = act['name']
   act['name'] = newName
   print ("Changed: %s -> %s" % (oldName, newName))

   return act

def RemoveActivity(actData, actNo):
   act = FindActivity(actData, actNo)
   del actData[actNo]

   return act

def BuildAndPrintWks(actData, wkCount):
   '''
   Example of how data could like:
   actData = {0: {'name': actName, 'times': [{'start': 01:00, 'end': 02:00}, {'start': 03:00, 'end': 04:00}],
              1: {'name': actName, 'times': [{'start': 01:00, 'end': 02:00}, {'start': 03:00, 'end': 04:00}]}

   wks = [wk0, wk1, wk2]
                Mo     Tue    Wed    Thu    Fri    Sat    Sun  
   wk[i] = {0: [00:00, 00:00, 00:00, 00:00, 00:00, 00:00, 00:00],
            1: [00:00, 00:00, 00:00, 00:00, 00:00, 00:00, 00:00],}
   '''
   actCount = len(actData.items())
   mondayDt = GetMondayDateTime(datetime.now()) # This is the current week's monday
   startDt = mondayDt - timedelta(weeks=wkCount - 1)
   endDt = mondayDt + timedelta(weeks=1) # Go to next monday
   print("Showing %d week(s) in the past." % (wkCount))
   
   # Initialize wks[]
   wks = []
   for i in range(wkCount):
      wk = {}
      wks.append(wk)
      for actNo in actData.keys():
         actSum = []
         wk[actNo] = actSum
         for d in range(7):
            actSum.append(timedelta(0))

   # Fill wks[] with actData
   baseWk = GetWkNumber(startDt)
   for actNo, act in actData.items():
      times = act['times']
      for i in range(len(times)):
         time = times[i]
         if (startDt <= time['start'] and time['start'] < endDt):
            if (time['end']): # Only show time for activities that have ended
               ellapsed = time['end'] - time['start']
               wkIdx = GetWkNumber(time['start']) - baseWk
               dIdx = time['start'].weekday()
               wk = wks[wkIdx]
               wk[actNo][dIdx] += ellapsed

   # Print wks[]
   sevenDaysDelta = timedelta(days=7)
   for i in reversed(range(len(wks))):
      print ("Wk: %s" % (startDt + i * sevenDaysDelta).date())
      PrintWk(wks[i], actData)
      print ()

def PrintWk(wkData, actData):
   print('{:<20s}{:<0s}'.format('', ' Mon     Tue     Wed     Thu     Fri     Sat     Sun       Total'))
   for actNo in actData.keys():
      strAct = '[%d] %s' % (actNo, actData[actNo]['name'])
      strTimes = ''
      total = timedelta(0)
      for d in range(7):
         time = wkData[actNo][d]
         total += time
         strTimes += ' %s' % str(time)[:7]
      strTimes += ' | %s' % str(total)[:7]
      print('{:<20s}{:<0s}'.format(strAct, strTimes))
      
if __name__ == '__main__':

   argsAll = [(('--dump'), {'required': False, 'help': 'Dump data of all activities', 'action': 'store_const', 'const': True}),
              (('--summary'), {'required': False, 'type': int, 'nargs': '?', 'help': 'Summary of activities by week. [wkCount] is used to determine number of weeks from now (default=1)', 'metavar': 'wkCount', 'const': 1, 'default': None}), # Note: if --summary is present but no argument, 1 is assigned. If not present, None is assigned
              (('-add'), {'required': False, 'help': 'Add activity', 'metavar': 'ActivityName'}),
              (('-start'), {'required': False, 'help': 'Start activity', 'metavar': 'ActivityNumber'}),
              (('-end'), {'required': False, 'help': 'End activity', 'metavar': 'ActivityNumber'}),
              (('-cancel'), {'required': False, 'help': 'Cancel activity', 'metavar': 'ActivityNumber'}),
              (('-rename'), {'required': False, 'nargs': 2, 'help': 'Rename activity', 'metavar': ('ActivityNumber','NewName')}),
              (('-remove'), {'required': False, 'help': 'Remove activity', 'metavar': 'ActivityNumber'}),]

   # Setup the argument parser
   parser = argparse.ArgumentParser(description='timeme: Utility to time weekly activities')
   for positional_args, keyword_args in argsAll:
      parser.add_argument(positional_args, **keyword_args)

   # Save result from parser in args
   args = vars(parser.parse_args(sys.argv[1:]))
   # print(args)

   if (len(sys.argv) <= 1):
      print ("Use -h for help")

   actData = LoadYaml()
   currentTime = datetime.now()
   act = None
   if (actData):
      if (args['start']):
         act = StartActivity(actData, int(args['start']))
      if (args['end']):
         act = EndActivity(actData, int(args['end']))
      if (args['cancel']):
         act = CancelActivity(actData, int(args['cancel']))
      if (args['rename']):
         act = RenameActivity(actData, int(args['rename'][0]), args['rename'][1])
      if (args['remove']):
         act = RemoveActivity(actData, int(args['remove']))
      if (args['summary']):
         BuildAndPrintWks(actData, args['summary'])
      if (args['dump']):
         DumpActivityData(actData)

   if (args['add']):
      act = BuildActivity(args['add'])
      if (actData):
         actNo = FindUnusedActNo(actData)
         actData[actNo] = act;
      else:
         actData = {0: None}
         actData[0] = act
         print ("First entry in actData: %s" % actData)

   if (act):
      print("Ok.")
      print("Activity=%s" % act['name'])
      
   SaveToYaml(actData)
