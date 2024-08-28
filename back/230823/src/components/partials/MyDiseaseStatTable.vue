<template lang="html">
    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        ARTICLES
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        PATIENTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        VARIABLES
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        DATA POINTS
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        COMPLETENESS
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2">
                        {{ tableData.gene }}
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{  tableData.articleCount }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{  tableData.patientCount }}
                    </td>
                    <td class="px-6 py-2 text-center"> 
                       {{  tableData.varCount }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ tableData.dataptCount }}
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{ tableData.completeness }}%
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
            default: () => ({gene: "KIF12", articleCount: 99, patientCount: 99, varCount: 99, dataptCount: 99, completeness: 99.9}) 
        }
    }
}
</script>

<style lang="">
    
</style>