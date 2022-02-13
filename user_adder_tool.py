import sys
import os
from categories import Categories

#TODO: check user input
#TODO: loop interval needs to come from an external file for both main and this tool

from user import User
from database_api import DatabaseAPI
import datetime
import argparse

loop_interval = 60
parser = argparse.ArgumentParser(description='')
parser.add_argument('-n', '--name', help='User name')
parser.add_argument('-e', '--email', help='User email address')
parser.add_argument('-c', '--category', help='User preference for news category')
parser.add_argument('-t', '--timing', help='User mail timing (ASAP, Daily, or Weekly')
parser.add_argument('-td', '--day', help='User preference for email timing (day of the week)')
parser.add_argument('-th', '--hour', help='User preference for email timing (hour of the day)'
'Hour for the email to be sent (relevant for weekly and daily timing')

args = parser.parse_args()

entry_viable = True

cat = Categories()
bad_arg = ''
if args.name is None:
    entry_viable = False
    bad_arg += ' name'
if args.email is None:
    entry_viable = False
    bad_arg = ' email'
if args.category is None or args.category not in cat.key_words.keys():
    entry_viable = False
    bad_arg += ' category'
if args.timing is None:
    entry_viable = False
    bad_arg += ' timing'
else:
    if args.timing.upper() == 'WEEKLY':
        if args.day is None or args.hour is None:
            entry_viable = False
            bad_arg += ' day/hour'
    elif args.timing.upper() == 'DAILY':
        if args.hour is None:
            entry_viable = False
            bad_arg += ' hour'

if not entry_viable:
    print('Issue with:' + bad_arg)
    print('User data is not complete, user not entered into the system')
else:
    database = DatabaseAPI('News_Aggregator_Database.db')
    new_user = User('new_user', loop_interval, name=args.name, email=args.email, category=args.category, timing=args.timing,
                    timing_day=args.day, timing_hour=args.hour, last_update=datetime.datetime.now())

    database.add_user(new_user)
