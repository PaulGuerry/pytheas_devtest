#!/usr/bin/env python3

import fileinput
import json
import re 
import numpy

json_data = ""
# 
substring = '('

print("Remember that this script reads temp.txt and outputs epdj_output.txt")
for line in fileinput.input(files="temp.txt"):
    json_data = json_data + line

patient_dict = json.loads(json_data)
count_sympdate = 0
count_sympdup = 0
for object in patient_dict:
  
  
  #
  # Check/curate symptoms
  #
  subs = 0
  res = []
  if 'symptoms' in object.keys():
    for symptom_code in object["symptoms"]:
      if substring in symptom_code:
        subs = 1
        candidate_code = re.sub(r'\([^()]*\)', '', symptom_code)
        if len(candidate_code) == 7:
          res.append(candidate_code)
        else:
          print('Error 29: Unrecognised HPO code, ' + candidate_code + ', for patient ', object['id'] + '.')
      else:
        if len(symptom_code) == 7:
          res.append(symptom_code)
        else: 
          print('Error 34: Unrecognised HPO code, ' + symptom_code + ', for patient ', object['id'] + '.')

  #
  #250815: specific editing for AlHussaini2021_
  #        if Hepat++, Splen++, Prurit, HCC, FTT, Rickets, Portal+, CLF, HCC, Cholith, Fract+ not in ['symptoms']
  #           add them to ['absentsymptoms']
    if object['id'][:15] == "AlHussaini2021_":
      print('Found patient ', object['id'])
      
      # Hepat++
      tempstr = "0002240" 
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      # Splen++
      tempstr = "0001744"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      # etc.
      tempstr = "0000989"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0001508"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0002748"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0001409"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0100626"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0001402"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0001081"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
      tempstr = "0002756"
      if tempstr not in object['symptoms']:
        if tempstr not in object['absentsymptoms']:
          object['absentsymptoms'].append(tempstr)
  # also save symptom_codes saved under "biology" key  
  if 'labfindings' in object.keys():
    for symptom_code in object["labfindings"]:
      if substring in symptom_code:
        subs = 1
        candidate_code = re.sub(r'\([^()]*\)', '', symptom_code)
        if len(candidate_code) == 7:
          res.append(candidate_code)
        else:
          print('Error 51: Unrecognised HPO code, ' + candidate_code + ', for patient ', object['id'] + '.')
      else:
        if len(symptom_code) == 7:
          res.append(symptom_code)
        else: 
          print('Error 56: Unrecognised HPO code, ' + symptom_code + ', for patient ', object['id'] + '.')
      res.append(symptom_code)  
  
  if (len(res) > 0): 
    #remove duplicates
    symptom_set = set(res)
    symptom_list = res
    if (len(symptom_set) < len(symptom_list)):
        count_sympdup+=1
    object["symptoms"] = list(symptom_set)



  # Check/curate absent symptoms
  #
  subs = 0
  res = []
  if 'absentsymptoms' in object.keys():
    for symptom_code in object["absentsymptoms"]:
      if substring in symptom_code:
        subs = 1
        candidate_code = re.sub(r'\([^()]*\)', '', symptom_code)
        if len(candidate_code) == 7:
          res.append(candidate_code)
        elif len(candidate_code) > 1:
          print('Error 81: Unrecognised HPO code, ' + candidate_code + ', for patient ', object['id'] + '.')
      else:
        if len(symptom_code) == 7:
          res.append(symptom_code)
        elif len(symptom_code) > 1: 
          print('Error 86: Unrecognised HPO code, ' + symptom_code + ', for patient ', object['id'] + '.')

    
  if (len(res) > 0): 
    #remove duplicates
    symptom_set = set(res)
    symptom_list = res
    if (len(symptom_set) < len(symptom_list)):
        count_sympdup+=1
    object["absentsymptoms"] = list(symptom_set)


  # 250320: define transient symptoms as those reported both present and absent
  if "symptoms" in object.keys() and "absentsymptoms" in object.keys():
    res = set(object["symptoms"]).intersection(object["absentsymptoms"])
    if (len(res) > 0):
      object["transientsymptoms"] = list(res)

  # 250322: classify MYO5B deficiency as PFIC10, MVID or MIXED based on symptoms
  try: 

    if object["gene"] == "MYO5B":

      if ("0011473" in object["symptoms"] and 
          ("0001396" in object["symptoms"] or "0002611" in object["symptoms"])):

        object["phenotype"] = "PFIC10+MVID"
    
      elif ("0011473" in object["symptoms"] and 
          ("0001396" not in object["symptoms"] and "0002611" not in object["symptoms"])): 

        object["phenotype"] = "MVID"

      elif ("0011473" not in object["symptoms"] and 
            ("0001396" in object["symptoms"] or "0002611" in object["symptoms"])):

        object["phenotype"] = "PFIC10"

      else:

        object["phenotype"] = "UNCLEAR"

  except:

    print('No gene for patient {0:s}'.format(str(object["id"])))
  

  if 'ageatmoleculardiagnostic' in object.keys():
     try:
      float(object["ageatmoleculardiagnostic"])
      if (float(object["ageatmoleculardiagnostic"]) > 999.):
        print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["ageatmoleculardiagnostic"]), object["id"])) 
     except:
      print('Non-numeric ageatmoleculardiagnostic, {0:s}, for patient {1:s}'.format(str(object["ageatmoleculardiagnostic"]), object["id"]))

  if 'firstsymptomagemonth' in object.keys():
     try:
      float(object["firstsymptomagemonth"])
      object["firstsymptomagemonth"] = float(object["firstsymptomagemonth"])
      if (float(object["firstsymptomagemonth"]) > 999.):
        print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["firstsymptomagemonth"]), object["id"])) 
     except:
      if object["firstsymptomagemonth"] is not None:
        print('Non-numeric firstsymptomagemonth, {0:s}, for patient {1:s}'.format(str(object["firstsymptomagemonth"]), object["id"]))
        print('Setting firstsymptomagemonth to null/none.')
        object["firstsymptomagemonth"] = None
  else:
    if 'ageatmoleculardiagnostic' in object.keys():
      object['firstsymptomagemonth'] = float(object['ageatmoleculardiagnostic']) * 12.
      print('Setting firstsymptomagemonth to {0:s} (from ageatmoleculardiagnostic) for patient {1:s}'.format(str(object["firstsymptomagemonth"]), object["id"]))

  if 'alivedeadage' in object.keys():
     try:
      float(object["alivedeadage"])
      object["alivedeadage"] = float(object["alivedeadage"])
      if (float(object["alivedeadage"]) > 80.):
        print('Age {0:s} years  for patient {1:s} does not seem reasonable'.format(str(object["alivedeadage"]), object["id"])) 
     except:
      if object["alivedeadage"] is not None:
        print('Non-numeric alivedeadage, {0:s}, for patient {1:s}'.format(str(object["alivedeadage"]), object["id"]))
        print('Setting alivedeadage to null/none.')
        object["alivedeadage"] = None

  if 'lastnewsageyear' in object.keys():
    try:
      float(object["lastnewsageyear"])
      object["lastnewsageyear"] = float(object["lastnewsageyear"])
      if 'alivedeadage' not in object.keys():
        object['alivedeadage'] = float(object['lastnewsageyear'])
      if 'alivedead' not in object.keys():
        object['alivedead'] = 'alive'
      if (float(object["lastnewsageyear"]) > 80.):
        print('Age {0:s} years  for patient {1:s} does not seem reasonable'.format(str(object["lastnewsageyear"]), object["id"])) 
    except:
      if object["lastnewsageyear"] is not None:
        print('Non-numeric lastnewsageyear, {0:s}, for patient {1:s}'.format(str(object["lastnewsageyear"]), object["id"]))
        print('Setting lastnewsageyear to null/none.')
        object["lastnewsageyear"] = None 

    

  elif 'ageatmoleculardiagnostic' in object.keys():
      try:
        float(object["ageatmoleculardiagnostic"])
        if (float(object["ageatmoleculardiagnostic"]) > 200.):
          print('Age {0:s} months for patient {1:s} does not seem reasonable'.format(str(object["ageatmoleculardiagnostic"]), object["id"])) 
      except:
        print('Non-numeric ageatmoleculardiagnostic, {0:s}, for patient {1:s}'.format(str(object["ageatmoleculardiagnostic"]), object["id"]))
      else:
        object["lastnewsageyear"] = round(float(object["ageatmoleculardiagnostic"]), 2)
  
  elif 'firstsymptomagemonth' in object.keys():
      try:
        float(object["firstsymptomagemonth"])
        if (float(object["firstsymptomagemonth"]) > 100.):
          print('Check age {0:s} months for patient {1:s}.'.format(str(object["firstsymptomagemonth"]), object["id"])) 
      except:
        print('Non-numeric firstsymptomagemonth, {0:s}, for patient {1:s}'.format(str(object["firstsymptomagemonth"]), object["id"]))
      else:
        object["lastnewsageyear"] = round(float(object["firstsymptomagemonth"]) / 12., 2)

  if 'alivedead' in object.keys():
      if (object["alivedead"] != "alive" and object["alivedead"] != "dead"):
        print('unrecognised alive/dead status, {0:s}, for patient {1:s}.'.format(str(object["alivedead"]), object["id"])) 
  else:
    print('No alive/dead information for patient {0:s}.'.format(object["id"]))


  if 'alivedeadage' not in object.keys():
    if 'lastnewsageyear' in object.keys():
      object['alivedeadage'] = object['lastnewsageyear']
    else:
      print('No alivedeadage for patient {0:s}.'.format(object['id'])) 


  # 240913
  if 'gene' in object.keys():
      #if object["gene"] == "ATP8B1":
      #  object["disease"] = "PFIC1"
      #  #print('Gene, {0:s}; Disease, {1:s}; ID, {2:s}.'.format(str(object["gene"]), object["disease"], object["id"]))
      #elif object["gene"] == "ABCB11":
      #  object["disease"] = "PFIC2"
      #elif object["gene"] == "ABCB4":
      #  object["disease"] = "PFIC3"
      #elif object["gene"] == "TJP2":
      #  object["disease"] = "PFIC4"
      #elif object["gene"] == "NR1H4":
      #  object["disease"] = "PFIC5"
      #elif object["gene"] == "SLC51A":
      #  object["disease"] = "PFIC6"
      #elif object["gene"] == "USP53":
      #  object["disease"] = "PFIC7"
      #elif object["gene"] == "KIF12":
      #  object["disease"] = "PFIC8"
      #elif object["gene"] == "ZFYVE19":
      #  object["disease"] = "PFIC9"
      if object["gene"] == "MYO5B":
        object['disease'] = 'MYO5B deficiency'
      #elif object["gene"] == "SEMA7A":
      #  object["disease"] = "PFIC11"
      #elif object["gene"] == "TMEM199":
      #  object["disease"] = "CDG2P"
      #elif object["gene"] == "SKIC3":
      #  object["disease"] = "THES1"
      #elif object["gene"] == "SKIC2":
      #  object["disease"] = "THES2"
      #elif object["gene"] == "FOCAD":
      #  object["disease"] = "FOCADS"
      
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


