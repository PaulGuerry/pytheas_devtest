<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5 "> 
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
                        <p>CONSANGUINOUS</p><p class="font-light lowercase">yes / no / n/a </p>
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        CONSANGUINITY RATE
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
                       {{ consanguinous.yes }} / {{ consanguinous.no }} / {{  consanguinous.missing }} 
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ consanguinous.rate }}%
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/3"></div>
            <div class="chart-container w-1/3">
                <VuePlotly :data="barConsanguinous" :layout="barLayout3" :config="plotConfig"></VuePlotly>
            </div>
            <div class="w-1/3"></div>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import myBarLayout3 from '@/assets/barLayout3.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotConsanguinityBar",
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
                barLayout3: myBarLayout3,
                patientTotal: 0,
                girlNo: 0,
                boyNo: 0,
                consanguinous: {yes: 0, no: 0, missing: 0, rate: 0},
                branchLevel: this.propData.branchLevel,
                barConsanguinous: [
                    {
                        "x": ["Yes", "No"],
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
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.propData.gene)})
            this.patientTotal = stats_disease[0].age_at_first_symp.all.array.length 
            this.consanguinous.yes = stats_disease[0].consanguinous.yes
            this.consanguinous.no = stats_disease[0].consanguinous.no
            this.consanguinous.missing = stats_disease[0].consanguinous.missing
            let x = stats_disease[0].consanguinous.yes / (this.consanguinous.no + this.consanguinous.yes) 
            x = Math.round((x * 100) * (1 + Number.EPSILON)) / 100 * 100
            this.consanguinous.rate = x
            this.barConsanguinous[0].y = [this.consanguinous.yes, this.consanguinous.no];
            this.barConsanguinous[0].text = [String(this.consanguinous.yes), String(this.consanguinous.no)];
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