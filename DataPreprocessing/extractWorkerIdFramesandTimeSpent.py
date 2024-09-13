import json
import os

worker_Ids = []
framesCount = []
json_files=[]
timeSpentInSecs = []
path_to_json = 'C:\\Users\\Manav\\Desktop\\KeypointEstimation\\stick-labelling-2\\annotations\\worker-response\\iteration-1\\'
for files in os.listdir(path_to_json):
	for file in os.listdir(path_to_json+files):
		#print(files)
		if file.endswith('.json'):
			json_files.append(file)
			#print(file)
			with open(path_to_json+files+"\\"+file) as f:
				json_data = json.load(f)

			worker_Ids.append(json_data["answers"][0]["workerId"])
			timeSpentInSecs.append(json_data["answers"][0]["timeSpentInSeconds"])
			framesCount.append(len(json_data["answers"][0]["answerContent"]["trackingAnnotations"]["frameData"]["entries"]))
print(timeSpentInSecs)
print(sum(timeSpentInSecs))

#myset = set(worker_Ids)
#print(list(myset))

diction = {"private.ap-southeast-2.38705c61b300087f":0,"private.ap-southeast-2.7e9a5da2a3b70b60":0,"private.ap-southeast-2.b118f28952ec4945":0}
dictionTime = {"private.ap-southeast-2.38705c61b300087f":0,"private.ap-southeast-2.7e9a5da2a3b70b60":0,"private.ap-southeast-2.b118f28952ec4945":0}
for x in range(0,71):
	#print(worker_Ids[x])
	#print(framesCount[x])
	diction[worker_Ids[x]] += framesCount[x]
	dictionTime[worker_Ids[x]] += timeSpentInSecs[x]
print(diction)
print(dictionTime)



#print(json_files)  # for me this prints ['foo.json']