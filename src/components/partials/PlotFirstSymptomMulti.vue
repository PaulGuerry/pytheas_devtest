<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1 text-left">
                        DISEASE
                    </th>
                    <th scope="col" class="px-6 py-1 text-left">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        AGE AT FIRST SYMPTOMS<sup>*</sup> 
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                v-for="(el, i) in tableStats" :key="i">
                    <td class="px-6 py-0 text-left">
                        {{ el.name }}
                    </td>
                    <td class="px-6 py-0 text-left italic">
                        {{ el.gene }}
                    </td>
                    <td class="px-6 py-0 text-center"> 
                       {{ el.patientTotal }}
                    </td>
                    <td class="px-6 py-0 text-center">
                      <p>{{ el.median  }} ({{ el.iqr }}) months</p> 
                    </td>
                </tr>
                <tr class="text-xs">
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-center py-2"><sup>*</sup>median (IQR)</td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/6"></div>
            <div class="chart-container w-2/3"><VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly></div>
            <div class="w-1/6"></div>
        </div>
        <div class="mt-0 mb-0 flex flex-row w-full">
            <p class="text-sm text-center w-full">Months of age </p>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import survLayout2 from '@/assets/survivalLayout2.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotFirstSymptomMulti",
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
                diseaseArray: myDiseaseStats,
                survLayout: survLayout2,
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                branchLevel: this.propData.branchLevel,
                tableStats: [],
                boxAgeAtFirstSymp: [],
                scatterSurvival: [],
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            var stats_disease = []
            //var box_el = {y: [], type: "box", name: "", mode:"lines", line: {width: 2, color: "", shape: "hv"}}
            var stats_el = {name: "", gene: "", patientTotal: 0, median: 0, iqr: 0}
            var medians = []
            var iqrs = []
            var survival_el = {x:[], y: {}, name: "", type: "scatter", mode:"lines", line: {width: 2, color: "", shape: "hv"}}
            for (var gene of this.propData.genes) {
                stats_disease = this.diseaseArray.filter((item) => {return (item.gene == gene)})
                //box_el = {y: {}, type: "box", name: "", mode:"lines", line: {width: 2, color: "", shape: "hv"}}
                stats_el = {name: "", gene: "", patientTotal: 0, median: 0, iqr: 0}
                survival_el = {x:[], y: {}, name: "", type: "scatter", mode:"lines", line: {width: 2, color: "", shape: "hv"}}
                //box_el.y = stats_disease[0].age_at_first_symp.all.array;
                //box_el.line.color = stats_disease[0].colour
                //box_el.name = stats_disease[0].name
                stats_el.name = stats_disease[0].name
                stats_el.gene = stats_disease[0].gene
                stats_el.patientTotal = stats_disease[0].age_at_first_symp.all.array.length 
                stats_el.median = stats_disease[0].age_at_first_symp.all.median
                medians.push(stats_el.median)
                stats_el.median = Math.round((stats_el.median * 1) * (1 + Number.EPSILON)) / 1
                stats_el.iqr = stats_disease[0].age_at_first_symp.all.iqr
                iqrs.push(stats_el.iqr)
                stats_el.iqr = Math.round((stats_el.iqr * 1) * (1 + Number.EPSILON)) / 1
                survival_el.x = stats_disease[0].age_at_first_symp.all.surv_x
                survival_el.y = stats_disease[0].age_at_first_symp.all.surv_y
                survival_el.line.color = stats_disease[0].colour
                survival_el.name = stats_disease[0].name
                //this.boxAgeAtFirstSymp.push(box_el)
                this.tableStats.push(stats_el)
                console.log(survival_el)
                this.scatterSurvival.push(survival_el)
            }
            //this.boxLayout_alt.yaxis.range[1] = Math.max(...medians) + 2.6 * Math.max(...iqrs)
            //this.boxLayout_alt.yaxis.autorange = false
        }
    },
    props: {
        propData: {
            type: Object,
            required: true,
            default: () => ({genes: []})
        }
    },

}
</script>

<style lang="">
    
</style>