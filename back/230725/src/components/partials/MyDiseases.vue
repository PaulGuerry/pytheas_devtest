<template>




<!-- need the check on isDataLoaded to stop the graph being rendered before the dataset has been updated  -->
<template v-if="diseaseVar == 'all' && isDataLoaded">
  <div class="grid grid-cols-2 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-5">
        <!-- Adjust mb of title paragraphs for vertical alignment -->
        <p class="italic "> Number of patients in database </p>
        <VuePlotly :data="barCaseCount" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Sex ratio </p>
        <VuePlotly :data="barSexRatio" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Age at first symptoms (months) </p>
        <VuePlotly :data="boxAgeAtFirstSymp" :layout="boxLayout"></VuePlotly>
        <p class="ml-10 italic"> Median age at first symptoms (months) </p>
        <VuePlotly :data="barMedianAafs" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Survival (years) </p>
        <VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly>
    </div>
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Consanguinity rate (%) </p>
        <VuePlotly :data="barConsanguinous" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>

<template v-if="diseaseVar == 'casecount' && isDataLoaded">
  <div class="grid grid-cols-1 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-5">
        <!-- Adjust mb of title paragraphs for vertical alignment -->
        <p class="italic "> Number of patients in database </p>
        <VuePlotly :data="barCaseCount" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>

<template v-if="diseaseVar == 'sexratio' && isDataLoaded">
  <div class="grid grid-cols-1 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Sex ratio </p>
        <VuePlotly :data="barSexRatio" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>

<template v-if="diseaseVar == 'ageatfirst' && isDataLoaded">
  <div class="grid grid-cols-1 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Age at first symptoms (months) </p>
        <VuePlotly :data="boxAgeAtFirstSymp" :layout="boxLayout"></VuePlotly>
        <p class="ml-10 italic"> Median age at first symptoms (months) </p>
        <VuePlotly :data="barMedianAafs" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>

<template v-if="diseaseVar == 'survival' && isDataLoaded">
  <div class="grid grid-cols-1 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Survival (years) </p>
        <VuePlotly :data="scatterSurvival" :layout="survLayout" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>

<template v-if="diseaseVar == 'consanguinity' && isDataLoaded">
  <div class="grid grid-cols-1 gap-10 max-w-[1200px] mx-auto my-2">
    <div v-if="isDataLoaded" class="chart-container flex flex-col gap-2">
        <p class="ml-10 italic"> Consanguinity rate (%) </p>
        <VuePlotly :data="barConsanguinous" :layout="barLayout3" :config="plotConfig"></VuePlotly>
    </div>
  </div>
</template>



</template>





<script>
import myDiseaseData from '@/assets/hp_disease_stats.json'
import mySurvivalLayout from '@/assets/survivalLayout1.json'
import myBarLayout3 from '@/assets/barLayout3.json'
import myBoxLayout from '@/assets/boxLayout.json'
import { VuePlotly } from 'vue3-plotly'


export default {
    name: "DiseaseData",
    components: { 
        VuePlotly 
    },
    data() {
      return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherDiseaseData();    
    },
    methods: {
      initialState() {
        return {
            diseaseData: myDiseaseData,
            isDataLoaded: false,
            barTemplate: [
                            {
                                x: [],
                                y: [],
                                type: "bar",
                                text: [],
                                textposition: "auto",
                                hoverinfo: "none",
                                marker: {
                                  color: [],
                                  line: {
                                    color: [],
                                    width: 1
                                  }
                                }
                            }
                        ],
            barCaseCount: [],
            barMedianAafs: [],
            barSexRatio: [],
            barConsanguinous: [],
            boxAgeAtFirstSymp: [],
            scatterSurvival: [],
            survLayout: mySurvivalLayout, 
            boxLayout: myBoxLayout, 
            barLayout3: myBarLayout3,
            plotConfig:{displayModeBar: false} 
        }
      },
      reset() {
        Object.assign(this.$data, this.initialState())
      },
      //source for rerendering: https://michaelnthiessen.com/force-re-render/
      gatherDiseaseData() {
          this.barCaseCount = JSON.parse(JSON.stringify(this.barTemplate))
          this.barSexRatio = JSON.parse(JSON.stringify(this.barTemplate))
          this.barMedianAafs = JSON.parse(JSON.stringify(this.barTemplate))
          this.barConsanguinous = JSON.parse(JSON.stringify(this.barTemplate))
          this.diseaseData.forEach((element) => {
               var boxplot_item = {
                     y: [], 
                     type:"box",
                     name: "",
                     color: "",
                     line: {width: 1, color: ""},
                     median: 0
                 }; 
               var scatter_item =  {
                              x:[],
                              y:[],
                              name: "",
                              type: "scatter",
                              mode: "lines",
                              line: {width: 2, color: "", shape: "hv"}
                            };
               this.barCaseCount[0].x.push(element.name); 
               this.barCaseCount[0].marker.color.push(element.colour + "33");
               this.barCaseCount[0].marker.line.color.push(element.colour);
               this.barCaseCount[0].y.push(element.patients.total);
               this.barCaseCount[0].text.push(String(element.patients.total)); 
               
               this.barSexRatio[0].x.push(element.name); 
               this.barSexRatio[0].marker.color.push(element.colour + "33");
               this.barSexRatio[0].marker.line.color.push(element.colour);
               this.barSexRatio[0].y.push((element.patients.boys)/element.patients.girls); 
               this.barSexRatio[0].text.push(String((element.patients.boys)/element.patients.girls)); 
               
              
               this.barMedianAafs[0].x.push(element.name)
               this.barMedianAafs[0].marker.color.push(element.colour + "33");
               this.barMedianAafs[0].marker.line.color.push(element.colour);
               this.barMedianAafs[0].y.push(element.age_at_first_symp.all.median)
               //Need a second copy of this array to sort the associated boxplot items 
               this.barMedianAafs[0].text.push(String(element.age_at_first_symp.all.median))
              
               this.barConsanguinous[0].x.push(element.name)
               this.barConsanguinous[0].marker.color.push(element.colour + "33");
               this.barConsanguinous[0].marker.line.color.push(element.colour);
               this.barConsanguinous[0].y.push((element.consanguinous.yes)/(element.patients.total));
               //Need a second copy of this array to sort the associated boxplot items 
               this.barConsanguinous[0].text.push( String( ((element.consanguinous.yes)/(element.patients.total) * 100).toFixed(1) ) )
            
               boxplot_item.name = element.name;
               boxplot_item.y = element.age_at_first_symp.all.array;
               boxplot_item.color = element.colour + "33";
               boxplot_item.line.color = element.colour;
               boxplot_item.median = element.age_at_first_symp.all.median;
               this.boxAgeAtFirstSymp.push(boxplot_item);

               scatter_item.name = element.name;
               scatter_item.line.color = element.colour;
               scatter_item.x = element.age_at_last_news.all.surv_x;
               console.log("x " + scatter_item.x)
               scatter_item.y = element.age_at_last_news.all.surv_y;
               console.log("y " + scatter_item.y)
               this.scatterSurvival.push(scatter_item);
             

          });
          this.isDataLoaded = true;
          
          var arrays_to_sort = {
            quant: this.barSexRatio[0].y,
            categ_1: this.barSexRatio[0].x,
            categ_2: this.barSexRatio[0].marker.color,
            categ_3: this.barSexRatio[0].marker.line.color,
            categ_4: this.barSexRatio[0].text
          }
          arrays_to_sort = this.sortArrays(arrays_to_sort)
          
          arrays_to_sort = {
            quant: this.barMedianAafs[0].y,
            categ_1: this.barMedianAafs[0].x,
            categ_2: this.barMedianAafs[0].marker.color,
            categ_3: this.barMedianAafs[0].marker.line.color,
            categ_4: this.barMedianAafs[0].text
          }
          arrays_to_sort = this.sortArrays(arrays_to_sort)
          
          arrays_to_sort = {
            quant: this.barConsanguinous[0].y,
            categ_1: this.barConsanguinous[0].x,
            categ_2: this.barConsanguinous[0].marker.color,
            categ_3: this.barConsanguinous[0].marker.line.color,
            categ_4: this.barConsanguinous[0].text
          }
          arrays_to_sort = this.sortArrays(arrays_to_sort) 
          
          arrays_to_sort = {
            quant: this.barCaseCount[0].y,
            categ_1: this.barCaseCount[0].x,
            categ_2: this.barCaseCount[0].marker.color,
            categ_3: this.barCaseCount[0].marker.line.color,
            categ_4: this.barCaseCount[0].text
          }
          // eslint-disable-next-line
          arrays_to_sort = this.sortArrays(arrays_to_sort)
          
          this.boxAgeAtFirstSymp.sort((a, b) => b.median - a.median)

      },
      sortArrays(arrays) {
        if (typeof arrays.categ_2 === 'undefined') { arrays.categ_2 = []; }
        if (typeof arrays.categ_3 === 'undefined') { arrays.categ_3 = []; }
        if (typeof arrays.categ_4 === 'undefined') { arrays.categ_4 = []; }
        
        //1. transfer value pairs to a sorting array
        var sorting_array = []
        for (var i = 0; i < arrays.quant.length; i++) {
          sorting_array.push([arrays.quant[i], arrays.categ_1[i], arrays.categ_2[i], arrays.categ_3[i], arrays.categ_4[i]])
        }
        //2. sort the sorting array using the sortable column
        sorting_array.sort((a, b) => b[0] - a[0])
        //3. transfer the sorted pairs back to the original arrays
        for (i = 0; i < arrays.quant.length; i++) {
          arrays.quant[i] = sorting_array[i][0];
          arrays.categ_1[i] = sorting_array[i][1]
          arrays.categ_2[i] = sorting_array[i][2];
          arrays.categ_3[i] = sorting_array[i][3];
          arrays.categ_4[i] = sorting_array[i][4];
        } 

        return { arrays }
      }
    },
    props: {
    diseaseVar: {
        type: String,
        required: true,
        default: "sexratio" 
        }
    },
}

</script>


<style>

</style>