<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center my-10 mx-auto">
        <router-link to="/">
            <img class="w-[200px] h-auto md:w-[200px] lg:w-[300px] " src="@/assets/PYTHEAS_Logo.svg">
        </router-link>
        <p  class="text-xl  text-gray-400 my-5"> Pytheas <span class="text-blue-600"> DB </span> is a living review of published clinical data on very rare Mendelian diseases. </p>
        <!-- <div class="w-1/2 grid grid-cols-3 gap-4 my-2 place-items-center"> 
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 14 </span> diseases </p>
                <div class="w-4 h-4 tex-center bg-blue-600 rounded-full"></div>
            </div>
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 350 </span> patients </p>
                <div class="w-16 h-16 tex-center bg-amber-500 rounded-full"></div>
            </div>
            <div class="w-full my-0 grid place-items-center">
                <p  class="text-xl text-center text-gray-400 mt-5 mb-0"> <span class="text-blue-600"> 2500 </span> data points </p>
                <div class="w-64 h-64 tex-center bg-emerald-600 rounded-full"></div>
            </div>
        </div> -->
        <div class="w-3/4 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 my-10 place-items-center"> 
            <button  @mouseover="isPFIC1 = true; tableData.gene = 'ATP8B1'; tableData.disease = 'PFIC1'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC1 = true; tableData.gene = 'ATP8B1'; tableData.disease = 'PFIC1'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC1 </button> 
                <template v-if="isPFIC1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC2 = true; tableData.gene = 'ABCB11'; tableData.disease = 'PFIC2'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC2 = true; tableData.gene = 'ABCB11'; tableData.disease = 'PFIC2'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC2 </button> 
                <template v-if="isPFIC2">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC3 = true; tableData.gene = 'ABCB4'; tableData.disease = 'PFIC3'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC3 = true; tableData.gene = 'ABCB4'; tableData.disease = 'PFIC3'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC3')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC3 </button> 
                <template v-if="isPFIC3">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC4 = true; tableData.gene = 'TJP2'; tableData.disease = 'PFIC4'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC4 = true; tableData.gene = 'TJP2'; tableData.disease = 'PFIC4'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC4')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC4 </button> 
                <template v-if="isPFIC4">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC5 = true; tableData.gene = 'NR1H4'; tableData.disease = 'PFIC5'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC5 = true; tableData.gene = 'NR1H4'; tableData.disease = 'PFIC5'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC5')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC5 </button> 
                <template v-if="isPFIC5">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC6 = true; tableData.gene = 'SLC51A'; tableData.disease = 'PFIC6'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC6 = true; tableData.gene = 'SLC51A'; tableData.disease = 'PFIC6'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC6')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC6 </button> 
                <template v-if="isPFIC6">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC7 = true; tableData.gene = 'USP53'; tableData.disease = 'PFIC7'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC7 = true; tableData.gene = 'USP53'; tableData.disease = 'PFIC7'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC7')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC7 </button> 
                <template v-if="isPFIC7">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC8 = true; tableData.gene = 'KIF12'; tableData.disease = 'PFIC8'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC8 = true; tableData.gene = 'KIF12'; tableData.disease = 'PFIC8'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC8')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC8 </button> 
                <template v-if="isPFIC8">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC9 = true; tableData.gene = 'ZFYVE19'; tableData.disease = 'PFIC9'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC9 = true; tableData.gene = 'ZFYVE19'; tableData.disease = 'PFIC9'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC9')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC9 </button> 
                <template v-if="isPFIC9">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC10 = true; tableData.gene = 'MYO5B'; tableData.disease = 'MYO5B deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC10 = true; tableData.gene = 'MYO5B'; tableData.disease = 'MYO5B deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC10')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> MYO5B deficiency </button> 
                <template v-if="isPFIC10">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFIC11 = true; tableData.gene = 'SEMA7A'; tableData.disease = 'PFIC11'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFIC11 = true; tableData.gene = 'SEMA7A'; tableData.disease = 'PFIC11'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFIC11')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC11 </button> 
                <template v-if="isPFIC11">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isPFICall = true; tableData.gene = 'All PFIC genes'; tableData.disease = 'PFIC1-11'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isPFICall = true; tableData.gene = 'All PFIC genes'; tableData.disease = 'PFIC1-11'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/PFICall')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> PFIC1&#8211;11 </button> 
                <template v-if="isPFICall">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isCDG2P = true; tableData.gene = 'TMEM199'; tableData.disease = 'CDG2P'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isCDG2P = true; tableData.gene = 'TMEM199'; tableData.disease = 'CDG2P'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/CDG2P')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> CDG2P </button> 
                <template v-if="isCDG2P">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHES1 = true; tableData.gene = 'SKIC3'; tableData.disease = 'THES1'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHES1 = true; tableData.gene = 'SKIC3'; tableData.disease = 'THES1'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THES1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES1 </button> 
                <template v-if="isTHES1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHES2 = true; tableData.gene = 'SKIC2'; tableData.disease = 'THES2'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHES2 = true; tableData.gene = 'SKIC2'; tableData.disease = 'THES2'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THES2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES2 </button> 
                <template v-if="isTHES2">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
            <button  @mouseover="isTHESall = true; tableData.gene = 'SKIC3,SKIC2'; tableData.disease = 'THES'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTHESall = true; tableData.gene = 'SKIC3,SKIC2'; tableData.disease = 'THES'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/THESall')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> THES1&#8211;2 </button> 
                <template v-if="isTHESall">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isFOCADS = true; tableData.gene = 'FOCAD'; tableData.disease = 'FOCADS'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isFOCADS = true; tableData.gene = 'FOCAD'; tableData.disease = 'FOCADS'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/FOCADS')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> FOCAD deficiency </button> 
                <template v-if="isFOCADS">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isARCS = true; tableData.gene = 'VPS33B,VIPAS39'; tableData.disease = 'ARCS'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isARCS = true; tableData.gene = 'VPS33B,VIPAS39'; tableData.disease = 'ARCS'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/ARCS')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ARCS </button> 
                <template v-if="isARCS">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isARCS1 = true; tableData.gene = 'VPS33B'; tableData.disease = 'ARCS1'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isARCS1 = true; tableData.gene = 'VPS33B'; tableData.disease = 'ARCS1'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/ARCS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ARCS1 </button> 
                <template v-if="isARCS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
            <button  @mouseover="isARCS2 = true; tableData.gene = 'VIPAS39'; tableData.disease = 'ARCS2'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isARCS2 = true; tableData.gene = 'VIPAS39'; tableData.disease = 'ARCS2'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/ARCS2')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> ARCS2 </button> 
                <template v-if="isARCS2">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isAARS1 = true; tableData.gene = 'AARS1'; tableData.disease = 'AARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isAARS1 = true; tableData.gene = 'AARS1'; tableData.disease = 'AARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/AARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> AARS1 deficiency </button> 
                <template v-if="isAARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>  
	    <button  @mouseover="isRARS1 = true; tableData.gene = 'RARS1'; tableData.disease = 'RARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isRARS1 = true; tableData.gene = 'RARS1'; tableData.disease = 'RARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/RARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> RARS1 deficiency </button> 
                <template v-if="isRARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
	    <button  @mouseover="isNARS1 = true; tableData.gene = 'NARS1'; tableData.disease = 'NARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isNARS1 = true; tableData.gene = 'NARS1'; tableData.disease = 'NARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/NARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> NARS1 deficiency </button> 
                <template v-if="isNARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isDARS1 = true; tableData.gene = 'DARS1'; tableData.disease = 'DARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isDARS1 = true; tableData.gene = 'DARS1'; tableData.disease = 'DARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/DARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> DARS1 deficiency </button> 
                <template v-if="isDARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isCARS1 = true; tableData.gene = 'CARS1'; tableData.disease = 'CARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isCARS1 = true; tableData.gene = 'CARS1'; tableData.disease = 'CARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/CARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> CARS1 deficiency </button> 
                <template v-if="isCARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isQARS1 = true; tableData.gene = 'QARS1'; tableData.disease = 'QARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isQARS1 = true; tableData.gene = 'QARS1'; tableData.disease = 'QARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/QARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> QARS1 deficiency </button> 
                <template v-if="isQARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isEPRS1 = true; tableData.gene = 'EPRS1'; tableData.disease = 'EPRS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isEPRS1 = true; tableData.gene = 'EPRS1'; tableData.disease = 'EPRS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/EPRS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> EPRS1 deficiency </button> 
                <template v-if="isEPRS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isHARS1 = true; tableData.gene = 'HARS1'; tableData.disease = 'HARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isHARS1 = true; tableData.gene = 'HARS1'; tableData.disease = 'HARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/HARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> HARS1 deficiency </button> 
                <template v-if="isHARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isIARS1 = true; tableData.gene = 'IARS1'; tableData.disease = 'IARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isIARS1 = true; tableData.gene = 'IARS1'; tableData.disease = 'IARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/IARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> IARS1 deficiency </button> 
                <template v-if="isIARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isLARS1 = true; tableData.gene = 'LARS1'; tableData.disease = 'LARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isLARS1 = true; tableData.gene = 'LARS1'; tableData.disease = 'LARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/LARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> LARS1 deficiency </button> 
                <template v-if="isLARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isKARS1 = true; tableData.gene = 'KARS1'; tableData.disease = 'KARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isKARS1 = true; tableData.gene = 'KARS1'; tableData.disease = 'KARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/KARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> KARS1 deficiency </button> 
                <template v-if="isKARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isMARS1 = true; tableData.gene = 'MARS1'; tableData.disease = 'MARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isMARS1 = true; tableData.gene = 'MARS1'; tableData.disease = 'MARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/MARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> MARS1 deficiency </button> 
                <template v-if="isMARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isFARSA = true; tableData.gene = 'FARSA'; tableData.disease = 'FARSA deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isFARSA = true; tableData.gene = 'FARSA'; tableData.disease = 'FARSA deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/FARSA')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> FARSA deficiency </button> 
                <template v-if="isFARSA">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isFARSB = true; tableData.gene = 'FARSB'; tableData.disease = 'FARSB deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isFARSB = true; tableData.gene = 'FARSB'; tableData.disease = 'FARSB deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/FARSB')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> FARSB deficiency </button> 
                <template v-if="isFARSB">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isSARS1 = true; tableData.gene = 'SARS1'; tableData.disease = 'SARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isSARS1 = true; tableData.gene = 'SARS1'; tableData.disease = 'SARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/SARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> SARS1 deficiency </button> 
                <template v-if="isSARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isTARS1 = true; tableData.gene = 'TARS1'; tableData.disease = 'TARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isTARS1 = true; tableData.gene = 'TARS1'; tableData.disease = 'TARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/TARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> TARS1 deficiency </button> 
                <template v-if="isTARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isWARS1 = true; tableData.gene = 'WARS1'; tableData.disease = 'WARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isWARS1 = true; tableData.gene = 'WARS1'; tableData.disease = 'WARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/WARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> WARS1 deficiency </button> 
                <template v-if="isWARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isYARS1 = true; tableData.gene = 'YARS1'; tableData.disease = 'YARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isYARS1 = true; tableData.gene = 'YARS1'; tableData.disease = 'YARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/YARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> YARS1 deficiency </button> 
                <template v-if="isYARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template> 
	    <button  @mouseover="isVARS1 = true; tableData.gene = 'VARS1'; tableData.disease = 'VARS1 deficiency'; getDiseaseStats()" @mouseleave="falsify()"  
                    @touchstart="isVARS1 = true; tableData.gene = 'VARS1'; tableData.disease = 'VARS1 deficiency'; getDiseaseStats()"   @touchend="falsify()" 
                    @click="$router.push('/VARS1')"
                    class="w-full py-4 text-xl bg-slate-200 hover:bg-amber-100 text-blue-400 rounded-full"> VARS1 deficiency </button> 
                <template v-if="isVARS1">
                    <MyDiseaseStatTable :tableData="tableData" :key="tableData.patientCount + tableData.articleCount"/>
                </template>
        </div>
    </div>
</template>


<script>
import myDiseaseData from '@/assets/hp_disease_stats.json'
import MyDiseaseStatTable from '@/components/partials/MyDiseaseStatTable.vue'

export default {
    name: "DiseasesView",
    components: {
        MyDiseaseStatTable
    },
    data() {
      return this.initialState()
    },
    mounted() { 
    },
    methods: {
        initialState() {
            return {
                diseaseArray: myDiseaseData,
                isPFIC1: false, isPFIC2: false, isPFIC3: false, isPFIC4: false, isPFIC5: false,
                isPFIC6: false, isPFIC7: false, isPFIC8: false, isPFIC9: false, isPFIC10: false,
                isPFIC11: false, isCDG2P: false, isTHES1: false, isTHES2: false, isTHESall: false, isFOCADS: false,
                isARCS: false, isARCS1: false, isARCS2: false, isPFICall: false, 
		isAARS1: false, isRARS1: false, isNARS1: false, isDARS1: false, isCARS1: false, isQARS1: false,
		isEPRS1: false, isHARS1: false, isIARS1: false, isLARS1: false, isKARS1: false, isMARS1: false,
		isFARSA: false, isFARSB: false, isSARS1: false, isTARS1: false, isWARS1: false, isYARS1: false, isVARS1: false,
                tableData: {
                    gene: "", disease: "", 
                    patientCount: 0, articleCount: 0, 
                    varCount: 0, dataptCount: 0, 
                    completeness: 0.001, 
                    zygosity: {
                        homo: 0,
                        hompct: 0.0,
                        compound: 0,
                        compct: 0.0,
                        hetero: 0,
                        hetpct: 0.0,
                        unknown: 0
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
                } 
            }
        },
        falsify() {
            this.isPFIC1 = false, this.isPFIC2 = false, this.isPFIC3 = false, this.isPFIC4 = false, this.isPFIC5 = false,
            this.isPFIC6 = false, this.isPFIC7 = false, this.isPFIC8 = false, this.isPFIC9 = false, this.isPFIC10 = false,
            this.isPFIC11 = false, this.isCDG2P = false, this.isTHES1 = false, this.isTHES2 = false, this.isTHESall = false, this.isFOCADS = false,
            this.isARCS = false, this.isARCS1 = false, this.isARCS2 = false, this.PFICall = false, 
	    this.isAARS1 = false, this.isRARS1 = false, this.isNARS1 = false, this.isDARS1 = false, this.isCARS1 = false, this.isQARS1 = false,
	    this.isEPRS1 = false, this.isHARS1 = false, this.isIARS1 = false, this.isLARS1 = false, this.isKARS1 = false, this.isMARS1 = false,
	    this.isFARSA = false, this.isFARSB = false, this.isSARS1 = false, this.isTARS1 = false, this.isWARS1 = false, this.isYARS1 = false, this.isVARS1 = false,
            this.tableData = {
                gene: "", disease: "", 
                articleCount: 0, 
                varCount: 0, dataptCount: 0, 
                completeness: 0.001,
                patients: {
                    total: 0,
                    girls: 0,
                    boys: 0
                },
                zygosity: {
                        homo: 0,
                        hompct: 0.0,
                        compound: 0,
                        compct: 0.0,
                        hetero: 0,
                        hetpct: 0.0,
                        unknown: 0
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
            } 
        },
        getDiseaseStats() {
            var stats_disease = this.diseaseArray.filter((item) => {return (item.name == this.tableData.disease)})
            if (typeof stats_disease !== 'undefined' && typeof stats_disease[0] !== 'undefined') {
                if ('patients' in stats_disease[0]) this.tableData.patients = stats_disease[0].patients;
                if ('articles' in stats_disease[0]) this.tableData.articleCount = stats_disease[0].articles;
                if ('variables' in stats_disease[0]) {
                    this.tableData.varCount = stats_disease[0].variables.present;
                    this.tableData.completeness = stats_disease[0].variables.present / (stats_disease[0].variables.present + stats_disease[0].variables.missing) * 100;
                    this.tableData.completeness = this.tableData.completeness.toFixed(1)
                }
                if ('datapoints' in stats_disease[0]) this.tableData.dataptCount = stats_disease[0].datapoints;
                if ('zygosity' in stats_disease[0]) this.tableData.zygosity = stats_disease[0].zygosity;
                if ('protvartypes' in stats_disease[0]) this.tableData.protvartypes = stats_disease[0].protvartypes;
            }
        }
    }
}   
</script>
<style lang="">
    
</style>
