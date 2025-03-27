<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" colspan="4" class="px-6 py-1 text-left">
                        REPORTED SYMPTOMS AS HPO CATEGORIES
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
                       <input type="number" min=2 step=1 max=3 v-model="branchLevel" class="text-center" @input="$emit('updateBrLvl', branchLevel)">
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
    </div>
    <div class="my-0 flex flex-row col-start-1 col-span-2 md:col-span-3 lg:col-span-5">
        <div class="chart-container w-full"><VuePlotly :data="barDataSymptoms" :layout="barLayout2" :config="plotConfig"></VuePlotly></div>
    </div>
    <div class="mt-2 flex flex-row col-start-1 col-span-2 md:col-span-3 lg:col-span-5" v-if="this.otherSymptoms.length > 0"> 
            <p class="italic text-sm font-semibold w-1/8"> Less frequently reported symptom classes (HPO term (n)): </p> 
            <span class="text-xs text-justify" v-for="(item, index) in this.otherSymptoms" :key="index">{{ item.name }} ({{ item.count }}), </span>
    </div>
    <div class="mt-2 flex flex-row col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
            <p class="italic text-sm font-semibold w-1/8"> Abbreviations: </p> 
            <span class="text-xs text-justify" v-for="(item, index) in this.barDataSymptoms[0].x" :key="index">{{ item }}, {{ this.barDataSymptoms[0].longname[index] }}; </span>
    </div>
        
</template>
<script>

import mySymptomStats from '@/assets/hp_symptom_stats.json'
import myBarLayout2 from '@/assets/barLayout2.json'
import douLayout1 from '@/assets/douLayout1.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSymptomBarDoughnut",
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
                barLayout2: myBarLayout2,
                douLayout: douLayout1,
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                sexRatio: 0,
                counts: [],
                branchLevel: this.propData.branchLevel,
                //VuePlotly requires data to be sent as an single entry array,
                //.. so each bar plot has to be saved as a single entry array,
                //.. so barDataSymptoms has to be an array of single-entry object arrays
                barDataSymptoms: [
                        {
                            "x": [],
                            "y": [],
                            "longname": [],
                            "type": "bar",
                            "orientation": "v",
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
                otherSymptoms: [],
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            var stats = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == this.propData.branchLevel)})
            //console.log(stats[0])
            this.counts = stats[0].counts
            this.girlNo = stats[0].girls;
            this.patientTotal = stats[0].patients;
            this.boyNo = this.patientTotal - this.girlNo;
            this.sexRatio = this.boyNo / this.girlNo
            this.sexRatio = Math.round((this.sexRatio * 100) * (1 + Number.EPSILON)) / 100
            this.douLayout.annotations[0].text = this.propData.disease;
            console.log("150", stats[0].counts.length)
            for (var i = 0; i < stats[0].counts.length; i++) {
                //Start a new bar plot every 21st symptom
                //if (i > 1 && i % 21 === 0){
                //    j++
                //    console.log("154", j)
                //    this.barDataSymptoms.push([{
                //            "x": [],
                //            "y": [],
                //            "longname": [],
                //            "type": "bar",
                //            "orientation": "v",
                //            "text": [],
                //            "textposition": "inside",
                //            "textshadow": "none",
                //            "textfont": {},
                //            "hoverinfo": "none",
                //            "marker": {
                //               "color": [],
                //               "line": {
                //                 "color": [],
                //                 "width": 1.5
                //               }
                //            }
                //        }])
                //    
                //}
                console.log("176", i, stats[0].counts[i].HPO_term, stats[0].counts[i].n)
                this.barDataSymptoms[0].y.push(Number(stats[0].counts[i].n)); 
                this.barDataSymptoms[0].x.push(stats[0].counts[i].HPO_acronym); 
                this.barDataSymptoms[0].longname.push(stats[0].counts[i].HPO_term); 
                this.barDataSymptoms[0].text.push(String(stats[0].counts[i].n));
                this.barDataSymptoms[0].marker.color.push(String(stats[0].counts[i].colour));
                this.barDataSymptoms[0].marker.line.color.push(String(stats[0].counts[i].colour).substring(0,7));
                this.douDataSymptoms[0].labels.push(stats[0].counts[i].HPO_acronym); 
                this.douDataSymptoms[0].values.push(stats[0].counts[i].n);
                this.douDataSymptoms[0].marker.colors.push(String(stats[0].counts[i].colour));
            }


            //for (i = 0; i <= 8; i++){
            //    console.log("name, " + this.barDataSymptoms[0][0].x[i] + "; pct, " + this.barDataSymptoms[0][0].y[i])
            //}

            
            // Now only keep symptoms reported in more than x% of patients
            //let cutoff = this.barDataSymptoms[0].y.length
            //for (let i = 0; i <= this.barDataSymptoms[0].y.length; i++) {
            //    if (this.barDataSymptoms[0].y[i] < .05 * this.patientTotal) {cutoff = i; break}
            //}
            let cutoff = 22
            ////console.log("total number of symptoms, " + this.barDataSymptoms[0].y.length + "; but keep only first " + cutoff)
            for (let i = cutoff; i < this.barDataSymptoms[0].y.length; i++) {
                this.otherSymptoms.push({"name": this.barDataSymptoms[0].x[i], "count": this.barDataSymptoms[0].y[i]});
                console.log("name, " + this.barDataSymptoms[0].x[i] + "; count, " + this.barDataSymptoms[0].y[i])
            }
            this.barDataSymptoms[0].y = this.barDataSymptoms[0].y.slice(0, cutoff);
            this.barDataSymptoms[0].x = this.barDataSymptoms[0].x.slice(0, cutoff);
            this.barDataSymptoms[0].text = this.barDataSymptoms[0].text.slice(0, cutoff);
            this.barDataSymptoms[0].marker.color = this.barDataSymptoms[0].marker.color.slice(0, cutoff);
            this.barDataSymptoms[0].marker.line.color = this.barDataSymptoms[0].marker.line.color.slice(0, cutoff);

            //this.douDataSymptoms[0].labels =  this.douDataSymptoms[0].labels.slice(0, cutoff);
            //this.douDataSymptoms[0].values =  this.douDataSymptoms[0].values.slice(0, cutoff);
            //this.douDataSymptoms[0].marker.colors = this.douDataSymptoms[0].marker.colors.slice(0, cutoff);
            

        }
    },
    props: {
        propData: {
            type: Object,
            required: true,
            default: () => ({gene: "KIF12", branchLevel: 3, disease: "PFIC8"}) 
        }
    },

}
</script>

<style lang="">
    
</style>