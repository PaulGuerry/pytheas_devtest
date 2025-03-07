<template lang="html">    
    <div class="w-full grid grid-cols-1 place-items-center mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-10"> PFIC3 (ABCB4 deficiency) </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="isBubbleSymptoms = !isBubbleSymptoms"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Symptoms 
            </button> 
            <template v-if="isBubbleSymptoms">
                <PlotSymptomBubble :propData="propData"  :key="propData.branchLevel" @update-br-lvl="(n) => n >= 2 && n <= 6 ? propData.branchLevel = n : propData.branchLevel = 3" />
            </template>
            <button @click="isSexRatio = !isSexRatio"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Sex ratio 
            </button> 
            <template v-if="isSexRatio">
                <PlotSexRatioBar :propData="propData"  :key="propData.branchLevel" />
            </template>
            <button @click="isFirstSymptoms = !isFirstSymptoms"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Age at first symptoms 
            </button> 
            <template v-if="isFirstSymptoms">
                <PlotFirstSymptomSurv :propData="propData"  :key="propData.branchLevel" />
            </template>
            <button @click="isSurvival = !isSurvival"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Survival
            </button> 
            <template v-if="isSurvival">
                <PlotSurvivalScatter :propData="propData"  :key="propData.branchLevel" />
            </template>
            <button @click="isConsanguinity = !isConsanguinity"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Consanguinity
            </button> 
            <template v-if="isConsanguinity">
                <PlotConsanguinityBar :propData="propData"  :key="propData.branchLevel" />
            </template>
            <button @click="isOrthologs = !isOrthologs"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Orthologs
            </button> 
            <template v-if="isOrthologs">
                <ShowOrthologTable :propData="propData"  :key="propData.branchLevel" />
            </template>
        </div>
    </div>
</template>
<script>

import PlotSymptomBubble from '@/components/partials/PlotSymptomBubble.vue';
import PlotSexRatioBar from '@/components/partials/PlotSexRatioBar.vue';
import PlotFirstSymptomSurv from '@/components/partials/PlotFirstSymptomSurv.vue';
import PlotSurvivalScatter from '@/components/partials/PlotSurvivalScatter.vue';
import PlotConsanguinityBar from '@/components/partials/PlotConsanguinityBar.vue';
import ShowOrthologTable from '@/components/partials/ShowOrthologTable.vue';

export default {
    name: 'PFIC3',
    components: {
    PlotSymptomBubble, PlotSexRatioBar, PlotFirstSymptomSurv, PlotSurvivalScatter,
    PlotConsanguinityBar, ShowOrthologTable
},
    data: () => ({
        propData: {gene: "ABCB4", disease: "PFIC3", branchLevel: 3},
        isBubbleSymptoms: false, isSexRatio: false, isFirstSymptoms: false,
        isSurvival: false, isConsanguinity: false, isOrthologs: false
    }),
}    
</script>

<style lang="">
    
</style>

