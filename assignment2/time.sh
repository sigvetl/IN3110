#!/bin/bash
#source runs script in current environment

declare -i task=1
logfile="./timer_logfile.txt"

function track {
  if [ $# > 2 ]; then
    echo "Illegal number of arguments"
    echo "To start a task: track start [label]"
    echo "label is an optional argument"
    echo "To stop a task: track stop"
    echo "To get status of latest task: track status"
  elif [[ $1 == start ]]; then
    date=$(date +"%a %b %d %T %Z %Y")
    echo "START $date" >> $logfile
    arg1=${2:-$(( task++ ))}
    echo "LABEL This is task $arg1" >> $logfile
    (( task++ ))
  elif [[ $1 == stop ]]; then
    date=$(date +"%a %b %d %T %Z %Y")
    echo "END $date" >> $logfile
  elif [[ $1 == status ]]; then
    tag=$( tail -n 1 $logfile )
    array=( $tag )
    if [[ ${array[0]} == LABEL ]]; then
      echo "Currently tracking task ${array[4]}"
    else
      echo "You don't have an active task"
    fi
  fi
}
