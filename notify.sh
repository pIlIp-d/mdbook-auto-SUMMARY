#!/bin/sh

P=${MDBOOK_DIR}/

builder() {
    echo "Building book index..."
    python "${P}"summary_builder.py
    mdbook build $P
}

# build at start of container
builder

inotifywait \
    --event create --event delete \
    --event modify --event move \
    --format "%f" \
    --monitor \
    --exclude '.*(.*index.md|.*SUMMARY.md)' \
    --recursive \
    ${P}src/ |
while read _;
do
  builder
done
