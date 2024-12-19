#!/usr/bin/env python3
import fileinput
import json
import numpy

json_data = ""
#for line in fileinput.input(files="epdj_output.json"):
for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line
patient_list = json.loads(json_data)

# 20 colours taken from https://tailwindcss.com/docs/customizing-colors 
# starting from neutral and working down, every second row, opacity 300 and 700
colours = ["#d4d4d4", "#404040", "#fca5a5", "#b91c1c", "#fcd34d", "#b45309", "#bef264", "#4d7c0f",
           "#6ee7b7", "#047857", "#67e8f9", "#0e7490", "#93c5fd", "#1d4ed8", "#c4b5fd", "#6d28d9",
           "#f0abfc", "#a21caf", "#fda4af", "#be123c"]


diseases = [dict(name = "PFIC1", gene = "ATP8B1", matches = ["PFIC1"], colour = colours[0]),
            dict(name = "PFIC2", gene = "ABCB11", matches = ["PFIC2"], colour = colours[1]),
            dict(name = "PFIC3", gene = "ABCB4", matches = ["PFIC3"], colour = colours[2]),
            dict(name = "PFIC4", gene = "TJP2", matches = ["PFIC4"], colour = colours[3]),
            dict(name = "PFIC5", gene = "NR1H4", matches = ["PFIC5"], colour = colours[4]),
            dict(name = "PFIC6", gene = "SLC51A", matches = ["PFIC6"], colour = colours[5]),
            dict(name = "PFIC7", gene = "USP53", matches = ["PFIC7"], colour = colours[6]),
            dict(name = "PFIC8", gene = "KIF12", matches = ["PFIC8"], colour = colours[7]),
            dict(name = "PFIC9", gene = "ZFYVE19", matches = ["PFIC9"], colour = colours[8]),
            dict(name = "PFIC10", gene = "MYO5B", matches = ["PFIC10"], colour = colours[9]),
            dict(name = "PFIC11", gene = "SEMA7A", matches = ["PFIC11"], colour = colours[10]),
            dict(name = "CDG2P", gene = "TMEM199", matches = ["CDG2P"], colour = colours[11]),
            dict(name = "THES1", gene = "SKIC3", matches = ["THES1"], colour = colours[12]),
            dict(name = "THES2", gene = "SKIC2", matches = ["THES2"], colour = colours[13]),
            dict(name = "THES", gene = "SKIC2,3,?", matches = ["THES", "THES1", "THES2"], colour = colours[14]),
            dict(name = "FOCADS", gene = "FOCAD", matches = ["FOCADS"], colour = colours[15]),
            dict(name = "ARCS1", gene = "VPS33B", matches = ["ARCS1"], colour = colours[16]),
            dict(name = "ARCS2", gene = "VIPAS39", matches = ["ARCS2"], colour = colours[17]),
            dict(name = "ARCS", gene = "VPSVIPAS?", matches = ["ARCS", "ARCS1", "ARCS2"], colour = colours[18])
            ]



disease_table = []

for disease in diseases:
   print("Building disease table for disease {0:s}".format(disease['name']))
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
      #if (disease["name"] == "ARCS1"): print(object["id"])
      if ('disease' in object.keys()):
         if (object["disease"] in disease['matches']):
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
            
            
            # If alivedeadage is specified (separately from age at last follow-up)
            if 'alivedeadage' in object.keys():
               if object["alivedeadage"] is not None:
                  presentVarCount += 1
                  #if (disease["name"] == "ARCS1"):
                  #   print(object["id"], object["alivedeadage"])
                  try:
                     ages_last["all"]["array"].append(float(object["alivedeadage"]))
                     ages_surv["all"]["array"].append(float(object["alivedeadage"]))
                     if ('sex' in object.keys() and object["sex"] == "F"):
                        ages_last["girls"]["array"].append(float(object["alivedeadage"]))
                        ages_surv["girls"]["array"].append(float(object["alivedeadage"]))
                     if ('sex' in object.keys() and object["sex"] == "M"):
                        ages_last["boys"]["array"].append(float(object["alivedeadage"]))
                        ages_surv["boys"]["array"].append(float(object["alivedeadage"]))
                  except:
                     print("Exception 128 at, '{0:s}', for patient {1:s}".format(object["alivedeadage"]), object["id"])
               
                  #fetch survival status (only if age is known)
                  if 'alivedead' in object.keys():
                     try:
                        if object["alivedead"] == "alive":
                           ages_last["all"]["status"].append("0")
                           ages_surv["all"]["status"].append("0")
                           if ('sex' in object.keys() and object["sex"] == "F"):
                              ages_last["girls"]["status"].append("0")
                              ages_surv["girls"]["status"].append("0")
                           if ('sex' in object.keys() and object["sex"] == "M"):
                              ages_last["boys"]["status"].append("0")
                              ages_surv["boys"]["status"].append("0")
                        elif object["alivedead"] == "dead": 
                           ages_last["all"]["status"].append("1")
                           ages_surv["all"]["status"].append("1")
                           if ('sex' in object.keys() and object["sex"] == "F"):
                              ages_last["girls"]["status"].append("1")
                              ages_surv["girls"]["status"].append("1")
                           if ('sex' in object.keys() and object["sex"] == "M"):
                              ages_last["boys"]["status"].append("1")
                              ages_surv["boys"]["status"].append("1")
                        else:
                           print("Exception 152 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                     except:
                        print("Exception 154 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])

            #if last known age is not specified, use age at last follow-up 
            elif 'lastnewsageyear' in object.keys():
               if object["lastnewsageyear"] is not None:
                  presentVarCount += 1
                  try:
                     ages_last["all"]["array"].append(float(object["lastnewsageyear"]))
                     ages_surv["all"]["array"].append(float(object["lastnewsageyear"]))
                     if ('sex' in object.keys() and object["sex"] == "F"):
                        ages_last["girls"]["array"].append(float(object["lastnewsageyear"]))
                        ages_surv["girls"]["array"].append(float(object["lastnewsageyear"]))
                     if ('sex' in object.keys() and object["sex"] == "M"):
                        ages_last["boys"]["array"].append(float(object["lastnewsageyear"]))
                        ages_surv["boys"]["array"].append(float(object["lastnewsageyear"]))
                  except:
                     print("Exception 170 at, '{0:s}', for patient {1:s}".format(object["lastnewsageyear"]), object["id"])
               
               #fetch survival status
               if 'alivedead' in object.keys():
                  try:
                     if object["alivedead"] == "alive":
                        ages_last["all"]["status"].append("0")
                        ages_surv["all"]["status"].append("0")
                        if ('sex' in object.keys() and object["sex"] == "F"):
                           ages_last["girls"]["status"].append("0")
                           ages_surv["girls"]["status"].append("0")
                        if ('sex' in object.keys() and object["sex"] == "M"):
                           ages_last["boys"]["status"].append("0")
                           ages_surv["boys"]["status"].append("0")
                     elif object["alivedead"] == "dead": 
                        ages_last["all"]["status"].append("1")
                        ages_surv["all"]["status"].append("1")
                        if ('sex' in object.keys() and object["sex"] == "F"):
                           ages_last["girls"]["status"].append("1")
                           ages_surv["girls"]["status"].append("1")
                        if ('sex' in object.keys() and object["sex"] == "M"):
                           ages_last["boys"]["status"].append("1")
                           ages_surv["boys"]["status"].append("1")
                     else:
                        print("Exception 194 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
                  except:
                     print("Exception 196 at, '{0:s}', for patient {1:s}".format(object["alivedead"]), object["id"])
               
               #if no survival status is specified (but age at last follow-up is specified) assume the patient was alive      
               else:  
                  ages_last["all"]["status"].append("0")      
                  ages_surv["all"]["status"].append("0")      
               
               
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
               if object["consanguinity"] == "yes" or object["consanguinity"] == "Y":
                  count_inbred["yes"] += 1
               elif object["consanguinity"] == "non" or object["consanguinity"] == "N": 
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
            print("119 - Unable to round {2:s}, for disease {0:s}, ages_first {1:s}".format(disease['name'], dict_val, v))

  
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
               print("290 - Unable to round {2:s}, for disease {0:s}, ages_last {1:s}".format(disease['name'], dict_val, v))
         
   
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
               print("305 - Unable to round {2:s}, for disease {0:s}, ages_last {1:s}".format(disease['name'], dict_val, v))
         
         if k == "status":
               for s in v:
                     status_string += str(s)+", "
                     
         elif k == "array":
               for t in v:
                  time_string += str(t)+", "     


      time_string += ")" 
      status_string += ")"
      print("   ")
      print(disease['name'] + "---------------------") 
      print(dict_key)
      print(time_string)
      print(status_string)


   
   disease_table.append(dict(gene = disease['gene'],
                             name = disease['name'],
                             colour = disease['colour'],
                             patients = count_patients,
                             articles = len(set(articles)),
                             datapoints = presentVarCount + symptomCount,
                             variables = dict(present = presentVarCount, missing = missingVarCount),
                             consanguinous = count_inbred, 
                             age_at_first_symp = ages_first,
                             age_at_last_news = ages_last))
   





# Serialize the python dictionnary to json
json_data = json.dumps(disease_table, indent = 4)

# Writing to bdt_out.json
# Check output before copying to hp_disease_stats.json
with open("bdt_out.json", "w") as outfile:
    outfile.write(json_data)


   



