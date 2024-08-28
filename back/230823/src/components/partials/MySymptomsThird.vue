<template>


<p> Loading... </p>
<ProgressComponent :progressVal="loadProgress" :key="progressKey"/>



<!-- vue-chartjs chart-->
<div v-if="isLoaded">
    <Bar :data="chartData" :options="chartOptions" :key="barKey"/>
</div>

<!-- <div id="symptomList">
    <div class="mb-1" v-for="(value, key, index) in convertedSymptomStats(gatherSymptoms())" :key="index">
        <p> {{ value.label }} ({{ key }}) "===>" {{  value.count }} </p>
    </div>
</div> -->




</template>





<script>
import myPatientData from '@/assets/patientData.json'
import hpoEdges from '@/assets/hp_edges.json'
import hpoNodes from '@/assets/hp_nodes.json'
import ProgressComponent from './MyProgressComponent.vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "PatientList",
    components: { Bar, ProgressComponent },
    data() {
        return {
            patientData: myPatientData,
            HPOedgeData: hpoEdges.graphs[0].edges,
            HPOnodeData: hpoNodes.graphs[0].nodes,
            HPOcodes: [],
            HPOcodeMap: [],
            starts: [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
            counts: {},
            barKey: 0,
            progressKey: 0,
            loadProgress: 0,
            loadTotal: 999,
            isLoaded: false,
            chartData: {
                labels: [],
                datasets: [
                    {
                        label: '',
                        backgroundColor: '#f87979',
                        data: []
                    }
                ]
            },
            chartOptions: {
                responsive: true,
                scales: { x: { grid: { display: false }}, 
                          y: { grid: { display: false }}
                        },
                plugins: {legend: { display: false }}
            }
        }
    },
    mounted() { this.gatherSymptoms() },
    methods: {
       loadData(runCount) {
            //On first run, fetch and count list symptoms to analyse
            if (runCount == 0) {
                this.gatherSymptoms();
                this.loadTotal = this.HPOcodes.length;
                this.starts = this.starts.map(val => Math.ceil(val * this.loadTotal));
                console.log("81 this.loadTotal = ", this.loadTotal, ", this.loadProgress = ", this.loadProgress, ", this.starts = ", this.starts)
                return "Loading..."
            //From second run onwards, convert and classify the next batch of symptoms     
            } else if (runCount <= this.loadTotal) {
                let start = this.starts[runCount - 1];
                let end = this.starts[runCount];
                this.convertedSymptomStats(start, end);
                runCount = 999;
                console.log("87 this.loadTotal = ", this.loadTotal, ", this.loadProgress = ", this.loadProgress, ", start = ", start, ", end =", end)
                return "Loading..."
            } else {
                console.log("93 runCount = ", runCount);
                return "Loading..."
            }
        }, 
        //source for rerendering: https://michaelnthiessen.com/force-re-render/
        rerender() { 
            this.barKey++
            this.progressKey++
            return
        },
        gatherSymptoms() {
            let patientList = this.patientData.filter((item) => {return (item.gene == this.gene)})
            patientList.forEach(
                patient => {
                    (patient.symptoms && this.HPOcodes.push(...patient.symptoms) )  // if patient.symptoms exists then append content to symptoms array (... is spread syntax)
                }
            )
            this.loadProgress++
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
                        this.HPOcodeMap.push({"code": HPOcode, "convertedCode": convertedCode, "label": convertedEntry.label, "level": this.branchLevel});
                        let obj = {"code": convertedCode, "count": 0, "label": convertedEntry.label};
                        this.counts[convertedCode] = obj;
                    }
                    this.counts[convertedCode].count++ ;
                }
                i++;
            }
            //sorting based on https://medium.com/@gmcharmy/sort-objects-in-javascript-e-c-how-to-get-sorted-values-from-an-object-142a9ae7157c
            this.chartData.labels = Object.entries(this.counts).sort((a, b) => b[1] - a[1]).map(element => element[1].label);
            // Carefully inspect structure of constructed object with console.log(Object.entries(this.counts));
            this.chartData.datasets[0].data = Object.entries(this.counts).sort((a, b) => b[1].count - a[1].count).map(element => element[1].count);
            //230206: is rerender still needed ?
            this.rerender();
            this.loadProgress++
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
            return result;
        },
        findHPOnode(HPOcode) {
            let node = this.HPOnodeData.filter((element) => element.id.includes(HPOcode));
            let result = (node && node[0] && 'lbl' in node[0] ? node[0].lbl : console.log("Error finding HPO node (l80)")) // result = node[0].lbl only if node[0].lbl actually exists
            return result
        },
        convertHPOcode(HPOcode){
            let maxLen = this.findHPOedges(HPOcode).length - 1;
            let result = this.findHPOedges(HPOcode).slice().reverse()[(this.branchLevel <= maxLen ? this.branchLevel : maxLen)];
            return result // result is an object {"code", "label", "level"}
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