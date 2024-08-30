<template lang="html">
    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1">
                        PYTHEAS ID 
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        SOURCE ARTICLE ID (in source article)
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        ARTICLE DOI
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        SEX
                    </th>
                    <th scope="col" class="px-6 py-1 text-center">
                        AGE AT FIRST SYMPTOMS (months)
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                    <td class="px-6 py-2">
                        <input type="text" placeholder=this.tableData.pytheasID v-model="tableData.pytheasID" class="border-none outline-none">
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{  tableData.articleID }}
                    </td>
                    <td class="px-6 py-2 text-center">
                        {{  tableData.articleDOI }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{ tableData.gene }}
                    </td>
                    <td class="px-6 py-2 text-center">
                       {{  tableData.sex }}
                    </td>
                    <td class="px-6 py-2 text-center"> 
                       {{  tableData.ageFirstSymp }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        
</template>
<script>
export default {
    name: "PatientDataTableA",
    data() {
        return this.initialState()
    },
    mounted() {},
    methods: {
        initialState() {
            return{
                tableData: {pytheasID: "THES123_10", articleID: "P1", articleDOI: "https://doi.org/10.1002/hep4.2051", gene: "ABCB4", sex: "F", ageFirstSymp: 4.0}
            }
        }
    }
}
</script>

<style lang="">
    
</style>