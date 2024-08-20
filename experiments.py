import rational_monitor
import os
import subprocess

Timeout = 3 # seconds

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
with open('res.txt', 'w') as file:
    file.write('')
with open('tmp-res.txt', 'w') as tmp_res:
    for i in range(0, 4):
        results[f'metric_{i}'] = {'True': 0, 'False': 0, 'Unknown': 0, 'Undefined': 0, 'Unknown(butitwon\'teverbeFalse)': 0, 'Unknown(butitwon\'teverbeTrue)': 0}
        with open('props.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.split('$ ')
                for trace in traces:
                    with open('tmp.txt', 'w') as file_t:
                        file_t.write(trace)
                    try:
                        # Run the code
                        run_process = subprocess.run(['python3', './rational_monitor.py', line[0], line[1], line[2], line[3], line[4], '100000', 'tmp.txt', f'metrics.metric_{i}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=Timeout)
                        # print('code: ' + str(run_process.returncode))
                        res = run_process.stdout.decode()
                        # print(res)
                        verdict = res[res.index('Verdict: ')+9:].replace(' ', '').replace('\n', '')
                            # verdict = rational_monitor.main(['', line[0], line[1], line[2], line[3], line[4], '100000', 'tmp.txt', f'metric_{i}'])
                        if verdict in results[f'metric_{i}']:
                            results[f'metric_{i}'][verdict] += 1
                    except subprocess.TimeoutExpired:
                        break
                    except Exception as e:
                        break
                tmp_res.write(str(results) + '\n')
        with open('res.txt', 'a') as file:
            file.write(f'metric_{i}' + str(results[f'metric_{i}']))
            file.write('\n')
print(results)