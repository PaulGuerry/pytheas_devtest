<template>

<DefaultLayout>
  
  <!-- div with grid-cols-3 -->
  <div class="grid grid-cols-3 gap-5 max-w-[1200px] mx-auto my-10">
    
    <!-- Form to select by gene, first column -->
    <form class="bg-gray-100 rounded p-5 flex flex-col gap-5 border-gray-800 z-10" @submit="handleSubmit">
      <div>
        <h3 class="text-2xl text-left text-blue-600 font-bold mb-4">
          Selection
        </h3>
      </div>
      <div class="grid grid-cols-2 gap-2 mx-auto">
        <label for="" class="block mb-3 ">GENE:</label>
        <label for="" class="block mb-3 ">BRANCH LEVEL:</label>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="accessCode">
          <option value="O43520">ATP8B1</option>
          <option value="Q96FN5">KIF12</option>
          <option value="Q96K21">ZFYVE19</option>
          <option value="Q6PGP7">SKIC3</option>
          <option value="Q15477">SKIC2</option>
          <option hidden value="Q70EK8">USP53</option>
          <option hidden value="Q9H3U1">UNC45A</option>
          <option hidden value="Q9UDY2">TJP2</option>
        </select>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="branchLevel">
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
        </select>
      </div>
    
    </form>
    
    <!-- Form to select by OMIM code, second column -->
    <form class="bg-gray-100 rounded p-5 flex flex-col gap-5 border-gray-800 z-10" @submit="handleSubmit">
      <div>
        <h3 class="text-2xl text-left text-blue-600 font-bold mb-4">
          Selection
        </h3>
      </div>
      <div class="grid grid-cols-2 gap-2 mx-auto">
        <label for="" class="block mb-3 ">DISEASE (OMIM code):</label>
        <label for="" class="block mb-3 ">BRANCH LEVEL:</label>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="accessCodeO">
          <option value="O43520">PFIC1 (211600)</option>
          <option value="Q96FN5">PFIC8 (619662)</option>
          <option value="Q96K21">PFIC9 (619849)</option>
          <option value="Q6PGP7">THES1 (222470)</option>
          <option value="Q15477">THES2 (614602)</option>
        </select>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="branchLevel">
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          <option value="6">6</option>
        </select>
      </div>
    
    </form>
     
    <!-- Form to select variable, third column -->
    <form class="bg-gray-100 rounded p-5 flex flex-col gap-5 border-gray-800 z-10" @submit="handleSubmit">
      <div>
        <h3 class="text-2xl text-left text-blue-600 font-bold mb-4">
          Compare diseases
        </h3>
      </div>
      <div>
        <label for="" class="block mb-3 ">Parameter:</label>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="diseaseParam">
          <option value="ageatfirst">Age at first symptoms</option>
          <option value="casecount">Cases in database</option>
          <option value="consanguinity">Consanguinity rate</option>
          <option value="sexratio">Sex ratio</option>
          <option value="survival">Survival</option>
          <option value="all">All available parameters</option>
        </select>
      </div>
    
    </form>     
  </div>
  
  
  <!-- Show protein sequence results -->
  
  
  <!-- Show results of search by gene -->
  <div class="flex flex-col gap-5 max-w-[1200px] mx-auto mt-5 mb-2">
      <template v-if="accessCode">
        
        
        <div class="mt-2 mb-2 italic" :key="branchLevel+accessCode">Phenotypic abnormalities (level {{ branchLevel }} HPO terms) reported for {{  geneList[codeList.indexOf(accessCode)] }} 
                                                        mutations by order of frequency among {{ patientTotal }} patients 
                                                        ({{ girlNo }} girls).</div>
        
        
        <MySymptoms :gene="geneList[codeList.indexOf(accessCode)]" :disease="diseaseList[codeList.indexOf(accessCode)]" :branchLevel="branchLevel" :key="branchLevel+accessCode" @patient-counts="updatePatientNo"/>
        <div class="mt-0 mb-0 italic" :key="branchLevel+accessCode">Molecular features of {{  geneList[codeList.indexOf(accessCode)] }} protein.  </div>
        <div class="mt-0 container mx-auto">
          <MyProteinViewer :accessionCode="accessCode" :key="branchLevel+accessCode"> </MyProteinViewer>
        </div>
      </template>
  </div>


  
  <!-- Show results of search by OMIM code -->
  <div class="flex flex-col gap-5 max-w-[1200px] mx-auto mt-5 mb-2">
    <template v-if="accessCodeO"> 
      <div class="mt-2 mb-2 italic" :key="branchLevel+accessCodeO">Phenotypic abnormalities (level {{ branchLevel }} HPO terms) reported for {{  diseaseList[codeList.indexOf(accessCodeO)] }} 
                                                by order of frequency among {{ patientTotal }} patients ({{ girlNo }} girls).</div>
      
      <MySymptoms :gene="geneList[codeList.indexOf(accessCodeO)]" :disease="diseaseList[codeList.indexOf(accessCodeO)]" :branchLevel="branchLevel" :key="branchLevel+accessCodeO" @patient-counts="updatePatientNo"/>
      <div class="mt-2 mb-0 italic" :key="branchLevel+accessCodeO">Molecular features of {{  geneList[codeList.indexOf(accessCodeO)] }} protein.  </div>
      <div class="mx-auto">
          <MyProteinViewer :accessionCode="accessCodeO" :key="branchLevel+accessCodeO"> </MyProteinViewer>
      </div>
    </template>
  </div>

  <!-- Show results of selection by variable -->
  <template v-if="diseaseParam">
      <MyDiseases :diseaseVar="diseaseParam" :key="diseaseParam" />
  </template>
  
   

</DefaultLayout>


</template>

<script>
import DefaultLayout from './components/layouts/DefaultLayout.vue';
import MyDiseases from './components/partials/MyDiseases.vue';
import MyProteinViewer from './components/partials/MyProteinViewer.vue';
//import LoadingComponent from './components/partials/MyLoadingComponent.vue';
//import MyFeatureViewer from './components/partials/MyFeatureViewer.vue';
//import MyGeneDataList from './components/partials/MyGeneDataList.vue';
import MySymptoms from './components/partials/MySymptoms.vue';


export default {
  name: 'App',
  components: {
    DefaultLayout,
    MySymptoms,
    MyDiseases,
    MyProteinViewer
},
  data() {
    return {
      compKey1: 0,
      compKey2: 0,
      patientTotal: 0,
      girlNo: 0,
      accessCode: "", //"Q96FN5", //"Q96K21",
      accessCodeO: "", //"Q96FN5", //"Q96K21",
      diseaseParam: "",
      branchLevel: "3",
      HPOcode: "0002847", //"Q96FN5", //"Q96K21",
      geneList:    [ "ZFYVE19",  "KIF12", "ATP8B1",  "SKIC3", "SKIC2", "USP53", "UNC45A", "TJP2"],
      diseaseList: [   "PFIC9",  "PFIC8",  "PFIC1",  "THES1", "THES2"],
      codeList:    [  "Q96K21", "Q96FN5", "O43520", "Q6PGP7", "Q15477", "Q70EK8", "Q9H3U1", "Q9UDY2"],
      emptyArray: [], //braces for an array
      optionsO: {showAxis: true, showSequence: false,
                brushActive: false, toolbar: false,
                bubbleHelp: false, zoomMax:20 }, //brackets for an object
    }
  },
  watch: {
    accessCode(){
      //Only rerender if accessCode exists (i.e. has not just been reset by this.rerenderDisease() to null)
      if (this.accessCode) {this.rerenderGene()}
    },
    accessCodeO(){
      //Only rerender if accessCodeO exists (i.e. has not just been reset by this.rerenderGene() to null)
      if (this.accessCodeO) {this.rerenderDisease()}
    },
    diseaseParam(){
      if (this.diseaseParam){this.rerenderParam()}
    }
  },
  methods: {
    //source for rerendering: https://michaelnthiessen.com/force-re-render/
    rerenderDisease() { 
        this.compKey2++;
        this.accessCode = "";
        this.diseaseParam = "" 
        return null
    },
    rerenderGene() { 
        this.compKey1++;
        this.accessCodeO = "";
        this.diseaseParam = "" 
        return null
    },
    rerenderParam() { 
        this.accessCode="";
        this.accessCodeO = "";
        return null
    },
    updatePatientNo(emittedObj) {
        this.patientTotal = emittedObj.totalNo;
        this.girlNo = emittedObj.girlNo;
    }
  }
}
</script>

<style>

</style>
