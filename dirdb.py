#!/usr/bin/env python2
"""
DirDB - Directory Database

- Create document based database systems inside a filesystem directory structure.
- Uses YAML or JSON as document storage.
- Human friendly for cross-system usage.
- Designed to work with SchemaMan project as a filesystem syncable database.  Export MySQL/Postgres/etc DBs to YAML/JSON files.
- Allows storing databases in a format that is compatible with revision control systems (git/svn/etc)

Intended for use on smaller data sets, such as those found in System and Network Operational Configuration Management systems.

The primary intention of DirDB is so that configuration databases can be exported with minimal example data to share
database contents, as SchemaMan shares their structure/schema, so that systems can be checked into revision control for
historical reference, and most importantly so they can be shared to external sources/other people.

This allows a database to be normally run in a normal DB environment (MySQL/Oracle/PgSQL/Mongo/whatever) and then exported
partially or fully to DirDB, checked into GitHub and shared with other people, who can then load the basic data into
their database of choice (which might be different than yours), allowing flexible sharing of database content which
was normally restricted to a database dump.

Database dumps typically require too much work to be part of a on-going full life-cycle management of a running
operational system (managing many machines), because of the work in migrating data.  This is a component that should
make this process automatible, allowing operations environments to be shared, even while different implementations all
use different software.

Copyright Geoff Howland, 2014.  MIT License.

"""


import sys
import os
import getopt

import utility
from utility.log import log
from utility.error import Error
from utility.path import *


def ProcessAction(action, action_args, command_options):
  """Process the specified action, by it's action arguments.  Using command options."""
  # Get the Datasource Handler
  datasource_handler = GetDatasourceHandler()
  
  # If Action is info
  if action == 'info':
    if action_args:
      Usage('info action does not take any arguments: %s' % action_args)
  
  # Else, Initialize a directory to be a SchemaMan location
  elif action == 'init':
    pass
    
  # Filter
  elif action == 'filter':
    result = datasource_handler.Filter()
  
  # Delete
  elif action == 'delete':
    result = datasource_handler.Delete()
  
  # ERROR
  else:
    Usage('Unknown action: %s' % action)


def Usage(error=None):
  """Print usage information, any errors, and exit.  

  If errors, exit code = 1, otherwise 0.
  """
  output = ''
  
  if error:
    output += '\nerror: %s\n' % error
    exit_code = 1
  else:
    exit_code = 0
  
  output += '\n'
  output += 'usage: %s [options] action <action_args>' % os.path.basename(sys.argv[0])
  output += '\n'
  output += 'Actions:\n'
  output += '\n'
  output += '  put <schema> <source> <json>        Put JSON data into a Schema instance\n'
  output += '  get <schema> <source> <json>        Get Schema instance records from JSON keys\n'
  output += '  filter <schema> <source> <json>     Filter Schema instance records\n'
  output += '  delete <schema> <source> <json>     Delete records from Schema instance\n'
  output += '\n'
  output += 'Options:\n'
  output += '\n'
  output += '  -d <path>, --dir=<path>             Directory for SchemaMan data/conf/schemas\n'
  output += '                                          (Default is current working directory)\n'
  output += '  -y, --yes                           Answer Yes to all prompts\n'
  output += '\n'
  output += '  -h, -?, --help                      This usage information\n'
  output += '  -v, --verbose                       Verbose output\n'
  output += '\n'
  
  
  # STDOUT - Non-error exit
  if exit_code == 0:
    sys.stdout.write(output)
  # STDERR - Failure exit
  else:
    sys.stderr.write(output)
  
  sys.exit(exit_code)


def Main(args=None):
  if not args:
    args = []

  
  long_options = ['dir=', 'verbose', 'help', 'yes']
  
  try:
    (options, args) = getopt.getopt(args, '?hvyd:', long_options)
  except getopt.GetoptError, e:
    Usage(e)
  
  # Dictionary of command options, with defaults
  command_options = {}
  command_options['verbose'] = False
  command_options['always_yes'] = False
  
  
  # Process out CLI options
  for (option, value) in options:
    # Help
    if option in ('-h', '-?', '--help'):
      Usage()
    
    # Verbose output information
    elif option in ('-v', '--verbose'):
      command_options['verbose'] = True
    
    # Always answer Yes to prompts
    elif option in ('-y', '--yes'):
      command_options['always_yes'] = True
    
    # Invalid option
    else:
      Usage('Unknown option: %s' % option)


  # Store the command options for our logging
  utility.log.RUN_OPTIONS = command_options
  
  
  # Ensure we at least have one spec file
  if len(args) < 1:
    Usage('No action specified')
  

  #try:
  if 1:
    ProcessAction(args[0], args[1:], command_options)
    pass
  
  #NOTE(g): Catch all exceptions, and return in properly formatted output
  #TODO(g): Implement stack trace in Exception handling so we dont lose where this
  #   exception came from, and can then wrap all runs and still get useful
  #   debugging information
  #except Exception, e:
  else:
    Error({'exception':str(e)}, command_options)


if __name__ == '__main__':
  #NOTE(g): Fixing the path here.  If you're calling this as a module, you have to 
  #   fix the utility/handlers module import problem yourself.
  sys.path.append(os.path.dirname(sys.argv[0]))
  
  Main(sys.argv[1:])
