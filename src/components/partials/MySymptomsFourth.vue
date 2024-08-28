<template>



<div v-if="HPOcodes.length && progressIndex <= 5">
    <div class="flex flex-col">
        <div class="w-1/2"> Loading... {{ progress[progressIndex + 1] }} %</div>
        <div class="w-1/2"> <ProgressComponent :current-count="progressIndex"  :current-percent="progress[progressIndex + 1]" :key="progressIndex" @emitted-count="nextStep"/> </div>
    </div>
</div>


<!-- vue-chartjs charts-->
<!-- need the check on barData data being actually present to stop the graph being rendered before the dataset has been updated  -->
<template v-if="barData.datasets[0].data.length > 0 && progressIndex >= 5">
    <div class="flex flex-row gap-12">
        <div class="chart-container w-3/5"><Bar :data="barData" :options="barOptions" :key="barKey"/></div>
        <div class="chart-container "><Doughnut :data="douData" :options="douOptions" :key="barKey"/></div>
    </div>
</template>

<!-- <div id="symptomList">
    <div class="mb-1" v-for="(value, key, index) in convertedSymptomStats(gatherSymptoms())" :key="index">
        <p> {{ value.label }} ({{ key }}) "===>" {{  value.count }} </p>
    </div>
</div> -->




</template>





<script>
import myPatientData from '@/assets/patientData.json'
import hpoEdges from '@/assets/hp_edges.json'
import myColourScheme from '@/assets/colourScheme.json'
import hpoNodes from '@/assets/hp_nodes.json'
import ProgressComponent from './MyProgressComponent.vue'
import { Bar, Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(ArcElement, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "MySymptoms",
    components: { Bar, Doughnut, ProgressComponent },
    data() {
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
            barKey: 0,
            progressKey: 0,
            receivedCount: 0,
            progressIndex: 0,
            patientTotal: 0,
            girlNo: 0,
            loadTotal: 999,
            barData: {
                labels: [],
                datasets: [
                    {
                        label: '',
                        backgroundColor: [],
                        borderColor: [],
                        borderWidth: 1,
                        data: []
                    }
                ]
            },
            barOptions: {
                responsive: true,
                scales: { x: { grid: { display: false }}, 
                          y: { grid: { display: false }, ticks: {beginAtZero: true, callback: ((value) => { if (value % 1 === 0) {return value}})}}
                        },
                plugins: {legend: { display: false }}
            },
            douData: {
                labels: [],
                datasets: [
                    {
                        label: '',
                        backgroundColor: [],
                        borderColor: [],
                        borderWidth: 0,
                        data: []
                    }
                ]
            },
            douOptions: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: { backgroundColor: '#e2e8f0', titleColor: '#334155', titleAlign: 'center', displayColors: false, bodyAlign: 'center', bodyColor: '#334155' }
                }
            }
        }
    },
    mounted() { 
        this.gatherSymptoms();    
        this.$emit('patientCounts', {"totalNo": this.patientTotal, "girlNo": this.girlNo});
    },
    methods: {
        nextStep(){
             let start = this.indexes[this.progressIndex];
             let end = this.indexes[this.progressIndex + 1];
             this.convertedSymptomStats(start, end);
         },
        //source for rerendering: https://michaelnthiessen.com/force-re-render/
        gatherSymptoms() {
            let patientList = this.patientData.filter((item) => {return (item.gene == this.gene)})
            patientList.forEach(
                patient => {
                    (patient.symptoms && this.HPOcodes.push(...patient.symptoms) );    // if patient.symptoms exists then append content to symptoms array (... is spread syntax)
                    (patient.labfindings && this.HPOcodes.push(...patient.labfindings) );  // if patient.labfindings exists then append content to symptoms array (... is spread syntax)
                    (patient.sex === 'F' && this.girlNo++ );  // if patient.sex is female
                    this.patientTotal++;
                }
            )
            this.loadTotal = this.HPOcodes.length;
            this.indexes = this.progress.map(val => Math.ceil(val * this.loadTotal / 100));
            return null;
        },
        rawSymptomStats(HPOcodes) {
            for (const HPOcode of HPOcodes) {
                this.counts[HPOcode] = this.counts[HPOcode] ? this.counts[HPOcode] + 1 : 1;
            }
            return null
        },
        convertedSymptomStats(start, stop) {
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
                            "level": this.branchLevel, 
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
                }
                i++;
            }
            //Only do the sorting the last time the function is run
            if (this.progressIndex == 5) {
                //sorting based on https://medium.com/@gmcharmy/sort-objects-in-javascript-e-c-how-to-get-sorted-values-from-an-object-142a9ae7157c
                //             and https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
                this.counts = Object.fromEntries(Object.entries(this.counts).sort((a, b) => b[1].count - a[1].count));
                this.barData.labels = Object.keys(this.counts).map((key) => this.counts[key].label);
                this.douData.labels = Object.keys(this.counts).map((key) => this.counts[key].label);
                // Carefully inspect structure of constructed object with console.log(Object.entries(this.counts));
                this.barData.datasets[0].data = Object.keys(this.counts).map((key) => this.counts[key].count);
                this.barData.datasets[0].backgroundColor = Object.keys(this.counts).map((key) => this.counts[key].colour);
                this.barData.datasets[0].borderColor = Object.keys(this.counts).map((key) => this.counts[key].borderColour);
                this.douData.datasets[0].data = Object.keys(this.counts).map((key) => this.counts[key].count);
                this.douData.datasets[0].backgroundColor = Object.keys(this.counts).map((key) => this.counts[key].colour);
                this.douData.datasets[0].borderColor = Object.keys(this.counts).map((key) => this.counts[key].borderColour);
            }
            this.progressIndex++
            return null
        },
        findHPOedges(HPOcode) {
            let result = [];
            let edge = [];
            let i = 0;
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

            let result = this.findHPOedges(HPOcode).slice().reverse()[(this.branchLevel <= maxLen ? this.branchLevel : maxLen)];
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
        type: Number,
        required: true,
        default: 12
        }
    },
}

</script>


<style>

</style>