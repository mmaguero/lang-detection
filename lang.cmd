#!/bin/bash
echo $(date '+%Y-%m-%d %H:%M:%S')

if [ "$1" = "" ]; then
  for filename in ../../guarani-tweets/out/gn_*utc.csv; do
    [ -e "$filename" ] || continue
    filename=$(basename $filename)
    echo "$filename"
    python run.py "../../guarani-tweets/out" "$filename" --detect_language --guarani
  done
fi

if [ "$1" = "lang_lookup" ]; then
  for filename in ../../guarani-tweets/out/gn_*utc.csv; do
    [ -e "$filename" ] || continue
    filename=$(basename $filename)
    echo "$filename"
    python run.py "../../guarani-tweets/out" "$filename" "../../guarani-tweets/aux/archivoe-g.txt" --detect_language --lang_lookup
  done
fi

echo $(date '+%Y-%m-%d %H:%M:%S')
