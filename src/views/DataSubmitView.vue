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
                                    <th scope="col" class="px-2 py-1">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-2 py-1">
                                        
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Disease
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Source article ID 
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Article DOI
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Gene
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Sex (M/F)
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Consaguinous (Y/N) 
                                    </th>
                                    
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                                v-for="(el, i) in tableData" :key="i">
                                    <td class="px-2 py-2">
                                            <input type="text" :placeholder="el.id" v-model="el.id" @change="this.fetchPatient(); this.activeID = el.id"  class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2">
                                        <input type="radio" name="activeID" :value="el.id" v-model="activeID" />
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                            <input type="text" :placeholder="el.disease" v-model="el.disease"  class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                        <input type="text" :placeholder=el.patients v-model="el.patients" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                        <input type="text" :placeholder=el.doi v-model="el.doi" @change="this.fetchDOI(); this.activeDOI = el.doi" @keypress="this.activeDOI = el.doi" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                        <input type="text" :placeholder=el.gene v-model="el.gene" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2 text-center">
                                        <input type="text" :placeholder=el.sex v-model="el.sex" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-2 py-2 text-center">
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
                                        <input type="textarea" :placeholder=el.symptoms v-model="el.symptoms" class="w-full outline-none bg-transparent border-none text-center">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="textarea" :placeholder=el.absentsymptoms v-model="el.absentsymptoms" class="w-full outline-none bg-transparent border-none text-center">
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
                                        <input type="text" :placeholder=el.id v-model="el.id" @change="this.fetchPatient(); this.activeID = el.id" @keypress="this.activeID = el.id" class="outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.gene v-model="el.gene" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.nucleotidevariant1 v-model="el.nucleotidevariant1" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.protvariant1 v-model="el.protvariant1" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.nucleotidevariant2 v-model="el.nucleotidevariant2" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
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
                                        <input type="text" :placeholder=el.id v-model="el.id" @change="this.fetchPatient(); this.activeID = el.id" @keypress="this.activeID = el.id" class="outline-none bg-transparent border-none text-left">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="number" :placeholder=el.birthweight v-model="el.birthweight" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="number" :placeholder=el.birthheight v-model="el.birthheight" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="number" :placeholder=el.lastweightkg v-model="el.lastweightkg" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="number" :placeholder=el.lastheightcm v-model="el.lastheightcm" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="number" :placeholder=el.term v-model="el.term" class="text-center outline-none bg-transparent border-none [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.lastnewsageyear v-model="el.lastnewsageyear" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                    <td class="px-6 py-2">
                                        <input type="text" :placeholder=el.alivedead v-model="el.alivedead" class="text-center outline-none bg-transparent border-none">
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </template>
            <button     
                    @click="isTreatments = isTreatments? false : true;"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> TREATMENTS </button> 
                <template v-if="isTreatments">
                    <div  class="w-full py-4 text-xl text-center text-gray-600 col-start-1 col-span-5"> 
                        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
                            <thead class="text-sm text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                                <tr>
                                    <th scope="col" class="px-2 py-1 text-left">
                                        Pytheas ID 
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Treatment name 
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Treatment type 
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Age at start (months)
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Duration (months)
                                    </th>
                                    <th scope="col" class="px-2 py-1 text-center">
                                        Efficacy (aggravation, none, unclear, partial, overall)
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <template v-for="(el, i) in tableData" :key="i">
                                    <template v-for="(tt, j) in el.treatments" :key="j">
                                        <tr class="text-xs bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600">
                                            <td class="px-2 py-2">
                                                <input type="text" :placeholder="el.id" v-model="el.id" class="outline-none bg-transparent border-none text-left">
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="text" :placeholder="tt.name" v-model="tt.name" class="outline-none bg-transparent border-none text-center">
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="radio" name="activeTT" :value="tt.id" v-model="activeTT" />
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="text" :placeholder="tt.type" v-model="tt.type" class="outline-none bg-transparent border-none text-center">
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="number" :placeholder="tt.ageatstart_m" v-model="tt.ageatstart_m" class="outline-none bg-transparent border-none text-center [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="number" :placeholder="tt.duration_m" v-model="tt.duration_m" class="outline-none bg-transparent border-none text-center [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none">
                                            </td>
                                            <td class="px-2 py-2">
                                                <input type="text" :placeholder="tt.efficacy" v-model="tt.efficacy" class="outline-none bg-transparent border-none text-center">
                                            </td>
                                        </tr>
                                    </template>
                                </template>
                            </tbody>
                        </table>
                    </div>
                </template>
        </div>
        <div class="w-3/4 grid grid-cols-5 gap-4 my-10 place-items-center"> 
            <button @click="this.addPatient(); isPatientID = true; "
                    class="w-full col-start-1 py-4 text-sm bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> ADD PATIENT </button> 
            <button @click="this.deletePatient(); isPatientID = true; "
                    class="w-full col-start-2 py-4 text-sm bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> DELETE PATIENT </button> 
            <button @click="this.addTreatment(); isTreatments = true"
                    class="w-full col-start-3 py-4 text-sm bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> ADD TREATMENT </button>
            <button @click="this.deleteTreatment(); isTreatments = true"
                    class="w-full col-start-4 py-4 text-sm bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> DELETE TREATMENT </button>
            <button @mouseover=this.str2Arr() 
                    @touchstart=this.str2Arr()
                    @click="isViewJSON = isViewJSON ? false : true; this.str2Arr()"
                    class="w-full col-start-5 py-4 text-sm bg-emerald-100 hover:bg-emerald-300 text-emerald-800 rounded-full"> VIEW JSON </button> 
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
                isWeiHei: false, activeID: "", activeDOI: "", 
                isTreatments: false, activeTT: "",
                tableData: []   
            }
        },
        falsify() {
            this.isSex = false, this.isAgeFirstSymp = false, this.isPatientID = false
        },
        addPatient() {
            this.activeID = "PFIC99_99";
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
                treatments: [{
                    id: "PFIC99_99.t0",
                    name: "corticosteroid",
                    type: "anti-inflammatory",
                    ageatstart_m: 1.0,
                    duration_m: 5.0,
                    efficacy: "unclear"  
                }],
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
        addTreatment() {
            if (this.tableData.length < 1) {this.addPatient()}
            else { 
                var i = this.tableData.findIndex((el) => {return el.id == this.activeID})
                if ("treatments" in this.tableData[i]) {
                    this.tableData[i].treatments.push({
                        id: this.tableData[i].id.concat('.',"t",this.tableData[i].treatments.length.toString()),
                        name: "corticosteroid",
                        type: "anti-inflammatory",
                        ageatstart_m: 1.0,
                        duration_m: 5.0,
                        efficacy: "unclear"  
                    })
                }
                else {
                    this.tableData[i].treatments = [];
                    this.tableData[i].treatments.push({
                        id: this.tableData[i].id.concat('.',"t",this.tableData[i].treatments.length.toString()),
                        name: "corticosteroid",
                        type: "anti-inflammatory",
                        ageatstart_m: 1.0,
                        duration_m: 5.0,
                        efficacy: "unclear"  
                    })
                }
            }
        },
        str2Arr() {
                this.tableData.forEach(el => {
                    if (typeof el.symptoms === 'string') 
                        el.symptoms = el.symptoms.split(",")
                    })
        },
        fetchPatient() {
            let patientEntry = {}
            this.tableData.forEach((tableel, index) => {
                patientEntry = []
                patientEntry = this.patientData.filter((jsonel) => {return (jsonel.id == tableel.id)})
                if (patientEntry.length !== 0) {
                    if (Object.keys(patientEntry[0]).length !== 0) {
                        this.tableData.splice(index, 1, patientEntry[0])
                    }
                }
            })
        },
        fetchDOI() {
            let patientEntries = this.patientData.filter((jsonel) => {return (jsonel.doi == this.activeDOI)})
            patientEntries.forEach((entry) => {
                //240904: if entry contains treatment info, check that tts have ids and add them if not
                if ("treatments" in entry)  {
                    entry.treatments.forEach((tt, i) => {
                        if (!("id" in tt)) {
                            tt.id = entry.id.concat('.',"t",i.toString())
                        }
                    })
                }
                this.tableData.push(entry)
            })
        },
        deletePatient() {
            let i = this.tableData.findIndex((tableel) => {return tableel.id == this.activeID})
            if (i > -1) {
                this.tableData.splice(i, 1)
                this.activeID = this.tableData[0].id
            }

        },
        deleteTreatment() {
            let j = -1
            this.tableData.forEach((tableel) => {
                j = tableel.treatments.findIndex((ttel) => {return ttel.id == this.activeTT})
                if (j > -1) {
                    tableel.treatments.splice(j, 1)
                    this.activeTT = ""
                }
                j = -1
            })
        }
    }
}
</script>

<style lang="">
    
</style>