
# ------------------------------
# Sequence for creating json files for pytheas-db


0. copy patientData_raw.txt to temp.txt 

1. run edit_patientData.json.py (reads temp.txt, outputs epdj_output.json)
   

2. copy epdj_output.json to patientData_edited.json
	
	check for blank symptom and absentsymptom entries

3.1 run add_variants.py (reads patientData_edited.json and variant1Data.txt, variant2Data.txt etc.)
  
3.2 copy adv_out.json to patientData_edited.txt 
	check everything is OK and then copy patientData_edited.txt to patientData_raw.txt for next round of additions


4. run build_symptom_trees.py (which outputs hp_trees.json, needed by build_disease_tables.py)


5. run build_disease_tables.py

	copy bdt_out.json to hp_disease_stats.json
	copy articles_out.json to article_DOIs.json


6. run build_symptom_tables.py

	(over)writes hp_disease_stats.json

 

