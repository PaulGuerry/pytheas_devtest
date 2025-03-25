<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-5"> 
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
                    <!--<th scope="col" class="px-6 py-1 text-center">
                        HPO BRANCH LEVEL
                    </th>-->
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
                       <input type="number" min=2 step=1 max=6 v-model="branchLevel" class="text-center" @input="$emit('updateBrLvl', branchLevel)">
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
        <template v-if="selAll">
            <div class="my-0 flex flex-row w-full">
                <div class="chart-container w-full"><VuePlotly :data="bubbleDataSymptoms" :layout="scatterLayout2" :config="plotConfig"></VuePlotly></div>
            </div>
        </template>
        <template v-if="!selAll">
            <div class="my-0 flex flex-row w-full">
                <div class="chart-container w-full"><VuePlotly :data="bubbleDataSymptomsSel1" :layout="scatterLayout2" :config="plotConfig" :key="bubbleDataSymptomsSel1[0].x.length"></VuePlotly></div>
            </div>
        </template>
        <table class="w-1/2 text-sm text-gray-500 dark:text-gray-400 my-5">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th class="px-6 py-1 text-left">
                        COMPARE SELECTIONS
                    </th>

                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="px-6 py-1 text-left">
                        <button  v-if="!selGirlsBoys"  
                            @click="reset(); gatherStats(); selAll = false; selGirlsBoys = true; sel[0] = 'GIRLS'; sel[1] = 'BOYS'; fetchSelection('Girls', 'Boys');  "
                            class="w-full py-2 text-sm bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> Girls/Boys </button> 
                        <button  v-if="selGirlsBoys" 
                            @click="reset(); gatherStats()"
                            class="w-full py-2 text-sm bg-emerald-600 text-white rounded-full"> &uarr;&uarr; Girls &uarr;&uarr; | &darr;&darr; Boys &darr;&darr; </button>
                    </td>
                    <td class="px-6 py-1 text-left">
                        <button  v-if="!selLoFLoF"  
                            @click="reset(); gatherStats(); selAll = false; selLoFLoF = true; sel[0] = 'LoF+LoF'; sel[1] = 'Other'; fetchSelection('LoF_LoF', '!LoF_LoF');  "
                            class="w-full py-2 text-sm bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> LoF+LoF/Other </button> 
                        <button  v-if="selLoFLoF" 
                            @click="reset(); gatherStats()"
                            class="w-full py-2 text-sm bg-emerald-600 text-white rounded-full"> &uarr;&uarr; LoF+LoF &uarr;&uarr; | &darr;&darr; Other &darr;&darr; </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <template v-if="!selAll">
            <div class="my-0 flex flex-row w-full">
                <div class="chart-container w-full"><VuePlotly :data="bubbleDataSymptomsSel2" :layout="scatterLayout2" :config="plotConfig" :key="bubbleDataSymptomsSel2[0].x.length"></VuePlotly></div>
            </div>
        </template>
        <table class="text-xs text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" colspan="4" class="px-6 py-10 text-left">
                        TABLE OF SYMPTOMS
                    </th>
                </tr> 
                <tr>
                    <th scope="col" class="px-6 py-1 text-center">
                        SYMPTOM
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        REPORTEDNESS OVERALL
                    </th>
                    <th v-if="!selAll" scope="col" class="px-6 py-1 text-center">
                        REPORTEDNESS IN {{ sel[0] }}
                    </th>
                    <th v-if="!selAll" scope="col" class="px-6 py-1 text-center">
                        REPORTEDNESS IN {{ sel[1] }}
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        REPORTED PRESENT BY
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        REPORTED ABSENT BY
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        REPORTED PRESENT + ABSENT BY
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                v-for="(el, i) in countsAsReported" :key="i">
                    <td class="px-6 py-5 text-center">
                        {{ el.HPO_term }}
                    </td>
                    <td class="px-6 py-5 text-center">
                        {{ el.n_pct }}%
                    </td>
                    <td v-if="!selAll" class="px-6 py-5 text-center">
                        {{ findSel1Pct(el.HPO_code) }}%
                    </td>
                    <td v-if="!selAll" class="px-6 py-5 text-center">
                        {{ findSel2Pct(el.HPO_code) }}%
                    </td>
                    <td class="px-6 py-2 text-center w-15">
                        <a v-for="(doiel, j) in el.DOIs_present" :href="doiel" :key="j"> [{{ j+1 }}] </a>
                    </td>
                    <td class="px-6 py-2 text-center w-15">
                        <a v-for="(doiabsel, k) in el.DOIs_absent" :href="doiabsel" :key="k"> [{{ k+1 }}] </a>
                    </td>
                    <td class="px-6 py-2 text-center w-15">
                        <a v-for="(doibothsel, l) in el.DOIs_sometimes" :href="doibothsel" :key="l"> [{{ l+1 }}] </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
    
       
</template>
<script>

import mySymptomStats from '@/assets/hp_symptom_stats.json'
import myScatterLayout2 from '@/assets/scatterLayout2.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSymptomBubble",
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
                scatterLayout2: myScatterLayout2,
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                sexRatio: 0,
                sel: ["ALL", "ALL"],
                countsAsReported: [],
                countsAsReportedSel1: [],
                countsAsReportedSel2: [],
                branchLevel: this.propData.branchLevel,
                selGirlsBoys: false,
                selLoFLoF: false, selAll: true,
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
                bubbleDataSymptomsSel1: [
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
                bubbleDataSymptomsSel2: [
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
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            var pa_ratio = 5.
            //console.log("HERE 61")
            //var stats = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == this.propData.branchLevel)})
            var statsAsReported = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == 999 && item.selection == "All")})
            this.countsAsReported = statsAsReported[0].counts
            this.countsAsReportedSel = statsAsReported[0].counts
            this.girlNo = statsAsReported[0].girls;
            this.patientTotal = statsAsReported[0].patients;
            this.boyNo = this.patientTotal - this.girlNo;
            this.sexRatio = this.boyNo / this.girlNo
            this.sexRatio = Math.round((this.sexRatio * 100) * (1 + Number.EPSILON)) / 100
            //for (var i = 0; i < statsAsReported[0].counts.length; i++) {
            for (var i = 0; i < Math.min(25, statsAsReported[0].counts.length); i++) {                
                //Deal with instances where pres_abs_ratio = "-"
                if (isNaN(pa_ratio)){
                    pa_ratio = 5.
                }
                this.bubbleDataSymptoms[0].marker.size.push(Math.max(Number(statsAsReported[0].counts[i].n_pct), 10.));
                this.bubbleDataSymptoms[0].y.push(Number(statsAsReported[0].counts[i].n_pct_scaled) + Math.random() / 10  ); 
                //this.bubbleDataSymptoms[0].y.push(Number(statsAsReported[0].counts[i].n_pct_scaled)  ); 
                this.bubbleDataSymptoms[0].x.push(Number(statsAsReported[0].counts[i].category_n_scaled)); 
                this.bubbleDataSymptoms[0].text.push(String(statsAsReported[0].counts[i].HPO_term));
                this.bubbleDataSymptoms[0].marker.color.push(String(statsAsReported[0].counts[i].colour));
                this.bubbleDataSymptoms[0].marker.line.color.push(String(statsAsReported[0].counts[i].colour).substring(0,7));
                //console.log(this.bubbleDataSymptoms[0].text[i], this.bubbleDataSymptoms[0].x[i], this.bubbleDataSymptoms[0].y[i], this.bubbleDataSymptoms[0].marker.size[i])
            }
            //console.log(this.bubbleDataSymptoms[0])
        },
        fetchSelection(sel1, sel2) {
            var pa_ratio = 5.
            //console.log("HERE 61, selection, ", sel)
            var statsAsReported = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == 999 && item.selection == sel1)})
            this.countsAsReportedSel1 = statsAsReported[0].counts
            statsAsReported = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == 999 && item.selection == sel2)})
            this.countsAsReportedSel2 = statsAsReported[0].counts
            for (var i = 0; i < Math.min(25, this.countsAsReportedSel1.length); i++) {                
                if (isNaN(pa_ratio)){
                    pa_ratio = 5.
                }
                this.bubbleDataSymptomsSel1[0].marker.size.push(Math.max(Number(this.countsAsReportedSel1[i].n_pct), 10.));
                this.bubbleDataSymptomsSel1[0].y.push(Number(this.countsAsReportedSel1[i].n_pct_scaled) + Math.random() / 10  ); 
                //this.bubbleDataSymptomsSel1[0].y.push(Number(this.countsAsReportedSel1[i].n_pct_scaled) ); 
                this.bubbleDataSymptomsSel1[0].x.push(Number(this.countsAsReportedSel1[i].category_n_scaled)); 
                this.bubbleDataSymptomsSel1[0].text.push(String(this.countsAsReportedSel1[i].HPO_term));
                this.bubbleDataSymptomsSel1[0].marker.color.push(String(this.countsAsReportedSel1[i].colour));
                this.bubbleDataSymptomsSel1[0].marker.line.color.push(String(this.countsAsReportedSel1[i].colour).substring(0,7));
            }
            for (i = 0; i < Math.min(25, this.countsAsReportedSel2.length); i++) {                
                if (isNaN(pa_ratio)){
                    pa_ratio = 5.
                }
                this.bubbleDataSymptomsSel2[0].marker.size.push(Math.max(Number(this.countsAsReportedSel2[i].n_pct), 10.));
                this.bubbleDataSymptomsSel2[0].y.push(Number(this.countsAsReportedSel2[i].n_pct_scaled) + Math.random() / 10  ); 
                //this.bubbleDataSymptomsSel1[0].y.push(Number(this.countsAsReportedSel2[i].n_pct_scaled) ); 
                this.bubbleDataSymptomsSel2[0].x.push(Number(this.countsAsReportedSel2[i].category_n_scaled)); 
                this.bubbleDataSymptomsSel2[0].text.push(String(this.countsAsReportedSel2[i].HPO_term));
                this.bubbleDataSymptomsSel2[0].marker.color.push(String(this.countsAsReportedSel2[i].colour));
                this.bubbleDataSymptomsSel2[0].marker.line.color.push(String(this.countsAsReportedSel2[i].colour).substring(0,7));
            }
        },
        findSel1Pct(HPO_code){
            var selPct = 0.0
            var matchingItem = this.countsAsReportedSel1.filter((item) => (item.HPO_code == HPO_code))
            if (typeof matchingItem[0] != 'undefined') {
                selPct = matchingItem[0].n_pct
            } else {
                selPct = 0.0
            }
            return selPct
        },
        findSel2Pct(HPO_code){
            var selPct = 0.0
            var matchingItem = this.countsAsReportedSel2.filter((item) => (item.HPO_code == HPO_code))
            if (typeof matchingItem[0] != 'undefined') {
                selPct = matchingItem[0].n_pct
            } else {
                selPct = 0.0
            }
            return selPct
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