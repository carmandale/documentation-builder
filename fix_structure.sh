#!/bin/bash
# fix_structure.sh - Fix project structure issues

echo "Fixing project structure..."

# Create missing directories
for dir in logs debug cache knowledge; do
    if [ ! -d "data/$dir" ]; then
        echo "Creating data/$dir directory"
        mkdir -p "data/$dir"
    fi
done

# Initialize cache files if missing
for file in url_cache.json discovered_samples.json; do
    if [ ! -f "data/cache/$file" ]; then
        echo "Initializing data/cache/$file"
        echo "[]" > "data/cache/$file"
    fi
done

# Clean up malformed debug files
echo "Cleaning up malformed debug files..."
cd data/debug || exit
for file in .html _initial.html _structure.html; do
    if [ -f "$file" ]; then
        echo "Removing malformed file: $file"
        rm "$file"
    fi
done

echo "Structure fixes complete" 