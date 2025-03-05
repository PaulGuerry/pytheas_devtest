<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 mt-10 mb-2"> Select the diseases to compare. </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
                <button  v-if="!selPFIC1"  
                    @click="selPFIC1 = true; tableData.genes.push('ATP8B1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 1 </button> 
                <button  v-if="selPFIC1" 
                    @click="selPFIC1 = false; removeGene('ATP8B1')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC1 </button>
                <button  v-if="!selPFIC2"  
                    @click="selPFIC2 = true; tableData.genes.push('ABCB11')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 2 </button> 
                <button  v-if="selPFIC2" 
                    @click="selPFIC2 = false; removeGene('ABCB11')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC2 </button> 
                <button  v-if="!selPFIC3"  
                    @click="selPFIC3 = true; tableData.genes.push('ABCB4')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 3 </button> 
                <button  v-if="selPFIC3" 
                    @click="selPFIC3 = false; removeGene('ABCB4')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC3 </button> 
                <button  v-if="!selPFIC4"  
                    @click="selPFIC4 = true; tableData.genes.push('TJP2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 4 </button> 
                <button  v-if="selPFIC4" 
                    @click="selPFIC4 = false; removeGene('TJP2')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC4 </button> 
                <button  v-if="!selPFIC5"  
                    @click="selPFIC5 = true; tableData.genes.push('NR1H4')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 5 </button> 
                <button  v-if="selPFIC5" 
                    @click="selPFIC5 = false; removeGene('NR1H4')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC5 </button>
                <button  v-if="!selPFIC6"  
                    @click="selPFIC6 = true; tableData.genes.push('SLC51A')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 6 </button> 
                <button  v-if="selPFIC6" 
                    @click="selPFIC6 = false; removeGene('SLC51A')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC6 </button>
                <button  v-if="!selPFIC7"  
                    @click="selPFIC7 = true; tableData.genes.push('USP53')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 7 </button> 
                <button  v-if="selPFIC7" 
                    @click="selPFIC7 = false; removeGene('USP53')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC7 </button>
                <button  v-if="!selPFIC8"  
                    @click="selPFIC8 = true; tableData.genes.push('KIF12')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 8 </button> 
                <button  v-if="selPFIC8" 
                    @click="selPFIC8 = false; removeGene('KIF12')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC8 </button>
                <button  v-if="!selPFIC9"  
                    @click="selPFIC9 = true; tableData.genes.push('ZFYVE19')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 9 </button> 
                <button  v-if="selPFIC9" 
                    @click="selPFIC9 = false; removeGene('ZFYVE19')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC9 </button>
                <button  v-if="!selPFIC10"  
                    @click="selPFIC10 = true; tableData.genes.push('MYO5B')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 10 </button> 
                <button  v-if="selPFIC10" 
                    @click="selPFIC10 = false; removeGene('MYO5B')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC10 </button>
                <button  v-if="!selPFIC11"  
                    @click="selPFIC11 = true; tableData.genes.push('SEMA7A')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> PFIC 11 </button> 
                <button  v-if="selPFIC11" 
                    @click="selPFIC11 = false; removeGene('SEMA7A')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> PFIC11 </button>

                <button  v-if="!selCDG2P"  
                    @click="selCDG2P = true; tableData.genes.push('TMEM199')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> CDG2P </button> 
                <button  v-if="selCDG2P" 
                    @click="selCDG2P = false; removeGene('TMEM199')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> CDG2P </button>

                <button  v-if="!selTHES1"  
                    @click="selTHES1 = true; tableData.genes.push('SKIC3')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> THES1 </button> 
                <button  v-if="selTHES1" 
                    @click="selTHES1 = false; removeGene('SKIC3')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> THES1 </button>

                <button  v-if="!selTHES2"  
                    @click="selTHES2 = true; tableData.genes.push('SKIC2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> THES2 </button> 
                <button  v-if="selTHES2" 
                    @click="selTHES2 = false; removeGene('SKIC2')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> THES2 </button>
                
                <button  v-if="!selTHESall"  
                    @click="selTHESall = true; tableData.genes.push('SKIC3,SKIC2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> THES </button> 
                <button  v-if="selTHESall" 
                    @click="selTHESall = false; removeGene('SKIC3,SKIC2')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> THES </button>
               
                <button  v-if="!selFOCADS"  
                    @click="selFOCADS = true; tableData.genes.push('FOCAD')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> FOCAD deficiency </button> 
                <button  v-if="selFOCADS" 
                    @click="selFOCADS = false; removeGene('FOCAD')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> FOCAD deficiency </button>
 
                <button  v-if="!selARCS1"  
                    @click="selARCS1 = true; tableData.genes.push('VPS33B')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> ARCS1 </button> 
                <button  v-if="selARCS1" 
                    @click="selARCS1 = false; removeGene('VPS33B')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> ARCS1 </button>

                <button  v-if="!selARCS2"  
                    @click="selARCS2 = true; tableData.genes.push('VIPAS39')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> ARCS2 </button> 
                <button  v-if="selARCS2" 
                    @click="selARCS2 = false; removeGene('VIPAS39')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> ARCS2 </button>
                
                <button  v-if="!selARCS"  
                    @click="selARCS = true; tableData.genes.push('VPS33B,VIPAS39')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> ARCS </button> 
                <button  v-if="selARCS" 
                    @click="selARCS = false; removeGene('VPS33B,VIPAS39')"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> ARCS </button>


                <button  v-if="!selAll"  
                    @click="selAll = true; addAll();"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> ALL </button> 
                <button  v-if="selAll" 
                    @click="selAll = false;  tableData.genes = []"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> ALL </button>
        </div>
    </div>

    <div class="w-full grid grid-cols-1 place-items-center mx-auto">
        <p  class="text-xl  text-gray-400 mt-10 mb-2"> Select the variable to compare these diseases with. </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button v-if="!isSexRatio"
                    @click="isSexRatio = true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> Sex ratio 
            </button> 
            <button v-if="isSexRatio"
                    @click="isSexRatio = false"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> Age at first symptoms 
            </button>
            <template v-if="isSexRatio">
                <PlotSexRatioMulti :propData="tableData"  :key="tableData.genes.length" />
            </template>
            <button v-if="!isFirstSymptoms"
                    @click="isFirstSymptoms = true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> Age at first symptoms
            </button>
            <button v-if="isFirstSymptoms"
                    @click="isFirstSymptoms = false"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> Age at first symptoms 
            </button> 
            <template v-if="isFirstSymptoms">
                <PlotFirstSymptomMulti :propData="tableData"  :key="tableData.genes.length" />
            </template>
            <button v-if="!isSurvival"
                    @click="isSurvival = true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> Survival
            </button> 
            <button v-if="isSurvival"
                    @click="isSurvival = false"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> Survival
            </button>
            <template v-if="isSurvival">
                <PlotSurvivalMulti :propData="tableData"  :key="tableData.genes.length" />
            </template>
            <button v-if="!isConsanguinity"
                    @click="isConsanguinity = true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-green-100 text-blue-400 rounded-full"> Consanguinity
            </button> 
            <button v-if="isConsanguinity"
                    @click="isConsanguinity = false"
                    class="w-full py-4 text-xl bg-emerald-600 text-white rounded-full"> Consanguinity
            </button>
            <template v-if="isConsanguinity">
                <PlotConsanguinityMulti :propData="tableData"  :key="tableData.genes.length" />
            </template>
        </div>
    </div>
</template>


<script>
import PlotSexRatioMulti from '@/components/partials/PlotSexRatioMulti.vue';
import PlotFirstSymptomMulti from '@/components/partials/PlotFirstSymptomMulti.vue';
import PlotSurvivalMulti from '@/components/partials/PlotSurvivalScatterMulti.vue';
import PlotConsanguinityMulti from '@/components/partials/PlotConsanguinityMulti.vue';


export default {
    name: "CompareView",
    components: {
        PlotSexRatioMulti, PlotFirstSymptomMulti, PlotSurvivalMulti,
        PlotConsanguinityMulti
    },
    data() {
      return this.initialState()
    },
    mounted() { 
    },
    methods: {
        initialState() {
            return {
                geneList: ["KIF12", "ZFYVE19", "ATP8B1", "SKIC3", "SKIC2", 
                          "ABCB11", "ABCB4", "TJP2", "NR1H4", "SLC51A", 
                          "USP53", "MYO5B", "SEMA7A", "TMEM199", "SKIC2,3,?", 
                          "FOCAD", "VPS33B", "VIPAS39", "VPSVIPAS?"],
                selPFIC1: false, selPFIC2: false, selPFIC3: false, selPFIC4: false, selPFIC5: false,
                selPFIC6: false, selPFIC7: false, selPFIC8: false, selPFIC9: false, selPFIC10: false,
                selPFIC11: false, selCDG2P: false, selTHES1: false, selTHES2: false, 
                selARCS1: false, selARCS2: false, selARCS: false, selAll: false,
                selTHESall: false, selFOCADS: false,
                isBarSymptoms: false, isSexRatio: false, isFirstSymptoms: false, isSurvival: false, isConsanguinity: false, 
                tableData: {genes: []}
            }
        },
        removeGene(geneName) {
            var index = this.tableData.genes.indexOf(geneName)
            if (index !== -1) {
                this.tableData.genes.splice(index, 1);
            }
        },
        addAll() {
            this.tableData.genes = []
            for (var gene of this.geneList) {
                this.tableData.genes.push(gene)
            }
        },
    }
}   
</script>
<style lang="">
    
</style>