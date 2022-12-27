#!/bin/bash

P=/var/www/website/
MDBOOK_DIR=/home/pi/.cargo/bin/mdbook

inotifywait \
    --event create --event delete \
    --event modify --event move \
    --format "%f" \
    --monitor \
    --exclude '.*(.*index.md|.*SUMMARY.md)' \
    --recursive \
    ${P}src/ |
while read CHANGED;
do
        echo "$CHANGED"
        python3 ${P}summary_builder.py
        ${MDBOOK_DIR} build ${P}
done
