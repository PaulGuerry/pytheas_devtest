#!/usr/bin/env python3
import fileinput
import json
import numpy

json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)



genes = ["KIF12", "ZFYVE19", "ATP8B1", "SKIC3", "SKIC2", "ABCB11", "ABCB4", "TJP2", "NR1H4", "SLC51A", "USP53", "MYO5B", "SEMA7A", "TMEM199"]
names = ["PFIC8", "PFIC9", "PFIC1", "THES1", "THES2", "PFIC2", "PFIC3", "PFIC4", "PFIC5", "PFIC6", "PFIC7", "PFIC10", "PFIC11", "CDG2P"]
# 20 colours taken from https://tailwindcss.com/docs/customizing-colors 
# starting from neutral and working down, every second row, opacity 300 and 700
colours = ["#d4d4d4", "#404040", "#fca5a5", "#b91c1c", "#fcd34d", "#b45309", "#bef264", "#4d7c0f",
           "#6ee7b7", "#047857", "#67e8f9", "#0e7490", "#93c5fd", "#1d4ed8", "#c4b5fd", "#6d28d9",
           "#f0abfc", "#a21caf", "#fda4af", "#be123c"]
analysis_levels = [1, 2, 3, 4, 5, 6, 7, 8]   
disease_table = []

for gene in genes:
   print("Building disease table for gene {0:s}".format(gene))
   ages_first = dict(all = dict(array = [], median = 0, iqr = 0),
               boys = dict(array = [], median = 0, iqr = 0),
               girls = dict(array = [], median = 0, iqr = 0))

   ages_last = dict(all = dict(array = [], status = [], median = 0, iqr = 0),
               boys = dict(array = [], status = [], median = 0, iqr = 0),
               girls = dict(array = [], status = [], median = 0, iqr = 0))
   
   # need to account for the fact that in some cases, the age of death is different from the age at last follow-up
   ages_surv = dict(all = dict(array = [], status = [], median = 0, iqr = 0),
               boys = dict(array = [], status = [], median = 0, iqr = 0),
               girls = dict(array = [], status = [], median = 0, iqr = 0))

   count_patients = dict(total = 0, girls = 0, boys = 0)
   count_inbred = dict(yes = 0, no = 0, missing = 0)
   articles = []
   symptomCount = 0
   missingVarCount = 0
   presentVarCount = 0

   for object in patient_list: 
      if ('gene' in object.keys()):
         if (object["gene"] == gene):
            count_patients["total"] += 1
            if 'sex' in object.keys():
               presentVarCount += 1
               if object["sex"] == "F":
                  count_patients["girls"] += 1
               elif object["sex"] == "M":
                  count_patients["boys"] += 1
            else:
               missingVarCount += 1

            if 'firstsymptomagemonth' in object.keys():
               presentVarCount += 1
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
               presentVarCount += 1
               try:
                  ages_first["all"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12)
               except:
                     print("Exception 65 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
               if ('sex' in object.keys() and object["sex"] == "F"):
                  try:
                     ages_first["girls"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12) 
                  except:
                     print("Exception 65 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
               else:
                  try:
                     ages_first["boys"]["array"].append(float(object["ageatmoleculardiagnostic"]) * 12) 
                  except:
                     print("Exception 70 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
            else:
               missingVarCount += 1
         
            #if age at last follow-up is specified 
            if 'lastnewsageyear' in object.keys():
               presentVarCount += 1
               try:
                  ages_last["all"]["array"].append(float(object["lastnewsageyear"]))
                  ages_surv["all"]["array"].append(float(object["lastnewsageyear"]))
               except:
                  print("Exception 78 at, '{0:s}', for patient {1:s}".format(object["lastnewsageyear"]), object["id"])
               
               #fetch survival status
               if 'alivedead' in object.keys():
                  try:
                     if object["alivedead"] == "alive":
                        ages_last["all"]["status"].append("0")
                        ages_surv["all"]["status"].append("0")
                     elif object["alivedead"] == "dead": 
                        ages_last["all"]["status"].append("1")
                        ages_surv["all"]["status"].append("1")
                        # if patient has died, check if the age of death is specified and if it is, use that rather than the age at last fo for survival analysis
                        # do the same for boys and girls below
                        if 'ageofdeathy' in object.keys():
                           ages_surv["all"]["array"].pop()
                           ages_surv["all"]["array"].append(float(object['ageofdeathy']))
                     else:
                        print("Exception 87 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                  except:
                     print("Exception 89 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
               
               #if no survival status is specified (but age at last follow-up is specified) assume the patient was alive      
               else:  
                  ages_last["all"]["status"].append("0")      
                  ages_surv["all"]["status"].append("0")      
               
               
               if ('sex' in object.keys() and object["sex"] == "F"):
                  try:
                     ages_last["girls"]["array"].append(float(object["lastnewsageyear"])) 
                     ages_surv["girls"]["array"].append(float(object["lastnewsageyear"]))
                  except:
                     pass

                  if 'alivedead' in object.keys():
                     try:
                        if object["alivedead"] == "alive":
                           ages_last["girls"]["status"].append("0")
                           ages_surv["girls"]["status"].append("0")
                        elif object["alivedead"] == "dead": 
                           ages_last["girls"]["status"].append("1")
                           ages_surv["girls"]["status"].append("1")
                           # casewhen dead & age of death specified   
                           if 'ageofdeathy' in object.keys():
                              ages_surv["girls"]["array"].pop()
                              ages_surv["girls"]["array"].append(float(object['ageofdeathy']))
                        else:
                           print("Exception 107 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                     except:
                        print("Exception 109 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                  else:  
                     ages_last["girls"]["status"].append("0")      
                     ages_surv["girls"]["status"].append("0")      
               

               elif ('sex' in object.keys() and object["sex"] == "M"):
                  try:
                     ages_last["boys"]["array"].append(float(object["lastnewsageyear"])) 
                     ages_surv["boys"]["array"].append(float(object["lastnewsageyear"])) 
                  except:
                     pass
                  
                  if 'alivedead' in object.keys():
                     try:
                        if object["alivedead"] == "alive":
                           ages_last["boys"]["status"].append("0")
                           ages_surv["boys"]["status"].append("0")
                        elif object["alivedead"] == "dead": 
                           ages_last["boys"]["status"].append("1")
                           ages_surv["boys"]["status"].append("1")
                           # casewhen dead & age of death specified   
                           if 'ageofdeathy' in object.keys():
                              ages_surv["boys"]["array"].pop()
                              ages_surv["boys"]["array"].append(float(object['ageofdeathy']))
                        else:
                           print("Exception 107 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                     except:
                        print("Exception 109 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                  else:  
                     ages_last["boys"]["status"].append("0")      
                     ages_surv["boys"]["status"].append("0")      
               
               else:
                  missingVarCount += 1
                  if 'sex' in object.keys():
                     print("Unrecognised sex for patient {0:s}".format(object["id"]))
                  else:
                     print("Missing sex for patient {0:s}".format(object["id"]))
         
            # if age at last fo is not specified, use age at molecular diagnostic instead and define patient as alive at this age
            elif 'ageatmoleculardiagnostic' in object.keys():
               presentVarCount += 1
               try:
                  ages_last["all"]["array"].append(float(object["ageatmoleculardiagnostic"]))
                  ages_surv["all"]["array"].append(float(object["ageatmoleculardiagnostic"]))
                  ages_last["all"]["status"].append("0")
                  ages_surv["all"]["status"].append("0")
               except:
                     print("Exception 191 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
               if ('sex' in object.keys() and object["sex"] == "F"):
                  try:
                     ages_last["girls"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
                     ages_surv["girls"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
                     ages_last["girls"]["status"].append("0")
                     ages_surv["girls"]["status"].append("0")
                  except:
                     print("Exception 196 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
               elif ('sex' in object.keys() and object["sex"] == "M"):
                  try:
                     ages_last["boys"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
                     ages_surv["boys"]["array"].append(float(object["ageatmoleculardiagnostic"])) 
                     ages_last["boys"]["status"].append("0")
                     ages_surv["boys"]["status"].append("0")
                  except:
                     print("Exception 106 at, '{0:s}', for patient {1:s}".format(object["ageatmoleculardiagnostic"]), object["id"])
               else:
                  missingVarCount += 1
                  if 'sex' in object.keys():
                     print("Unrecognised sex for patient {0:s}".format(object["id"]))
                  else:
                     print("Missing sex for patient {0:s}".format(object["id"]))

            else:
               missingVarCount += 1

         

            if 'consanguinity' in object.keys():
               presentVarCount += 1
               if object["consanguinity"] == "yes":
                  count_inbred["yes"] += 1
               else:
                  count_inbred["no"] += 1 
            else:
               count_inbred["missing"] += 1
               missingVarCount += 1

            if 'doi' in object.keys():
               articles.append(object["doi"])

            if 'symptoms' in object.keys():
               presentVarCount += 1
               symptomCount += len(set(object["symptoms"]))
            else:
               missingVarCount += 1


            #print(gene, count_patients["total"], object["id"], len(ages_last["all"]["array"]), len(ages_last["all"]["status"]) )         


   if len(ages_first["all"]["array"]) > 0:
      ages_first["all"]["median"] = numpy.median(ages_first["all"]["array"])        
   if len(ages_first["girls"]["array"]) > 0:
      ages_first["girls"]["median"] = numpy.median(ages_first["girls"]["array"])        
   if len(ages_first["boys"]["array"]) > 0:
      ages_first["boys"]["median"] = numpy.median(ages_first["boys"]["array"])        

   if len(ages_first["all"]["array"]) > 1:
      ages_first["all"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["all"]["array"], [75, 25]))
   if len(ages_first["girls"]["array"]) > 1:
      ages_first["girls"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["girls"]["array"], [75, 25]))
   if len(ages_first["boys"]["array"]) > 1:
      ages_first["boys"]["iqr"] = numpy.subtract(*numpy.percentile(ages_first["boys"]["array"], [75, 25]))
  
   if len(ages_last["all"]["array"]) > 0:
      ages_last["all"]["median"] = numpy.median(ages_last["all"]["array"])        
   if len(ages_last["girls"]["array"]) > 0:
      ages_last["girls"]["median"] = numpy.median(ages_last["girls"]["array"])        
   if len(ages_last["boys"]["array"]) > 0:
      ages_last["boys"]["median"] = numpy.median(ages_last["boys"]["array"])        

   if len(ages_last["all"]["array"]) > 1:
      ages_last["all"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["all"]["array"], [75, 25]))
   if len(ages_last["girls"]["array"]) > 1:
      ages_last["girls"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["girls"]["array"], [75, 25]))
   if len(ages_last["boys"]["array"]) > 1:
      ages_last["boys"]["iqr"] = numpy.subtract(*numpy.percentile(ages_last["boys"]["array"], [75, 25]))
 
 
   if len(ages_surv["all"]["array"]) > 0:
      ages_surv["all"]["median"] = numpy.median(ages_surv["all"]["array"])        
   if len(ages_surv["girls"]["array"]) > 0:
      ages_surv["girls"]["median"] = numpy.median(ages_surv["girls"]["array"])        
   if len(ages_surv["boys"]["array"]) > 0:
      ages_surv["boys"]["median"] = numpy.median(ages_surv["boys"]["array"])        

   if len(ages_surv["all"]["array"]) > 1:
      ages_surv["all"]["iqr"] = numpy.subtract(*numpy.percentile(ages_surv["all"]["array"], [75, 25]))
   if len(ages_surv["girls"]["array"]) > 1:
      ages_surv["girls"]["iqr"] = numpy.subtract(*numpy.percentile(ages_surv["girls"]["array"], [75, 25]))
   if len(ages_surv["boys"]["array"]) > 1:
      ages_surv["boys"]["iqr"] = numpy.subtract(*numpy.percentile(ages_surv["boys"]["array"], [75, 25]))
   
 
   for dict_key, dict_val in ages_first.items():
      for k, v in dict_val.items():
         try:
            #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
               if type(v) is list:
                  v = [round(x, 2) for x in v] 
               else: 
                  v = round(v)

         except:
            print("119 - Unable to round {2:s}, for gene {0:s}, ages_first {1:s}".format(gene, dict_val, v))

  
   #round values to two digits and output information in R-readable format
   for dict_key, dict_val in ages_last.items():
      
      for k, v in dict_val.items():
         if k != "status":
            try:
               #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
               if type(v) is list:
                  v = [round(x, 2) for x in v] 
               else: 
                  v = round(v)

            except:
               print("290 - Unable to round {2:s}, for gene {0:s}, ages_last {1:s}".format(gene, dict_val, v))
         
   
   #round values to two digits and output information in R-readable format
   for dict_key, dict_val in ages_surv.items():
      time_string = "time <- c("
      status_string = "status <-c("
      
      for k, v in dict_val.items():
         if k != "status":
            try:
               #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
               if type(v) is list:
                  v = [round(x, 2) for x in v] 
               else: 
                  v = round(v)

            except:
               print("305 - Unable to round {2:s}, for gene {0:s}, ages_last {1:s}".format(gene, dict_val, v))
         
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
                             articles = len(set(articles)),
                             datapoints = presentVarCount + symptomCount,
                             variables = dict(present = presentVarCount, missing = missingVarCount),
                             consanguinous = count_inbred, 
                             age_at_first_symp = ages_first,
                             age_at_last_news = ages_last))
   





# Serialize the python dictionnary to json
json_data = json.dumps(disease_table, indent = 4)

# Writing to hp_trees.json
with open("bpt_out.json", "w") as outfile:
    outfile.write(json_data)


   



