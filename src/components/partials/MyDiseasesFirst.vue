<template>



<!-- <div v-if="HPOcodes.length && progressIndex <= 5">
    <div class="flex flex-col">
        <div class="w-1/2"> Loading... {{ progress[progressIndex + 1] }} %</div>
        <div class="w-1/2"> <ProgressComponent :current-count="progressIndex"  :current-percent="progress[progressIndex + 1]" :key="progressIndex" @emitted-count="nextStep"/> </div>
    </div>
</div> -->


<!-- vue-chartjs charts-->
<!-- need the check on barData data being actually present to stop the graph being rendered before the dataset has been updated  -->
<template v-if="barData1.datasets[0].data.length > 0">
  <div class="grid grid-cols-3 gap-10 max-w-[1200px] mx-auto my-2">
    <div class="chart-container flex flex-col gap-5">
        <!-- Adjust mb of title paragraphs for vertical alignment -->
        <p class="italic mb-8"> Number of patients in database </p>
        <Bar :data="barData1" :options="barOptions"/>
    </div>
    <div class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic mb-11"> Sex ratio </p>
        <Bar :data="barData2" :options="barOptions"/>
    </div>
    <div class="chart-container flex flex-col h-50 gap-2">
        <p class="ml-10 italic"> Age at diagnosis (months) </p>
        <apexchart type="boxPlot" height="auto" :options="boxOptions" :series="boxData"></apexchart>
    </div>
  </div>
</template>





</template>





<script>
import myPatientData from '@/assets/patientData.json'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
import VueApexCharts from "vue3-apexcharts";
ChartJS.register(ArcElement, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: "DiseaseData",
    components: { 
        Bar,
        apexchart: VueApexCharts, 
    },
    data() {
        return {
            patientData: myPatientData,
            diseaseData: [
                {
                    omim: "619662",
                    name: "PFIC8",
                    patientNo: 0,
                    girlNo: 0,
                    birthGA: [],
                    ageAtDiag: [],
                    bgColor: "#fca5a533"
                },
                {
                    omim: "619849",
                    name: "PFIC9",
                    patientNo: 0,
                    girlNo: 0,
                    birthGA: [],
                    ageAtDiag: [],
                    bgColor: "#e5e5e533"
                },
                {
                    omim: "211600",
                    name: "PFIC1",
                    patientNo: 0,
                    girlNo: 0,
                    birthGA: [],
                    ageAtDiag: [],
                    bgColor: "#38bdf833"
                }
            ],
            barData1: {
                labels: [],
                datasets: [
                    {
                        label: '',
                        backgroundColor: ["#fca5a533", "#e5e5e533", "#38bdf833", "#4338ca33"],
                        borderColor: ["#fca5a5", "#e5e5e5", "#38bdf8", "#4338ca"],
                        borderWidth: 1,
                        data: []
                    }
                ]
            },
            barData2: {
                labels: [],
                datasets: [
                    {
                        label: '',
                        backgroundColor: ["#fca5a533", "#e5e5e533", "#38bdf833", "#4338ca33"],
                        borderColor: ["#fca5a5", "#e5e5e5", "#38bdf8", "#4338ca"],
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
            boxData: [
                {
                  type: 'boxPlot',
                  data: [
                  ]
                }
            ],
            boxOptions: {
                fill: {
                    colors: ["#fca5a533", "#e5e5e533", "#38bdf833", "#4338ca33"],
                },
                legend: {
                    show: false
                },
                chart: {
                  type: 'boxPlot',
                  height: 350,
                    toolbar: {
                        show: false,
                    }
                },
                title: {
                  text: undefined,
                  align: 'left'
                },
                grid: {
                    show: false,
                    yaxis: {
                        lines: {
                            show: true
                        }
                    },
                    xaxis: {
                        lines: {
                            show: true
                        }
                    },
                },
                plotOptions: {
                  boxPlot: {
                     colors: {
                       upper: "",
                       lower: ""
                    }
                  }
                }
            },
        }
    },
    mounted() { 
        this.gatherDiseaseData();    
    },
    methods: {
        //source for rerendering: https://michaelnthiessen.com/force-re-render/
        gatherDiseaseData() {
            //for each entry in patient data
            this.patientData.forEach(
                patient => {
                    //if required entries are present, increment patient count, increment female count, add GA to array of GAs and add age at first symptoms to corresponding array
                    (patient.omim && this.diseaseData.forEach((element) => (element.omim == patient.omim && element.patientNo++)));    //
                    (patient.omim && patient.sex === 'F' && this.diseaseData.forEach((element) => (element.omim == patient.omim && element.girlNo++)));  // 
                    (patient.omim && patient.term && this.diseaseData.forEach((element) => (element.omim == patient.omim && element.birthGA.push(patient.term))));  // 
                    (patient.omim && patient.firstsymptomagemonth && this.diseaseData.forEach((element) => (element.omim == patient.omim && element.ageAtDiag.push(patient.firstsymptomagemonth))));  // 
                }
            );
            //convert birthGA and ageAtDiag data to apexchart format, i.e. min, q1, median, q3, max
            this.diseaseData.forEach((element) => { 
                let temp = [];
                temp.push(Math.min(...element.birthGA));
                temp.push(this.q25(element.birthGA));
                temp.push(this.median(element.birthGA));
                temp.push(this.q75(element.birthGA));
                temp.push(Math.max(...element.birthGA));
                element.birthGA = temp;
                temp = [];
                temp.push(Math.min(...element.ageAtDiag));
                temp.push(this.q25(element.ageAtDiag));
                temp.push(this.median(element.ageAtDiag));
                temp.push(this.q75(element.ageAtDiag));
                temp.push(Math.max(...element.ageAtDiag));
                element.ageAtDiag = temp;
            });
            //Add boxplot data to separate data series (using i counter), to have separate colors (controlled by boxOptions.fill) for each
            this.diseaseData.forEach((element) => {
                let obj = {"x":'', "y": []};
                this.barData1.labels.push(element.name); 
                this.barData2.labels.push(element.name); 
                obj.x = element.name; 
                this.barData1.datasets[0].data.push(element.patientNo);
                this.barData2.datasets[0].data.push((element.patientNo - element.girlNo)/element.girlNo); 
                //obj.backgroundColor = element.bgColor;
                //obj.y = element.birthGA;
                obj.y = element.ageAtDiag;
                this.boxData[0].data.push(obj);
            });
        },
        sortAsc(array){
            array.sort((a, b) => a - b)
        },
        sum(array) {
            array.reduce((a, b) => a + b, 0)
        },
        mean(array) { 
            this.sum(array) / array.length;
        },
        // sample standard deviation
        std(array) {
            const mu = this.mean(array);
            const diffArr = array.map(a => (a - mu) ** 2);
            return Math.sqrt(this.sum(diffArr) / (array.length - 1));
        },
        quartile(array, q) {
          const sorted = array.sort((a, b) => a - b);
          const pos = (sorted.length - 1) * q;
          const base = Math.floor(pos);
          const rest = pos - base;
          if (sorted[base + 1] !== undefined) {
            return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
          } else {
              return sorted[base];
          }
        },
        q25(array){
            return this.quartile(array, .25)
        },
        q50(array){
            return this.quartile(array, .50)
        },
        q75(array){
            return this.quartile(array, .75)
        },
        median(array) {
            return this.q50(array)
        } 
    },
    props: {
    diseaseVar: {
        type: String,
        required: true,
        default: "sexratio" 
        }
    },
}

</script>


<style>

</style>