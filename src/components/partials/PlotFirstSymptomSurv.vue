<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-1 py-1 text-left">
                        GENE
                    </th>
                    <th scope="col" class="px-1 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-1 py-1 text-center">
                        AGE AT FIRST SYMPTOMS<sup>*</sup> 
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 rounded-full">
                    <td class="px-1 pt-1 pb-0 text-left">
                        {{ propData.gene }}
                    </td>
                    <td class="px-1 pt-1 pb-0 text-center"> 
                       {{ patientTotal }}
                    </td>
                    <td class="px-1 pt-1 pb-0 text-center">
                       <p>{{ stats.all.median  }} ({{ stats.all.iqr }}) months</p>
                    </td>
                </tr>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-1 py-0 text-left">
                    </td>
                    <td scope="row" class="px-1 pr-1 py-0 text-center"> 
                       Girls ({{ girlNo }})
                    </td>
                    <td class="px-1 py-0 text-center">
                       <p>{{ stats.girls.median  }} ({{ stats.girls.iqr }}) months</p>
                    </td>
                </tr>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-1 py-0 text-left">
                    </td>
                    <td scope="row" class="px-1 pr-1 py-0 text-center"> 
                       Boys ({{ boyNo }})
                    </td>
                    <td class="px-1 py-0 text-center">
                       <p>{{ stats.boys.median  }} ({{ stats.boys.iqr }}) months</p>
                    </td>
                </tr>
                <tr class="text-xs">
                    <td></td>
                    <td></td>
                    <td class="text-center py-2"><sup>*</sup>median (IQR)</td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/6"></div>
            <div class="chart-container w-full"><VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly></div>
            <div class="w-1/6"></div>
        </div>
        <div class="mt-0 mb-0 flex flex-row w-full">
            <p class="text-sm text-center w-full">Months of age </p>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import survLayout1 from '@/assets/survivalLayout2.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotFirstSymptomSurv",
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
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                sexRatio: 0,
                branchLevel: this.propData.branchLevel,
                survLayout: survLayout1,
                stats: {
                    all: {median: 0, iqr: 0},
                    girls: {median: 0, iqr: 0},
                    boys: {median: 0, iqr: 0}
                },
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
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            console.log("gene, ", this.propData.gene)
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.propData.gene)})
            console.log("stats_disease[0]", stats_disease[0])
            console.log("stats_disease[0].age_at_first_symp", stats_disease[0].age_at_first_symp)
            this.patientTotal = stats_disease[0].age_at_first_symp.all.array.length 
            console.log("patientTotal", this.patientTotal)
            this.boyNo = stats_disease[0].age_at_first_symp.boys.array.length 
            console.log("boyNo", this.boyNo)
            this.girlNo = stats_disease[0].age_at_first_symp.girls.array.length 
            this.stats.all.median = stats_disease[0].age_at_first_symp.all.median
            this.stats.all.median = Math.round((this.stats.all.median * 1) * (1 + Number.EPSILON)) / 1
            this.stats.all.iqr = stats_disease[0].age_at_first_symp.all.iqr
            this.stats.all.iqr = Math.round((this.stats.all.iqr * 1) * (1 + Number.EPSILON)) / 1
            this.stats.boys.median = stats_disease[0].age_at_first_symp.boys.median
            this.stats.boys.median = Math.round((this.stats.boys.median * 1) * (1 + Number.EPSILON)) / 1
            this.stats.boys.iqr = stats_disease[0].age_at_first_symp.boys.iqr
            this.stats.boys.iqr = Math.round((this.stats.boys.iqr * 1) * (1 + Number.EPSILON)) / 1
            this.stats.girls.median = stats_disease[0].age_at_first_symp.girls.median
            this.stats.girls.median = Math.round((this.stats.girls.median * 1) * (1 + Number.EPSILON)) / 1
            this.stats.girls.iqr = stats_disease[0].age_at_first_symp.girls.iqr
            this.stats.girls.iqr = Math.round((this.stats.girls.iqr * 1) * (1 + Number.EPSILON)) / 1
            this.scatterSurvival[0].x = stats_disease[0].age_at_first_symp.girls.surv_x
            this.scatterSurvival[0].y = stats_disease[0].age_at_first_symp.girls.surv_y
            this.scatterSurvival[1].x = stats_disease[0].age_at_first_symp.boys.surv_x
            this.scatterSurvival[1].y = stats_disease[0].age_at_first_symp.boys.surv_y
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