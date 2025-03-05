<template>
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="isBarSymptoms = true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Symptoms </button> 
                <template v-if="isBarSymptoms">
                    <div class="chart-container w-full"><VuePlotly :data="barDataSymptoms" :layout="barLayout2" :config="plotConfig"></VuePlotly></div>
                    <div class="chart-container w-full"><VuePlotly :data="douDataSymptoms" :layout="douLayout" :config="plotConfig"></VuePlotly></div>
                </template>
        </div>
    </div>




    <div class="mb-40">
        <div class="flex flex-row w-3/4">
            <div class="chart-container w-full"><VuePlotly :data="barDataSymptoms" :layout="barLayout2" :config="plotConfig"></VuePlotly></div>
            <div class="chart-container w-full"><VuePlotly :data="douDataSymptoms" :layout="douLayout" :config="plotConfig"></VuePlotly></div>
        </div>
        <div class="mt-10" v-if="this.otherSymptoms.length > 0"> 
            <p class="italic text-sm"> Less frequently reported symptoms (HPO term (n)): </p> 
            <span class="text-xs text-justify" v-for="(item, index) in this.otherSymptoms" :key="index">{{ item.name }} ({{ item.count }}), </span>
        </div>
    </div>

    <div class="flex flex-row w-3/4">
        <div class="chart-container w-full">
            <!-- Adjust mb of title paragraphs for vertical alignment -->
            <p class="italic "> Sex ratio </p>
            <VuePlotly :data="barDataSexRatio" :layout="barLayout3" :config="plotConfig"></VuePlotly>
        </div>
        <div class="chart-container w-full">
            <p class="ml-10 italic"> Age at first symptoms (months) </p>
            <VuePlotly :data="boxAgeAtFirstSymp" :layout="boxLayout" :config="plotConfig"></VuePlotly>
        </div>
    </div>

    <div class="flex flex-row">
        <div class="chart-container w-full">
            <p class="ml-10 italic"> Survival (months) </p>
            <VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly>
        </div>
    </div>


</template>





<script>
import myPatientData from '@/assets/patientData_edited.json'
import mySymptomStats from '@/assets/hp_symptom_stats.json'
import myDiseaseStats from '@/assets/hp_disease_stats.json'
import myColourScheme from '@/assets/colourScheme.json'
import douLayout1 from '@/assets/douLayout1.json'
import boxLayout1 from '@/assets/boxLayout.json'
import myBarLayout2 from '@/assets/barLayout2.json'
import myBarLayout3 from '@/assets/barLayout3.json'
import survLayout1 from '@/assets/survivalLayout1.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "MySymptoms",
    components: {  VuePlotly },
    emits: ["patientCounts"],
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherStats();    
        this.$emit('patientCounts', {"totalNo": this.patientTotal, "girlNo": this.girlNo});
        //this.$emit('patientCounts', {"totalNo": 999, "girlNo": 99});
    },
    methods: {
        initialState() {
            return {
                patientData: myPatientData,
                symptomArray: mySymptomStats,
                diseaseArray: myDiseaseStats,
                // HPOedgeData: hpoEdges.graphs[0].edges,
                // HPOnodeData: hpoNodes.graphs[0].nodes,
                colourScheme: myColourScheme,
                HPOcodes: [],
                HPOcodeMap: [],
                indexes: [],
                counts: {},
                otherSymptoms: [],
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
                           "color": [],
                           "line": {
                             "color": [],
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
                        "textinfo":"label+value", //"label+percent"
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
                boxAgeAtFirstSymp: [
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Girls" ,
                        "color": "#f8717133",
                        "line": {"width": 1, "color": "#f87171"}
                    },
                    {
                        "y": [], 
                        "type":"box",
                        "name": "Boys" ,
                        "color": "#7dd3fc33",
                        "line": {"width": 2, "color": "#7dd3fc"}
                    }
                ], 
                scatterSurvival: [ 
                                    {
                                      x:[],
                                      y:[],
                                      name: "Girls",
                                      type: "scatter",
                                      mode: "lines", 
                                      line: {width: 2, color: "#f87171", shape: "hv"}
                                    },
                                    {
                                      x:[],
                                      y:[],
                                      name: "Boys",
                                      type: "scatter",
                                      mode: "lines", 
                                      line: {width: 2, color: "#7dd3fc", shape: "hv"}
                                    }
                ],
                barLayout2: myBarLayout2, 
                barLayout3: myBarLayout3, 
                douLayout: douLayout1,
                boxLayout: boxLayout1,
                survLayout: survLayout1, 
                plotConfig:{displayModeBar: false} 
            }
        }, 
        reset() {
            Object.assign(this.$data, this.initialState())
        },
        gatherStats() {
            var stats = this.symptomArray.filter((item) => {return (item.gene == this.gene && item.analysis_level == this.branchLevel)})
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.gene)})
            
            this.boxAgeAtFirstSymp[0].y = stats_disease[0].age_at_first_symp.girls.array;
            this.boxAgeAtFirstSymp[1].y = stats_disease[0].age_at_first_symp.boys.array;
            this.girlNo = stats[0].girls;
            this.patientTotal = stats[0].patients;
            this.barDataSexRatio[0].y = [this.girlNo, this.patientTotal - this.girlNo];
            this.barDataSexRatio[0].text = [String(this.girlNo), String(this.patientTotal - this.girlNo)];
            this.douLayout.annotations[0].text = this.disease;

            this.scatterSurvival[0].x = stats_disease[0].age_at_last_news.girls.surv_x;
            this.scatterSurvival[0].y = stats_disease[0].age_at_last_news.girls.surv_y;
            this.scatterSurvival[1].x = stats_disease[0].age_at_last_news.boys.surv_x;
            this.scatterSurvival[1].y = stats_disease[0].age_at_last_news.boys.surv_y;
            
            for (var i = 0; i < stats[0].counts.length; i++) {
                this.barDataSymptoms[0].x.push(stats[0].counts[i].n); 
                this.barDataSymptoms[0].y.push(stats[0].counts[i].HPO_term); 
                this.barDataSymptoms[0].text.push(String(stats[0].counts[i].n));
                this.barDataSymptoms[0].marker.color.push(String(stats[0].counts[i].colour));
                this.barDataSymptoms[0].marker.line.color.push(String(stats[0].counts[i].colour).substring(0,7));

                this.douDataSymptoms[0].labels.push(stats[0].counts[i].HPO_acronym); 
                this.douDataSymptoms[0].values.push(stats[0].counts[i].n);
                this.douDataSymptoms[0].marker.colors.push(String(stats[0].counts[i].colour));
                //console.log("HPO term, ", stats[0].counts[i].HPO_term, "; colour, ", String(stats[0].counts[i].colour))
            }

            
            // Now only keep symptoms reported in more than x% of patients
            let cutoff = this.barDataSymptoms[0].x.length
            for (let i = 0; i <= this.barDataSymptoms[0].x.length; i++) {
                if (this.barDataSymptoms[0].x[i] < .1 * this.patientTotal) {cutoff = i; break}
            }
            for (let i = this.cutoff; i < this.barDataSymptoms[0].x.length; i++) {
                this.otherSymptoms.push({"name": this.barDataSymptoms[0].y[i], "count": this.barDataSymptoms[0].x[i]});
            }
            this.barDataSymptoms[0].y = this.barDataSymptoms[0].y.slice(0, cutoff);
            this.barDataSymptoms[0].x = this.barDataSymptoms[0].x.slice(0, cutoff);
            this.barDataSymptoms[0].text = this.barDataSymptoms[0].text.slice(0, cutoff);
            this.barDataSymptoms[0].marker.color = this.barDataSymptoms[0].marker.color.slice(0, cutoff);
            this.barDataSymptoms[0].marker.line.color = this.barDataSymptoms[0].marker.line.color.slice(0, cutoff);

            this.douDataSymptoms[0].labels =  this.douDataSymptoms[0].labels.slice(0, cutoff);
            this.douDataSymptoms[0].values =  this.douDataSymptoms[0].values.slice(0, cutoff);
            this.douDataSymptoms[0].marker.colors = this.douDataSymptoms[0].marker.colors.slice(0, cutoff);
            

        },
    },
    props: {
    gene: {
        type: String,
        required: true,
        default: "ATP8B1" 
        },
    disease: {
        type: String,
        required: true,
        default: "PFIC1" 
        },
    branchLevel: {
        type: String,
        required: true,
        default: "999"
        }
    },
}

</script>


<style>

</style>