<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <h1 class="text-3xl font-bold text-gray-500"> Pytheas <span class="text-blue-600"> DB </span> </h1> 
        <p  class="text-xl  text-gray-400 my-5"> Pytheas <span class="text-blue-600"> DB </span> is a curated repository of clinical data on very rare Mendelian diseases. </p>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button     
                    @click="isPatientID = isPatientID ? false : true; "
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ID, GENE, AGE, SEX </button> 
                <template v-if="isPatientID">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-sm text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Source article ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Article DOI
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Gene
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Sex (M/F)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Consaguinous (Y/N) 
                                    </th>
                                    
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" @change=this.fetchPatient() class="outline-none bg-transparent border-none">
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
                                        <input type="text" :placeholder=el.consanguinity v-model="el.consanguinity" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template> 
            <button    
                    @click="isSymptoms = isSymptoms ? false : true; "
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> SYMPTOMS </button> 
                <template v-if="isSymptoms">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-sm text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 ">
                                        Symptoms (comma-separated 7-digit HPO codes) 
                                    </th>
                                    <th scope="col" class="px-6 py-1 ">
                                        Symptoms reported absent (comma-separated HPO codes)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Age at first symptoms (months)
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="textarea" :placeholder=el.symptoms v-model="el.symptoms" class="w-full outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="textarea" :placeholder=el.absentsymptoms v-model="el.symptoms" class="w-full outline-none bg-transparent border-none">
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
                    @click="isVariantData = isVariantData ? false : true; "
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> VARIANT </button> 
                <template v-if="isVariantData">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-sm text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Gene
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Nucleotide variant 1
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Protein variant 1
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Nucleotide variant 2
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Protein variant 2
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="text-xs">
                                    <td class="px-6 py-2">
                                        
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        
                                    </td>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        HGVS genomic or RNA description 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        HGVS protein description
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        HGVS genomic or RNA description
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        HGVS protein description
                                    </th>
                                </tr>
                                <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" @change=this.fetchPatient() class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.gene v-model="el.gene" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.nucleotidevariant1 v-model="el.nucleotidevariant1" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.protvariant1 v-model="el.protvariant1" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.nucleotidevariant2 v-model="el.nucleotidevariant2" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.protvariant2 v-model="el.protvariant2" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template>
                <button     
                    @click="isWeiHei = isWeiHei ? false : true;"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> AGE, WEIGHT, HEIGHT </button> 
                <template v-if="isWeiHei">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                            <thead class="text-sm text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-6 py-1">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Birth weigth (kg) 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Birth length (cm) 
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Weight at last follow-up (kg)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Height at last follow-up (cm)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        GA at birth (weeks)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Age at last follow-up (years)
                                    </th>
                                    <th scope="col" class="px-6 py-1 text-center">
                                        Status at last follow-up (alive/dead)
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.id v-model="el.id" @change=this.fetchPatient() class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.birthweight v-model="el.birthweight" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.birthheight v-model="el.birthheight" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.lastweightkg v-model="el.lastweightkg" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.lastheightcm v-model="el.lastheightcm" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="number" :placeholder=el.term v-model="el.term" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.lastnewsageyear v-model="el.lastnewsageyear" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2 text-center">
                                        <input type="text" :placeholder=el.alivedead v-model="el.alivedead" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template>
        </div>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="this.addPatient(); isPatientID = true; "
                    class="w-full col-start-2 py-4 text-xl bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> ADD PATIENT </button> 
            <button @mouseover=this.str2Arr() 
                    @touchstart=this.str2Arr()
                    @click="isViewJSON = isViewJSON ? false : true; this.str2Arr()"
                    class="w-full col-start-3 py-4 text-xl bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> VIEW JSON </button> 
                <template v-if="isViewJSON">
                    <div  class="w-full py-4 text-center text-gray-600 col-start-1 col-span-5"> 
                        <p text-xs> {{ JSON.stringify(this.tableData) }} </p>
                    </div>
                </template> 
        </div>              
    </div>
</template>


<script>

import myPatientData from '@/assets/patientData_edited.json'

  
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
                patientData: myPatientData,
                isSex: false, isAgeFirstSymp: false, isPatientID: false, 
                isViewJSON: false, isSymptoms: false, isVariantData: false,
                isWeiHei: false,
                tableData: []   
            }
        },
        falsify() {
            this.isSex = false, this.isAgeFirstSymp = false, this.isPatientID = false
        },
        addPatient() {
            this.tableData.push({
                id: "PFIC99_99",
                disease: "PFIC99", 
                patients: "P15",
                doi: "https://doi.org/10.1002/hep4.2051", 
                gene: "ABCB4", 
                sex: "F", 
                term: 37,
                firstsymptomagemonth: 4.0,
                consanguinity: "N",
                symptoms: [
                            "0045056",
                            "0002240",
                            "0003077"
                ],
                absentsymptoms: [
                            "0012768",
                            "0032807"
                ],
                nucleotidevariant1: "NG_007374.1(NM_003742.2):c.3767C>T",
                protvariant1: "NG_007374.1(NP_003733.2):p.(Thr1256Met)",
                nucleotidevariant2: "WT",
                protvariant2: "WT",
                birthweight: 3000,
                birthheight: 51,
                lastweightkg: 15,
                lastheightcm: 100,
                lastnewsageyear: 12,
                alivedead: "alive"
            })
        },
        str2Arr() {
                this.tableData.forEach(el => {
                    if (typeof el.symptoms === 'string') 
                        el.symptoms = el.symptoms.split(",")
                    })
        },
        fetchPatient() {
            var patientEntry = {}
            this.tableData.forEach(tableel => {
                patientEntry = []
                patientEntry = this.patientData.filter((jsonel) => {return (jsonel.id == tableel.id)})
                console.log("242", tableel.id, patientEntry, patientEntry.length)
                if (patientEntry.length !== 0) {
                    console.log("244", patientEntry[0])
                    if (!Object.keys(patientEntry[0]).length !== 0) {
                        tableel.disease = patientEntry[0].disease;
                        tableel.patients = patientEntry[0].patients;
                        tableel.doi = patientEntry[0].doi;
                        tableel.gene = patientEntry[0].gene;
                        tableel.sex = patientEntry[0].sex;
                        tableel.term = patientEntry[0].term;
                        tableel.firstsymptomagemonth = patientEntry[0].firstsymptomagemonth;
                        tableel.consanguinity = patientEntry[0].consanguinity;
                        tableel.symptoms = patientEntry[0].symptoms;
                        tableel.absentsymptoms = patientEntry[0].absentsymptoms;
                        tableel.nucleotidevariant1 = patientEntry[0].nucleotidevariant1;
                        tableel.protvariant1 = patientEntry[0].protvariant1;
                        tableel.nucleotidevariant2 = patientEntry[0].nucleotidevariant2;
                        tableel.protvariant2 = patientEntry[0].protvariant2;
                        tableel.birthweight = patientEntry[0].birthweight;
                        tableel.birthheight = patientEntry[0].birthheight;
                        tableel.lastweigthkg = patientEntry[0].lastweigthkg;
                        tableel.lastheightcm = patientEntry[0].lastheightcm;
                        tableel.lastnewsageyear = patientEntry[0].lastnewsageyear;
                        tableel.alivedead = patientEntry[0].alivedead;
                    }
                }
            })
        }
    }
}
</script>

<style lang="">
    
</style>