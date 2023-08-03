#!/bin/bash

# Get the list of changed .cpp files using Git
changed_files=$(git diff --name-only --diff-filter=ACMR "*.cpp")

# Loop through the changed .cpp files
for file in $changed_files; do
    folder=$(dirname "$file")
    md_folder="./$folder/md"
    md_file="./$folder/md/$(basename "$file" .cpp).md"
    readme_file="./$folder/README.md"

    # Check if the md folder exists, if not, create it
    if [ ! -d "$md_folder" ]; then
        mkdir -p "$md_folder"
    fi

    # Step 1: Create/overwrite the .md file and wrap the cpp content
    echo "Creating/overwriting $md_file"
    echo '```cpp' > "$md_file"
    if [ -f "$file" ]; then
        cat "$file" >> "$md_file"
    fi
    echo '```' >> "$md_file"

    # Step 2: Update README.md with the link to the new/modified .md file
    title=$(basename "$file" .cpp | sed -E 's/_/ /g' | awk '{for(i=1;i<=NF;i++) sub(".", substr(toupper($i), 1, 1) , $i)}1')
    link="* [${title}](./md/$(basename "$file" .cpp).md)"

    if [ -f "$md_file" ] && ! grep -qF "$link" "$readme_file"; then
        echo "$link" >> "$readme_file"
    fi
done

echo "Script executed successfully!"
