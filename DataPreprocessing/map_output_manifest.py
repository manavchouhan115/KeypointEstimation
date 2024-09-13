#import json

# Define the path to your JSON manifest file
#file_path = r"C:\Users\Manav\Desktop\KeypointEstimation\stick-labelling-2\manifests\output\output.manifest"

# Open and load the JSON file
#with open(file_path, 'r') as file:
#    manifest_data = json.load(file)

# Print the content of the manifest file
#print(manifest_data)


import os

# Specify the directory path
directory = r'C:\Users\Manav\Desktop\KeypointEstimation\video_stills'

# List all directories in the given directory
directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
print(len(directories))
# Print the directories
count = 0
map_output_dict = {}

for d in directories:
	if not d.startswith("clip"):
		map_output_dict[d] = count
		count+=1
    #print(d)
for x in range(1,5):
	map_output_dict["clip_" + str(x)] = count
	count+=1
print(map_output_dict)
	