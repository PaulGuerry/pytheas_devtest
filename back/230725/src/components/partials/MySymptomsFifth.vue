<template>



<div v-if="HPOcodes.length && progressIndex <= 5">
    <div class="flex flex-col">
        <div class="w-1/2"> Loading... {{ progress[progressIndex + 1] }} %</div>
        <div class="w-1/2"> <ProgressComponent :current-count="progressIndex"  :current-percent="progress[progressIndex + 1]" :key="progressIndex" @emitted-count="nextStep"/> </div>
    </div>
</div>


<!-- need the check on progressIndex to only render the plot once all the data have been loaded !-->
<template v-if="progressIndex >= 5 && isDataLoaded">
    <div class="flex flex-row">
        <div class="chart-container w-full"><VuePlotly :data="barDataSymptoms" :layout="barLayout"></VuePlotly></div>
        <div class="chart-container w-full"><VuePlotly :data="douDataSymptoms" :layout="douLayout"></VuePlotly></div>
    </div>
    <template v-if="this.otherSymptoms.length > 0">
        <div class="mb-20"> 
            <p class="italic text-sm"> Less frequently reported symptoms (HPO term (n)): </p> 
            <span class="text-xs text-justify" v-for="(item, index) in this.otherSymptoms" :key="index">{{ item.name }} ({{ item.count }}), </span>
        </div>
    </template>
    <div class="grid grid-cols-2 gap-12 max-w-[1200px] mt-50">
        <div class="chart-container">
            <!-- Adjust mb of title paragraphs for vertical alignment -->
            <p class="italic "> Sex ratio </p>
            <VuePlotly :data="barDataSexRatio" :layout="barSRlayout"></VuePlotly>
        </div>
        <div class="chart-container">
            <p class="ml-10 italic"> Age at diagnosis (months) </p>
            <VuePlotly :data="boxAgeAtDiag" :layout="boxLayout"></VuePlotly>
        </div>
        <div class="chart-container">
            <p class="ml-10 italic"> Survival (months) </p>
            <VuePlotly :data="survData" :layout="survLayout"></VuePlotly>
        </div>
        <div class="chart-container">
            <p class="ml-10 italic"> Age at last follow-up (years) </p>
            <VuePlotly :data="boxAgeAtLastFoUp" :layout="boxLayout"></VuePlotly>
        </div>
    </div>
</template>

<!-- <div id="symptomList">
    <div class="mb-1" v-for="(value, key, index) in convertedSymptomStats(gatherSymptoms())" :key="index">
        <p> {{ value.label }} ({{ key }}) "===>" {{  value.count }} </p>
    </div>
</div> -->




</template>





<script>
import myPatientData from '@/assets/patientData_edited.json'
import hpoEdges from '@/assets/hp_edges.json'
import myColourScheme from '@/assets/colourScheme.json'
import hpoNodes from '@/assets/hp_nodes.json'
import douLayout1 from '@/assets/douLayout1.json'
import boxLayout1 from '@/assets/boxLayout.json'
import barLayout2 from '@/assets/barLayout2.json'
import barLayout3 from '@/assets/barLayout3.json'
import survLayout1 from '@/assets/survivalLayout1.json'
import ProgressComponent from './MyProgressComponent.vue'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "MySymptoms",
    components: { ProgressComponent, VuePlotly },
    emits: ["patientCounts"],
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherSymptoms();    
        this.$emit('patientCounts', {"totalNo": this.patientTotal, "girlNo": this.girlNo});
    },
    methods: {
        initialState() {
            return {
                patientData: myPatientData,
                HPOedgeData: hpoEdges.graphs[0].edges,
                HPOnodeData: hpoNodes.graphs[0].nodes,
                colourScheme: myColourScheme,
                HPOcodes: [],
                HPOcodeMap: [],
                progress: [0, 5, 10, 20, 40, 80, 100],
                indexes: [],
                counts: {},
                otherSymptoms: [],
                cutoff: 999,
                barKey: 0,
                progressKey: 0,
                receivedCount: 0,
                progressIndex: 0,
                patientTotal: 0,
                girlNo: 0,
                loadTotal: 999,
                isDataLoaded: false,
                barDataSymptoms: [
                    {
                        "x": [],
                        "y": [],
                        "type": "bar",
                        "orientation": "h",
                        "text": [],
                        "textposition": "inside",
                        "textshadow": "none",
                        "textfont": {},
                        "hoverinfo": "none",
                        "marker": {
                           "color": "",
                           "line": {
                             "color": "",
                             "width": 1.5
                           }
                        }
                    }
                ], 
                barDataSymptoms2: this.barDataSymptoms,
                barDataSexRatio: [
                    {
                        "x": ["Girls", "Boys"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "marker": {
                            "color": ["#f8717133", "#7dd3fc33"],
                            "line": {
                                "color": ["#f87171", "#7dd3fc"],
                                "width": 1.5
                            }
                        }
                    }
                ], 
                douDataSymptoms: [
                    {
                        "values": [],
                        "labels": [],
                        "type": "pie",
                        "name": "",
                        "hoverinfo": "none",
                        "hole": 0.4,
                        "textpostition": "inside",
                        "textinfo":"label+percent",
                        "textfont":{
                            "size": 10
                        },
                        "marker": {
                        "colors": [],
                        "line": {
                            "width": 0
                        }
                        }
                    }
                ], 
                douDataSymptoms2: this.douDataSymptoms,
                boxAgeAtLastFoUp: [
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Girls" ,
                        "line": {"width": 1, "color": "#f87171"}
                    },
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Boys" ,
                        "line": {"width": 1, "color": "#7dd3fc"}
                    }
                ], 
                boxAgeAtDiag: [
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Girls" ,
                        "line": {"width": 1, "color": "#f87171"}
                    },
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Boys" ,
                        "line": {"width": 2, "color": "#7dd3fc"}
                    }
                ], 
                survData: [
                    {
                        "x": [9,13,18,23,28,31,34,45,48],
                        "y": [0.909,0.818,0.716,0.614,0.614,0.491,0.368,0.368,0.184],
                        "name":"Girls",
                        "type": "scatter",
                        "mode": "lines+markers",
                        "line": {"width": 1, "color": "#f87171"}
                    },
                    {
                        "x": [5,8,12,16,23,27,30,33,43,45],
                        "y": [0.833,0.667,0.583,0.583,0.486,0.389,0.292,0.194,0.097,0],
                        "name":"Boys",
                        "type": "scatter",
                        "mode": "lines+markers",
                        "line": {"width": 1, "color": "#7dd3fc"}
                    }
                ],
                barLayout: barLayout2, 
                barSRlayout: barLayout3, 
                douLayout: douLayout1,
                boxLayout: boxLayout1,
                survLayout: survLayout1, 
            }
        }, 
        reset() {
            Object.assign(this.$data, this.initialState())
        },
        nextStep(){
             let start = this.indexes[this.progressIndex];
             let end = this.indexes[this.progressIndex + 1];
             this.convertedSymptomStats(start, end);
         },
        //source for rerendering: https://michaelnthiessen.com/force-re-render/
        gatherSymptoms() {
            let patientList = this.patientData.filter((item) => {return (item.gene == this.gene)})
            let patientCodes = [];
            patientList.forEach(
                patient => {
                    patientCodes = [];
                    (patient.symptoms && patientCodes.push(...patient.symptoms) );    // if patient.symptoms exists then append content to symptoms array (... is spread syntax)
                    (patient.labfindings && patientCodes.push(...patient.labfindings) );  // if patient.labfindings exists then append content to symptoms array (... is spread syntax)
                    this.HPOcodes.push(...new Set(patientCodes)); // only save unique entries. Deals with situation of symptoms appearing both in symptoms and labfindings
                    (patient.sex === 'F' && this.girlNo++ && patient.firstsymptomagemonth & this.boxAgeAtDiag[0].y.push(patient.firstsymptomagemonth));  // if patient.sex is female
                    (patient.sex === 'M' && patient.firstsymptomagemonth && this.boxAgeAtDiag[1].y.push(patient.firstsymptomagemonth));  // if patient.sex is male
                    (patient.sex === 'F' && patient.lastnewsageyear && this.boxAgeAtLastFoUp[0].y.push(patient.lastnewsageyear));  // 
                    (patient.sex === 'M' && patient.lastnewsageyear && this.boxAgeAtLastFoUp[1].y.push(patient.lastnewsageyear));  // if patient.sex is male
                    this.patientTotal++;
                }
            )
            this.loadTotal = this.HPOcodes.length;
            this.indexes = this.progress.map(val => Math.ceil(val * this.loadTotal / 100));
            this.barDataSexRatio[0].y = [this.girlNo, this.patientTotal - this.girlNo];
            this.barDataSexRatio[0].text = [String(this.girlNo), String(this.patientTotal - this.girlNo)];
            return null;
        },
        rawSymptomStats(HPOcodes) {
            for (const HPOcode of HPOcodes) {
                this.counts[HPOcode] = this.counts[HPOcode] ? this.counts[HPOcode] + 1 : 1;
            }
            return null
        },
        convertedSymptomStats(start, stop) {
            this.isDataLoaded = false;
            let convertedEntry = {};
            let convertedCode = "";
            let i = 0;
            //Loop over all entries in HPOcode list but only convert and count those with indexes between start and end 
            //(i.e. those that have not yet been analysed) 
            for (let HPOcode of this.HPOcodes) {
                if (i >= start && i < stop) {   
                    if (this.HPOcodeMap.some(element => HPOcode === element.code)) { 
                        let objArray = this.HPOcodeMap.filter(element => {return (HPOcode === element.code)});
                        convertedCode = objArray[0].convertedCode;
                    } else {
                        convertedEntry = this.convertHPOcode(HPOcode);
                        convertedCode = convertedEntry.code;
                        this.HPOcodeMap.push({
                            "code": HPOcode, 
                            "convertedCode": convertedCode, 
                            "label": convertedEntry.label, 
                            "level": parseInt(this.branchLevel), 
                            "colour": convertedEntry.colour, 
                            "borderColour": convertedEntry.borderColour
                        });
                        let obj = {
                            "code": convertedCode, 
                            "count": 0, 
                            "label": convertedEntry.label, 
                            "colour": convertedEntry.colour, 
                            "borderColour": convertedEntry.borderColour
                        };
                        this.counts[convertedCode] = obj;
                    }
                    this.counts[convertedCode].count++ ;
                    console.log(convertedCode, this.counts[convertedCode].count)    
                }
                i++;
            }
            //Only do the sorting the last time the function is run
            if (this.progressIndex == 5) {
                //sorting based on https://medium.com/@gmcharmy/sort-objects-in-javascript-e-c-how-to-get-sorted-values-from-an-object-142a9ae7157c
                //             and https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
                this.counts = Object.fromEntries(Object.entries(this.counts).sort((a, b) => b[1].count - a[1].count));
                
                // Slice here to split counts into top n entries and remainder
                //this.counts = Object.fromEntries(Object.entries(this.counts).slice(0, 8));
                //remcounts = Object.fromEntries(Object.entries(this.counts).slice(9, 999));
                // 
                this.barDataSymptoms[0].y = Object.keys(this.counts).map((key) => this.counts[key].label);
                this.barDataSymptoms[0].x = Object.keys(this.counts).map(key => this.counts[key].count);
                this.barDataSymptoms[0].text = Object.keys(this.counts).map(key => this.counts[key].count);
                this.barDataSymptoms[0].marker.color = Object.keys(this.counts).map((key) => this.counts[key].colour);
                this.barDataSymptoms[0].marker.line.color = Object.keys(this.counts).map((key) => this.counts[key].borderColour);
                // Carefully inspect structure of constructed object with console.log(Object.entries(this.counts));
                this.douDataSymptoms[0].labels = Object.keys(this.counts).map((key) => this.counts[key].label);
                this.douDataSymptoms[0].values = Object.keys(this.counts).map((key) => this.counts[key].count);
                this.douDataSymptoms[0].marker.colors = Object.keys(this.counts).map((key) => this.counts[key].colour);

                // Now only keep symptoms reported in more than 5% of patients
                for (let i = 0; i <= this.barDataSymptoms[0].x.length; i++) {
                    if (this.barDataSymptoms[0].x[i] < .05 * this.patientTotal) {this.cutoff = i; break}
                }
                for (let i = this.cutoff; i < this.barDataSymptoms[0].x.length; i++) {
                    this.otherSymptoms.push({"name": this.barDataSymptoms[0].y[i], "count": this.barDataSymptoms[0].x[i]});
                }
                
                this.barDataSymptoms[0].y = this.barDataSymptoms[0].y.slice(0, this.cutoff);
                this.barDataSymptoms[0].x = this.barDataSymptoms[0].x.slice(0, this.cutoff);
                this.barDataSymptoms[0].text = this.barDataSymptoms[0].text.slice(0, this.cutoff);
                this.barDataSymptoms[0].marker.color = this.barDataSymptoms[0].marker.color.slice(0, this.cutoff);
                this.barDataSymptoms[0].marker.line.color = this.barDataSymptoms[0].marker.line.color.slice(0, this.cutoff);
                this.douDataSymptoms[0].labels =  this.douDataSymptoms[0].labels.slice(0, this.cutoff);
                this.douDataSymptoms[0].values =  this.douDataSymptoms[0].values.slice(0, this.cutoff);
                this.douDataSymptoms[0].marker.colors = this.douDataSymptoms[0].marker.colors.slice(0, this.cutoff);
                //
                this.douLayout.annotations[0].text = this.gene;
                this.isDataLoaded = true;
            }
            this.progressIndex++
            return null
        },
        findHPOedges(HPOcode) {
            let result = [];
            let edge = [];
            let i = 0;
            //console.log("code " + HPOcode);
            result.push({"code": HPOcode, "label": this.findHPOnode(HPOcode), "level": i});
            while (HPOcode != "0000001") {
                edge = this.HPOedgeData.filter((element) => element.sub.includes(HPOcode));
                HPOcode = edge[0].obj.substring(34);
                i++;
                result.push({"code": edge[0].obj.substring(34), "label": this.findHPOnode(HPOcode), "level": i});
            }
            result.map(element => {element.level = Math.abs(element.level - result.length) - 1});
            //set type of hierarchy to the level 2 code and then get the corresponding colour from the colourscheme matrix 
            let type = result.filter((element) => element.level == 2)[0].code;
            result.map((element) => {
                element.colour = this.colourScheme.filter((element) => element.code.includes(type))[0].colour;
                element.borderColour = this.colourScheme.filter((element) => element.code.includes(type))[0].borderColour;
                        });
            return result;
        },
        findHPOnode(HPOcode) {
            let node = this.HPOnodeData.filter((element) => element.id.includes(HPOcode));
            let result = (node && node[0] && 'lbl' in node[0] ? node[0].lbl : console.log("Error finding HPO node (177)")) // result = node[0].lbl only if node[0].lbl actually exists
            return result
        },
        convertHPOcode(HPOcode){
            let maxLen = this.findHPOedges(HPOcode).length - 1;

            let result = this.findHPOedges(HPOcode).slice().reverse()[(parseInt(this.branchLevel) <= maxLen ? parseInt(this.branchLevel) : maxLen)];
            return result // result is an object {"code", "label", "level", "colour"}
        },
    },
    props: {
    gene: {
        type: String,
        required: true,
        default: "ATP8B1" 
        },
    branchLevel: {
        type: String,
        required: true,
        default: "12"
        }
    },
}

</script>


<style>

</style>