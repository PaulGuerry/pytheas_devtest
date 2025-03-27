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
for line in fileinput.input(files="hp_nodes_modPG.json"):
    json_data = json_data + line
HPO_nodes_list = json.loads(json_data)

json_data = ""
for line in fileinput.input(files="colourScheme.json"):
    json_data = json_data + line
colour_list = json.loads(json_data)

with open("hp_symptom_matrix.txt", "w") as outfile:
   outfile.write("Ouput from build_symptom_tables.py") 
   outfile.write("\n")


#analysis_levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]   
analysis_levels = [2, 3, 4, 5]   
#analysis_levels = [1, 2]   
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
            dict(name = "MYO5B deficiency", gene = "MYO5B", matches = ["MYO5B deficiency"]),
            dict(name = "PFIC11", gene = "SEMA7A", matches = ["PFIC11"]),
            dict(name = "CDG2P", gene = "TMEM199", matches = ["CDG2P"]),
            dict(name = "THES1", gene = "SKIC3", matches = ["THES1"]),
            dict(name = "THES2", gene = "SKIC2", matches = ["THES2"]),
            dict(name = "THES", gene = "SKIC3,SKIC2", matches = ["THES", "THES1", "THES2"]),
            #dict(name = "CLUST", gene = "#####", matches = ["THES", "THES1", "THES2", "PFIC2"]),
            dict(name = "PFIC1-11", gene = "All PFIC genes", matches = ["PFIC1", "PFIC2", "PFIC3", "PFIC4", "PFIC5", "PFIC6", "PFIC7", "PFIC8", "PFIC9", "MYO5B deficiency", "PFIC11"]),
            dict(name = "FOCADS", gene = "FOCAD", matches = ["FOCADS"]),
            dict(name = "ARCS1", gene = "VPS33B", matches = ["ARCS1"]),
            dict(name = "ARCS2", gene = "VIPAS39", matches = ["ARCS2"]),
            dict(name = "ARCS", gene = "VPS33B,VIPAS39", matches = ["ARCS", "ARCS1", "ARCS2"])
            ]

#diseases = [dict(name = "PFIC1", gene = "ATP8B1", matches = ["PFIC1"])]

for disease in diseases:
  
   
   print("Gathering symptom stats for disease {0:s}".format(disease['name']))

   for analysis_level in analysis_levels: 
      unique_symptoms = 0
      counts = []
      count_patients = 0
      count_girls = 0
      colour = "#9ca3af33" # default colour is grey
      category = ""
      category_n = 0

      for object in patient_list: 
        
         if "gene" in object.keys() and "symptoms" in object.keys():

            if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
               count_patients += 1 
                
               if ("sex" in object.keys() and object["sex"] == "F"):
                  count_girls += 1

               # Check for Cholestatis and diarrhea doubles
               if ("0001396" and "0002611" in object["symptoms"]):
                  object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

               if ("0002041" and "0002028" in object["symptoms"]):
                  object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

               # Check for hyperbilirubinemia without jaundice                                
               if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                  object["symptoms"].append("0000952")
            
               if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                  object["symptoms"].append("0000952")
            
               if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                  object["symptoms"].append("0000952")


               for HPO_code in object["symptoms"]:

                 #make corrections here for eg. Cholestasis (0001396 and 0002611)
                 if HPO_code == "0002611":
                    #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                    HPO_code = "0001396"
                 elif HPO_code == "0002041":
                    #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                    HPO_code = "0002028"

  
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
                                         item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                                         #if (object["doi"] not in item["dois"]):
                                         #   item["dois"].append(object["doi"])
                                         break

                                   #if having searched through the entire count dictionary, no matching entries have been found   
                                   if found == False:
                                 
                                      #find the corresponding colour          
                                      for colour_el in colour_list:
                                         if colour_el["code"] == level2_code:
                                            colour = str(colour_el["colour"])
                                            category = str(colour_el["label"])
                                            category_n = colour_el["category"]
                                            break
                                         
                                      #add an entry to the count dictionnary
                                      counts.append(dict(HPO_code = pb_code, 
                                                         HPO_term = lbl, 
                                                         HPO_acronym = short_lbl, 
                                                         n=1, 
                                                         n_pct="0",
                                                         n_pct_scaled="0",
                                                         colour = colour,
                                                         category = category,
                                                         category_n = category_n * 100,
                                                         category_n_scaled = "0"
                                                         ))
                                      unique_symptoms += 1

         else:
            if analysis_level == 13:
               print("No disease information for patient {0:s}".format(object["id"]))
                 
      #Calculate n_pct for the symptom counts
      #.. and present/absent ratios
      category_n_max = 0.
      n_pct_max = 0.
      for item in counts:
          item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
          category_n_scaled = item["category_n"] 

          n_pct_max = max(n_pct_max, float(item["n_pct"])) 
          # add random jitter (for x dimension of symptom plots)
          category_n_scaled = category_n_scaled + np.random.rand()
          category_n_max = max(category_n_scaled, category_n_max)
          item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

      #Normalize category offsets and n_pct
      for item in counts:
          #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
          #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
          item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
          item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
  
      #for each analysis level, sort the counts from most to least frequent
      counts = sorted(counts, key=lambda d: d["n"], reverse = True)
      #add an entry to the symptom_table dictionary
      symptom_table.append(dict(gene = disease['gene'], disease = disease['name'], analysis_level = analysis_level, patients = count_patients, girls = count_girls, counts = counts))
      symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
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
                  if len(object['symptoms']) < 3: 
                     continue 
                  
                  # Initialize each patient as a row of zeros
                  # .. with the name of the disease as the first column
                  row = np.array([f"{object['id']:>15}",f"{object['disease']:>10}"])
                  row = np.append(row, np.zeros(unique_symptoms, dtype = 'int'))
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

                           # Once the branches of the code have been found, stop searching through the branches               
                           # .. i.e. break the for branch in hp_tree_list loop
                           break               
                                       

         #Write the symptom_matrix to the output file
         nl = "\n"
         with open("hp_symptom_matrix.txt", "a") as outfile:
            outfile.write("Disease, " + disease['name'] + "; level, " + str(analysis_level) + "; unique symptoms, " + str(unique_symptoms) + "\n")
            outfile.write(f",".join(f'{col:>8}' for col in symptom_matrix[0]))
            outfile.write("\n")
            for row in symptom_matrix[1:]:
               #join each column (0 or 1, integer), right-aligned to 8 characters (:>8), separated by a comma  
               outfile.write(",".join(f'{str(col):>8}' for col in row))
               outfile.write("\n")
            
            outfile.write("\n\n\n")





# 241218: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..for all patients
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "All"
   
   print("Gathering as-reported symptom stats for disease {0:s}".format(disease['name']))

   for object in patient_list: 
        
      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])
                             else:
                                item["n_absent"] += 1
                                
                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"

                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100, 
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


    


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; all patients; symptoms as reported; unique symptoms, ", unique_symptoms)
   #for el in counts:
   #   print(el)



    #print(symptom_matrix, symptom_matrix.shape, symptom_matrix.shape[0], np.argwhere(symptom_matrix == '0025032'))
    

    # Now write each patient as a row vector in a matrix where the columns are the unique HPO codes for that level
   for object in patient_list: 
       
       
        if "gene" in object.keys():

            if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
              
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")




                # Only include patients with more than a certain number of symptoms
                # (i.e cycle current loop if no more than N symptoms in current patient entry)
                if len(object['symptoms']) < 3: 
                   continue 
             
                # Initialize each patient as a row of zeros
                # .. with the name of the disease as the first column
                row = np.array([f"{object['id']:>15}",f"{object['disease']:>10}"])
                row = np.append(row, np.zeros(unique_symptoms, dtype = 'int'))
                # np.vstack appends the second argument (array) to the first 
                symptom_matrix = np.vstack((symptom_matrix, row))
                #print(symptom_matrix, symptom_matrix.shape, symptom_matrix.shape[0], np.argwhere(symptom_matrix == '0025032')) 
                 
                try: 
                  for HPO_code in object["symptoms"]:
                
                     #make corrections here for eg. Cholestasis (0001396 and 0002611)
                     if HPO_code == "0002611":
                        #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                        HPO_code = "0001396"
                     elif HPO_code == "0002041":
                        #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                        HPO_code = "0002028" 

                     #set the value of the corresponding column to 1                                          
                     symptom_matrix[-1, np.argwhere(symptom_matrix == HPO_code)[0][1]] = 1
                
                except: 
                   print("Check symptoms for patient {0:s}.".format(object["id"]))
                
                                                       

   #Write the symptom_matrix to the output file
   nl = "\n"
   with open("hp_symptom_matrix.txt", "a") as outfile:
        outfile.write("Disease, " + disease['name'] + "; ** as reported **; unique symptoms, " + str(unique_symptoms) + "\n")
        outfile.write(f",".join(f'{col:>8}' for col in symptom_matrix[0]))
        outfile.write("\n")
        for row in symptom_matrix[1:]:
           #join each column (0 or 1, integer), right-aligned to 8 characters (:>8), separated by a comma  
           outfile.write(",".join(f'{str(col):>8}' for col in row))
           outfile.write("\n")
        
        outfile.write("\n\n\n")

             
# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..only for girls
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "Girls"
   
   print("Gathering as-reported symptom stats for disease {0:s}".format(disease['name']))

   for object in patient_list: 
        
      if ("sex" not in object.keys() or ("sex" in object.keys() and object["sex"] != "F")):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])
                             else:
                                item["n_absent"] += 1
                                
                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])

                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"

                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


    


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)

                                    
# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..only for boys
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "Boys"
   

   for object in patient_list: 
        
      if ("sex" not in object.keys() or ("sex" in object.keys() and object["sex"] != "M")):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])

                             else:
                                item["n_absent"] += 1

                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"


                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)


# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..only for double LoF patients
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "LoF_LoF"
   

   for object in patient_list: 
        
      if ("protvartypes" not in object.keys() or object["protvartypes"].count("LoF") < 2):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])

                             else:
                                item["n_absent"] += 1

                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"


                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)

# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..for all but double LoF patients
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "!LoF_LoF"
   

   for object in patient_list: 
        
      if ("protvartypes" not in object.keys() or object["protvartypes"].count("LoF") > 0):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])

                             else:
                                item["n_absent"] += 1

                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"


                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)

# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..only for patients with first symptoms before 5 years of age
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "Before5y"
   

   for object in patient_list: 
        
      if ("firstsymptomagemonth" not in object.keys() or object["firstsymptomagemonth"] is None or object["firstsymptomagemonth"] > 60):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])

                             else:
                                item["n_absent"] += 1

                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"


                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)

# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..for patients with first symptoms at age > 5 years
for disease in diseases:
  
   colour = "#9ca3af33" # default colour is grey
   category = ""
   category_n = 0
   unique_symptoms = 0
   counts = []
   count_patients = 0
   count_girls = 0
   sel = "After5y"
   

   for object in patient_list: 
        
      if ("firstsymptomagemonth" not in object.keys() or object["firstsymptomagemonth"] is None or object["firstsymptomagemonth"] <= 60):
         continue

      if "gene" in object.keys():

         if (object["disease"] in disease['matches'] and 'symptoms' in object.keys()):
            count_patients += 1 
             
            if ("sex" in object.keys() and object["sex"] == "F"):
               count_girls += 1

            # Check for Cholestatis and diarrhea doubles
            if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

            if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
               object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

            # Check for hyperbilirubinemia without jaundice
            if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")
            
            if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")

            if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
               object["symptoms"].append("0000952")


            for HPO_code in object["symptoms"]:
                
                lbl = "<--BLANK-->"
                found = False
                #make corrections here for eg. Cholestasis (0001396 and 0002611)
                if HPO_code == "0002611":
                     #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                     HPO_code = "0001396"
                elif HPO_code == "0002041":
                     #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                     HPO_code = "0002028"

                #find this symptom in the tree (here, only to get the appropriate labeling colour)
                for branch in hp_tree_list:
                    
                    if branch["code"] == HPO_code:
                      #if the symptom matches, search all the parent_branches of this code 
                      #pb means parent_branch
                      for i in range(0, len(branch["parent_branches"]), 1):
                          parent_branch = branch["parent_branches"][i]
                          #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                          pb_length = branch["branch_lengths"][i]
                          #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                          pb_level = -1
                          level2_code = ""
                          
                          #go through all codes in the parent_branch 
                          #starting from the top and working down (from the end of the list and work backwards)
                          #The convention I have chosen to follow is 
                          #pb_level = 0 corresponds to 0000001: All
                          #         = 1 corresponds to 0000118: Phenotypic abnormality
                          #         = 2 gives the colour of all codes lower down the hierarchy
                          for j in range(pb_length, 0, -1):
                              #codes are stored from the end to the start of a branch
                              #so have to reverse the count
                              pb_level += 1
                              #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                              if pb_level == 2:
                                 level2_code = parent_branch[j]
                                 break
                      # Once the branches of the code have been found, stop searching through the branches               
                      # .. i.e. break the for branch in hp_tree_list loop
                      break                               


                #find the corresponding label
                for item in HPO_nodes_list["graphs"][0]["nodes"]:
                   if HPO_code == item["id"][34:]:
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
                
                #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                #but first check that this code does not already have an entry
                for item in counts:
                   #if there is already an entry for this code, increment the counter
                   if item["HPO_code"] == HPO_code:
                      found = True
                      # It is possible the entry in the "counts" dict was created with an absent symptom
                      # .. in which case unique_symptoms will not have been incremented
                      # .. so to account for this possibility, increment unique_symptoms if n == 0
                      if item["n"] == 0: unique_symptoms += 1
                      item["n"] += 1
                      item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                      if item["n_absent"] > 0:
                        item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                      else:
                        item["abs_pct"] = "-"

                      if (object["doi"] not in item["DOIs_present"]):
                         item["DOIs_present"].append(object["doi"])

                      break

                #if having searched through the entire count dictionary, no matching entries have been found   
                if found == False:
                
                   #find the corresponding colour          
                   for colour_el in colour_list:
                      if colour_el["code"] == level2_code:
                         colour = str(colour_el["colour"])
                         category = str(colour_el["label"])
                         category_n = colour_el["category"]
                         break
                      
                   #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                   #add an entry to the count dictionnary
                   counts.append(dict(HPO_code = HPO_code, 
                                      HPO_term = lbl, 
                                      HPO_acronym = short_lbl, 
                                      n=1, 
                                      n_pct="{0:.1f}".format(100 / count_patients),
                                      n_pct_scaled="0",
                                      n_absent=0, 
                                      n_sometimes=0, 
                                      abs_pct = "-", 
                                      colour = colour,
                                      category = category,
                                      category_n = category_n * 100,
                                      category_n_scaled = "0",
                                      DOIs_sometimes = [],
                                      DOIs_absent = [],
                                      DOIs_present = [object["doi"]]))
                   
                   unique_symptoms += 1
 
            # Symptoms reported absent
            if ('absentsymptoms' in object.keys()):
               
                # Check for Cholestatis and diarrhea doubles
                if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

                if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                   object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

                # Check for hyperbilirubinemia without jaundice
                if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")
                
                if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                   object["symptoms"].append("0000952")



                for HPO_code in object["absentsymptoms"]:

                    #make corrections here for eg. Cholestasis (0001396 and 0002611)
                    if HPO_code == "0002611":
                       #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                       HPO_code = "0001396"
                    elif HPO_code == "0002041":
                       #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                       HPO_code = "0002028"
                
                    lbl = "<--BLANK-->"
                    found = False

                    #find this symptom in the tree (here, only to get the appropriate labeling colour)
                    for branch in hp_tree_list:


                      if branch["code"] == HPO_code:
                        #if the symptom matches, search all the parent_branches of this code 
                        #pb means parent_branch
                        for i in range(0, len(branch["parent_branches"]), 1):
                            parent_branch = branch["parent_branches"][i]
                            pb_length = branch["branch_lengths"][i]
                            #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                            pb_level = -1
                            level2_code = ""
                            
                            #go through all codes in the parent_branch 
                            #starting from the top and working down (from the end of the list and work backwards)
                            #The convention I have chosen to follow is 
                            #pb_level = 0 corresponds to 0000001: All
                            #         = 1 corresponds to 0000118: Phenotypic abnormality
                            #         = 2 gives the colour of all codes lower down the hierarchy
                            for j in range(pb_length, 0, -1):
                                #codes are stored from the end to the start of a branch
                                #so have to reverse the count
                                pb_level += 1

                                if pb_level == 2:
                                   level2_code = parent_branch[j]
                                   break
                        
                        # Once the branches of the code have been found, stop searching through the branches               
                        # .. i.e. break the for branch in hp_tree_list loop
                        break         


                    #find the corresponding label
                    for item in HPO_nodes_list["graphs"][0]["nodes"]:
                       if HPO_code == item["id"][34:]:
                          if 'lbl' in item.keys():
                            lbl = item["lbl"]
                          else:
                            print("Patient ID -->", object["id"])
                            print("HPO code -->", HPO_code)
                            print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                             
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
                
                    # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                    #.. !!as reported absent!!
                    for item in counts:
                       #if there is already an entry for this code, increment the counter
                       if item["HPO_code"] == HPO_code:
                          found = True
                          # If the HPO_code is also reported as present for current patient
                          # ..(i.e. the code is also present in object["symptoms"])
                          # .. increment n_sometimes
                          if ('symptoms' in object.keys()):
                             if HPO_code in object["symptoms"]:
                                item["n_sometimes"] += 1
                                #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                                if (object["doi"] not in item["DOIs_sometimes"]):
                                   item["DOIs_sometimes"].append(object["doi"])

                             else:
                                item["n_absent"] += 1

                                if (object["doi"] not in item["DOIs_absent"]):
                                   item["DOIs_absent"].append(object["doi"])
                                
                                if item["n_absent"] > 0:
                                  item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                                else:
                                  item["abs_pct"] = "-"


                          else:
                             item["n_absent"] += 1
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])     

                          break

                    # If having searched through the entire count dictionary, no matching entries have been found   
                    if found == False:
                
                       # Find the corresponding colour          
                       for colour_el in colour_list:
                          if colour_el["code"] == level2_code:
                             colour = str(colour_el["colour"])
                             category = str(colour_el["label"])
                             category_n = colour_el["category"]
                             break
                          
                       #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                       # Add an entry to the count dictionnary 
                       #.. !!as reported absent!! 
                       #.. !!and do not count it as a unique symptom!!
                       # ..but it the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes and not n_absent or n
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=0, 
                                               n_sometimes=1, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category = category,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_absent = [],
                                               DOIs_sometimes = [object["doi"]]))
                          else:
                            counts.append(dict(HPO_code = HPO_code, 
                                               HPO_term = lbl, 
                                               HPO_acronym = short_lbl, 
                                               n=0, 
                                               n_pct="0",
                                               n_pct_scaled="0",
                                               n_absent=1, 
                                               n_sometimes=0, 
                                               abs_pct = "-", 
                                               colour = colour,
                                               category_n = category_n * 100,
                                               category_n_scaled = "0",
                                               DOIs_present = [],
                                               DOIs_sometimes = [],
                                               DOIs_absent = [object["doi"]]))
                       else:
                          counts.append(dict(HPO_code = HPO_code, 
                                             HPO_term = lbl, 
                                             HPO_acronym = short_lbl, 
                                             n=0, 
                                             n_pct="0",
                                             n_pct_scaled="0",
                                             n_absent=1, 
                                             n_sometimes=0, 
                                             abs_pct = "-", 
                                             colour = colour,
                                             category_n = category_n * 100,
                                             category_n_scaled = "0",
                                             DOIs_present = [],
                                             DOIs_sometimes = [],
                                             DOIs = [object["doi"]]))


   #Calculate n_pct for the symptom counts
   #.. and present/absent ratios
   category_n_max = 0.
   n_pct_max = 0.
   for item in counts:
       item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
       pa_ratio = item["abs_pct"]
       category_n_scaled = item["category_n"] 
       if pa_ratio == "-":
          pa_ratio = 1.
       else:
          pa_ratio = min(99., float(pa_ratio)) 

       n_pct_max = max(n_pct_max, float(item["n_pct"])) 
       # add random jitter (for x dimension of symptom plots)
       category_n_scaled = category_n_scaled + np.random.rand()
       category_n_max = max(category_n_scaled, category_n_max)
       item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
       
      

   #Normalize category offsets and n_pct
   for item in counts:
       #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
       #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
       item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
       item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
    
   #sort the counts from most to least frequent
   counts = sorted(counts, key=lambda d: d["n"], reverse = True)
   #add an entry to the symptom_table dictionary
   symptom_table.append(dict(gene = disease['gene'], 
                              disease = disease['name'], 
                              analysis_level = 999, 
                              patients = count_patients, 
                              girls = count_girls, 
                              selection = sel,
                              counts = counts,
                              ))
   #symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
   #symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
   print("Disease, ", disease['name'], "; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)



# 250324: stats of symptoms as reported
#         ..and of symptoms reported absent
#         ..only for pure PFIC10 patients

colour = "#9ca3af33" # default colour is grey
category = ""
category_n = 0
unique_symptoms = 0
counts = []
count_patients = 0
count_girls = 0
sel = "PFIC10"
disease = "MYO5B deficiency"


for object in patient_list: 
     
   if ("symptoms" in object.keys() and "0011473" in object["symptoms"] and "0001396" not in object["symptoms"]):
      continue

   if "gene" in object.keys():

      if (object["gene"] == "MYO5B" and 'symptoms' in object.keys()):
         count_patients += 1 
          
         if ("sex" in object.keys() and object["sex"] == "F"):
            count_girls += 1

         # Check for Cholestatis and diarrhea doubles
         if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
            object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

         if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
            object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

         # Check for hyperbilirubinemia without jaundice
         if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
            object["symptoms"].append("0000952")
         
         if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
            object["symptoms"].append("0000952")

         if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
            object["symptoms"].append("0000952")


         for HPO_code in object["symptoms"]:
             
             lbl = "<--BLANK-->"
             found = False
             #make corrections here for eg. Cholestasis (0001396 and 0002611)
             if HPO_code == "0002611":
                  #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                  HPO_code = "0001396"
             elif HPO_code == "0002041":
                  #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                  HPO_code = "0002028"

             #find this symptom in the tree (here, only to get the appropriate labeling colour)
             for branch in hp_tree_list:
                 
                 if branch["code"] == HPO_code:
                   #if the symptom matches, search all the parent_branches of this code 
                   #pb means parent_branch
                   for i in range(0, len(branch["parent_branches"]), 1):
                       parent_branch = branch["parent_branches"][i]
                       #if HPO_code == "0001892": print("Parent branch, ", parent_branch)
                       pb_length = branch["branch_lengths"][i]
                       #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                       pb_level = -1
                       level2_code = ""
                       
                       #go through all codes in the parent_branch 
                       #starting from the top and working down (from the end of the list and work backwards)
                       #The convention I have chosen to follow is 
                       #pb_level = 0 corresponds to 0000001: All
                       #         = 1 corresponds to 0000118: Phenotypic abnormality
                       #         = 2 gives the colour of all codes lower down the hierarchy
                       for j in range(pb_length, 0, -1):
                           #codes are stored from the end to the start of a branch
                           #so have to reverse the count
                           pb_level += 1
                           #if HPO_code == "0001395": print(HPO_code, j, pb_level, parent_branch[j])
                           if pb_level == 2:
                              level2_code = parent_branch[j]
                              break
                   # Once the branches of the code have been found, stop searching through the branches               
                   # .. i.e. break the for branch in hp_tree_list loop
                   break                               


             #find the corresponding label
             for item in HPO_nodes_list["graphs"][0]["nodes"]:
                if HPO_code == item["id"][34:]:
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
             
             #add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
             #but first check that this code does not already have an entry
             for item in counts:
                #if there is already an entry for this code, increment the counter
                if item["HPO_code"] == HPO_code:
                   found = True
                   # It is possible the entry in the "counts" dict was created with an absent symptom
                   # .. in which case unique_symptoms will not have been incremented
                   # .. so to account for this possibility, increment unique_symptoms if n == 0
                   if item["n"] == 0: unique_symptoms += 1
                   item["n"] += 1
                   item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
                   if item["n_absent"] > 0:
                     item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                   else:
                     item["abs_pct"] = "-"

                   if (object["doi"] not in item["DOIs_present"]):
                      item["DOIs_present"].append(object["doi"])

                   break

             #if having searched through the entire count dictionary, no matching entries have been found   
             if found == False:
             
                #find the corresponding colour          
                for colour_el in colour_list:
                   if colour_el["code"] == level2_code:
                      colour = str(colour_el["colour"])
                      category = str(colour_el["label"])
                      category_n = colour_el["category"]
                      break
                   
                #print("** As reported; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                #add an entry to the count dictionnary
                counts.append(dict(HPO_code = HPO_code, 
                                   HPO_term = lbl, 
                                   HPO_acronym = short_lbl, 
                                   n=1, 
                                   n_pct="{0:.1f}".format(100 / count_patients),
                                   n_pct_scaled="0",
                                   n_absent=0, 
                                   n_sometimes=0, 
                                   abs_pct = "-", 
                                   colour = colour,
                                   category = category,
                                   category_n = category_n * 100,
                                   category_n_scaled = "0",
                                   DOIs_sometimes = [],
                                   DOIs_absent = [],
                                   DOIs_present = [object["doi"]]))
                
                unique_symptoms += 1

         # Symptoms reported absent
         if ('absentsymptoms' in object.keys()):
            
             # Check for Cholestatis and diarrhea doubles
             if ("0001396" in object["symptoms"] and "0002611" in object["symptoms"]):
                object["symptoms"] = [el for el in object["symptoms"] if el != "0002611"]

             if ("0002041" in object["symptoms"] and "0002028" in object["symptoms"]):
                object["symptoms"] = [el for el in object["symptoms"] if el != "0002041"]

             # Check for hyperbilirubinemia without jaundice
             if ("0002908" in object["symptoms"] and "0000952" not in object["symptoms"]):
                object["symptoms"].append("0000952")
             
             if ("0002904" in object["symptoms"] and "0000952" not in object["symptoms"]):
                object["symptoms"].append("0000952")
             
             if ("0008282" in object["symptoms"] and "0000952" not in object["symptoms"]):
                object["symptoms"].append("0000952")



             for HPO_code in object["absentsymptoms"]:

                 #make corrections here for eg. Cholestasis (0001396 and 0002611)
                 if HPO_code == "0002611":
                    #print("Recoding 0002611, Cholestatic liver disease, as 0001396, Cholestasis")
                    HPO_code = "0001396"
                 elif HPO_code == "0002041":
                    #print("Recoding 0002041, Intractable diarrhea, as 0002028, Chronic diarrhea")
                    HPO_code = "0002028"
             
                 lbl = "<--BLANK-->"
                 found = False

                 #find this symptom in the tree (here, only to get the appropriate labeling colour)
                 for branch in hp_tree_list:


                   if branch["code"] == HPO_code:
                     #if the symptom matches, search all the parent_branches of this code 
                     #pb means parent_branch
                     for i in range(0, len(branch["parent_branches"]), 1):
                         parent_branch = branch["parent_branches"][i]
                         pb_length = branch["branch_lengths"][i]
                         #initialized at -1 to make code more readable (so that increment statement appears at the start of the loop)
                         pb_level = -1
                         level2_code = ""
                         
                         #go through all codes in the parent_branch 
                         #starting from the top and working down (from the end of the list and work backwards)
                         #The convention I have chosen to follow is 
                         #pb_level = 0 corresponds to 0000001: All
                         #         = 1 corresponds to 0000118: Phenotypic abnormality
                         #         = 2 gives the colour of all codes lower down the hierarchy
                         for j in range(pb_length, 0, -1):
                             #codes are stored from the end to the start of a branch
                             #so have to reverse the count
                             pb_level += 1

                             if pb_level == 2:
                                level2_code = parent_branch[j]
                                break
                     
                     # Once the branches of the code have been found, stop searching through the branches               
                     # .. i.e. break the for branch in hp_tree_list loop
                     break         


                 #find the corresponding label
                 for item in HPO_nodes_list["graphs"][0]["nodes"]:
                    if HPO_code == item["id"][34:]:
                       if 'lbl' in item.keys():
                         lbl = item["lbl"]
                       else:
                         print("Patient ID -->", object["id"])
                         print("HPO code -->", HPO_code)
                         print("No lbl for HPO code".format(HPO_code) + ", HPO node".format(item))
                          
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
             
                 # Add the HPO_code and the corresponding label (HPO_term) to the count dictionnary
                 #.. !!as reported absent!!
                 for item in counts:
                    #if there is already an entry for this code, increment the counter
                    if item["HPO_code"] == HPO_code:
                       found = True
                       # If the HPO_code is also reported as present for current patient
                       # ..(i.e. the code is also present in object["symptoms"])
                       # .. increment n_sometimes
                       if ('symptoms' in object.keys()):
                          if HPO_code in object["symptoms"]:
                             item["n_sometimes"] += 1
                             #print("Symptom {0:s} present and absent for patient {1:s}".format(HPO_code, object["id"]))
                             if (object["doi"] not in item["DOIs_sometimes"]):
                                item["DOIs_sometimes"].append(object["doi"])

                          else:
                             item["n_absent"] += 1

                             if (object["doi"] not in item["DOIs_absent"]):
                                item["DOIs_absent"].append(object["doi"])
                             
                             if item["n_absent"] > 0:
                               item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                             else:
                               item["abs_pct"] = "-"


                       else:
                          item["n_absent"] += 1
                          if item["n_absent"] > 0:
                            item["abs_pct"] = "{0:.1f}".format(item["n_absent"] / count_patients)
                          else:
                            item["abs_pct"] = "-"

                          if (object["doi"] not in item["DOIs_absent"]):
                             item["DOIs_absent"].append(object["doi"])     

                       break

                 # If having searched through the entire count dictionary, no matching entries have been found   
                 if found == False:
             
                    # Find the corresponding colour          
                    for colour_el in colour_list:
                       if colour_el["code"] == level2_code:
                          colour = str(colour_el["colour"])
                          category = str(colour_el["label"])
                          category_n = colour_el["category"]
                          break
                       
                    #print("** As reported absent; symptom,", lbl, HPO_code, "; level 2 code, ", level2_code,",  colour, ", colour, ", category, ", category)      
                    # Add an entry to the count dictionnary 
                    #.. !!as reported absent!! 
                    #.. !!and do not count it as a unique symptom!!
                    # ..but it the HPO_code is also reported as present for current patient
                    # ..(i.e. the code is also present in object["symptoms"])
                    # .. increment n_sometimes and not n_absent or n
                    if ('symptoms' in object.keys()):
                       if HPO_code in object["symptoms"]:
                         counts.append(dict(HPO_code = HPO_code, 
                                            HPO_term = lbl, 
                                            HPO_acronym = short_lbl, 
                                            n=0, 
                                            n_pct="0",
                                            n_pct_scaled="0",
                                            n_absent=0, 
                                            n_sometimes=1, 
                                            abs_pct = "-", 
                                            colour = colour,
                                            category = category,
                                            category_n = category_n * 100,
                                            category_n_scaled = "0",
                                            DOIs_present = [],
                                            DOIs_absent = [],
                                            DOIs_sometimes = [object["doi"]]))
                       else:
                         counts.append(dict(HPO_code = HPO_code, 
                                            HPO_term = lbl, 
                                            HPO_acronym = short_lbl, 
                                            n=0, 
                                            n_pct="0",
                                            n_pct_scaled="0",
                                            n_absent=1, 
                                            n_sometimes=0, 
                                            abs_pct = "-", 
                                            colour = colour,
                                            category_n = category_n * 100,
                                            category_n_scaled = "0",
                                            DOIs_present = [],
                                            DOIs_sometimes = [],
                                            DOIs_absent = [object["doi"]]))
                    else:
                       counts.append(dict(HPO_code = HPO_code, 
                                          HPO_term = lbl, 
                                          HPO_acronym = short_lbl, 
                                          n=0, 
                                          n_pct="0",
                                          n_pct_scaled="0",
                                          n_absent=1, 
                                          n_sometimes=0, 
                                          abs_pct = "-", 
                                          colour = colour,
                                          category_n = category_n * 100,
                                          category_n_scaled = "0",
                                          DOIs_present = [],
                                          DOIs_sometimes = [],
                                          DOIs = [object["doi"]]))


#Calculate n_pct for the symptom counts
#.. and present/absent ratios
category_n_max = 0.
n_pct_max = 0.
for item in counts:
    item["n_pct"] = "{0:.0f}".format(100 * item["n"] / count_patients)
    pa_ratio = item["abs_pct"]
    category_n_scaled = item["category_n"] 
    if pa_ratio == "-":
       pa_ratio = 1.
    else:
       pa_ratio = min(99., float(pa_ratio)) 

    n_pct_max = max(n_pct_max, float(item["n_pct"])) 
    # add random jitter (for x dimension of symptom plots)
    category_n_scaled = category_n_scaled + np.random.rand()
    category_n_max = max(category_n_scaled, category_n_max)
    item["category_n_scaled"] = "{0:.0f}".format(category_n_scaled)
    
   

#Normalize category offsets and n_pct
for item in counts:
    #PG 250327: normalize to maximum number of categories (i.e. 23) * 100 (because category_n is multiplied by 100)
    #item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/category_n_max)
    item["category_n_scaled"] = "{0:.3f}".format(float(item["category_n_scaled"])/2300)
    item["n_pct_scaled"] = "{0:.3f}".format(float(item["n_pct"])/n_pct_max)
 
#sort the counts from most to least frequent
counts = sorted(counts, key=lambda d: d["n"], reverse = True)
#add an entry to the symptom_table dictionary
symptom_table.append(dict(gene = 'MYO5B', 
                           disease = 'MYO5B deficiency',
                           analysis_level = 999, 
                           patients = count_patients, 
                           girls = count_girls, 
                           selection = sel,
                           counts = counts,
                           ))
#symptom_matrix = np.array([f"{'ID':>15}",f"{'disease':>10}"])
#symptom_matrix = np.append(symptom_matrix, [el["HPO_code"] for el in counts if el["n"] > 0])
print("Disease, MYO5B deficiency, ; selection, ", sel, "; symptoms as reported; unique symptoms, ", unique_symptoms)


    


                                       




# Serialize the python dictionnary to json
json_data = json.dumps(symptom_table, indent = 4)

# Writing to hp_symptom_stats.json
with open("hp_symptom_stats.json", "w") as outfile:
    outfile.write(json_data)


   



