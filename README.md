TIMEME
===

### Description ###
Utility to time weekly activities.<br>
A local yaml file (timeme_data.yaml) is saved to disk with all activities and their timing.

### Usage ###
For help, run timeme.py -h

### Example ###
```
python3 timeme.py -add Exercise
Ok.
Activity=Exercise
```
```
python3 timeme.py -start 0
Ok.
Activity=Exercise
```
```
python3 timeme.py -end 0
Ellapsed=0:00:03.617549
Ok.
Activity=Exercise
```
```
python3 timeme.py --summary
Showing 1 week(s) in the past.
Wk: 2010-04-29
                     Mon     Tue     Wed     Thu     Fri     Sat     Sun       Total
[0] Exercise         0:00:00 0:11:22 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 | 0:11:22
[1] Read books       0:00:00 0:00:22 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 | 0:00:22
[2] Blog             0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 | 0:00:00
[3] OpenSource       3:00:00 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 0:00:00 | 3:00:00
```
### Clearing data ###
Remove the yaml file to clear all activity data
