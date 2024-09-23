<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-5"> Pytheas <span class="text-blue-600"> DB </span> is a curated repository of clinical data on very rare Mendelian diseases. </p>
        <!-- <div class="w-1/2 grid grid-cols-3 gap-4 my-2 place-items-center"> 
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 14 </span> diseases </p>
                <div class="w-4 h-4 tex-center bg-blue-600 rounded-full"></div>
            </div>
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 350 </span> patients </p>
                <div class="w-16 h-16 tex-center bg-amber-500 rounded-full"></div>
            </div>
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 2500 </span> data points </p>
                <div class="w-64 h-64 tex-center bg-emerald-600 rounded-full"></div>
            </div>
        </div> -->
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button  @mouseover="isPFIC1 = true; tableData.gene = 'ATP8B1'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC1 = true; tableData.gene = 'ATP8B1'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 1 </button> 
                <template v-if="isPFIC1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC2 = true; tableData.gene = 'ABCB11'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC2 = true; tableData.gene = 'ABCB11'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 2 </button> 
                <template v-if="isPFIC2">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC3 = true; tableData.gene = 'ABCB4'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC3 = true; tableData.gene = 'ABCB4'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC3')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 3 </button> 
                <template v-if="isPFIC3">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC4 = true; tableData.gene = 'TJP2'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC4 = true; tableData.gene = 'TJP2'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC4')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 4 </button> 
                <template v-if="isPFIC4">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC5 = true; tableData.gene = 'NR1H4'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC5 = true; tableData.gene = 'NR1H4'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC5')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 5 </button> 
                <template v-if="isPFIC5">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC6 = true; tableData.gene = 'SLC51A'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC6 = true; tableData.gene = 'SLC51A'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC6')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 6 </button> 
                <template v-if="isPFIC6">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC7 = true; tableData.gene = 'USP53'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC7 = true; tableData.gene = 'USP53'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC7')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 7 </button> 
                <template v-if="isPFIC7">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC8 = true; tableData.gene = 'KIF12'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC8 = true; tableData.gene = 'KIF12'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC8')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 8 </button> 
                <template v-if="isPFIC8">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC9 = true; tableData.gene = 'ZFYVE19'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC9 = true; tableData.gene = 'ZFYVE19'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC9')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 9 </button> 
                <template v-if="isPFIC9">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC10 = true; tableData.gene = 'MYO5B'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC10 = true; tableData.gene = 'MYO5B'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC10')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 10 </button> 
                <template v-if="isPFIC10">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC11 = true; tableData.gene = 'SEMA7A'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC11 = true; tableData.gene = 'SEMA7A'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC11')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC 11 </button> 
                <template v-if="isPFIC11">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isCDG2P = true; tableData.gene = 'TMEM199'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isCDG2P = true; tableData.gene = 'TMEM199'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/CDG2P')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> CDG2P </button> 
                <template v-if="isCDG2P">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHES1 = true; tableData.gene = 'SKIC3'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHES1 = true; tableData.gene = 'SKIC3'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THES1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES 1 </button> 
                <template v-if="isTHES1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHES2 = true; tableData.gene = 'SKIC2'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHES2 = true; tableData.gene = 'SKIC2'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THES2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES 2 </button> 
                <template v-if="isTHES2">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHESall = true; tableData.gene = 'SKIC2,3,?'; tableData.disease = 'THES'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHESall = true; tableData.gene = 'SKIC2,3,?'; tableData.disease = 'THES'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THESall')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES </button> 
                <template v-if="isTHESall">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isFOCADS = true; tableData.gene = 'FOCAD'; tableData.disease = 'FOCADS'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isFOCADS = true; tableData.gene = 'FOCAD'; tableData.disease = 'FOCADS'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/FOCADS')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> FOCAD deficiency </button> 
                <template v-if="isFOCADS">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
        </div>
    </div>
</template>


<script>
import myDiseaseData from '@/assets/hp_disease_stats.json'
import MyDiseaseStatTable from '@/components/partials/MyDiseaseStatTable.vue'

export default {
    name: "HomeView",
    components: {
        MyDiseaseStatTable
    },
    data() {
      return this.initialState()
    },
    mounted() { 
    },
    methods: {
        initialState() {
            return {
                diseaseArray: myDiseaseData,
                isPFIC1: false, isPFIC2: false, isPFIC3: false, isPFIC4: false, isPFIC5: false,
                isPFIC6: false, isPFIC7: false, isPFIC8: false, isPFIC9: false, isPFIC10: false,
                isPFIC11: false, isCDG2P: false, isTHES1: false, isTHES2: false, isTHESall: false, isFOCADS: false,
                tableData: {gene: "", patientCount: 0, articleCount: 0, varCount: 0, dataptCount: 0, completeness: 0.001} 
            }
        },
        falsify() {
            this.isPFIC1 = false, this.isPFIC2 = false, this.isPFIC3 = false, this.isPFIC4 = false, this.isPFIC5 = false,
            this.isPFIC6 = false, this.isPFIC7 = false, this.isPFIC8 = false, this.isPFIC9 = false, this.isPFIC10 = false,
            this.isPFIC11 = false, this.isCDG2P = false, this.isTHES1 = false, this.isTHES2 = false, this.isTHESall = false, this.isFOCADS = false,
            this.tableData = {gene: "", patientCount: 0, articleCount: 0, varCount: 0, dataptCount: 0, completeness: 0.001} 
        },
        getDiseaseStats() {
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.tableData.gene)})
            if (typeof stats_disease !== 'undefined' && typeof stats_disease[0] !== 'undefined') {
                if ('patients' in stats_disease[0]) this.tableData.patientCount = stats_disease[0].patients.total;
                if ('articles' in stats_disease[0]) this.tableData.articleCount = stats_disease[0].articles;
                if ('variables' in stats_disease[0]) {
                    this.tableData.varCount = stats_disease[0].variables.present;
                    this.tableData.completeness = stats_disease[0].variables.present / (stats_disease[0].variables.present + stats_disease[0].variables.missing) * 100;
                    this.tableData.completeness = this.tableData.completeness.toFixed(1)
                }
                if ('datapoints' in stats_disease[0]) this.tableData.dataptCount = stats_disease[0].datapoints;
            }
        }
    }
}   
</script>
<style lang="">
    
</style>