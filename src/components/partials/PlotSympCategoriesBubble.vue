<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" colspan="4" class="px-6 py-1 text-left">
                        REPORTED PHENOTYPIC ABNORMALITIES (HPO TERMS)
                    </th>
                </tr>
                <tr>
                    <th scope="col" class="px-6 py-1 text-left">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        HPO BRANCH LEVEL
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        BOYS / GIRLS
                    </th>
                </tr>

            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2 text-left">
                        {{ propData.gene }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       <input type="number" min=2 step=1 max=5 v-model="branchLevel" class="text-center" @input="$emit('updateBrLvl', branchLevel)">
                    </td>
                    <td class="px-6 py-2 text-center"> 
                       {{ patientTotal }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ boyNo }} / {{ girlNo }} ({{ sexRatio }})
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="my-0 flex flex-row w-full">
            <div class="chart-container w-full"><VuePlotly :data="bubbleDataSymptoms" :layout="scatterLayout3" :config="plotConfig"></VuePlotly></div>
        </div>
    </div>
    
    
       
</template>
<script>

import mySymptomStats from '@/assets/hp_symptom_stats.json'
import myScatterLayout2 from '@/assets/scatterLayout3.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSympCategoriesBubble",
    components: {  VuePlotly },
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherStats();    
    },
    methods: {
        reset() {
            Object.assign(this.$data, this.initialState())
        },
        initialState() {
            return {
                symptomArray: mySymptomStats,
                scatterLayout3: myScatterLayout2,
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                sexRatio: 0,
                sel: ["All", "All"],
                counts: [],
                branchLevel: this.propData.branchLevel,
                selGirlsBoys: false,
                selLoFLoF: false, selAll: true, selAges: false,
                bubbleDataSymptoms: [
                        {
                            "x": [],
                            "y": [],
                            "text": [],
                            "mode": "markers+text",
                            "textposition": "center",
                            "type": "scatter",
                            "hoverinfo": "text",
                            "marker": {
                               "color": [],
                               "size": [],
                               "line": {
                                 "color": [],
                                 "width": 1.5
                               }
                            }
                        }
                    ],
                plotConfig:{displayModeBar: false, responsive: true}
            }
        },
        gatherStats() {
            var pa_ratio = 5.
            console.log("HERE 61")
            var stats = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == this.propData.branchLevel)})
            //var stats = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == this.propData.branchLevel)})
            this.counts = stats[0].counts
            this.countsSel = stats[0].counts
            this.girlNo = stats[0].girls;
            this.patientTotal = stats[0].patients;
            this.boyNo = this.patientTotal - this.girlNo;
            this.sexRatio = this.boyNo / this.girlNo
            this.sexRatio = Math.round((this.sexRatio * 100) * (1 + Number.EPSILON)) / 100
            //for (var i = 0; i < stats[0].counts.length; i++) {
            for (var i = 0; i < Math.min(25, stats[0].counts.length); i++) {                
                //Deal with instances where pres_abs_ratio = "-"
                if (isNaN(pa_ratio)){
                    pa_ratio = 5.
                }
                this.bubbleDataSymptoms[0].marker.size.push(Math.max(Number(stats[0].counts[i].n_pct), 10.));
                this.bubbleDataSymptoms[0].y.push(Number(stats[0].counts[i].n_pct_scaled) + Math.random() / 10  ); 
                //this.bubbleDataSymptoms[0].y.push(Number(stats[0].counts[i].n_pct_scaled)  ); 
                this.bubbleDataSymptoms[0].x.push(Number(stats[0].counts[i].category_n_scaled)); 
                this.bubbleDataSymptoms[0].text.push(String(stats[0].counts[i].HPO_term));
                this.bubbleDataSymptoms[0].marker.color.push(String(stats[0].counts[i].colour));
                this.bubbleDataSymptoms[0].marker.line.color.push(String(stats[0].counts[i].colour).substring(0,7));
                console.log(this.bubbleDataSymptoms[0].text[i], this.bubbleDataSymptoms[0].x[i], this.bubbleDataSymptoms[0].y[i], this.bubbleDataSymptoms[0].marker.size[i])
            }
            //console.log(this.bubbleDataSymptoms[0])
        }
    },
    props: {
        propData: {
            type: Object,
            required: true,
            default: () => ({gene: "KIF12", branchLevel: 2, disease: "PFIC8"}) 
        }
    },

}
</script>

<style lang="">
    
</style>
