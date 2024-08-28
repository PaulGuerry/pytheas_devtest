<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-10"> PFIC3 </p>
        
        <div class="w-full italic my-10 text-center" :key="branchLevel+accessCode">Phenotypic abnormalities (level {{ branchLevel }} HPO terms) reported for {{ gene }} 
                                                        mutations by order of frequency among {{ patientTotal }} patients 
                                                        ({{ girlNo }} girls).</div>

        <MySymptoms :gene="gene" :disease="PFIC3" :branchLevel="branchLevel" :key="branchLevel+girlNo" @patient-counts="updatePatientNo"/>
 

    </div>
</template>
<script>

import MySymptoms from '@/components/partials/MySymptoms.vue';

export default {
    name: 'PFIC3',
    components: {
        MySymptoms
    },
    data: () => ({
        branchLevel: 4,
        patientTotal: 0,
        girlNo: 0,
        gene: "ABCB4",
    }),
    methods: {
        updatePatientNo(emittedObj) {
            this.patientTotal = emittedObj.totalNo;
            this.girlNo = emittedObj.girlNo;
        }
    }
}    
</script>

<style lang="">
    
</style>