#!/bin/bash

# Get the list of changed .py files using Git
changed_files=$(git diff --name-only --diff-filter=ACMR "*.py")
untracked_files=$(git ls-files --others --exclude-standard "*.py")
staged_files=$(git diff --name-only --cached "*.py")

echo "staged files: $staged_files"

# Combine the lists of changed, untracked, and staged files
all_files_string="$changed_files"$'\n'"$untracked_files"$'\n'"$staged_files"

# Convert the string of filenames into an array of filenames
IFS=$'\n' read -r -d '' -a all_files <<< "$all_files_string"

# Echo all the elements of the array
echo "all files: ${all_files[@]}"

# Loop through the changed .py files
for file in "${all_files[@]}"; do
    if [ -z "$file" ]; then
        continue  # Skip empty lines
    fi

    echo "Processing $file"
    folder=$(dirname "$file")
    md_folder="./$folder/md"
    md_file="./$md_folder/$(basename "$file" .py).md"
    readme_file="./$folder/README.md"

    # Check if the md folder exists, if not, create it
    if [ ! -d "$md_folder" ]; then
        mkdir -p "$md_folder"
    fi

    # Step 1: Create/overwrite the .md file and wrap the Python content
    echo "Creating/overwriting $md_file"
    echo '```python' > "$md_file"
    if [ -f "$file" ]; then
        cat "$file" >> "$md_file"
    fi
    echo '```' >> "$md_file"

    # Step 2: Update README.md with the link to the new/modified .md file
    title=$(basename "$file" .py | sed -E 's/_/ /g' | awk '{for(i=1;i<=NF;i++) sub(".", substr(toupper($i), 1, 1) , $i)}1')
    link="* [${title}](./md/$(basename "$file" .py).md)"

    if [ -f "$md_file" ] && ! grep -qF "$link" "$readme_file"; then
        echo "$link" >> "$readme_file"
    fi
done

echo "Script executed successfully!"
