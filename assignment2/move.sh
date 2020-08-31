#!/bin/sh

function move {
  src="$1"
  dst="$2"

  if [ $# != 2 ]; then
    echo "ugyldig antall argumenter"
    exit 1
  fi

  if [ -d $src ] && [ -d $dst ]; then
    echo "gyldig dir"
  elif [ ! -d $src ] && [ ! -d $dst ]; then
    echo "ugyldige dir"
    exit 1
  elif [ ! -d $src ]; then
    echo "ugyldig src"
    exit 1
  elif [ ! -d $dst ]; then
    echo "ugyldig dst. Vil du opprette dst?\ny/n"
    read input
    while [ $input != y ] && [ $input != n ]; do
      echo "ugyldig dst. Vil du opprette dst?\ny/n"
      read input
    done
    if [ $input = y ]; then
      mkdir $dst
    else
      exit 1
    fi
  fi

  cd $src

  echo "Do you want to move all files or .txt files?\nall/txt"
  read input

  while [ $input != txt ] && [ $input != all ]; do
    echo "Do you want to move all files or .txt files?\nall/txt"
    read input
  done

  if [ $input == txt ]; then
    files=`ls *.txt`
  elif [ $input == all ]; then
    files=`ls`
  fi

  echo $files

  dato=$(date +"%F"-"%k"-"%M")
  mkdir $dst/$dato

  for file in $files; do
    mv $file $dst/$dato
  done

}

move $1 $2
