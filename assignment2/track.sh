#!/bin/bash

#Using $HOME as I could not get ~/.local/share/ to work

if [ ! -e "$HOME/.local/share/timer_logfile.log" ]; then
  touch "$HOME/.local/share/timer_logfile.log"
fi
declare -i task=1
logfile="$HOME/.local/share/timer_logfile.log"

function track {
  tag=$( tail -n 1 $logfile )
  if [ $# -gt 2 ]; then
    echo "Illegal number of arguments"
    echo "To start a task: track start [label]"
    echo "label is an optional argument"
    echo "To stop a task: track stop"
    echo "To get status of latest task: track status"
    echo "To get time spent on finished tasks: track log"
  elif [[ $1 == start ]]; then
    #check if task is currently running
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
    if [[ ${tag/%\ */} == LABEL ]]; then
      echo "Currently tracking task $(echo $tag | awk '{print $5}')"
    else
      echo "You don't have an active task"
    fi
  #I may have misunderstood this task, and I'm not writing the time spent to
  #the logfile. I'm parsing the logfile and are writing the time spent on the
  #individual tasks to the user terminal
  elif [[ $1 == log ]]; then
    declare -i counter=1
    #check if third line of task is empty
    while [[ $(sed ''`expr ${counter} + 2`'q;d' $logfile) != "" ]]; do
      #fetch all lines related to task
      start=$(sed ''${counter}'q;d' $logfile | awk '{print $5}' | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
      label=$(sed ''`expr ${counter} + 1`'q;d' $logfile | awk '{print $5}')
      end=$(sed ''`expr ${counter} + 2`'q;d' $logfile | awk '{print $5}' | awk -F: '{ print ($1 * 3600) + ($2 * 60) + $3 }')
      diff=`expr $end - $start`
      #stupid solution to tasks starting and ending on different days
      if [[ diff -lt 0 ]]; then
        (( diff=diff+86400 ))
      fi
      logtime $diff $label
      (( counter=counter+3 ))
    done
  fi
}

function logtime {
  local T=$1
  local L=$2
  local H=$((T/60/60%24))
  local M=$((T/60%60))
  local S=$((T%60))
  #usage of printf to avoid newline
  #checking if value is number or string
  re='^[0-9]+$'
  if ! [[ $L =~ $re ]]; then
    printf 'Task %s: ' $L
  else
    printf 'Task %d: ' $L
  fi
  printf '%02d:' $H
  printf '%02d:' $M
  printf '%02d\n' $S
}
