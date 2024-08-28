<template>


<!-- vue-chartjs chart-->
<div>
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
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "PatientList",
    components: { Bar },
    async setup() {
        this.HPOcodes = await this.gatherSymptoms();
        this.countData = await this.convertedSymptomStats(this.HPOcodes);
    },
    data() {
        return {
            patientData: myPatientData,
            HPOedgeData: hpoEdges.graphs[0].edges,
            HPOnodeData: hpoNodes.graphs[0].nodes,
            HPOcodeMap: [],
            HPOcodes: [],
            countData:{},
            barKey: 0,
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
    methods: {
        //source for rerendering: https://michaelnthiessen.com/force-re-render/
        rerender() { 
            this.barKey++
            return
        },
        gatherSymptoms() {
            let HPOcodes = [];
            let patientList = this.patientData.filter((item) => {return (item.gene == this.gene)})
            patientList.forEach(
                patient => {
                    (patient.symptoms && HPOcodes.push(...patient.symptoms) )  // if patient.symptoms exists then append content to symptoms array (... is spread syntax)
                }
            )
            return HPOcodes;
        },
        rawSymptomStats(HPOcodes) {
            const counts = {};
            for (const HPOcode of HPOcodes) {
                counts[HPOcode] = counts[HPOcode] ? counts[HPOcode] + 1 : 1;
            }
            return counts
        },
        convertedSymptomStats(HPOcodes) {
            let counts = {};
            let convertedEntry = {};
            let convertedCode = "";
            this.entriesDone = 0;
            this.entriesTotal = HPOcodes.length;
            for (let HPOcode of HPOcodes) {
                if (this.HPOcodeMap.some(element => HPOcode === element.code)) { 
                    let objArray = this.HPOcodeMap.filter(element => {return (HPOcode === element.code)});
                    convertedCode = objArray[0].convertedCode;
                } else {
                    convertedEntry = this.convertHPOcode(HPOcode);
                    convertedCode = convertedEntry.code;
                    this.HPOcodeMap.push({"code": HPOcode, "convertedCode": convertedCode, "label": convertedEntry.label, "level": this.branchLevel});
                    let obj = {"code": convertedCode, "count": 0, "label": convertedEntry.label};
                    counts[convertedCode] = obj;
                }
                counts[convertedCode].count++ ;
                ++this.entriesDone;
            }
            
            //sorting based on https://medium.com/@gmcharmy/sort-objects-in-javascript-e-c-how-to-get-sorted-values-from-an-object-142a9ae7157c
            this.chartData.labels = Object.entries(counts).sort((a, b) => b[1] - a[1]).map(element => element[1].label);
            // Carefully inspect structure of constructed object with console.log(Object.entries(counts));
            this.chartData.datasets[0].data = Object.entries(counts).sort((a, b) => b[1].count - a[1].count).map(element => element[1].count);
            this.rerender();
            return counts
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