<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
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
                        DEATHS
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
                        <td class="px-6 py-0.5 text-center"> 
                           {{ el.deaths }}
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="chart-container w-full"><VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly></div>
        </div>
        <div class="mt-0 mb-0 flex flex-row w-full">
            <p class="text-sm text-center w-full">Years of age </p>
        </div>
        <div class="w-full grid grid-cols-4 gap-10 mt-10 mb-20 place-items-center"> 
            <button  class="w-full py-2 text-sm invisible"> Invisible </button>
            <button  v-if="!selGirlsBoys" @click="reset(); gatherStats('girls', 'boys'); selGirlsBoys = true;"
                class="w-full py-2 text-sm bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> 
                Girls/Boys 
            </button> 
            <button  v-if="selGirlsBoys" @click="reset(); gatherStats('all')" 
                class="w-full py-2 text-sm bg-emerald-600 text-white rounded-full"> 
                Girls/Boys 
            </button>
            <button  v-if="!selVarTypes" @click="reset(); gatherStats('LoF_LoF', 'LoF_Mis', 'Mis_Mis', 'LoF_Het', 'Mis_Het'); selVarTypes = true;"
                class="w-full py-2 text-sm bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> 
                Variant types 
            </button> 
            <button  v-if="selVarTypes" @click="reset(); gatherStats('all')" 
                class="w-full py-2 text-sm bg-emerald-600 text-white rounded-full"> 
                Variant types
            </button>
            <button  class="w-full py-2 text-sm invisible"> Invisible </button>
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
                survLayout: survLayout1,
                selGirlsBoys: false, selVarTypes: false,
                selFirstSymp: false,
                colors: [
                    "#374E55FF", "#DF8F44FF", "#00A1D5FF", "#FF4745FF", "#79AF97FF", "#6A6599FF", "#80796BFF"
                ],
                scatterSurvival: [ 
                ],
                plotConfig:{displayModeBar: false, responsive: true}
            }
        },
        gatherStats(...Args) {
            var stats_disease = this.diseaseArray.filter(item => item.gene == this.propData.gene)
            this.patientTotal = stats_disease[0].survival.all.status.length
            this.deadTotal = stats_disease[0].survival.all.status.filter(item => item == 1).length
            let i = 0
            for (var sel of Args) {
                let survival_el = {x:[], y:[], name: "", deaths: 0, type: "scatter", mode: "lines", line: {width: 2, color: this.colors[i], shape: "hv"}}
                let stats_sel = stats_disease[0].survival[sel]
                survival_el.x = stats_sel.surv_x
                survival_el.y = stats_sel.surv_y
                survival_el.name = stats_sel.name
                survival_el.deaths = stats_sel.status.filter(item => item == 1).length
                this.scatterSurvival.push(survival_el)
                i++
            }
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