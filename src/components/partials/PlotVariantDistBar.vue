<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-3"> 
        <MyDiseaseStatTable :tableData="tableData" :key="tableData.patients.total + tableData.patients.boys"/>
        <div class="mt-10 mb-0 flex flex-row w-full">
            <div class="chart-container w-1/2 mx-10"><VuePlotly :data="barDataZygTypes" :layout="barLayout3" :config="plotConfig"></VuePlotly></div>
            <div class="chart-container w-1/2 mx-10"><VuePlotly :data="barDataVarTypes" :layout="barLayout3" :config="plotConfig"></VuePlotly></div>
        </div>
        <table class="text-xs text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" colspan="8" class="px-6 py-10 text-left">
                        REPORTED VARIANTS
                    </th>
                </tr> 
                <tr>
                    <th scope="col" class="px-6 py-1 text-center">
                        mRNA OR GENOMIC VARIANT
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PROTEIN VARIANT
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        TYPE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PREFIX
                    </th>
                    <th scope="col"  class="px-6 py-1 text-center">
                        REPORTED IN
                    </th>
                </tr>
            </thead>
            <tbody>
                <template v-for="(el, i) in variants" :key="i">
                    <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                        <td class="px-6 py-1 text-center">
                            {{ el.cvariant }}
                        </td>
                        <td class="px-6 py-1 text-center">
                            {{ el.pvariant }}
                        </td>
                        <td class="px-6 py-1 text-center">
                            {{ el.type }}
                        </td>
                        <td class="px-6 py-1 text-center">
                            {{ el.prefix }}
                        </td>
                        <td class="px-6 py-1 text-center w-flex">
                            <a v-for="(doiel, j) in el.DOIs" :href="doiel" :key="j"> [{{ j+1 }}] </a>
                        </td>
                    </tr>
                </template>
            </tbody>
        </table>
    </div>
</template>

<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import MyDiseaseStatTable from '@/components/partials/MyDiseaseStatTable.vue'
import myBarLayout3 from '@/assets/barLayout3.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotVariantDistBar",
    components: {  VuePlotly, MyDiseaseStatTable },
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
                branchLevel: this.propData.branchLevel,
                variants: [],
                variantsEven: [],
                variantsOdd: [],
                barDataVarTypes: [
                    {
                        "x": ["LoF+LoF", "LoF+Mis", "Mis+Mis", "LoF+WT/Syn", "Mis+WT/Syn"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "marker": {
                            "color": ["#bc3c2933", "#0072b533", "#e1872733", "#20854e33", "#7876b133"],
                            "line": {
                                "color": ["#bc3c29", "#0072b5", "#e18727", "#20854e", "#7876b1"],
                                "width": 1.5
                            }
                        }
                    }
                ],
		barDataZygTypes: [
                    {
                        "x": ["Homozygous", "Compound", "Heterozygous"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "marker": {
                            "color": ["#374e5533", "#dfef4433", "#00a1d533"],
                            "line": {
                                "color": ["#374e55", "#dfef44", "#00a1d5"],
                                "width": 1.5
                            }
                        }
                    }
                ],
                plotConfig:{displayModeBar: false},
                tableData: {
                    gene: this.propData.gene, disease: this.propData.disease, 
                    articleCount: 0, 
                    varCount: 0, dataptCount: 0, 
                    completeness: 0.001, 
                    patients: {
                        total: 0,
                        girls: 0,
                        boys: 0
                    },
                    zygosity: {
                        homo: 0,
                        hompct: 0.0,
                        compound: 0.0,
                        compct: 0.0,
                        hetero: 0,
                        hetpct: 0.0,
                        unknown: 0
                    },
                    protvartypes: {
                        LoF_LoF: 0,
                        LLpct: 0.,
                        LoF_Mis: 0,
                        LMpct: 0.,
                        Mis_Mis: 0,
                        MMpct: 0.,
                        LoF_Het: 0,
                        LHpct: 0.,
                        Mis_Het: 0,
                        MHpct: 0.,
                        Unkown: 0
                    }

                }
            }
        },
        gatherStats() {
            //console.log("gene, ", this.propData.gene)
            var stats = this.diseaseArray.filter((item) => {return (item.gene == this.tableData.gene)})
            if ('zygosity' in stats[0]) this.tableData.zygosity = stats[0].zygosity;
            if ('protvartypes' in stats[0]) this.tableData.protvartypes = stats[0].protvartypes;
            if ('patients' in stats[0]) this.tableData.patients = stats[0].patients;
            if ('variants' in stats[0]) this.variants = stats[0].variants;
            this.variantsEven = this.variants.filter((el, i) => {return (i % 2 === 0)})
            this.variantsOdd = this.variants.filter((el, i) => {return (i % 2 !== 0)})
            this.barDataVarTypes[0].y = [
					this.tableData.protvartypes.LoF_LoF, 
					this.tableData.protvartypes.LoF_Mis, 
					this.tableData.protvartypes.Mis_Mis, 
					this.tableData.protvartypes.LoF_Het, 
					this.tableData.protvartypes.Mis_Het];
            this.barDataVarTypes[0].text = [
					String(this.tableData.protvartypes.LLpct + '%'), 
					String(this.tableData.protvartypes.LMpct+ '%'), 
					String(this.tableData.protvartypes.MMpct+ '%'), 
					String(this.tableData.protvartypes.LHpct + '%'), 
					String(this.tableData.protvartypes.MHpct + '%')];
            this.barDataZygTypes[0].y = [
					this.tableData.zygosity.homo, 
					this.tableData.zygosity.compound, 
					this.tableData.zygosity.hetero];
            this.barDataZygTypes[0].text = [
					String(this.tableData.zygosity.hompct + '%'), 
					String(this.tableData.zygosity.compct + '%'), 
					String(this.tableData.zygosity.hetpct + '%')];
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
