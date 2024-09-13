import os
import shutil

# Set the source and destination directories
source_dir = r"C:\Users\Manav\Desktop\KeypointEstimation\video_stills"
destination_dir = r"C:\Users\Manav\Desktop\KeypointEstimation\codebase\filtered_images"

# List of image file extensions to look for
image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')

#code to create the map from video stills images to the label output folder
# Specify the directory path
directory = r'C:\Users\Manav\Desktop\KeypointEstimation\video_stills'

# List all directories in the given directory
directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
# Print the directories
count = 0
map_output_dict = {}

for d in directories:
    if not d.startswith("clip"):
        map_output_dict[d] = count
        count+=1
for x in range(1,5):
    map_output_dict["clip_" + str(x)] = count
    count+=1
#print(map_output_dict)


def copy_images_with_suffix(source, destination):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Traverse all subdirectories
    for root, dirs, files in os.walk(source):
        parent_dir_name = os.path.basename(root)  # Get the current directory name

        # Process all the files in the current directory
        for file in files:
            if file.lower().endswith(image_extensions):  # Check if the file is an image
                # Get the full file path
                file_path = os.path.join(root, file)
                
                # Create the new file name by adding parent directory name as a suffix
                new_file_name = str(map_output_dict[parent_dir_name]) + "_" + os.path.splitext(file)[0] + os.path.splitext(file)[1]
                
                # Define the destination path for the renamed image
                dest_file_path = os.path.join(destination, new_file_name)

                # Copy the image file to the destination
                shutil.copy2(file_path, dest_file_path)
                print(f"Copied: {file_path} to {dest_file_path}")

# Call the function to start the process
copy_images_with_suffix(source_dir, destination_dir)
