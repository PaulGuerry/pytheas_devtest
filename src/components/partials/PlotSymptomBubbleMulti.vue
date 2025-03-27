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
                <template v-for="(el, i) of tableStats" :key="i">
                    <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td class="px-6 py-2 text-left">
                            {{ el.gene }}
                        </td>
                        <td class="px-6 py-2 text-center"> 
                           {{ el.patientTotal }}
                        </td>
                        <td class="px-6 py-2 text-center">
                           {{ el.boyNo }} / {{ el.girlNo }} ({{ el.sexRatio }})
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
        <template v-for="(el, i) of bubbleDataSymptoms" :key="i">
            <div class="chart-container w-full my-0"><VuePlotly :data="el" :layout="scatterLayout2" :config="plotConfig" :key="el[0].y.length"></VuePlotly></div>
            <div class="my-0 flex flex-row w-full justify-center">
                <p class="text-sm text-center py-2 font-bold text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full mt-5 ">{{ el.disease }}</p>
            </div>
        </template>
    </div>
</template>
<script>

import mySymptomStats from '@/assets/hp_symptom_stats.json'
import myScatterLayout2 from '@/assets/scatterLayout2.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotSymptomBubbleMulti",
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
                branchLevel: this.propData.branchLevel,
                selGirlsBoys: false,
                selLoFLoF: false, selAll: true, selAges: false,
                bubbleDataSymptoms: [],
                tableStats: [],
                plotConfig:{displayModeBar: false}
            }
        },
        gatherStats() {
            for (let gene of this.propData.genes) {
                var pa_ratio = 5.
                var plot_el = [{
                                "x": [],
                                "y": [],
                                "text": [],
                                "mode": "markers+text",
                                "textposition": "center",
                                "type": "scatter",
                                "hoverinfo": "text",
                                "disease": "",
                                "marker": {
                                   "color": [],
                                   "size": [],
                                   "line": {
                                     "color": [],
                                     "width": 1.5
                                   }
                                }
                            }]
                var tb_el = {gene: "", disease: "", girlNo: 0, boyNo: 0, patientTotal: 0, sexRatio: 0}
                //var stats = this.symptomArray.filter((item) => {return (item.gene == this.propData.gene && item.analysis_level == this.propData.branchLevel)})
                var statsAsReported = this.symptomArray.filter((item) => {return (item.gene == gene && item.analysis_level == 999 && item.selection == "All")})
                tb_el.gene = gene
                tb_el.disease = statsAsReported[0].disease
                plot_el.disease = statsAsReported[0].disease
                tb_el.girlNo = statsAsReported[0].girls;
                tb_el.patientTotal = statsAsReported[0].patients;
                tb_el.boyNo = tb_el.patientTotal - tb_el.girlNo;
                tb_el.sexRatio = tb_el.boyNo / tb_el.girlNo
                tb_el.sexRatio = Math.round((tb_el.sexRatio * 100) * (1 + Number.EPSILON)) / 100
                for (var i = 0; i < Math.min(25, statsAsReported[0].counts.length); i++) {                
                    //Deal with instances where pres_abs_ratio = "-"
                    if (isNaN(pa_ratio)){
                        pa_ratio = 5.
                    }
                    plot_el[0].marker.size.push(Math.max(Number(statsAsReported[0].counts[i].n_pct), 10.));
                    plot_el[0].y.push(Number(statsAsReported[0].counts[i].n_pct_scaled) + Math.random() / 10  ); 
                    //plot_el[0].y.push(Number(statsAsReported[0].counts[i].n_pct_scaled)  ); 
                    plot_el[0].x.push(Number(statsAsReported[0].counts[i].category_n_scaled)); 
                    plot_el[0].text.push(String(statsAsReported[0].counts[i].HPO_term));
                    plot_el[0].marker.color.push(String(statsAsReported[0].counts[i].colour));
                    plot_el[0].marker.line.color.push(String(statsAsReported[0].counts[i].colour).substring(0,7));

                }
                this.tableStats.push(tb_el)
                this.bubbleDataSymptoms.push(plot_el)
            }
        },
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
