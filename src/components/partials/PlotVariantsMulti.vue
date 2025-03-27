<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-2 md:col-span-3 lg:col-span-5"> 
        <div class="chart-container w-full mx-10 my-10"><VuePlotly :data="barDataZygTypes" :layout="barLayout4" :config="plotConfig"></VuePlotly></div>
        <div class="chart-container w-full mx-10 my-10"><VuePlotly :data="barDataVarTypes" :layout="barLayout4" :config="plotConfig"></VuePlotly></div>
        <template v-for="(el, i) of tableData" :key="i">
            <MyDiseaseStatTable :tableData="el"/>
        </template>
    </div>
</template>

<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'
import MyDiseaseStatTable from '@/components/partials/MyDiseaseStatTable.vue'
import myBarLayout4 from '@/assets/barLayout4.json'
import { VuePlotly } from 'vue3-plotly'

export default {
    name: "PlotVariantMulti",
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
                barLayout4: myBarLayout4,
                branchLevel: this.propData.branchLevel,
                barDataVarTypes_el: 
                    {
                        "x": ["LoF+LoF", "LoF+Mis", "Mis+Mis", "LoF+WT/Syn", "Mis+WT/Syn"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "name": "",
                        "marker": {
                            "color": [],
                            "line": {
                                "color": [],
                                "width": 1.5
                            }
                        }
                    },
                barDataVarTypes: [],
                barDataZygTypes_el: {
                        "x": ["Homozygous", "Compound", "Heterozygous"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "name": "",
                        "marker": {
                            "color": [],
                            "line": {
                                "color": [],
                                "width": 1.5
                            }
                        }
                },
                barDataZygTypes: [],
                plotConfig:{displayModeBar: false, responsive: true},
                tableData_el: {
                    gene: "", disease: "", 
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
                },
                tableData: []
            }
        },
        gatherStats() {
            //console.log("gene, ", this.propData.gene)
            for (let gene of this.propData.genes) {
                console.log("114", gene)
                var stats = []
                var tbDat_el = {
                    gene: "", disease: "", 
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
                var bDVT_el = {
                        "x": ["LoF+LoF", "LoF+Mis", "Mis+Mis", "LoF+WT/Syn", "Mis+WT/Syn"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "name": "",
                        "marker": {
                            "color": [],
                            "line": {
                                "color": [],
                                "width": 1.5
                            }
                        }
                    }
                var bDZT_el = {
                        "x": ["Homozygous", "Compound", "Heterozygous"],
                        "y": [],
                        "type": "bar",
                        "text": [],
                        "textposition": "auto",
                        "hoverinfo": "none",
                        "name": "",
                        "marker": {
                            "color": [],
                            "line": {
                                "color": [],
                                "width": 1.5
                            }
                        }
                }
                stats = this.diseaseArray.filter((item) => {return (item.gene == gene)}) 
                console.log("121", stats[0].name)
                if ('zygosity' in stats[0]) tbDat_el.zygosity = stats[0].zygosity;
                if ('protvartypes' in stats[0]) tbDat_el.protvartypes = stats[0].protvartypes;
                if ('patients' in stats[0]) tbDat_el.patients = stats[0].patients;
                tbDat_el.gene = stats[0].gene
                tbDat_el.disease = stats[0].name
                bDVT_el.y = [
					tbDat_el.protvartypes.LLpct, 
					tbDat_el.protvartypes.LMpct, 
					tbDat_el.protvartypes.MMpct, 
					tbDat_el.protvartypes.LHpct, 
					tbDat_el.protvartypes.MHpct];
                bDVT_el.text = [
					String(tbDat_el.protvartypes.LLpct + '%'), 
					String(tbDat_el.protvartypes.LMpct+ '%'), 
					String(tbDat_el.protvartypes.MMpct+ '%'), 
					String(tbDat_el.protvartypes.LHpct + '%'), 
					String(tbDat_el.protvartypes.MHpct + '%')];
                bDVT_el.name = stats[0].name
                bDVT_el.marker.color = stats[0].colour + "55"
                bDVT_el.marker.line.color = stats[0].colour
                bDZT_el.y = [
					tbDat_el.zygosity.hompct, 
					tbDat_el.zygosity.compct, 
					tbDat_el.zygosity.hetpct];
                bDZT_el.text = [
					String(tbDat_el.zygosity.hompct + '%'), 
					String(tbDat_el.zygosity.compct + '%'), 
					String(tbDat_el.zygosity.hetpct + '%')];
                bDZT_el.marker.color = stats[0].colour + "55"
                bDZT_el.marker.line.color = stats[0].colour
                bDZT_el.name = stats[0].name
                console.log("151", bDZT_el.marker.color, bDZT_el.marker.line.color, bDZT_el.name)


                this.tableData.push(tbDat_el)
                this.barDataVarTypes.push(bDVT_el)
                this.barDataZygTypes.push(bDZT_el)

            }

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
    }
}
</script>

<style lang="">
    
</style>
