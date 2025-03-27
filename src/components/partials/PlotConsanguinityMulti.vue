<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
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
                        <p>CONSANGUINOUS</p><p class="font-light lowercase">yes / no / n/a </p>
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        CONSANGUINITY RATE
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                v-for="(el, i) in tableStats" :key="i">
                    <td class="px-6 py-0 text-left">
                        {{ el.name }}
                    </td>
                    <td class="px-6 py-0 text-left">
                        {{ el.gene }}
                    </td>
                    <td class="px-6 py-0 text-center"> 
                       {{ el.patientTotal }}
                    </td>
                    <td class="px-6 py-0 text-center">
                       {{ el.yes }} / {{ el.no }} / {{  el.missing }} 
                    </td>
                    <td class="px-6 py-0 text-center">
                       {{ el.rate }}%
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="w-1/6"></div>
            <div class="chart-container w-2/3">
                <VuePlotly :data="barConsanguinous" :layout="barLayout3" :config="plotConfig"></VuePlotly>
            </div>
            <div class="w-1/6"></div>
        </div>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import myBarLayout3 from '@/assets/barLayout3.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotConsanguinityMulti",
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
                tableStats: [],
                branchLevel: this.propData.branchLevel,
                barConsanguinous: [
                    {
                        "x": [],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
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
                plotConfig:{displayModeBar: false, responsive: true}
            }
        },
        gatherStats() {
            var stats_disease = []
            var stats_el = {name: "", gene: "", patientTotal: 0, yes: 0, no: 0, missing: 0, rate: 0}
            for (let gene of this.propData.genes) {
                stats_disease = this.diseaseArray.filter((item) => {return (item.gene == gene)})
                stats_el = {name: "", gene: "", patientTotal: 0, yes: 0, no: 0, missing: 0, rate: 0}
                stats_el.name = stats_disease[0].name
                stats_el.gene = stats_disease[0].gene
                stats_el.patientTotal = stats_disease[0].patients.total 
                stats_el.yes = stats_disease[0].consanguinous.yes
                stats_el.no = stats_disease[0].consanguinous.no
                stats_el.missing = stats_disease[0].consanguinous.missing
                let x = stats_el.yes / (stats_el.no + stats_el.yes) 
                stats_el.rate = Math.round((x * 100) * (1 + Number.EPSILON)) / 100 * 100
                this.barConsanguinous[0].y.push(stats_el.rate);
                this.barConsanguinous[0].x.push(stats_el.name);
                this.barConsanguinous[0].text.push(stats_el.rate + "%");
                this.barConsanguinous[0].marker.color.push(stats_disease[0].colour + "33")
                this.barConsanguinous[0].marker.line.color.push(stats_disease[0].colour)
                this.tableStats.push(stats_el)
            }
            
            var arrays_to_sort = {
                quant: this.barConsanguinous[0].y,
                categ_1: this.barConsanguinous[0].x,
                categ_2: this.barConsanguinous[0].marker.color,
                categ_3: this.barConsanguinous[0].marker.line.color,
                categ_4: this.barConsanguinous[0].text
            }
            this.sortArrays(arrays_to_sort)
            
            this.tableStats.sort((p1, p2) => (p1.rate < p2.rate) ? 1 : (p1.rate > p2.rate) ? -1 : 0)

        },
        sortArrays(arrays) {
            if (typeof arrays.categ_2 === 'undefined') { arrays.categ_2 = []; }
            if (typeof arrays.categ_3 === 'undefined') { arrays.categ_3 = []; }
            if (typeof arrays.categ_4 === 'undefined') { arrays.categ_4 = []; }
        
            //1. transfer value pairs to a sorting array
            var sorting_array = []
            for (var i = 0; i < arrays.quant.length; i++) {
              sorting_array.push([arrays.quant[i], arrays.categ_1[i], arrays.categ_2[i], arrays.categ_3[i], arrays.categ_4[i]])
            }
            //2. sort the sorting array using the sortable column
            sorting_array.sort((a, b) => b[0] - a[0])
            //3. transfer the sorted pairs back to the original arrays
            for (i = 0; i < arrays.quant.length; i++) {
              arrays.quant[i] = sorting_array[i][0];
              arrays.categ_1[i] = sorting_array[i][1]
              arrays.categ_2[i] = sorting_array[i][2];
              arrays.categ_3[i] = sorting_array[i][3];
              arrays.categ_4[i] = sorting_array[i][4];
            } 

            return { arrays }
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