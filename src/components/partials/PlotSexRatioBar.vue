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
                        SEX RATIO
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
                       {{ sexRatio }}
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/3"></div>
            <div class="chart-container w-1/3"><VuePlotly :data="barDataSexRatio" :layout="barLayout3" :config="plotConfig"></VuePlotly></div>
            <div class="w-1/3"></div>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import myBarLayout3 from '@/assets/barLayout3.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSexRatioBar",
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
                sexRatio: 0,
                branchLevel: this.propData.branchLevel,
                barDataSexRatio: [
                    {
                        "x": ["Girls", "Boys"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "marker": {
                            "color": ["#bc3c2933", "#0072b533"],
                            "line": {
                                "color": ["#bc3c29", "#0072b5"],
                                "width": 1.5
                            }
                        }
                    }
                ],
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            console.log("gene, ", this.propData.gene)
            var stats = this.diseaseArray.filter((item) => {return (item.gene == this.propData.gene)})
            this.girlNo = stats[0].patients.girls;
            this.patientTotal = stats[0].patients.total;
            this.boyNo = stats[0].patients.boys;
            this.sexRatio = this.boyNo / this.girlNo
            this.sexRatio = Math.round((this.sexRatio * 100) * (1 + Number.EPSILON)) / 100
            this.barDataSexRatio[0].y = [this.girlNo, this.boyNo];
            this.barDataSexRatio[0].text = [String(this.girlNo), String(this.boyNo)];
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