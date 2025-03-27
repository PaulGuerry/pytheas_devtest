<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1 text-left">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        SELECTION
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
                <template v-for="(el, i) in scatterSurvival" :key="i">
                    <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td v-if="i==0" class="px-6 py-0.5 text-left">
                            {{ propData.gene }}
                        </td>
                        <td v-if="i>0" class="px-6 py-0.5 text-left">
                            
                        </td>
                        <td class="px-6 py-0.5 text-center"> 
                           {{ el.name }}
                        </td>
                        <td class="px-6 py-0.5 text-center"> 
                           {{ el.x.length }}
                        </td>
                        <td class="pr-44 pt-1 pb-0 text-right">
                            {{ el.median  }} ({{ el.iqr }}) months
                        </td>
                    </tr>
                </template>
                <tr class="text-xs">
                    <td></td>
                    <td></td>
                    <td></td>
                    <td class="text-right py-2 pr-32"><sup>*</sup>median (IQR)</td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="chart-container w-full"><VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly></div>
        </div>
        <div class="mt-0 mb-0 flex flex-row w-full">
            <p class="text-sm text-center w-full">Years of age </p>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import survLayout2 from '@/assets/survivalLayout2.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSurvivalScatter",
    components: {  VuePlotly },
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherStats("all");    
    },
    methods: {
        reset() {
            Object.assign(this.$data, this.initialState())
        },
        initialState() {
            return {
                diseaseArray: myDiseaseStats,
                patientTotal: 0,
                deadTotal: 0,
                branchLevel: this.propData.branchLevel,
                survLayout: survLayout2,
                selGirlsBoys: false, selVarTypes: false,
                selFirstSymp: false,
                scatterSurvival: [ 
                ],
                plotConfig:{displayModeBar: false, responsive: true}
            }
        },
        gatherStats() {
            for (var gene of this.propData.genes) {
                var stats_disease = this.diseaseArray.filter(item => item.gene == gene)
                let survival_el = {x:[], y:[], name: "", median: 0, iqr: 0, type: "scatter", mode: "lines", line: {width: 2, color: "", shape: "hv"}}
                let stats_sel = stats_disease[0].age_at_first_symp["all"]
                survival_el.x = stats_sel.surv_x.map(x => x / 12)
                survival_el.y = stats_sel.surv_y
                survival_el.name = stats_disease[0].name
                survival_el.median = Math.round(stats_sel.median * 10) / 10 
                survival_el.iqr = Math.round(stats_sel.iqr * 10) / 10 
                survival_el.color = stats_sel.colour
                this.scatterSurvival.push(survival_el)
            }
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