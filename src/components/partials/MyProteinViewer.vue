<template lang="html">
    
<div v-if="dataLoaded" class="chart-container flex flex-col gap-2 -mt-60 mb-4 -z-50"><VuePlotly :data="scatterData" :layout="scatterLayout"></VuePlotly></div>

</template>

<script>

import { VuePlotly } from 'vue3-plotly'
import { ProteinService } from '@/services/FetchProteinData'
import scatterLayout1  from '@/assets/scatterLayout1.json'

export default {
    name: 'MyProteinViewer', 
    components: { 
        VuePlotly 
    },
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.createFeatures();
    },
    methods: {
        initialState() {
            return {
                proteinData: [],
                proteinName: "",
                dataLoaded: false,
                scatterData: [
                    //0 sequence (line)
                    {
                    "x": [],
                    "y": [0.01, 0.01],
                    "mode": 'lines',
                    "type": 'scatter',
                    "line": {
                        "width": 2,
                        "color": "#9ca3af"
                        },
                    "showlegend": false,
                    },
                    //1 Disordered regions
                    {
                    "name": "Disordered region",
                    "x": [],
                    "y": [],
                    "mode": "markers",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 5,
                        "color": "#0284c7" 
                        }, 
                    "hoverinfo": "text"
                    },
                    //2 Zinc fingers
                    {
                    "name": "Zinc finger",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 10,
                        "color": "#10b981" 
                        },
                    "hoverinfo": "text"
                    },
                    //3 Motifs (needs extra text)
                    {
                    "name": "Annotated motif",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 15,
                        "color": "#f87171" 
                        },
                    "hoverinfo": "text"
                    },
                    // 4 Polar residues
                    {
                    "name": "Polar residues",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 10,
                        "color": "#cbd5e1" 
                        },
                    "hoverinfo": "text"
                     },
                    // 5 Pro residues
                    {
                    "name": "Pro residues",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 10,
                        "color": "#6b7280" 
                        },
                    "hoverinfo": "text"
                     },
                    // 6 Domains (needs extra text)
                    {
                    "name": "Functional domain",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 12,
                        "color": "#84cc16" 
                        },
                    "hoverinfo": "text"
                     },
                     // 7 Coiled coils
                    {
                    "name": "Coiled coil",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 12,
                        "color": "#84cc16" 
                        },
                    "hoverinfo": "text"
                     },
                    // 8 Acidic residues
                    {
                    "name": "Acidic residues",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers+text",
                    "type": "scatter",
                    "marker": {
                        "symbol": "square",
                        "size": 10,
                        "color": "#404040" 
                        },
                    "hoverinfo": "text"
                     },
                    //9 Motifs (extra text)
                    {
                    "name": "",
                    "x": [],
                    "y": [],
                    "text": [],
                    "textposition": "bottom center",
                    "mode": "text",
                    "type": "scatter",
                    "hoverinfo": "text",
                    "showlegend": false
                    },
                    //10 Domains (extra text)
                    {
                    "name": "",
                    "x": [],
                    "y": [],
                    "text": [],
                    "textposition": "bottom center",
                    "mode": "text",
                    "type": "scatter",
                    "hoverinfo": "text",
                    "showlegend": false
                    },
                    //11 Missense variants
                    {
                    "name": "Missense variant",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers",
                    "type": "scatter",
                    "marker": {
                        "size": 8,
                        "color": "#e879f9" 
                        },
                    "hoverinfo": "text"
                    }, 
                    //12 Nonsense variants
                    {
                    "name": "Nonsense variant",
                    "x": [],
                    "y": [],
                    "text": [],
                    "mode": "markers",
                    "type": "scatter",
                    "marker": {
                        "size": 8,
                        "color": "#22d3ee" 
                        },
                    "hoverinfo": "text"
                    },
                ],
                scatterLayout: scatterLayout1
            } 
        }, 
        reset() {
            //console.log("resetting!")
            Object.assign(this.$data, this.initialState())
        },
        async fetchData(accessionCode) {
            try {
                let response = await ProteinService.getEBIdata(accessionCode);
                this.proteinData = response.data;
                } catch(error) {
                console.log("Error fetching EBI data in MyFeatureViewer line 64.")
            }
        },
        async createFeatures() {
            await this.fetchData(this.accessionCode)
            var len = this.proteinData[0].sequence.length;
            this.scatterData[0].x.push(1, len);
            this.proteinData[0].features.forEach(
                element => {
                    //console.log("TYPE: ", element.type)
                    //console.log("DESCRIPTION: ", element.description);
                    //console.log("ALTSEQ: ", element.alternativeSequence)
                    if (element.description && element.description.includes("Disordered")) {
                        this.scatterData[1].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[1].y.push(...Array(50).fill(0.01));
                    } else if (element.type && element.type.includes("ZN_FING")) {
                        this.scatterData[2].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[2].y.push(...Array(50).fill(0.01));
                    } else if (element.type && element.type.includes("MOTIF")) {
                        this.scatterData[3].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[3].y.push(...Array(50).fill(0.01));
                        this.scatterData[9].x.push((parseInt(element.begin) + parseInt(element.end)) / 2);
                        this.scatterData[9].y.push(0.015);
                        this.scatterData[9].text.push(element.description);
                        //console.log("Added motif", element.type)
                    } else if (element.description && element.description.includes("Polar residues")) {
                        this.scatterData[4].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[4].y.push(...Array(50).fill(0.01));
                    } else if (element.description && element.description.includes("Pro residues")) {
                        this.scatterData[5].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[5].y.push(...Array(50).fill(0.01));
                    } else if (element.type && element.type.includes("DOMAIN")) {
                        this.scatterData[6].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[6].y.push(...Array(50).fill(0.01));
                        this.scatterData[10].x.push((parseInt(element.begin) + parseInt(element.end)) / 2);
                        this.scatterData[10].y.push(0.007);
                        this.scatterData[10].text.push(element.description);
                        //console.log("Added domain", element.description);
                    } else if (element.type && element.type.includes("COILED")) {
                        this.scatterData[7].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[7].y.push(...Array(50).fill(0.01));
                    } else if (element.description && element.description.includes("Acidic residues")) {
                        this.scatterData[8].x.push(...this.linspace(parseInt(element.begin), parseInt(element.end), 50));
                        this.scatterData[8].y.push(...Array(50).fill(0.01));
                    } else if (element.type && element.description && element.type.includes("VARIANT") && element.alternativeSequence) {
                        this.scatterData[11].x.push((parseInt(element.begin) + parseInt(element.end)) / 2);
                        this.scatterData[11].y.push(0.013);
                        this.scatterData[11].text.push(element.description);
                    } else if (element.type && element.description && element.type.includes("VARIANT") &! element.alternativeSequence) {
                        this.scatterData[12].x.push((parseInt(element.begin) + parseInt(element.end)) / 2);
                        this.scatterData[12].y.push(0.013);
                        this.scatterData[12].text.push(element.description);
                    }
                }
            );
            this.proteinName = this.proteinData[0].protein.recommendedName.fullName.value;
            //console.log(this.proteinName, len, this.dataLoaded, this.scatterData[0].x[0], this.scatterData[0].x[1], this.scatterData[11].x[0], this.scatterData[12].x[0]);
            this.dataLoaded = true;
        },
        linspace(startValue, stopValue, cardinality) {
            var arr = [];
            var step = (stopValue - startValue) / (cardinality - 1);
            for (var i = 0; i < cardinality; i++) {
                arr.push(startValue + (step * i));
            }
            return arr;
        },  
    },
    props: {
        accessionCode: {
            type: String,
            required: true,
            default: "Q96K21"
        }
    }
}
</script>

<style lang="css" scoped>
    
</style>
