import json
import os
# Prepare the new JSON format
new_data = []

# Script to convert Seqlabel.json in to the demo data of format
    # {
    #     "frame_name": "frame_0002.jpg",
    #     "x1": 695,
    #     "y1": 354,
    #     "x2": 726,
    #     "y2": 745,
    #     "x3": 1104,
    #     "y3": 195,
    #     "x4": 1132,
    #     "y4": 852
    # },
    # x1,y1 are the top coordinates for small sticks, x3,y3 top coordinates of big stick

#Add the path to the stick-labels-2-main/annotations/consolidated-annotation/output 
# containing all the SeqLabel.json files
path_to_json = path = os.path.join('stick-labels-2-main','annotations','consolidated-annotation','output')


for files in os.listdir(path_to_json):
    for file in os.listdir(os.path.join(path_to_json,files)):
        #print(files)
        if file.endswith('.json'):
            with open(os.path.join(path_to_json,files,file)) as f:
                data = json.load(f)
            for annotation in data["tracking-annotations"]:
                # List to hold big and small stick details for the current frame
                big_coords = None
                small_coords = None
                frame_name = annotation["frame"]
                for polyline in annotation["polylines"]:
                    object_name = polyline["object-name"]
                    vertices = polyline["vertices"]
                    
                    
                    if object_name == "big:1":
                        x1, y1 = vertices[0]["x"], vertices[0]["y"]
                        x2, y2 = vertices[1]["x"], vertices[1]["y"]
                        big_coords = [x1,y1,x2,y2]
                        #frame_details.append(big_stick_data)
                    
                    elif object_name == "small:1":
                        x1, y1 = vertices[0]["x"], vertices[0]["y"]
                        x2, y2 = vertices[1]["x"], vertices[1]["y"]
                        small_coords = [x1,y1,x2,y2]

                #Rearranging the coordinates
                if(big_coords == None or small_coords ==None):
                    continue
                
                big_x1, big_y1, big_x2, big_y2 = (
                    (big_coords[0], big_coords[1], big_coords[2], big_coords[3])
                    if big_coords[0] < big_coords[2]
                    else (big_coords[2], big_coords[3], big_coords[0], big_coords[1])
                )
                small_x1, small_y1, small_x2, small_y2 = (
                    (small_coords[0], small_coords[1], small_coords[2], small_coords[3])
                    if small_coords[0] < small_coords[2]
                    else (small_coords[2], small_coords[3], small_coords[0], small_coords[1])
                )

                # Append transformed object
                new_data.append({"frame_name":frame_name, 
                    "x1": small_x1, "y1": small_y1, "x2": small_x2, "y2": small_y2,
                    "x3": big_x1, "y3": big_y1, "x4": big_x2, "y4": big_y2
                })


                        
# Save the new JSON data
with open('demoCoordinates1.json', 'w') as f:
    json.dump(new_data, f, indent=4)

print("New JSON file created with transformed coordinates!")
