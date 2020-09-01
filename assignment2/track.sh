#!/bin/bash
#source runs script in current environment

declare -i task=1
logfile="./timer_logfile.txt"

function track {
  if [ $# -gt 2 ]; then
    echo $#
    echo "Illegal number of arguments"
    echo "To start a task: track start [label]"
    echo "label is an optional argument"
    echo "To stop a task: track stop"
    echo "To get status of latest task: track status"
  elif [[ $1 == start ]]; then
    #check if task is currently running
    tag=$( tail -n 1 $logfile )
    if [[ ${tag/%\ */} == LABEL ]]; then
      echo "A task is currently running"
      echo "track status to see which one"
    else
      date=$(date +"%a %b %d %T %Z %Y")
      echo "START $date" >> $logfile
      arg1=${2:-$(( task++ ))}
      echo "LABEL This is task $arg1" >> $logfile
    fi
  elif [[ $1 == stop ]]; then
    #check if no tasks are currently running
    if [[ ${tag/%\ */} == END ]]; then
      echo "No task is currently running"
      echo "track start [label] to start a new task"
    else
      date=$(date +"%a %b %d %T %Z %Y")
      echo "END $date" >> $logfile
    fi
  elif [[ $1 == status ]]; then
    tag=$( tail -n 1 $logfile )
    if [[ ${tag/%\ */} == LABEL ]]; then
      echo "Currently tracking task $(echo $tag | awk '{print $5}')"
    else
      echo "You don't have an active task"
    fi
  fi
}
