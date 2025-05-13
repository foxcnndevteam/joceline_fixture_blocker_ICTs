import sys
from gui.assets import get_asset

def get_help() -> str:
  app_name = sys.argv[0].replace('./', '')
  help_data_dir = get_asset('commands/help.txt')
  
  with open(help_data_dir) as file_help:
    data_help = file_help.read()
    data_help = data_help.replace('${{ process_name }}', app_name)
    print(data_help)
