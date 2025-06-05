import os
import re # Import the regular expression module

def load_prompt(folder_path: str, replacements: dict = None, version: int = None) -> str:
    """
    Load a prompt from a .txt file within a specified folder.
    If a version number is provided, it loads that specific version (e.g., "2.txt" for version=2).
    Otherwise, it identifies the latest prompt by looking for files named numerically
    (e.g., "1.txt", "2.txt", "3.txt") and selecting the one with the highest number.

    Args:
        folder_path (str): Relative path to the folder containing prompt files,
                           e.g., "ArticleWriter/Outline"
        replacements (dict): Optional dictionary of placeholder -> value replacements.
        version (int, optional): Specific version number of the prompt to load.
                                 If None, loads the latest version. Defaults to None.

    Returns:
        str: The loaded and optionally formatted prompt.

    Raises:
        FileNotFoundError: If the folder does not exist, no valid prompt files are found,
                           or the specified version file is not found.
        ValueError: If filenames are not in the expected numeric format (should not occur with regex).
    """

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Prompt folder not found: {folder_path}")

    prompt_files = []
    # Regex to match filenames like "1.txt", "123.txt", etc.
    # It captures the number part of the filename.
    file_pattern = re.compile(r"^(\d+)\.txt$")

    for filename in os.listdir(folder_path):
        match = file_pattern.match(filename)
        if match:
            # Convert the numeric part of the filename to an integer
            try:
                version_number = int(match.group(1))
                prompt_files.append((version_number, filename))
            except ValueError:
                # This case should ideally not be reached if regex matches correctly
                print(f"Warning: Could not parse version number from filename: {filename}")
                continue # Skip files that don't have a purely numeric name before .txt

    if not prompt_files:
        raise FileNotFoundError(f"No valid prompt files (e.g., '1.txt', '2.txt') found in {folder_path}")

    # Sort files by version number to easily find specific or latest versions
    prompt_files.sort(key=lambda x: x[0]) # Sort ascending to find specific version by index if needed

    target_filename = None
    if version is not None:
        # User specified a version
        target_filename = f"{version}.txt"
        # Check if this version exists in our collected files
        found_version = False
        for v_num, fname in prompt_files:
            if v_num == version and fname == target_filename:
                found_version = True
                break
        if not found_version:
            raise FileNotFoundError(f"Prompt version {version} ('{target_filename}') not found in {folder_path}")
    else:
        # No version specified, get the latest (highest number)
        # Sort files by version number in descending order to get the latest
        prompt_files.sort(key=lambda x: x[0], reverse=True)
        target_filename = prompt_files[0][1]
    
    # Construct the full path to the target prompt file
    prompt_file_path = os.path.join(folder_path, target_filename)

    # Read the content of the target prompt file
    with open(prompt_file_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    # Perform placeholder replacements if any are provided
    if replacements:
        for placeholder, value in replacements.items():
            prompt = prompt.replace(placeholder, str(value)) # Ensure value is a string

    return prompt