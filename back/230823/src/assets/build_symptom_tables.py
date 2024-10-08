#!/usr/bin/env python3
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

for gene in genes:
  
   colour = "#9ca3af33" # default colour is grey
   
   for analysis_level in analysis_levels: 
      unique_symptoms = 0
      counts = []
      count_patients = 0
      count_girls = 0

      for object in patient_list: 
        
         if "gene" in object.keys():

            if (object["gene"] == gene and 'symptoms' in object.keys()):
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
               print("No gene information for patient {0:s}".format(object["id"]))
                 
  
      #for each analysis level, sort the counts from most to least frequent
      counts = sorted(counts, key=lambda d: d["n"], reverse = True)
      #add an entry to the symptom_table dictionary
      symptom_table.append(dict(gene = gene, analysis_level = analysis_level, patients = count_patients, girls = count_girls, counts = counts))

      print("Gene, ", gene, "; level, ", analysis_level, "; unique symptoms, ", unique_symptoms)



# Serialize the python dictionnary to json
json_data = json.dumps(symptom_table, indent = 4)

# Writing to hp_trees.json
with open("hp_symptom_stats.json", "w") as outfile:
    outfile.write(json_data)


   



