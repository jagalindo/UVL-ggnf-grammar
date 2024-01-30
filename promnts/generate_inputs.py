import json
import itertools
import os

def concatenate_files(file_paths, output_path):
    # Concatenate the contents of the files
    content = ''
    for path in file_paths:
        with open(path, 'r') as file:
            content += file.read() + '\n\n'  # Adding a newline for separation
    # Write the concatenated content to the output file
    with open(output_path, 'w') as file:
        file.write(content)

def find_combinations_and_concatenate(base_path, file_path, threshold):
    # Load JSON data from file
    with open(file_path, 'r') as file:
        file_data = json.load(file)

    # Separate the mandatory file and the rest
    mandatory_file_name, mandatory_file_value = "0.header.txt", file_data.pop("0.header.txt")

    # Convert the remaining JSON data into a list of tuples (filename, value)
    items = [(k, v) for k, v in file_data.items()]

    # Create a directory for the output files
    output_dir = os.path.join(base_path, str(threshold))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dictionary to store combinations and their sums
    combinations_dict = {}
    
    # Generate all combinations, always including the mandatory file
    for r in range(1, len(items) + 1):
        for combo in itertools.combinations(items, r):
            total_value = sum(item[1] for item in combo) + mandatory_file_value
            if total_value <= threshold:
                # Prepare file paths for concatenation
                file_paths = [os.path.join(base_path, mandatory_file_name)] + [os.path.join(base_path, item[0]) for item in combo]
                # Output file path
                output_file_path = os.path.join(output_dir, f"{total_value}.txt")
                # Concatenate and save the files
                concatenate_files(file_paths, output_file_path)
                print(f"Saved: {output_file_path}")

                # Add the combination to the dictionary
                combinations_dict[total_value] = [mandatory_file_name] + [item[0] for item in combo]

    # Save the combinations dictionary as JSON
    json_output_path = os.path.join(output_dir, "combinations.json")
    with open(json_output_path, 'w') as json_file:
        json.dump(combinations_dict, json_file, indent=4)

    print(f"Combinations JSON saved: {json_output_path}")

# Base path where the files are located
base_path = './promnts_no_ctc/'  # Replace with the path to your files

# Path to the JSON file
file_path = os.path.join(base_path, 'tokens.json')  # JSON file should be in the same directory as the files

# Set the threshold values
threshold_values = [256,512,1024,2048]  # Change this value as needed

# Find valid combinations and concatenate files
for threshold in threshold_values:
    find_combinations_and_concatenate(base_path, file_path, threshold)