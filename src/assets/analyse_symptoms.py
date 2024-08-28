#!/usr/bin/env python3
import sys
import fileinput
import json

json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)

json_data = ""
for line in fileinput.input(files="hp_trees.json"):
    json_data = json_data + line
hp_tree_list = json.loads(json_data)



count_symptoms = 0
counts = []
gene = sys.argv[1]
analysis_level = int(sys.argv[2])

for object in patient_list: 
  
  if (object["gene"] == gene and 'symptoms' in object.keys()):
    
    for symptom_code in object["symptoms"]:
        found = False

        #find this symptom in the tree
        for branch in hp_tree_list:
           if branch["code"] == symptom_code:
              level = branch["level"]
              description = branch["description"]
              if (level > analysis_level):
                i = -1
                while (level > analysis_level):
                  i+=1
                  level-=1
                
                #find the description of the parent code
                symptom_code = branch["parents"][i]
                for br in hp_tree_list:
                   if br["code"] == symptom_code:
                      description = br["description"]
                      break

              break
                   
        for item in counts:
           if item["code"] == symptom_code:
              found = True
              item["n"] += 1

        if found == False:
           counts.append(dict(gene = gene, analysis_level = analysis_level, code = symptom_code, description = description, n=1))

        
        count_symptoms += 1


counts = sorted(counts, key=lambda d: d["n"], reverse = True)


print('{0:4d} symptoms in total for gene {1:4s}'.format(count_symptoms, sys.argv[1]))
print('List of symptoms (level {0:1d} HPO codes) by order of frequency: '.format(analysis_level))

for item in counts:
   print('{0:7s} {2:4d} {1:s} '.format(item["code"], item["description"], item["n"]))


