#!/usr/bin/env python3
import sys
import fileinput
import json

json_data = ""

for line in fileinput.input(files="patientData_edited.json"):
    json_data = json_data + line

patient_dict = json.loads(json_data)
count_symptoms = 0

for object in patient_dict: 
  
  if (object["gene"] == sys.argv[1] and 'symptoms' in object.keys()):
    
    for symptom_code in object["symptoms"]:
      count_symptoms += 1



print('{0:4d} symptoms in total for gene {1:4s}'.format(count_symptoms, sys.argv[1]))


