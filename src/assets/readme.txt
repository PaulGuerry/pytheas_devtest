
# ------------------------------
# Sequence for creating json files for pytheas-db


1. edit_patientData.json.py
   edit file names inside the script

2. copy output of edit_patientData.json.py to patientData_edited.json
	
	check for blank symptom and absentsymptom entries


3. run build_disease_tables.py

	fill in survival values (see 230620)
	copy bdt_out.json to hp_disease_stats.json
	copy articles_out.json to articles_DOI.json


4. run build_symptom_tables.py

	(over)writes hp_disease_stats.json

 

