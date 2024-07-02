import os
import random
import string
import sys


# Function to remove all files from a folder
def remove_files_in_folder(folder_path):
    # Check if the path is a directory
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return
    
    # List all files in the directory
    files = os.listdir(folder_path)
    
    # Iterate through each file and delete it
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        try:
            # Check if it's a file (not a directory) and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted {file_name}")
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

# Function to generate and write trace files with unique letters per line
def generate_trace_files(folder_path, num_files, max_length):
    # Create the 'traces' folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    remove_files_in_folder(folder_path)
    
    # Define possible letters (lowercase) for generating content
    letters = list(string.ascii_lowercase)
    
    for i in range(1, num_files + 1):
        # Generate a random length for the trace (between 1 and 10 lines)
        num_lines = random.randint(1, max_length)
        
        # Generate content for the trace
        content = []
        for _ in range(num_lines):
            # Generate a random line of unique letters separated by commas
            line_length = random.randint(1, 5)  # Random length for each line
            unique_letters = random.sample(letters, min(line_length, len(letters)))
            line = ','.join(unique_letters)
            content.append(line)
        
        # Write the content to a file
        file_name = f"trace_{i}.txt"
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'w') as file:
            file.write('\n'.join(content))
        
        print(f"Generated {file_name} with {num_lines} lines.")

def main(args):
    generate_trace_files('./traces/', int(args[1]), int(args[2]))

if __name__ == '__main__':
    main(sys.argv)