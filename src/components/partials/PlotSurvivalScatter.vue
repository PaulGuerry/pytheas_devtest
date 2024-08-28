<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1 text-left">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        BOYS / GIRLS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        DEATHS
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2 text-left">
                        {{ propData.gene }}
                    </td>
                    <td class="px-6 py-2 text-center"> 
                       {{ patientTotal }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ boyNo }} / {{ girlNo }} 
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ boysDead }} / {{ girlsDead }}
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/4"></div>
            <div class="chart-container w-1/2"><VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly></div>
            <div class="w-1/4"></div>
        </div>
        <div class="mt-0 mb-0 flex flex-row w-full">
            <p class="text-sm text-center w-full">Years of age </p>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import survLayout1 from '@/assets/survivalLayout1.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSurvivalScatter",
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
                girlsDead: 0,
                boysDead: 0,
                sexRatio: 0,
                branchLevel: this.propData.branchLevel,
                survLayout: survLayout1,
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
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.propData.gene)})
            this.patientTotal = stats_disease[0].age_at_last_news.all.array.length 
            this.girlNo = stats_disease[0].age_at_last_news.girls.array.length
            this.boyNo = stats_disease[0].age_at_last_news.boys.array.length
            this.girlsDead = stats_disease[0].age_at_last_news.girls.status.filter((val) => val == 1).length
            this.boysDead = stats_disease[0].age_at_last_news.boys.status.filter((val) => val == 1).length
            this.scatterSurvival[0].x = stats_disease[0].age_at_last_news.girls.surv_x
            this.scatterSurvival[0].y = stats_disease[0].age_at_last_news.girls.surv_y
            this.scatterSurvival[1].x = stats_disease[0].age_at_last_news.boys.surv_x
            this.scatterSurvival[1].y = stats_disease[0].age_at_last_news.boys.surv_y
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