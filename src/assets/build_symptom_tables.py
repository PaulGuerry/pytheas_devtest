#!/usr/bin/env python3
import fileinput
import json
import numpy as np

json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)

json_data = ""
for line in fileinput.input(files="hp_trees.json"):
    json_data = json_data + line
hp_tree_list = json.loads(json_data)

json_data=""
for line in fileinput.input(files="hp_nodes.json"):
    json_data = json_data + line
HPO_nodes_list = json.loads(json_data)

json_data = ""
for line in fileinput.input(files="colourScheme.json"):
    json_data = json_data + line
colour_list = json.loads(json_data)



genes = ["KIF12", "ZFYVE19", "ATP8B1", "SKIC3", "SKIC2", "ABCB11", "ABCB4", "TJP2", "NR1H4", "SLC51A", "USP53", "MYO5B", "SEMA7A", "TMEM199"]
analysis_levels = [1, 2, 3, 4, 5, 6, 7, 8]   
symptom_table = []

diseases = [dict(name = "PFIC1", gene = "ATP8B1", matches = ["PFIC1"]),
            dict(name = "PFIC2", gene = "ABCB11", matches = ["PFIC2"]),
            dict(name = "PFIC3", gene = "ABCB4", matches = ["PFIC3"]),
            dict(name = "PFIC4", gene = "TJP2", matches = ["PFIC4"]),
            dict(name = "PFIC5", gene = "NR1H4", matches = ["PFIC5"]),
            dict(name = "PFIC6", gene = "SLC51A", matches = ["PFIC6"]),
            dict(name = "PFIC7", gene = "USP53", matches = ["PFIC7"]),
            dict(name = "PFIC8", gene = "KIF12", matches = ["PFIC8"]),
            dict(name = "PFIC9", gene = "ZFYVE19", matches = ["PFIC9"]),
            dict(name = "PFIC10", gene = "MYO5B", matches = ["PFIC10"]),
            dict(name = "PFIC11", gene = "SEMA7A", matches = ["PFIC11"]),
            dict(name = "CDG2P", gene = "TMEM199", matches = ["CDG2P"]),
            dict(name = "THES1", gene = "SKIC3", matches = ["THES1"]),
            dict(name = "THES2", gene = "SKIC2", matches = ["THES2"]),
            dict(name = "THES", gene = "SKIC2,3,?", matches = ["THES", "THES1", "THES2"]),
            dict(name = "CLUST", gene = "#####", matches = ["THES", "THES1", "THES2", "PFIC2"]),
            dict(name = "FOCADS", gene = "FOCAD", matches = ["FOCADS"])
            ]

for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   
   for analysis_level in analysis_levels: 
      unique_symptoms = 0
      counts = []
      count_patients = 0
      count_girls = 0

      for object in patient_list: 
        
         if "gene" in object.keys():

            if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
               count_patients += 1 
                
               if ("sex" in object.keys() and object["sex"] == "F"):
                  count_girls += 1

               for HPO_code in object["symptoms"]:
  
                  #find this symptom in the tree 
                  for branch in hp_tree_list:

                     if branch["code"] == HPO_code:
                       
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                           parent_branch = branch["parent_branches"][i]
                           pb_length = branch["branch_lengths"][i]
                           #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                           pb_level = -1
                           found = False
                           level2_code = ""
                           lbl = "<--BLANK-->"

                           #go through all codes in the parent_branch 
                           #starting from the top and working down (from the end of the list and work backwards)
                           #The convention I have chosen to follow is 
                           #pb_level = 0 corresponds to 0000001: All
                           #         = 1 corresponds to 0000118: Phenotypic abnormality
                           #         = 2 gives the colour of all codes lower down the hierarchy
                           for j in range(pb_length, 1, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                          
                              if pb_level == analysis_level:
                                 #find the label of the parent code at the chosen analysis level
                                 pb_code = parent_branch[j]
                                 #if the code at the chosen level is not blank
                                 if pb_code != "-------":
                                    #find the corresponding label
                                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                                       if pb_code == item["id"][34:]:
                                          lbl = item["lbl"]
                                          short_lbl=""
                                          for word in lbl.split():
                                             if word in ("of", "the"):
                                                short_lbl = short_lbl + word[0] 
                                             #avoid identical acronyms   
                                             elif word in ("hair", "heart", "humoral"):
                                                short_lbl = short_lbl + word[0].upper()
                                                short_lbl = short_lbl + word[1]
                                             else:
                                                short_lbl = short_lbl + word[0].upper()
                                          break
                                 
                                    #add the pb_code and the corresponding label (HPO_term) to the count dictionnary
                                    #but first check that this code does not already have an entry
                                    for item in counts:
                                       #if there is already an entry for this code, increment the counter
                                       if item["HPO_code"] == pb_code:
                                          found = True
                                          item["n"] += 1
                                          break

                                    #if having searched through the entire count dictionary, no matching entries have been found   
                                    if found == False:
                        
                                       #find the corresponding colour          
                                       for colour_el in colour_list:
                                          if colour_el["code"] == level2_code:
                                             colour = str(colour_el["colour"])
                                             break
                                          
                                      #add an entry to the count dictionnary
                                       counts.append(dict(HPO_code = pb_code, HPO_term = lbl, HPO_acronym = short_lbl, n=1, colour = colour))
                                       unique_symptoms += 1
         else:
            if analysis_level == 8:
               print("No disease information for patient {0:s}".format(object["id"]))
                 
  
      #for each analysis level, sort the counts from most to least frequent
      counts = sorted(counts, key=lambda d: d["n"], reverse = True)
      #add an entry to the symptom_table dictionary
      symptom_table.append(dict(gene = disease['gene'], disease = disease['name'], analysis_level = analysis_level, patients = count_patients, girls = count_girls, counts = counts))
      symptom_matrix = np.array(" disease")
      symptom_matrix = np.append(symptom_matrix, [code["HPO_code"] for code in counts])
      print("Disease, ", disease['name'], "; level, ", analysis_level, "; unique symptoms, ", unique_symptoms)

      if analysis_level > 2:

         #print(symptom_matrix, symptom_matrix.shape, symptom_matrix.shape[0], np.argwhere(symptom_matrix == '0025032'))
         

         # Now write each patient as a row vector in a matrix where the columns are the unique HPO codes for that level
         for object in patient_list: 
            
            
            if "gene" in object.keys():

               if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
                   
                  # Only include patients with more than a certain number of symptoms
                  # (i.e cycle current loop if no more than N symptoms in current patient entry)
                  if len(object['symptoms']) < 5: 
                     continue 
                  
                  # Initialize each patient as a row of zeros
                  # .. with the name of the disease as the first column
                  row = np.array(f"{object['disease']:>8}")
                  row = np.append(row, np.zeros(unique_symptoms, dtype = int))
                  # np.vstack appends the second argument (array) to the first 
                  symptom_matrix = np.vstack((symptom_matrix, row))
                  #print(symptom_matrix, symptom_matrix.shape, symptom_matrix.shape[0], np.argwhere(symptom_matrix == '0025032')) 
                   
                  for HPO_code in object["symptoms"]:
                     #find this symptom in the tree 
                     for branch in hp_tree_list:

                        if branch["code"] == HPO_code:
                        
                           #if the symptom matches, search all the parent_branches of this code 
                           #pb means parent_branch
                           for i in range(0, len(branch["parent_branches"]), 1):
                              parent_branch = branch["parent_branches"][i]
                              pb_length = branch["branch_lengths"][i]
                              #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                              pb_level = -1
                              found = False
                              level2_code = ""
                              lbl = "<--BLANK-->"

                              #go through all codes in the parent_branch 
                              #starting from the top and working down (from the end of the list and work backwards)
                              #The convention I have chosen to follow is 
                              #pb_level = 0 corresponds to 0000001: All
                              #         = 1 corresponds to 0000118: Phenotypic abnormality
                              #         = 2 gives the colour of all codes lower down the hierarchy
                              for j in range(pb_length, 1, -1):
                                 #codes are stored from the end to the start of a branch
                                 #so have to reverse the count
                                 pb_level += 1

                                 if pb_level == 2:
                                    level2_code = parent_branch[j]

                                 if pb_level == analysis_level:
                                    #find the label of the parent code at the chosen analysis level
                                    pb_code = parent_branch[j]
                                    #if the code at the chosen level is not blank
                                    if pb_code != "-------":
                                       #set the value of the corresponding column to 1
                                       symptom_matrix[-1, np.argwhere(symptom_matrix == pb_code)[0][1]] = 1

         #Write the symptom_matrix to the output file
         with open("hp_symptom_matrix.txt", "a") as outfile:
            outfile.write("Disease, " + disease['name'] + "; level, " + str(analysis_level) + "; unique symptoms, " + str(unique_symptoms) + "\n")
            outfile.write(f", ".join(symptom_matrix[0]) + "\n")
            for row in symptom_matrix[1:]:
               outfile.write(",       ".join(row) + "\n")
            
            outfile.write("\n\n\n")




# Serialize the python dictionnary to json
json_data = json.dumps(symptom_table, indent = 4)

# Writing to hp_trees.json
with open("hp_symptom_stats.json", "w") as outfile:
    outfile.write(json_data)


   



