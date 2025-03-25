<template lang="html">
    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        HOMOZYGOUS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        COMPOUND
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        HETEROZYGOUS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2">
                        {{ tableData.gene }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{  tableData.patientCount }}
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.zygosity.homo }} ({{ tableData.zygosity.hompct }}%) 
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.zygosity.compound }} ({{ tableData.zygosity.compct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.zygosity.hetero }} ({{ tableData.zygosity.hetpct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">

                    </td>
                    <td class="px-6 py-2 text-center">

                    </td>
                </tr>
            </tbody>
            <thead class="text-xs text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1">
                        
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                       
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        LoF&#8211;LoF
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        LoF&#8211;Mis
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        Mis&#8211;Mis
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        LoF&#8211;WT/Syn
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        Mis&#8211;WT/Syn
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2">
                        
                    </td>
                    <td class="px-6 py-2 text-center">
                       
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.protvartypes.LoF_LoF }} ({{ tableData.protvartypes.LLpct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.protvartypes.LoF_Mis }} ({{ tableData.protvartypes.LMpct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.protvartypes.Mis_Mis }} ({{ tableData.protvartypes.MMpct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.protvartypes.LoF_Het }} ({{ tableData.protvartypes.LHpct }}%)  
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.protvartypes.Mis_Het }} ({{ tableData.protvartypes.MHpct }}%)  
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        
</template>
<script>
export default {
    name: "DiseaseStatTable",
    props: {
        tableData: {
            type: Object,
            required: true,
            default: () => ({
                gene: "KIF12", disease: "PFIC8",
                articleCount: 99, 
                patientCount: 99, varCount: 99, 
                dataptCount: 99, completeness: 99.9,
                zygosity: {
                    homo: 0, compound: 0, hetero: 0, unknown: 0,
                    hompct: 0.0, compct: 0.0, hetpct: 0.0
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
            }) 
        }
    }
}
</script>

<style lang="">
    
</style>