#!/usr/bin/env python3
import sys
import fileinput
import json


json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)



json_data=""
for line in fileinput.input(files="hp_edges.json"):
    json_data = json_data + line
HPO_edges_list = json.loads(json_data)

json_data=""
for line in fileinput.input(files="hp_nodes.json"):
    json_data = json_data + line
HPO_nodes_list = json.loads(json_data)

count_symptoms = 0
count_added = 0


for patient in patient_list:

      HPO_code_list = []   
      
      parent_code=""
      found = False
      
      for item in HPO_code_list:
         if item["code"] == symptom_code:
            found = True


      if found == False: 
        node_list = list(item["lbl"] for item in HPO_nodes_list["graphs"][0]["nodes"] if symptom_code in item["id"])
        HPO_code_list.append(dict(code = symptom_code, description = node_list[0], level = 0, parents = []))
        
        while parent_code != "0000001":
          edge_list = (item["obj"] for item in HPO_edges_list["graphs"][0]["edges"] if symptom_code in item["sub"]) 
          edge_list = list(edge_list)
          parent_code = edge_list[0][34:]
          HPO_code_list[count_added]["parents"].append(parent_code)
          HPO_code_list[count_added]["level"] += 1
          #print(HPO_code_list[count_added]["code"], HPO_code_list[count_added]["parents"])
          symptom_code = parent_code
        
        count_added += 1
      
      count_symptoms += 1

# Also analyse all parent items
for item in HPO_code_list:
   for symptom_code in item["parents"]:
      parent_code=""
      found = False
      
      for object in HPO_code_list:
          if object["code"] == symptom_code:
             found = True

      if found == False:
        node_list = list(item["lbl"] for item in HPO_nodes_list["graphs"][0]["nodes"] if symptom_code in item["id"])
        HPO_code_list.append(dict(code = symptom_code, description = node_list[0], level = 0, parents = []))
                
        while parent_code != "0000001" and symptom_code != "0000001":
          edge_dict = (el["obj"] for el in HPO_edges_list["graphs"][0]["edges"] if symptom_code in el["sub"]) 
          edge_dict = list(edge_dict)
          parent_code = edge_dict[0][34:]
          HPO_code_list[count_added]["parents"].append(parent_code)
          HPO_code_list[count_added]["level"] += 1
          symptom_code = parent_code
        
        count_added += 1
     


print('{0:4d} symptoms analyzed'.format(count_symptoms))
print('{0:4d} HPO trees written to hp_trees.json'.format(count_added))


# Serialize the python dictionnary to json
json_data = json.dumps(HPO_code_list, indent=4)

# Writing to hp_trees.json
with open("hp_trees.json", "w") as outfile:
    outfile.write(json_data)


