import rationalMonitor
import os

# Function to list all files in a folder and read each file
def list_and_read_traces(folder_path):
    # Check if the path is a directory
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return
    
    # List all files in the directory
    files = os.listdir(folder_path)
    
    traces = []

    # Iterate through each file
    for file_name in files:
        # Construct the full path to the file
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            try:
                # Open the file and read its contents
                with open(file_path, 'r') as file:
                    contents = file.read()
                    traces.append(contents)
            except Exception as e:
                print(f"Error reading {file_name}: {e}")
                print("-----------------------------")
    return traces

traces = list_and_read_traces('./traces/')
results = {}
for i in range(1, 2):
    results[f'metric_{i}'] = {'True': 0, 'False': 0, 'Unknown': 0, 'Undefined': 0, 'Unknown (but it won\'t ever be False)': 0, 'Unknown (but it won\'t ever be True)': 0}
    with open('props.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('$ ')
            for trace in traces:
                with open('tmp.txt', 'w') as file_t:
                    file_t.write(trace)
                try:
                    verdict = rationalMonitor.main(['', line[0], line[1], line[2], line[3], line[4], 'tmp.txt', f'metric_{i}'])
                    if verdict in results[f'metric_{i}']:
                        results[f'metric_{i}'][verdict] += 1
                except Exception:
                    break
print(results)