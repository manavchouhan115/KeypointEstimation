import json
import os
import pandas as pd

json_files =[]
json_data = None
Labels_dataframe = pd.DataFrame(columns=['image_name','small_start_x', 'small_start_y', 'small_end_x', 'small_end_y' , 'big_start_x', 'big_start_y', 'big_end_x', 'big_end_y'])
count = 0
path_to_json = 'C:\\Users\\Manav\\Desktop\\KeypointEstimation\\stick-labelling-2\\annotations\\consolidated-annotation\\output\\'
for files in os.listdir(path_to_json):
	for file in os.listdir(path_to_json+files):
		#print(files)
		if file.endswith('.json'):
			#json_files.append(file)
			#print(file)
			with open(path_to_json+files+"\\"+file) as f:
				json_data = json.load(f)
		frame_list = json_data["tracking-annotations"]
		
		for frame in frame_list:
			small_start_x = None
			small_start_y = None
			small_end_x = None
			small_end_y = None
			big_start_x = None
			big_start_y = None
			big_end_x = None
			big_end_y = None
			objects_list = frame["polylines"]
			if len(objects_list) > 2:
				print("Invalid frame!!!!! More than 2 sticks")

			for objects in objects_list:
				if(objects["object-name"].startswith("big")):
					big_start_x = objects["vertices"][0]['x']
					big_start_y = objects["vertices"][0]['y']
					big_end_x = objects["vertices"][1]['x']
					big_end_y =objects["vertices"][1]['y']
				elif objects["object-name"].startswith("small"):
					#print(objects["vertices"][0])
					small_start_x = objects["vertices"][0]['x']
					small_start_y = objects["vertices"][0]['y']
					small_end_x = objects["vertices"][1]['x']
					small_end_y = objects["vertices"][1]['y']
			#print([files+"\\"+file, small_start_x, small_start_y, small_end_x, small_end_y , big_start_x, big_start_y, big_end_x, big_end_y])
			image_name = files + "_" + frame["frame"]
			Labels_dataframe.loc[count] = [image_name,small_start_x, small_start_y, small_end_x, small_end_y , big_start_x, big_start_y, big_end_x, big_end_y]
			count +=1
print(Labels_dataframe)
print(count)
rows_with_all_none = Labels_dataframe.isna().all(axis=1).sum()
print(rows_with_all_none)

excel_file_loc = r"C:\Users\Manav\Desktop\KeypointEstimation\codebase"
Labels_dataframe.to_excel(excel_file_loc + '\\imageAndLabels.xlsx', index=False)