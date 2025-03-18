#!/usr/bin/env python3
import fileinput
import json
import numpy
import pandas
import re



json_data = ""
for line in fileinput.input(files="patientData_edited.json"):
#for line in fileinput.input(files="temp.txt"):
    json_data = json_data + line
patient_list = json.loads(json_data)


variants = []
ids = []
with open('variant1Data.txt') as fobj:
    for index, line in enumerate(fobj):
        variant = dict(label = "", n1 = "", p1 = "", n2 = "", p2 = "", n3 = "", p3 = "", n4 = "", p4 = "" )
        row = line.split()
        if len(row) == 3:
            variant["label"] = row[0]
            ids.append(row[0])
            variant["n1"] = row[1]
            variant["p1"] = row[2]
            print(index, len(row), variant["label"], variant["n1"], variant["p1"])
        else:
            print("Check input on line ", index, "of variant1Data.txt")

        variants.append(variant)

fobj.close()

with open('variant2Data.txt') as fobj:
    for index, line in enumerate(fobj):
        row = line.split()
        if len(row) == 3:
            variants[index]["n2"] = row[1]
            variants[index]["p2"] = row[2]
        else:
            print("Check input on line ", index, "of variant2Data.txt")

fobj.close()

with open('variant3Data.txt') as fobj:
    for index, line in enumerate(fobj):
        row = line.split()
        if len(row) == 3:
            variants[index]["n3"] = row[1]
            variants[index]["p3"] = row[2]

fobj.close()

with open('variant4Data.txt') as fobj:
    for index, line in enumerate(fobj):
        row = line.split()
        if len(row) == 3:
            variants[index]["n4"] = row[1]
            variants[index]["p4"] = row[2]

fobj.close()


#print(variants[5]["label"], variants[5]["n1"], variants[5]["p1"], variants[5]["n2"], variants[5]["p2"])
#print(variants[143]["label"], variants[5]["n1"], variants[5]["p1"], variants[5]["n2"], variants[5]["p2"])
#print(ids)


for object in patient_list:
    #Add externaly coded variant information
    if 'id' in object.keys():
        if object["id"] in ids:
            var_item = next(filter(lambda item: item["label"] == object["id"], variants), None)
            #print(object["id"])
            object["nucleotidevariant1"] = var_item["n1"]     
            object["protvariant1"] = var_item["p1"]     
            object["nucleotidevariant2"] = var_item["n2"]     
            object["protvariant2"] = var_item["p2"]     
            if var_item["n3"] != "":
                object["othernucleotidevariant"] = var_item["n3"]
                object["otherprotvariant"] = var_item["p3"]
                if 'othervariantgene' not in object.keys():
                    object["othervariantgene"] = "!!check!!"
            if var_item["n4"] != "":
                object["othernucleotidevariant2"] = var_item["n4"]
                object["otherprotvariant2"] = var_item["p4"]
                if 'othervariantgene' not in object.keys():
                    object["othervariantgene"] = "!!check!!"

        
    #Add variant classification    
    #Possible types are LoF, missense, synonymous, WT, other
    protvartypes = ["",""]    
    if 'protvariant1' in object.keys():
        #search1 is for a sequence of three letters followed by a number of any length, followed by three letters != del
        search1 = re.search(r'[A-Za-z][A-Za-z][A-Za-z][0-9]+(?!del)[A-Za-z][A-Za-z][A-Za-z]', object["protvariant1"])
        #search2 is for a sequence of p., capital letter, number of any length, any letter but not X 
        search2 = re.search(r'p\.[A-Z][0-9]+(?!X)[A-Z]', object["protvariant1"])

        if ('WT' in object["protvariant1"]):
            protvartypes[0] = "WT"

        elif ('*' in object["protvariant1"] or 
            'Ter' in object["protvariant1"] or 
            'Splice' in object["protvariant1"] or 
            'Xaa' in object["protvariant1"] or
            object["protvariant1"] == "No_protein"):
            protvartypes[0] = "LoF" 
        
        elif ('=' in object["protvariant1"]):
            #print(object["id"], object["protvariant1"]) 
            protvartypes[0] = "synonymous"

        elif(search1 != None or search2 != None):
            #print(object["id"], object["protvariant1"])
            protvartypes[0] = "missense"

        else:
            protvartypes[0] = "other"

    if 'protvariant2' in object.keys():
        #search1 is for a sequence of three letters followed by a number of any length, followed by three letters != del
        search1 = re.search(r'[A-Za-z][A-Za-z][A-Za-z][0-9]+(?!del)[A-Za-z][A-Za-z][A-Za-z]', object["protvariant2"])
        #search2 is for a sequence of capital letter, number of any length, any letter but not X 
        search2 = re.search(r'p\.[A-Z][0-9]+(?!X)[A-Z]', object["protvariant2"])

        if ('WT' in object["protvariant2"]):
            protvartypes[1] = "WT"

        elif ('*' in object["protvariant2"] or 
            'Ter' in object["protvariant2"] or 
            'Splice' in object["protvariant2"] or 
            'Xaa' in object["protvariant2"] or
            object["protvariant2"] == "No_protein"):
            protvartypes[1] = "LoF" 
        
        elif ('=' in object["protvariant2"]):
            #print(object["id"], object["protvariant2"]) 
            protvartypes[1] = "synonymous"

        elif(search1 != None or search2 != None):
            #print(object["id"], object["protvariant2"])
            protvartypes[1] = "missense"

        else:
            protvartypes[1] = "other"

    if 'otherprotvariant' in object.keys():
        #search1 is for a sequence of three letters followed by a number of any length, followed by three letters != del
        search1 = re.search(r'[A-Za-z][A-Za-z][A-Za-z][0-9]+(?!del)[A-Za-z][A-Za-z][A-Za-z]', object["otherprotvariant"])
        #search2 is for a sequence of capital letter, number of any length, any letter but not X 
        search2 = re.search(r'p\.[A-Z][0-9]+(?!X)[A-Z]', object["otherprotvariant"])

        if ('WT' in object["otherprotvariant"]):
            protvartypes.append("WT")

        elif ('*' in object["otherprotvariant"] or 
            'Ter' in object["otherprotvariant"] or 
            'Splice' in object["otherprotvariant"] or 
            'Xaa' in object["otherprotvariant"] or
            object["otherprotvariant"] == "No_protein"):
            protvartypes.append("LoF") 
        
        elif ('=' in object["otherprotvariant"]):
            #print(object["id"], object["otherprotvariant"]) 
            protvartypes.append("synonymous")

        elif(search1 != None or search2 != None):
            #print(object["id"], object["otherprotvariant"])
            protvartypes.append("missense")

        else:
            protvartypes.append("other")    
    
    if 'otherprotvariant2' in object.keys():
        #search1 is for a sequence of three letters followed by a number of any length, followed by three letters != del
        search1 = re.search(r'[A-Za-z][A-Za-z][A-Za-z][0-9]+(?!del)[A-Za-z][A-Za-z][A-Za-z]', object["otherprotvariant2"])
        #search2 is for a sequence of capital letter, number of any length, any letter but not X 
        search2 = re.search(r'p\.[A-Z][0-9]+(?!X)[A-Z]', object["otherprotvariant2"])

        if ('WT' in object["otherprotvariant2"]):
            protvartypes.append("WT")

        elif ('*' in object["otherprotvariant2"] or 
            'Ter' in object["otherprotvariant2"] or 
            'Xaa' in object["otherprotvariant2"]):
            protvartypes.append("LoF") 
        
        elif ('=' in object["otherprotvariant2"]):
            #print(object["id"], object["otherprotvariant2"]) 
            protvartypes.append("synonymous")

        elif(search1 != None or search2 != None):
            #print(object["id"], object["otherprotvariant2"])
            protvartypes.append("missense")

        else:
            protvartypes.append("other")    

    # Add phenotype classification (if absent, set to disease name)

    object["protvartypes"] = protvartypes



# Serialize the python dictionnary to json
json_data = json.dumps(patient_list, indent=4)

# Writing to bdt_out.json
# Check output before copying to hp_disease_stats.json
with open("adv_out.json", "w") as outfile:
    outfile.write(json_data)

outfile.close()
   



