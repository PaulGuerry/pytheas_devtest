#!/usr/bin/env python3
import fileinput
import json
import numpy
import pandas
from lifelines import KaplanMeierFitter


# This function searches for a DOI in a dictionnary
def search_in_dict(search_string, search_dict):
    return [el for el in search_dict if el['articledoi'] == search_string]

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


diseases = [
   dict(
      name = "PFIC1", 
      gene = "ATP8B1", 
      matches = ["PFIC1"], 
      colour = colours[0],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "ATP8B1",
            link = "https://www.alliancegenome.org/gene/HGNC:3706",
            uniprot = dict(
               code = "O43520",
               link = "https://www.uniprot.org/uniprotkb/O43520/entry"
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Atp8b1",
            link = "https://www.alliancegenome.org/gene/MGI:1859665",
            uniprot = dict(
               code = "Q148W0",
               link = "https://www.uniprot.org/uniprotkb/Q148W0/entry"
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "atp8b1",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-091116-14",
            uniprot = dict(
               code = "F1R881",
               link = "https://www.uniprot.org/uniprotkb/F1R881/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "ATP8B",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0037989",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "tat-2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00019166",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "DNF1",
            link = "https://www.alliancegenome.org/gene/SGD:S000000968",
            uniprot = dict(
               code = "P32660",
               link = "https://www.uniprot.org/uniprotkb/P32660/entry"
            )
         )
      ]
   ), 
   dict(
      name = "PFIC2", 
      gene = "ABCB11", 
      matches = ["PFIC2"], 
      colour = colours[1],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "ABCB11",
            link = "https://www.alliancegenome.org/gene/HGNC:42",
            uniprot = dict(
               code = "O95342",
               link = "https://www.uniprot.org/uniprotkb/O95342/entry"
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Abcb11",
            link = "https://www.mousephenotype.org/data/genes/MGI:1351619",
            uniprot = dict(
               code = "Q9JL39",
               link = "https://www.uniprot.org/uniprotkb/Q9JL39/entry"
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "abcb11a",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-050517-13",
            uniprot = dict(
               code = "F1QSX6",
               link = "https://www.uniprot.org/uniprotkb/F1QSX6/entry"
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "abcb11b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-050517-14",
            uniprot = dict(
               code = "A0A8M1RNN7",
               link = "https://www.uniprot.org/uniprotkb/A0A8M1RNN7/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Mdr50",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0010241",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "Multiple orthologs",
            link = "https://www.alliancegenome.org/gene/HGNC:42",
            uniprot = dict(
               code = "",
               link = ""
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "STE6",
            link = "https://www.alliancegenome.org/gene/SGD:S000001692",
            uniprot = dict(
               code = "P12866",
               link = "https://www.uniprot.org/uniprotkb/P12866/entry"
            )
         )
      ]   
   ),
   dict(
      name = "PFIC3", 
      gene = "ABCB4", 
      matches = ["PFIC3"], 
      colour = colours[2],
      link = "https://www.alliancegenome.org/gene/HGNC:45",
      uniprot = dict(
         code = "P21439",
         link = "https://www.uniprot.org/uniprotkb/P21439/entry"
         ),
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "ABCB4",
            link = "https://www.alliancegenome.org/gene/HGNC:45",
            uniprot = dict(
               code = "P21439",
               link = "https://www.uniprot.org/uniprotkb/P21439/entry"
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Abcb4",
            link = "https://www.mousephenotype.org/data/genes/MGI:97569",
            uniprot = dict(
               code = "P21440",
               link = "https://www.uniprot.org/uniprotkb/P21440/entry"
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "abcb4",
            link = "https://zfin.org/ZDB-GENE-080204-52",
            uniprot = dict(
               code = "E7F1E3",
               link = "https://www.uniprot.org/uniprotkb/E7F1E3/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Multiple orthologs",
            link = "https://www.alliancegenome.org/gene/HGNC:45",
            uniprot = dict(
               code = "",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "Multiple orthologs",
            link = "https://www.alliancegenome.org/gene/HGNC:45",
            uniprot = dict(
               code = "",
               link = ""
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "STE6",
            link = "https://www.alliancegenome.org/gene/SGD:S000001692",
            uniprot = dict(
               code = "P12866",
               link = "https://www.uniprot.org/uniprotkb/P12866/entry"
            )
         ),
         dict(
            species = "Dictyostelium discoideum",
            gene = "abcB4",
            link = "http://dictybase.org/gene/DDB_G0279915",
            uniprot = dict(
               code = "Q54W24",
               link = "https://www.uniprot.org/uniprotkb/Q54W24/entry"
            )
         )

      ]
   ),
   dict(
      name = "PFIC4", 
      gene = "TJP2", 
      matches = ["PFIC4"], 
      colour = colours[3],
      link = "https://www.alliancegenome.org/gene/HGNC:11828",
      uniprot = dict(
         code = "Q9UDY2",
         link = "https://www.uniprot.org/uniprotkb/Q9UDY2/entry",
         ),
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "TJP2",
            link = "https://www.alliancegenome.org/gene/HGNC:11828",
            uniprot = dict(
               code = "Q9UDY2",
               link = "https://www.uniprot.org/uniprotkb/Q9UDY2/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Tjp2",
            link = "https://www.alliancegenome.org/gene/MGI:1341872",
            uniprot = dict(
               code = "Q9Z0U1",
               link = "https://www.uniprot.org/uniprotkb/Q9Z0U1/entry"
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "tjp2a",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-070925-2",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "tjp2b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-040718-58",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "pyd",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0262614",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "zoo-1",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00013683",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "PFIC5", 
      gene = "NR1H4", 
      matches = ["PFIC5"], 
      colour = colours[4],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "NR1H4",
            link = "https://www.alliancegenome.org/gene/HGNC:7967",
            uniprot = dict(
               code = "Q96RI1",
               link = "https://www.uniprot.org/uniprotkb/Q96RI1/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Nr1h4",
            link = "https://www.alliancegenome.org/gene/MGI:1352464",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "nr1h4",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-040718-313",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "nhr-166",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00016772",
            uniprot = dict(
               code = "O16609",
               link = "https://www.uniprot.org/uniprotkb/O16609/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "nhr-253",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00022639",
            uniprot = dict(
               code = "O61869",
               link = "https://www.uniprot.org/uniprotkb/O61869/entry"
            )
         )
      ]
   ),
   dict(
      name = "PFIC6",
      gene = "SLC51A",
      matches = ["PFIC6"],
      colour = colours[5],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "SLC51A",
            link = "https://www.alliancegenome.org/gene/HGNC:29955",
            uniprot = dict(
               code = "Q86UW1",
               link = "https://www.uniprot.org/uniprotkb/Q86UW1/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Slc51a",
            link = "https://www.alliancegenome.org/gene/MGI:2146634",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "slc51a",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-040912-10",
            uniprot = dict(
               code = "Q66I08",
               link = "https://www.uniprot.org/uniprotkb/Q66I08/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "CG6836",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0036834",
            uniprot = dict(
               code = "Q9VVV2",
               link = "https://www.uniprot.org/uniprotkb/Q9VVV2/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "osta-1",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00015287",
            uniprot = dict(
               code = "O17204",
               link = "https://www.uniprot.org/uniprotkb/O17204/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "osta-2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00015942",
            uniprot = dict(
               code = "Q18071",
               link = "https://www.uniprot.org/uniprotkb/Q18071/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "osta-3",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00012182",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "PFIC7",
      gene = "USP53",
      matches = ["PFIC7"],
      colour = colours[6],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "USP53",
            link = "https://www.alliancegenome.org/gene/HGNC:29255",
            uniprot = dict(
               code = "Q70EK8",
               link = "https://www.uniprot.org/uniprotkb/Q70EK8/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Usp53",
            link = "https://www.alliancegenome.org/gene/MGI:2139607",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "usp53b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-090312-168",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "ec",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0000542",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "PFIC8", 
      gene = "KIF12", 
      matches = ["PFIC8"], 
      colour = colours[7],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "KIF12",
            link = "https://www.alliancegenome.org/gene/HGNC:21495",
            uniprot = dict(
               code = "Q96FN5",
               link = "https://www.uniprot.org/uniprotkb/Q96FN5/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Kif12",
            link = "https://www.alliancegenome.org/gene/MGI:1098232",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Klp54D",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0263076",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Dictyostelium discoideum",
            gene = "kif12",
            link = "http://dictybase.org/gene/DDB_G0268258",
            uniprot = dict(
               code = "Q6S000",
               link = "https://www.uniprot.org/uniprotkb/Q6S000/entry"
            )
         )

      ]
   ),
   dict(
      name = "PFIC9", 
      gene = "ZFYVE19", 
      matches = ["PFIC9"], 
      colour = colours[8],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "ZFYVE9",
            link = "https://www.alliancegenome.org/gene/HGNC:6775",
            uniprot = dict(
               code = "O95405",
               link = "https://www.uniprot.org/uniprotkb/O95405/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Zfyve9",
            link = "https://www.alliancegenome.org/gene/MGI:2652838",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "zfyve9a",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-070705-182",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "zfyve9b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-110825-2",
            uniprot = dict(
               code = "A0A8M3BDK8",
               link = "https://www.uniprot.org/uniprotkb/A0A8M3BDK8/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Sara",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0026369",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "aka-1",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00000101",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "PFIC10", 
      gene = "MYO5B", 
      matches = ["PFIC10"], 
      colour = colours[9],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "MYO5B",
            link = "https://www.alliancegenome.org/gene/HGNC:7603",
            uniprot = dict(
               code = "Q9ULV0",
               link = "https://www.uniprot.org/uniprotkb/Q9ULV0/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Myo5b",
            link = "https://www.alliancegenome.org/gene/MGI:106598",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "myo5b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-031219-7",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "didum",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0261397",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "hum-2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00002036",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "MYO4",
            link = "https://www.alliancegenome.org/gene/SGD:S000000027",
            uniprot = dict(
               code = "P32492",
               link = "https://www.uniprot.org/uniprotkb/P32492/entry"
            )
         ),
         dict(
            species = "Dictyostelium discoideum",
            gene = "myoJ",
            link = "http://dictybase.org/gene/DDB_G0272112",
            uniprot = dict(
               code = "P54697",
               link = "https://www.uniprot.org/uniprotkb/P54697/entry"
            )
         )
      ]
   ),
   dict(
      name = "PFIC11", 
      gene = "SEMA7A", 
      matches = ["PFIC11"], 
      colour = colours[10],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "SEMA7A",
            link = "https://www.alliancegenome.org/gene/HGNC:10741",
            uniprot = dict(
               code = "O75326",
               link = "https://www.uniprot.org/uniprotkb/O75326/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Sema7a",
            link = "https://www.alliancegenome.org/gene/MGI:1306826",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "sema7a",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-030131-3633",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "CDG2P", 
      gene = "TMEM199", 
      matches = ["CDG2P"], 
      colour = colours[11],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "TMEM199",
            link = "https://www.alliancegenome.org/gene/HGNC:18085",
            uniprot = dict(
               code = "Q8N511",
               link = "https://www.uniprot.org/uniprotkb/Q8N511/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Tmem199",
            link = "https://www.alliancegenome.org/gene/MGI:2144113",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "tmem199",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-050522-150",
            uniprot = dict(
               code = "A8E5C6",
               link = "https://www.uniprot.org/uniprotkb/A8E5C6/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "CG7071",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0260467",
            uniprot = dict(
               code = "Q8SXS0",
               link = "https://www.uniprot.org/uniprotkb/Q8SXS0/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "F09E5.11",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00017289",
            uniprot = dict(
               code = "Q19259",
               link = "https://www.uniprot.org/uniprotkb/Q19259/entry"
            )
         )
      ]
   ),
   dict(
      name = "THES1", 
      gene = "SKIC3", 
      matches = ["THES1"], 
      colour = colours[12],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "SKIC3",
            link = "https://www.alliancegenome.org/gene/HGNC:23639",
            uniprot = dict(
               code = "Q6PGP7",
               link = "https://www.uniprot.org/uniprotkb/Q6PGP7/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Skic3",
            link = "https://www.alliancegenome.org/gene/MGI:2679923",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "skic3",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-110125-2",
            uniprot = dict(
               code = "E7F2R1",
               link = "https://www.uniprot.org/uniprotkb/E7F2R1/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "CG8777",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0033376",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "ttc-37",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00021613",
            uniprot = dict(
               code = "Q9BKR2",
               link = "https://www.uniprot.org/uniprotkb/Q9BKR2/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "SKI3",
            link = "https://www.alliancegenome.org/gene/SGD:S000006393",
            uniprot = dict(
               code = "P17883",
               link = "https://www.uniprot.org/uniprotkb/P17883/entry"
            )
         )
      ]
   ),
   dict(
      name = "THES2", 
      gene = "SKIC2", 
      matches = ["THES2"], 
      colour = colours[13],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "SKIC2",
            link = "https://www.alliancegenome.org/gene/HGNC:10898",
            uniprot = dict(
               code = "Q15477",
               link = "https://www.uniprot.org/uniprotkb/Q15477/entry",
               )
         ),
         dict(
            species = "Danio rerio",
            gene = "skic2",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-010430-5",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "tst",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039117",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "skih-2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00008502",
            uniprot = dict(
               code = "Q19103",
               link = "https://www.uniprot.org/uniprotkb/Q19103/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "SKI2",
            link = "https://www.alliancegenome.org/gene/SGD:S000004390",
            uniprot = dict(
               code = "P35207",
               link = "https://www.uniprot.org/uniprotkb/P35207/entry"
            )
         )
      ]
   ),
   dict(
      name = "THES", 
      gene = "SKIC3,SKIC2", 
      matches = ["THES", "THES1", "THES2"], 
      colour = colours[14],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "SKIC3",
            link = "https://www.alliancegenome.org/gene/HGNC:23639",
            uniprot = dict(
               code = "Q6PGP7",
               link = "https://www.uniprot.org/uniprotkb/Q6PGP7/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Skic3",
            link = "https://www.alliancegenome.org/gene/MGI:2679923",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "skic3",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-110125-2",
            uniprot = dict(
               code = "E7F2R1",
               link = "https://www.uniprot.org/uniprotkb/E7F2R1/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "CG8777",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0033376",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "ttc-37",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00021613",
            uniprot = dict(
               code = "Q9BKR2",
               link = "https://www.uniprot.org/uniprotkb/Q9BKR2/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "SKI3",
            link = "https://www.alliancegenome.org/gene/SGD:S000006393",
            uniprot = dict(
               code = "P17883",
               link = "https://www.uniprot.org/uniprotkb/P17883/entry"
            )
         ),
         dict(
            species = "Homo sapiens",
            gene = "SKIC2",
            link = "https://www.alliancegenome.org/gene/HGNC:10898",
            uniprot = dict(
               code = "Q15477",
               link = "https://www.uniprot.org/uniprotkb/Q15477/entry",
               )
         ),
         dict(
            species = "Danio rerio",
            gene = "skic2",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-010430-5",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "tst",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039117",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "skih-2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00008502",
            uniprot = dict(
               code = "Q19103",
               link = "https://www.uniprot.org/uniprotkb/Q19103/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "SKI2",
            link = "https://www.alliancegenome.org/gene/SGD:S000004390",
            uniprot = dict(
               code = "P35207",
               link = "https://www.uniprot.org/uniprotkb/P35207/entry"
            )
         )
      ]
   ),
   dict(
      name = "FOCADS", 
      gene = "FOCAD", 
      matches = ["FOCADS"], 
      colour = colours[15],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "FOCAD",
            link = "https://www.alliancegenome.org/gene/HGNC:23377",
            uniprot = dict(
               code = "Q5VW36",
               link = "https://www.uniprot.org/uniprotkb/Q5VW36/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Focad",
            link = "https://www.alliancegenome.org/gene/MGI:2676921",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "focad",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-080213-1",
            uniprot = dict(
               code = "",
               link = ""
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "CG3520",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0034859",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "ARCS1", 
      gene = "VPS33B", 
      matches = ["ARCS1"], 
      colour = colours[16],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "VPS33B",
            link = "https://www.alliancegenome.org/gene/HGNC:12712",
            uniprot = dict(
               code = "Q9H267",
               link = "https://www.uniprot.org/uniprotkb/Q9H267/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Vps33b",
            link = "https://www.alliancegenome.org/gene/MGI:2446237",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "vps33b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-050327-73",
            uniprot = dict(
               code = "Q58EN8",
               link = "https://www.uniprot.org/uniprotkb/Q58EN8/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Vps33B",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039335",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "vps-33.2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00016960",
            uniprot = dict(
               code = "Q18891",
               link = "https://www.uniprot.org/uniprotkb/Q18891/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "VPS33",
            link = "https://www.alliancegenome.org/gene/SGD:S000004388",
            uniprot = dict(
               code = "P20795",
               link = "https://www.uniprot.org/uniprotkb/P20795/entry"
            )
         )
      ]
   ),
   dict(
      name = "ARCS2", 
      gene = "VIPAS39", 
      matches = ["ARCS2"], 
      colour = colours[17],
      animals = [
         dict(
            species = "Homo sapiens",
            gene = "VIPAS39",
            link = "https://www.alliancegenome.org/gene/HGNC:20347",
            uniprot = dict(
               code = "Q9H9C1",
               link = "https://www.uniprot.org/uniprotkb/Q9H9C1/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Vipas39",
            link = "https://www.alliancegenome.org/gene/MGI:2144805",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "vipas39",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-040520-1",
            uniprot = dict(
               code = "Q5TYV4",
               link = "https://www.uniprot.org/uniprotkb/Q5TYV4/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Vps16B",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039702",
            uniprot = dict(
               code = "Q9VAG4",
               link = "https://www.uniprot.org/uniprotkb/Q9VAG4/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "spe-39",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00004975",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ]
   ),
   dict(
      name = "ARCS", 
      gene = "VPS33B,VIPAS39", 
      matches = ["ARCS", "ARCS1", "ARCS2"], 
      colour = colours[18],
      link = "",
      uniprot = dict(
         code = "",
         link = "",
         ),
     animals = [
         dict(
            species = "Homo sapiens",
            gene = "VPS33B",
            link = "https://www.alliancegenome.org/gene/HGNC:12712",
            uniprot = dict(
               code = "Q9H267",
               link = "https://www.uniprot.org/uniprotkb/Q9H267/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Vps33b",
            link = "https://www.alliancegenome.org/gene/MGI:2446237",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "vps33b",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-050327-73",
            uniprot = dict(
               code = "Q58EN8",
               link = "https://www.uniprot.org/uniprotkb/Q58EN8/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Vps33B",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039335",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "vps-33.2",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00016960",
            uniprot = dict(
               code = "Q18891",
               link = "https://www.uniprot.org/uniprotkb/Q18891/entry"
            )
         ),
         dict(
            species = "Saccharomyces cerevisiae",
            gene = "VPS33",
            link = "https://www.alliancegenome.org/gene/SGD:S000004388",
            uniprot = dict(
               code = "P20795",
               link = "https://www.uniprot.org/uniprotkb/P20795/entry"
            )
         ),
         dict(
            species = "Homo sapiens",
            gene = "VIPAS39",
            link = "https://www.alliancegenome.org/gene/HGNC:20347",
            uniprot = dict(
               code = "Q9H9C1",
               link = "https://www.uniprot.org/uniprotkb/Q9H9C1/entry",
               )
         ),
         dict(
            species = "Mus musculus",
            gene = "Vipas39",
            link = "https://www.alliancegenome.org/gene/MGI:2144805",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         ),
         dict(
            species = "Danio rerio",
            gene = "vipas39",
            link = "https://www.alliancegenome.org/gene/ZFIN:ZDB-GENE-040520-1",
            uniprot = dict(
               code = "Q5TYV4",
               link = "https://www.uniprot.org/uniprotkb/Q5TYV4/entry"
            )
         ),
         dict(
            species = "Drosophila melanogaster",
            gene = "Vps16B",
            link = "https://www.alliancegenome.org/gene/FB:FBgn0039702",
            uniprot = dict(
               code = "Q9VAG4",
               link = "https://www.uniprot.org/uniprotkb/Q9VAG4/entry"
            )
         ),
         dict(
            species = "Caenorhabditis elegans",
            gene = "spe-39",
            link = "https://www.alliancegenome.org/gene/WB:WBGene00004975",
            uniprot = dict(
               code = "Multiple",
               link = ""
            )
         )
      ] 
   )
]


disease_table = []
articles = []

for disease in diseases:
   print("Building disease table for disease {0:s}".format(disease['name']))
   ages_first = dict(all = dict(array = [], median = 0, iqr = 0, surv_x = [], surv_y = []),
               boys = dict(array = [], median = 0, iqr = 0, surv_x = [], surv_y = []),
               girls = dict(array = [], median = 0, iqr = 0, surv_x = [], surv_y = []))

   ages_last = dict(all = dict(array = [], status = [], median = 0, iqr = 0),
               boys = dict(array = [], status = [], median = 0, iqr = 0),
               girls = dict(array = [], status = [], median = 0, iqr = 0))
   
   # need to account for the fact that in some cases, the age of death is different from the age at last follow-up
   ages_surv = dict(all = dict(array = [], status = [], surv_x = [], surv_y = [], median = 0, iqr = 0),
               boys = dict(array = [], status = [], surv_x = [], surv_y = [], median = 0, iqr = 0),
               girls = dict(array = [], status = [], surv_x = [], surv_y = [], median = 0, iqr = 0))

   count_patients = dict(total = 0, girls = 0, boys = 0)
   count_inbred = dict(yes = 0, no = 0, missing = 0)
   article_count = 0
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
                  
                  if ('sex' in object.keys() and object["sex"] == "F"):
                     ages_last["girls"]["status"].append("0")      
                     ages_surv["girls"]["status"].append("0")      
                  elif ('sex' in object.keys() and object["sex"] == "M"):
                     ages_last["boys"]["status"].append("0")      
                     ages_surv["boys"]["status"].append("0")      

               
               
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
               # Check definition of search_in_dict function at top of script
               if (len(search_in_dict(object["doi"],  articles)) == 0):
                  article_count += 1
                  articles.append(dict(articlenumber = article_count, articledoi = object["doi"], disease = object["disease"]))

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
   
   # 250305: perform survival analysis directly in Python
   # all
   df = pandas.DataFrame({'T': [float(i) for i in ages_surv["all"]["array"]], 
                          'S': [float(i) for i in ages_surv["all"]["status"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_surv["all"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_surv["all"]["surv_y"] = [round(x, 4) for x in kmf.survival_function_['KM_estimate']]

   # girls
   #print("length array ", len(ages_surv["girls"]["array"]))
   #print("length status ", len(ages_surv["girls"]["status"]))
   df = pandas.DataFrame({'T': [float(i) for i in ages_surv["girls"]["array"]], 
                          'S': [float(i) for i in ages_surv["girls"]["status"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_surv["girls"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_surv["girls"]["surv_y"] = [round(x, 4) for x in kmf.survival_function_['KM_estimate']]

   # boys
   df = pandas.DataFrame({'T': [float(i) for i in ages_surv["boys"]["array"]], 
                          'S': [float(i) for i in ages_surv["boys"]["status"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_surv["boys"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_surv["boys"]["surv_y"] = [round(x, 4) for x in kmf.survival_function_['KM_estimate']]


   # 250307: perform survival analysis for age at first symptoms
   # all
   df = pandas.DataFrame({'T': [float(i) for i in ages_first["all"]["array"]], 
                          'S': [float(1) for i in ages_first["all"]["array"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_first["all"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_first["all"]["surv_y"] = [round(x, 4) for x in kmf.cumulative_density_['KM_estimate']]

  # boys
   df = pandas.DataFrame({'T': [float(i) for i in ages_first["boys"]["array"]], 
                          'S': [float(1) for i in ages_first["boys"]["array"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_first["boys"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_first["boys"]["surv_y"] = [round(x, 4) for x in kmf.cumulative_density_['KM_estimate']]

  # girls
   df = pandas.DataFrame({'T': [float(i) for i in ages_first["girls"]["array"]], 
                          'S': [float(1) for i in ages_first["girls"]["array"]]
                          })
   time = df['T']
   status = df['S']
   kmf = KaplanMeierFitter()
   
   if (len(time) > 1):
      kmf.fit(time, status)
      ages_first["girls"]["surv_x"] = [round(x, 3) for x in kmf.timeline]
      ages_first["girls"]["surv_y"] = [round(x, 4) for x in kmf.cumulative_density_['KM_estimate']]

 

 
   #for dict_key, dict_val in ages_first.items():
   #   for k, v in dict_val.items():
   #      try:
   #         #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
   #            if type(v) is list:
   #               v = [round(x, 2) for x in v] 
   #            else: 
   #               v = round(v)

   #      except:
   #         print("119 - Unable to round {2:s}, for disease {0:s}, ages_first {1:s}".format(disease['name'], dict_val, v))

  
   ##round values to two digits and output information in R-readable format
   #for dict_key, dict_val in ages_last.items():
   #   
   #   for k, v in dict_val.items():
   #      if k != "status":
   #         try:
   #            #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
   #            if type(v) is list:
   #               v = [round(x, 2) for x in v] 
   #            else: 
   #               v = round(v)

   #         except:
   #            print("290 - Unable to round {2:s}, for disease {0:s}, ages_last {1:s}".format(disease['name'], dict_val, v))
   #      
   
   ##round values to two digits and output information in R-readable format
   #for dict_key, dict_val in ages_surv.items():
   #   time_string = "time <- c("
   #   status_string = "status <-c("
   #   
   #   for k, v in dict_val.items():
   #      if k != "status":
   #         try:
   #            #230822: Round (with round rather than numpy.round) and allow for single valued arrays (check that v is a list before interating to avoid crash)
   #            if type(v) is list:
   #               v = [round(x, 2) for x in v] 
   #            else: 
   #               v = round(v)

   #         except:
   #            print("305 - Unable to round {2:s}, for disease {0:s}, ages_last {1:s}".format(disease['name'], dict_val, v))
   #      
   #      if k == "status":
   #            for s in v:
   #                  status_string += str(s)+", "
   #                  
   #      elif k == "array":
   #            for t in v:
   #               time_string += str(t)+", "     


   #   time_string += ")" 
   #   status_string += ")"
   #   print("   ")
   #   print(disease['name'] + "---------------------") 
   #   print(dict_key)
   #   print(time_string)
   #   print(status_string)


   
   disease_table.append(dict(gene = disease['gene'],
                             name = disease['name'],
                             colour = disease['colour'],
                             animals = disease['animals'],
                             patients = count_patients,
                             articles = article_count,
                             datapoints = presentVarCount + symptomCount,
                             variables = dict(present = presentVarCount, missing = missingVarCount),
                             consanguinous = count_inbred, 
                             age_at_first_symp = ages_first,
                             age_at_last_news = ages_last,
                             survival = dict(all_surv_x = ages_surv["all"]["surv_x"],
                                             all_surv_y = ages_surv["all"]["surv_y"],
                                             boys_surv_x = ages_surv["boys"]["surv_x"],
                                             boys_surv_y = ages_surv["boys"]["surv_y"],
                                             girls_surv_x = ages_surv["girls"]["surv_x"],
                                             girls_surv_y = ages_surv["girls"]["surv_y"]
                                             )
                              )
   )



# Serialize the article dictionnary to json
json_data = json.dumps(articles, indent = 4)
# Writing (append) to articles_out.json
# Check output before copying to articles_DOI.json
with open("articles_out.json", "w") as outfile:
   outfile.write(json_data)
outfile.close()



# Serialize the python dictionnary to json
json_data = json.dumps(disease_table, indent = 4)

# Writing to bdt_out.json
# Check output before copying to hp_disease_stats.json
with open("bdt_out.json", "w") as outfile:
    outfile.write(json_data)

outfile.close()
   



