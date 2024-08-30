<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-5"> Pytheas <span class="text-blue-600"> DB </span> is a curated repository of clinical data on very rare Mendelian diseases. </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button     
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
                                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.patients v-model="el.patients" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.doi v-model="el.doi" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.gene v-model="el.gene" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.sex v-model="el.sex" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center"> 
                                        <input type="number" :placeholder=el.firstsymptomagemonth v-model="el.firstsymptomagemonth" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template> 
            <button    
                    @click="isSymptoms = isSymptoms ? false : true"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> SYMPTOMS </button> 
                <template v-if="isSymptoms">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        PYTHEAS ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 ">
                                        SYMPTOMS (comma-separated 7-digit HPO codes) 
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="textarea" :placeholder=el.symptoms v-model="el.symptoms" class="w-full outline-none bg-transparent border-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template>
        </div>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="this.addPatient()"
                    class="w-full col-start-2 py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ADD PATIENT </button> 
            <button @mouseover=this.str2Arr() 
                    @touchstart=this.str2Arr()
                    @click="isViewJSON = isViewJSON ? false : true; this.str2Arr()"
                    class="w-full col-start-3 py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> VIEW JSON </button> 
                <template v-if="isViewJSON">
                    <div  class="w-full py-4 text-center text-gray-600 col-start-1 col-span-5"> 
                        <p text-xs> {{ JSON.stringify(this.tableData) }} </p>
                    </div>
                </template> 
        </div>              
    </div>
</template>


<script>


  
export default {
    name: "DataSubmitView",
    components: {},
    data() {
      return this.initialState()
    },
    mounted() { },
    methods: {
        initialState() {
            return {
                isSex: false, isAgeFirstSymp: false, isPatientID: false, 
                isViewJSON: false, isSymptoms: false,
                tableData: [
                            {
                            id: "THES123_10", 
                            disease: "PFIC8", 
                            doi: "https://doi.org/10.1002/hep4.2051", 
                            gene: "ABCB4", 
                            sex: "F", 
                            firstsymptomagemonth: 4.0,
                            symptoms: [
                                "0002904",
                                "0000952",
                                "0030948",
                                "0000077"
                            ]
                            }
                        ]   
            }
        },
        falsify() {
            this.isSex = false, this.isAgeFirstSymp = false, this.isPatientID = false
        },
        addPatient() {
            this.tableData.push({
                id: "PFIC99_99",
                disease: "PFIC99", 
                doi: "https://doi.org/10.1002/hep4.2051", 
                gene: "ABCB4", 
                sex: "F", 
                firstsymptomagemonth: 4.0,
                symptoms: [
                            "0045056",
                            "0002240",
                            "0003077"
                ]
            })
        },
        str2Arr() {
                this.tableData.forEach(el => {
                    if (typeof el.symptoms === 'string') 
                        el.symptoms = el.symptoms.split(",")
                    })
        }
    }
}
</script>

<style lang="">
    
</style>