#!/usr/bin/env python3

import fileinput
import json
import re 
import numpy

json_data = ""
# 
substring = '('

for line in fileinput.input(files="temp.txt"):
    json_data = json_data + line

patient_dict = json.loads(json_data)
count_sympdate = 0
count_sympdup = 0
for object in patient_dict:
  subs = 0
  res = []
  if 'symptoms' in object.keys():
    for symptom_code in object["symptoms"]:
      if substring in symptom_code:
        subs = 1
        res.append(re.sub(r'\([^()]*\)', '', symptom_code))
      else:
        res.append(symptom_code)
    
  # also save symptom_codes saved under "biology" key  
  if 'labfindings' in object.keys():
    for symptom_code in object["labfindings"]:
      res.append(symptom_code)  
  
  if (len(res) > 0): 
    #remove duplicates
    symptom_set = set(res)
    symptom_list = res
    if (len(symptom_set) < len(symptom_list)):
        count_sympdup+=1
    object["symptoms"] = list(symptom_set)

  if 'ageatmoleculardiagnostic' in object.keys():
     try:
      float(object["ageatmoleculardiagnostic"])
      if (float(object["ageatmoleculardiagnostic"]) > 999.):
        print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["ageatmoleculardiagnostic"]), object["id"])) 
     except:
      print('Non-numeric age, {0:s}, for patient {1:s}'.format(str(object["ageatmoleculardiagnostic"]), object["id"]))

  if 'ageatfirstsymptoms' in object.keys():
     try:
      float(object["ageatfirstsymptoms"])
      if (float(object["ageatfirstsymptoms"]) > 999.):
        print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["ageatfirstsymptoms"]), object["id"])) 
     except:
      print('Non-numeric age, {0:s}, for patient {1:s}'.format(str(object["ageatfirstsymptoms"]), object["id"]))

  if 'lastnewsageyear' in object.keys():
     try:
      float(object["lastnewsageyear"])
      if (float(object["lastnewsageyear"]) > 200.):
        print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["lastnewsageyear"]), object["id"])) 
     except:
      print('Non-numeric age, {0:s}, for patient {1:s}'.format(str(object["lastnewsageyear"]), object["id"]))
  elif 'ageatmoleculardiagnostic' in object.keys():
      try:
        float(object["ageatmoleculardiagnostic"])
        if (float(object["ageatmoleculardiagnostic"]) > 200.):
          print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["ageatmoleculardiagnostic"]), object["id"])) 
      except:
        print('Non-numeric age, {0:s}, for patient {1:s}'.format(str(object["ageatmoleculardiagnostic"]), object["id"]))
      else:
        object["lastnewsageyear"] = round(float(object["ageatmoleculardiagnostic"]), 2)
  elif 'firstsymptomagemonth' in object.keys():
      try:
        float(object["firstsymptomagemonth"])
        if (float(object["firstsymptomagemonth"]) > 100.):
          print('Check age {0:s} months for patient {1:s}.'.format(str(object["firstsymptomagemonth"]), object["id"])) 
      except:
        print('Non-numeric age, {0:s}, for patient {1:s}'.format(str(object["firstsymptomagemonth"]), object["id"]))
      else:
        object["lastnewsageyear"] = round(float(object["firstsymptomagemonth"]) / 12., 2)

  if 'alivedead' in object.keys():
      if (object["alivedead"] != "alive" and object["alivedead"] != "dead"):
        print('unrecognised alive/dead status, {0:s}, for patient {1:s}.'.format(str(object["alivedead"]), object["id"])) 
  else:
    print('No alive/dead information for patient {0:s}.'.format(object["id"]))

  # 240913
  if 'gene' in object.keys():
      if object["gene"] == "ATP8B1":
        object["disease"] = "PFIC1"
        #print('Gene, {0:s}; Disease, {1:s}; ID, {2:s}.'.format(str(object["gene"]), object["disease"], object["id"]))
      elif object["gene"] == "ABCB11":
        object["disease"] = "PFIC2"
      elif object["gene"] == "ABCB4":
        object["disease"] = "PFIC3"
      elif object["gene"] == "TJP2":
        object["disease"] = "PFIC4"
      elif object["gene"] == "NR1H4":
        object["disease"] = "PFIC5"
      elif object["gene"] == "SLC51A":
        object["disease"] = "PFIC6"
      elif object["gene"] == "USP53":
        object["disease"] = "PFIC7"
      elif object["gene"] == "KIF12":
        object["disease"] = "PFIC8"
      elif object["gene"] == "ZFYVE19":
        object["disease"] = "PFIC9"
      elif object["gene"] == "MYO5B":
        object["disease"] = "PFIC10"
      elif object["gene"] == "SEMA7A":
        object["disease"] = "PFIC11"
      elif object["gene"] == "TMEM199":
        object["disease"] = "CDG2P"
      elif object["gene"] == "SKIC3":
        object["disease"] = "THES1"
      elif object["gene"] == "SKIC2":
        object["disease"] = "THES2"
      elif object["gene"] == "FOCAD":
        object["disease"] = "FOCADS"
      
      if 'disease' not in object.keys(): 
        print('No disease specified for patient {0:s}.'.format(str(object["id"])))

  else:
    print('No gene specified for patient {0:s}.'.format(str(object["id"])))

print('{0:4d} lists of symptoms with duplicate entries were corrected.'.format(count_sympdup))

# Serialize the python dictionnary to json
json_data = json.dumps(patient_dict, indent=4)

# Writing to sample.json
#with open("patientData_edited.json", "w") as outfile:
with open("epdj_output.json", "w") as outfile:
    outfile.write(json_data)


