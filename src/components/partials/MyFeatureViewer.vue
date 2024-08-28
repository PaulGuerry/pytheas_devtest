<template lang="html">
    
    <div class="mt-0 mb-1 text-blue-700 font-light"> {{ proteinName }}</div>
    <div id="myfv" > </div> 

</template>

<script>
import { createFeature } from 'feature-viewer';
import { ProteinService } from '@/services/FetchProteinData'

export default {
   name: 'MyFeatureViewer', 
   data() {
    return {
        proteinData: [],
        proteinName: ""
    } 
   },
   props: {
    options: {
        type: Object,
        required: true,
        default() { 
            return {
                showAxis: true, showSequence: false,
                brushActive: true, toolbar: false,
                bubbleHelp: true, zoomMax:20 
            } 
        }
    },
    featuresA: {
        type: Array,
        required: true,
        default() { 
            return [
                {
                    data: [{x:20,y:32},{x:46,y:100},{x:123,y:167}],
                    name: "default feature",
                    className: "default ft",
                    color: "#005572",
                    type: "rect",
                    filter: "default"
                }
            ]
        }   
    },
    accessionCode: {
        type: String,
        required: true,
        default: "Q96K21"
    }
   },
   mounted() {
        this.createFeatureLocal()
    },
   methods: {
    async fetchData(accessionCode) {
        try {
            let response = await ProteinService.getEBIdata(accessionCode);
            console.log(response.data);
            this.proteinData = response.data;
            console.log(this.proteinData[0]);
            console.log(this.proteinData[0].protein);
            this.proteinName = this.proteinData[0].protein.recommendedName.fullName.value;
        } catch(error) {
            console.log("Error fetching EBI data in MyFeatureViewer line 64.")
        }
    },
    async createFeatureLocal() {
        await this.fetchData(this.accessionCode)
        var ft = new createFeature(this.proteinData[0].sequence.sequence,"#myfv", this.options);
        var domainData = [];
        var siteData = [];
        var variantData = [];
        this.proteinData[0].features.forEach(element => {
            if (element.type.includes("MOTIF") || element.type.includes("REGION")) {
                domainData.push({x: parseInt(element.begin), y: parseInt(element.end), description: element.description + "                   "});
            } else if (element.type.includes("COILED")) {
                domainData.push({x: parseInt(element.begin), y: parseInt(element.end), description: element.type + " COIL" + "                "})
            } else if (element.type.includes("BINDING")) {
                siteData.push({x: parseInt(element.begin), y: parseInt(element.end), description: element.ligand.name + " binding site"});
            } else if (element.category.includes("PTM")) {
                siteData.push({x: parseInt(element.begin), y: parseInt(element.end), description: element.description});
            } else if (element.type.includes("VARIANT") && element.description.includes("in ")) {
                if (element.alternativeSequence.length > 0) {
                    variantData.push({x: parseInt(element.begin), y: parseInt(element.begin), description: "> " + element.alternativeSequence + " " + element.description});
                } else {
                    variantData.push({x: parseInt(element.begin), y: parseInt(element.begin), description: "> MISSING " + element.description});
                }
            }
        });
        var featureA = [ 
            {
                data: domainData,
                name: "Domains and motifs",
                className: "A",
                color: "#F4D4AD",
                type: "rect",
                filter: "type 1"
            },
            {
                data: siteData,
                name: "Binding and PTMs",
                className: "A",
                color: "#C03000",
                type: "rect",
                filter: "type 1"

            },
            {
                data: variantData,
                name: "Dis.-assoc. variants",
                className: "A",
                color: "#C09000",
                type: "rect",
                filter: "type 1"

            },
        ];
        featureA.forEach(element => {ft.addFeature(element)});
        }
    }
}
</script>
<style lang="css" scoped>
    
</style>

