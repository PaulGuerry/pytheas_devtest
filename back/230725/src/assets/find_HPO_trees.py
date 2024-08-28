#!/usr/bin/env python3
import sys
import fileinput
import json
import numpy


json_data=""
for line in fileinput.input(files="hp_edges.json"):
    json_data = json_data + line
HPO_edges_list = json.loads(json_data)

json_data=""
for line in fileinput.input(files="hp_nodes.json"):
    json_data = json_data + line
HPO_nodes_list = json.loads(json_data)

parent_branches = numpy.full((1, 1), "--------")
append_array = numpy.full((1, 1), "--------")
#print(parent_branches)

child_code = sys.argv[1]
parent_branches[0, 0] = child_code

edge_list = (item["obj"] for item in HPO_edges_list["graphs"][0]["edges"] if child_code == item["sub"][34:]) 
edge_array = numpy.array(list(edge_list))
edge_array.shape = (edge_array.shape[0], 1)
parent_code = edge_array[0, 0][34:]
append_array[0, 0] = parent_code

#add extra rows to the parent_branches array if more than one parent_codes are found
if (edge_array.shape[0] > 1):
   for j in range(1, edge_array.shape[0]):
      parent_code = edge_array[j, 0][34:]
      extra_row = numpy.array([parent_branches[0, :]])
      #print(parent_code, [parent_code], numpy.full((1, 1), parent_code), parent_branches[0, :], extra_row)
      #print(numpy.full((1, 1), parent_code).shape, parent_branches[0, :].shape, extra_row.shape)
      parent_branches = numpy.append(parent_branches, extra_row, axis = 0) 
      append_array = numpy.append(append_array, numpy.full((1, 1), parent_code), axis = 0)


parent_branches = numpy.append(parent_branches, append_array, axis = 1)    

#print("start")
#print(parent_branches)


parent_code = ""
parent_code_alt = ""
loopNo = 0
finished = False

#print(parent_branches.shape, parent_branches.shape[1], parent_branches)

while finished == False:
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
  loopNo += 1

  branch_no = parent_branches.shape[0]
  branch_len = parent_branches.shape[1]

  #print(loopNo, branch_no, branch_len)

  #Only stop looping (finished = True) when all the branches have reached the top
  for i in range(branch_no):
     #print(loopNo, i, parent_branches[i, branch_len - 1])
     if (parent_branches[i, branch_len - 1] != "0000001" and parent_branches[i, branch_len - 1] != "-------" ):
        break
     
     if i == branch_no - 1: 
        finished = True

branch_no = parent_branches.shape[0]
for i in range(branch_no):
   print("branch ", i, " --> ", parent_branches[i, :])


exit()


while parent_code != "0000001":
  edge_list = (item["obj"] for item in HPO_edges_list["graphs"][0]["edges"] if symptom_code in item["sub"]) 
  edge_list = list(edge_list)
  parent_code = edge_list[0][34:]
  parent_code_list.append(parent_code)
  print(parent_code_list)
  symptom_code = parent_code


  

# Serialize the python dictionnary to json
# json_data = json.dumps(HPO_code_list, indent=4)

# Writing to hp_trees.json
# with open("hp_trees.json", "w") as outfile:
#    outfile.write(json_data)


