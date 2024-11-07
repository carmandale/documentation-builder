#!/bin/bash
# verify.sh - Project structure and file verification

echo "Verifying project structure and files..."

# Check directory structure
echo -e "\n1. Checking core directories..."
[ -d "data/logs" ] && echo "✓ data/logs directory exists" || echo "✗ data/logs directory missing"
[ -d "data/debug" ] && echo "✓ data/debug directory exists" || echo "✗ data/debug directory missing"
[ -d "data/cache" ] && echo "✓ data/cache directory exists" || echo "✗ data/cache directory missing"
[ -d "data/knowledge" ] && echo "✓ data/knowledge directory exists" || echo "✗ data/knowledge directory missing"

# Check log files
echo -e "\n2. Checking log files..."
[ -f "data/logs/scraper.log" ] && echo "✓ scraper.log in correct location" || echo "✗ scraper.log missing"

# Check for stray files
echo -e "\n3. Checking for stray files..."
find . -maxdepth 1 -type f -name "*.log" | while read -r file; do
    echo "! Found stray log file in root: $file"
done

# Check debug files
echo -e "\n4. Checking debug files..."
find data/debug -type f -name "*.html" | while read -r file; do
    filename=$(basename "$file")
    if [[ "$filename" == ".html" || "$filename" == "_initial.html" || "$filename" == "_structure.html" ]]; then
        echo "! Found malformed debug file: $filename"
    else
        echo "✓ Found debug file: $filename"
    fi
done

# Check cache files
echo -e "\n5. Checking cache files..."
[ -f "data/cache/url_cache.json" ] && echo "✓ URL cache exists" || echo "! URL cache missing"
[ -f "data/cache/discovered_samples.json" ] && echo "✓ Samples cache exists" || echo "! Samples cache missing"

# Validate JSON files
echo -e "\n6. Validating cache files..."
for file in data/cache/*.json; do
    if [ -f "$file" ]; then
        if jq empty "$file" 2>/dev/null; then
            echo "✓ $(basename "$file") is valid JSON"
        else
            echo "! $(basename "$file") contains invalid JSON"
        fi
    fi
done

# Add to validation section
echo -e "\n7. Validating cache content..."
if [ -f "data/cache/discovered_samples.json" ]; then
    sample_count=$(jq length data/cache/discovered_samples.json)
    echo "✓ Cache contains $sample_count samples"
fi