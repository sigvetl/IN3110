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
  elif [ ! -d $src ]; then
    echo "ugyldig src"
  elif [ ! -d $dst ]; then
    echo "ugyldig dst"
  fi

  files=`ls $src`
  echo $files

  dato=$(date +"%F"-"%k"-"%M")
  mkdir $dst/$dato

  for file in $files; do
    mv $src/$file $dst/$dato
  done

}

move $1 $2
