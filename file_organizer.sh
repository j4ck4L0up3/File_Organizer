#!/bin/bash

# Parse arguments using getopts
OPTS=$(getopt -o d:t:vl:h -l desktop-flag:,trash-flag:,verbose,log:,help -n 'file_organizer.sh' -- "$@")

if [ $? -ne 0 ]; then
  echo "Failed to parse options" >&2
  exit 1
fi

eval set -- "$OPTS"

# initialize variables 
DESKTOP_FLAG=""
TRASH_FLAG=""
VERBOSE=false
LOG=""
HELP=false

# set option to positional arg or boolean if found
while true; do
  case "$1" in
    -d | --desktop-flag)
      DESKTOP_FLAG="$2"
      shift 2
      ;;
    -t | --trash-flag)
      TRASH_FLAG="$2"
      shift 2
      ;;
    -v | --verbose)
      VERBOSE=true
      shift
      ;;
    -l | --log)
      LOG="$2"
      shift 2
      ;;
    -h | --help)
      HELP=true
      shift
      ;;
    --)
      shift
      break
      ;;
    *)
      echo "Internal error"
      exit 1
      ;;
  esac
done

if [ "$HELP" = true ]; then
  python3 -c "import script; script.format_menu(script.OPTIONS, 40, 5)"
fi
