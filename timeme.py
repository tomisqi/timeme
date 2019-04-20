#!/usr/bin/python
"""  timeme: Utility to keep track of time in activities
     For help use: python3 timeme -h

     Author: Antonio Fiallos (afiallosh@gmail.com)
"""
__version__ = '0.0'

import sys
import argparse

if __name__ == '__main__':
   argsAll = [(('-show'), {'required': False, 'help': 'Show activities', 'action': 'store_const', 'const': True})]
   parser = argparse.ArgumentParser(description='timeme: Utility to keep track of time in activities')
   for positional_args, keyword_args in argsAll:
      parser.add_argument(positional_args, **keyword_args)
   parser.parse_args(sys.argv[1:])

