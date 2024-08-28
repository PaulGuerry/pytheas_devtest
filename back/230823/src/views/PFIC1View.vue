<template lang="html">    
    <div class="w-full grid grid-cols-1 place-items-center mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-10"> PFIC1 </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="isBarSymptoms = !isBarSymptoms"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> Symptoms </button> 
                <template v-if="isBarSymptoms">
                    <PlotSymptomBarDoughnut :propData="propData"  :key="propData.branchLevel" @update-br-lvl="(n) => n >= 2 && n <= 6 ? propData.branchLevel = n : propData.branchLevel = 3" />
                </template>
        </div>
    </div>
</template>
<script>

import PlotSymptomBarDoughnut from '@/components/partials/PlotSymptomBarDoughnut.vue';

export default {
    name: 'PFIC1',
    components: {
        PlotSymptomBarDoughnut
    },
    data: () => ({
        propData: {gene: "ATP8B1", disease: "PFIC1", branchLevel: 3},
        isBarSymptoms: false
    }),
}    
</script>

<style lang="">
    
</style>