<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-5"> Pytheas <span class="text-blue-600"> DB </span> is a curated repository of clinical data on very rare Mendelian diseases. </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button  @mouseover="isPatientID = true" 
                    @touchstart="isPatientID = true"   
                    @click="isPatientID = isPatientID ? false : true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ID, GENE, AGE, SEX </button> 
                <template v-if="isPatientID">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        PYTHEAS ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        SOURCE ARTICLE ID 
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
                                        <input type="text" :placeholder=tableData.pytheasID v-model="tableData.pytheasID" class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=tableData.articleID v-model="tableData.articleID" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=tableData.articleDOI v-model="tableData.articleDOI" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=tableData.gene v-model="tableData.gene" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=tableData.sex v-model="tableData.sex" class="text-center outline-none bg-transparent border-none">
                                        <Vueform>
                                            <TextElement name="hello_world" label="Hello" placeholder="World" class="text-center outline-none bg-transparent border-none"/>
                                        </Vueform>
                                    </td>
                                    <td class="px-6 py-2 text-center"> 
                                        <input type="number" :placeholder=tableData.ageFirstSymp v-model="tableData.ageFirstSymp" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template> 
        </div>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button  @mouseover="isPatientID = true" 
                    @touchstart="isPatientID = true"   
                    @click="isPatientID = isPatientID ? false : true"
                    class="w-full col-start-3 py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> SUBMIT </button> 
        </div>              
    </div>
</template>


<script>

import { mapStores } from 'pinia'
import { useFormsStore } from '../store/forms.js'

  
export default {
    name: "DataSubmitView",
    components: {},
    computed: {
        ...mapStores(useFormsStore),
        data: {
          get() {
            return this.formsStore.registration
          },
          set(data) {
            this.formsStore.registration = data
          }
        }
    },
    data() {
      return this.initialState()
    },
    mounted() { },
    methods: {
        initialState() {
            return {
                isSex: false, isAgeFirstSymp: false, isPatientID: false, 
                tableData: {pytheasID: "THES123_10", articleID: "P1", articleDOI: "https://doi.org/10.1002/hep4.2051", gene: "ABCB4", sex: "F", ageFirstSymp: 4.0}
            }
        },
        falsify() {
            this.isSex = false, this.isAgeFirstSymp = false, this.isPatientID = false
        }
    },
}
</script>

<style lang="">
    
</style>