#!/usr/bin/env python3
import fileinput
import json
import numpy


json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)



json_data=""
for line in fileinput.input(files="hp_edges.json"):
    json_data = json_data + line
HPO_edges_list = json.loads(json_data)

json_data=""
for line in fileinput.input(files="hp_nodes_modPG.json"):
    json_data = json_data + line
HPO_nodes_list = json.loads(json_data)

symptom_no = 0
added_no = 0

HPO_code_library = []
already_in_library = False


for patient in patient_list:

  patient_symptoms = []

  if 'symptoms' in patient.keys():
    patient_symptoms = patient["symptoms"]


  for child_code in patient_symptoms:   

    #print(symptom_no, " unique symptoms, ", added_no, " HPO branches.")
    if (len(child_code) != 7):
       print("Warning: ", child_code, " is not a valid HPO code! Skipping")
       already_in_library = True
    
    else:
       already_in_library = False
       for item in HPO_code_library:
          if item["code"] == child_code:
             already_in_library = True

    if already_in_library == False:
      for item in HPO_nodes_list["graphs"][0]["nodes"]:
         if child_code  == item["id"][34:]:
            lbl = item["lbl"]
            break
      
      #new entry in library created here
      HPO_code_library.append(dict(code = child_code, description = lbl, parent_branches = [], branch_lengths = []))
      
      parent_branches = numpy.full((1, 1), "--------")
      append_array = numpy.full((1, 1), "--------")
      parent_branches[0, 0] = child_code

      edge_list = (item["obj"] for item in HPO_edges_list["graphs"][0]["edges"] if child_code == item["sub"][34:]) 
      edge_array = numpy.array(list(edge_list))
      #print("Test 71. Patient, ", patient["id"], "; child code, ", child_code)
      #print("Test 71. edge_array, ", edge_array)
      #print("Test 71. edge_array.shape, ", edge_array.shape[0])
      parent_code = edge_array[0][34:]
      append_array[0, 0] = parent_code


      #add extra rows to the parent_branches array if more than one parent_codes are found
      if (edge_array.shape[0] > 1):
         for j in range(1, edge_array.shape[0]):
            parent_code = edge_array[j][34:]
            extra_row = numpy.array([parent_branches[0, :]])
            #print(parent_code, [parent_code], numpy.full((1, 1), parent_code), parent_branches[0, :], extra_row)
            #print(numpy.full((1, 1), parent_code).shape, parent_branches[0, :].shape, extra_row.shape)
            parent_branches = numpy.append(parent_branches, extra_row, axis = 0) 
            append_array = numpy.append(append_array, numpy.full((1, 1), parent_code), axis = 0)


      parent_branches = numpy.append(parent_branches, append_array, axis = 1)    
      branches_all_finished = False

      while branches_all_finished == False:
        branch_no = parent_branches.shape[0]
        branch_len = parent_branches.shape[1]
        #initialize the column array to append to the end of the branches
        append_array = numpy.full((branch_no, 1), "--------")

        for i in range(branch_no):
           child_code = parent_branches[i, branch_len - 1]
           if child_code != "0000001" and child_code != "-------": 
            edge_list = (item["obj"] for item in HPO_edges_list["graphs"][0]["edges"] if child_code == item["sub"][34:]) 
            edge_array = numpy.array(list(edge_list))
            #print(child_code, parent_code, parent_code_alt, parent_branches[i, :])
            edge_array.shape = (edge_array.shape[0], 1)
            #print("edge_array.shape, edge_array", edge_array[0], edge_array[0, 0], edge_array[0, 0][34:])
            parent_code = edge_array[0, 0][34:]
           else:
            parent_code = "-------"

           #print("append_array 1, ", append_array)
           append_array[i, 0] = parent_code
           #print("append_array 2, ", append_array)

           #add extra rows to the parent_branches array if more than one parent_codes are found
           if (edge_array.shape[0] > 1):
              for j in range(1, edge_array.shape[0]):
                 parent_code_alt = edge_array[j, 0][34:]
                 extra_row = numpy.array([parent_branches[i, :]])
                 #print("extra row", extra_row, parent_branches)
                 parent_branches = numpy.append(parent_branches, extra_row, axis = 0) 
                 append_array = numpy.append(append_array, numpy.full((1, 1), parent_code_alt), axis = 0)



        parent_branches = numpy.append(parent_branches, append_array, axis = 1)    
        #print("loop", loopNo, ", parent branches, ", parent_branches)

        branch_no = parent_branches.shape[0]
        branch_len = parent_branches.shape[1]

        #print(loopNo, branch_no, branch_len)

        #Only stop looping (branches_all_finished = True) when all the branches have reached the top
        for i in range(branch_no):
           #print(loopNo, i, parent_branches[i, branch_len - 1])
           if (parent_branches[i, branch_len - 1] != "0000001" and parent_branches[i, branch_len - 1] != "-------" ):
              break
            
           if i == branch_no - 1: 
              branches_all_finished = True

        branch_lengths = numpy.full((branch_no), 0)
        #Loop again over all branches to determine how long they each are
        for i in range(branch_no):
           for j in range(branch_len):
               if parent_branches[i, j] == "0000001":
                  branch_lengths[i] = j
                  break

         
      HPO_code_library[symptom_no]["parent_branches"] = parent_branches.tolist()
      HPO_code_library[symptom_no]["branch_lengths"] = branch_lengths.tolist()
      added_no += branch_no        
      symptom_no += 1
      #for i in range(branch_no):
      #  print("branch ", i, " --> ", parent_branches[i, :])
    


print('{0:4d} unique symptoms analyzed'.format(symptom_no))
print('{0:4d} HPO trees written to hp_trees.json'.format(added_no))


# Serialize the python dictionnary to json
json_data = json.dumps(HPO_code_library, indent=4, sort_keys=True)

# Writing to hp_trees.json
with open("hp_trees.json", "w") as outfile:
    outfile.write(json_data)



exit()


#DEFUNCT CODE BELOW

for patient in patient_list:

      HPO_code_list = patient["symptoms"]   
      
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
json_data = json.dumps(HPO_code_list, indent=4, sort_keys=True)

# Writing to hp_trees.json
with open("hp_trees.json", "w") as outfile:
    outfile.write(json_data)
