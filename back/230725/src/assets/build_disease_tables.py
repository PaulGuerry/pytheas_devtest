#!/usr/bin/env python3
import fileinput
import json
import numpy

json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)



genes = ["KIF12", "ZFYVE19", "ATP8B1", "SKIC3", "SKIC2"]
names = ["PFIC8", "PFIC9", "PFIC1", "THES1", "THES2"]
colours = ["#e5e5e5", "#525252", "#e9d5ff", "#dc2626", "#a7f2d0"]
analysis_levels = [1, 2, 3, 4, 5, 6, 7, 8]   
disease_table = []

for gene in genes:
   ages_first = dict(all = dict(array = [], median = 0, iqr = 0),
               boys = dict(array = [], median = 0, iqr = 0),
               girls = dict(array = [], median = 0, iqr = 0))

   ages_last = dict(all = dict(array = [], status = [], median = 0, iqr = 0),
               boys = dict(array = [], status = [], median = 0, iqr = 0),
               girls = dict(array = [], status = [], median = 0, iqr = 0))
   
   count_patients = dict(total = 0, girls = 0, boys = 0)
   count_inbred = dict(yes = 0, no = 0, missing = 0)

   for object in patient_list: 
      if (object["gene"] == gene):
         count_patients["total"] += 1
         if 'sex' in object.keys():
            if object["sex"] == "F":
               count_patients["girls"] += 1
            elif object["sex"] == "M":
               count_patients["boys"] += 1

         if 'firstsymptomagemonth' in object.keys():
            try:
               ages_first["all"]["array"].append(float(object["firstsymptomagemonth"]))
            except:
               pass
            if ('sex' in object.keys() and object["sex"] == "F"):
               try:
                  ages_first["girls"]["array"].append(float(object["firstsymptomagemonth"])) 
               except:
                  pass
            else:
               try:
                  ages_first["boys"]["array"].append(float(object["firstsymptomagemonth"])) 
               except:
                  pass
        
        
         elif 'ageatmoleculardiagnostic' in object.keys():
            try:
               ages_first["all"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12)
            except:
                  print("Exception 65 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])
            if ('sex' in object.keys() and object["sex"] == "F"):
               try:
                  ages_first["girls"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12) 
               except:
                  print("Exception 65 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])
            else:
               try:
                  ages_first["boys"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12) 
               except:
                  print("Exception 70 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])

         
         #if age at last follow-up is specified
         if 'lastnewsageyear' in object.keys():
            try:
               ages_last["all"]["array"].append(float(object["lastnewsageyear"]))
            except:
               print("Exception 78 at, '{0:%s}', for patient {1:%s}".format(object["lastnewsageyear"]), object["id"])
            
            #fetch survival status
            if 'alivedead' in object.keys():
               try:
                  if object["alivedead"] == "alive":
                     ages_last["all"]["status"].append("0")
                  elif object["alivedead"] == "dead": 
                     ages_last["all"]["status"].append("1")
                  else:
                     print("Exception 87 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
               except:
                  print("Exception 89 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
            #if no survival status is specified (but age at last follow-up is specified) assume the patient was alive      
            else:  
               ages_last["all"]["status"].append("0")      
            
            
            if ('sex' in object.keys() and object["sex"] == "F"):
               try:
                  ages_last["girls"]["array"].append(float(object["lastnewsageyear"])) 
               except:
                  pass

               if 'alivedead' in object.keys():
                  try:
                     if object["alivedead"] == "alive":
                        ages_last["girls"]["status"].append("0")
                     elif object["alivedead"] == "dead": 
                        ages_last["girls"]["status"].append("1")
                     else:
                        print("Exception 107 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
                  except:
                     print("Exception 109 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
               else:  
                  ages_last["girls"]["status"].append("0")      
            

            else:
               try:
                  ages_last["boys"]["array"].append(float(object["lastnewsageyear"])) 
               except:
                  pass
               
               if 'alivedead' in object.keys():
                  try:
                     if object["alivedead"] == "alive":
                        ages_last["boys"]["status"].append("0")
                     elif object["alivedead"] == "dead": 
                        ages_last["boys"]["status"].append("1")
                     else:
                        print("Exception 107 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
                  except:
                     print("Exception 109 at, '{0:%s}', for patient {1:%s}".format(object["alivedead"]), object["id"])
               else:  
                  ages_last["boys"]["status"].append("0")      
            

         
         
         elif 'ageatmoleculardiagnostic' in object.keys():
            try:
               ages_last["all"]["array"].append(float(object["ageatmoleculardiagnostic"]))
            except:
                  print("Exception 96 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])
            if ('sex' in object.keys() and object["sex"] == "F"):
               try:
                  ages_last["girls"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
               except:
                  print("Exception 101 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])
            else:
               try:
                  ages_last["boys"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
               except:
                  print("Exception 106 at, '{0:%s}', for patient {1:%s}".format(object["ageatmoleculardiagnostic"]), object["id"])

         

         if 'consanguinity' in object.keys():
            if object["consanguinity"] == "yes":
               count_inbred["yes"] += 1
            else:
               count_inbred["no"] += 1 
         else:
            count_inbred["missing"] += 1

         #print(gene, count_patients["total"], object["id"], len(ages_last["all"]["array"]), len(ages_last["all"]["status"]) )         


   ages_first["all"]["median"] = numpy.median(ages_first["all"]["array"])        
   ages_first["girls"]["median"] = numpy.median(ages_first["girls"]["array"])        
   ages_first["boys"]["median"] = numpy.median(ages_first["girls"]["array"])        
   ages_first["all"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["all"]["array"], [75, 25]))
   ages_first["girls"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["girls"]["array"], [75, 25]))
   ages_first["boys"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["boys"]["array"], [75, 25]))
   
   ages_last["all"]["median"] = numpy.median(ages_last["all"]["array"])        
   ages_last["girls"]["median"] = numpy.median(ages_last["girls"]["array"])        
   ages_last["boys"]["median"] = numpy.median(ages_last["girls"]["array"])        
   ages_last["all"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["all"]["array"], [75, 25]))
   ages_last["girls"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["girls"]["array"], [75, 25]))
   ages_last["boys"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["boys"]["array"], [75, 25]))
 
   for dict_key, dict_val in ages_first.items():
      for k, v in dict_val.items():
         try:
            #Round and convert to list for compatibility with json.dumps lated
            dict_val[k] = numpy.round(v, 2).tolist()
         except:
            print("119 - Unable to round {2:s}, for gene {0:s}, ages_first {1:s}".format(gene, dict_val, v))

  
   #round values to two digits and output information in R-readable format
   for dict_key, dict_val in ages_last.items():
      time_string = "time <- c("
      status_string = "status <-c("
      
      for k, v in dict_val.items():
         if k != "status":
            try:
               #Round and convert to list for compatibility with json.dumps lated
               dict_val[k] = numpy.round(v, 2).tolist()

            except:
               print("127 - Unable to round {2:s}, for gene {0:s}, ages_last {1:s}".format(gene, dict_val, v))
         
         if k == "status":
               for s in v:
                     status_string += str(s)+", "
                     
         elif k == "array":
               for t in v:
                  time_string += str(t)+", "         

      time_string += ")" 
      status_string += ")"
      print("   ")
      print(gene + "---------------------") 
      print(dict_key)
      print(time_string)
      print(status_string)


   
   disease_table.append(dict(gene = gene, 
                             name = names[genes.index(gene)],
                             colour = colours[genes.index(gene)], 
                             patients = count_patients,
                             consanguinous = count_inbred, 
                             age_at_first_symp = ages_first,
                             age_at_last_news = ages_last))
   





# Serialize the python dictionnary to json
json_data = json.dumps(disease_table, indent = 4)

# Writing to hp_trees.json
with open("hp_disease_stats.json", "w") as outfile:
    outfile.write(json_data)


   



