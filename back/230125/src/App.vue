<template>

<DefaultLayout>
  
  <div class="grid grid-cols-2 gap-5 max-w-[1200px] mx-auto my-10">
    <form class="bg-gray-100 rounded p-5 flex flex-col gap-5 border-[2px] border-gray-800" @submit="handleSubmit">
      <div>
        <h3 class="text-2xl text-left text-blue-600 font-bold mb-4">
          Selection
        </h3>
      </div>
      
     
      <div>
        <label for="" class="block mb-3 ">GENE:</label>
        <select name="" id="" class="w-full py-2 px-4 bg-white text-sm" v-model="accessCode">
          <option value="Q96K21">ZFYVE19</option>
          <option value="Q96FN5">KIF12</option>
          <option value="Q70EK8">USP53</option>
          <option value="Q9H3U1">UNC45A</option>
          <option value="Q9UDY2">TJP2</option>
        </select>
      </div>
    
    </form>
    
      <div class="p-5 flex flex-col gap-5 ">
        <div>
          <h3 class="py-[10px] text-4xl text-center text-blue-700 font-bold mb-4"> </h3>
        </div>
        <div>
          <h3 class="py-[10px] text-4xl text-center text-blue-700 font-bold mb-4"></h3>
        </div>

      </div>
      
  </div>
  
  <div class="container mx-auto " v-if="accessCode">
    <MyFeatureViewer :options="optionsO" :featuresA="featuresA" :accessionCode="accessCode" :key="accessCode"/>
  </div>
  
</DefaultLayout>


</template>

<script>
import DefaultLayout from './components/layouts/DefaultLayout.vue';
import MyFeatureViewer from './components/partials/MyFeatureViewer.vue';

export default {
  name: 'App',
  components: { DefaultLayout, MyFeatureViewer },
  data() {
    return {
      gensel: "",
      accessCode: "Q70EK8", //"Q96FN5", //"Q96K21",
      emptyArray: [], //braces for an array
      optionsO: {showAxis: true, showSequence: false,
                brushActive: false, toolbar: false,
                bubbleHelp: false, zoomMax:20 }, //brackets for an object
      featuresA: [
        {
          data: [{x:120,y:154},{x:21,y:163},{x:90,y:108},{x:10,y:25},{x:193,y:210},{x:78,y:85},{x:96,y:143},{x:14,y:65},{x:56,y:167}],
          name: "feature A",
          className: "A",
          color: "#F4D4AD",
          type: "rect",
          height: 8,
          filter: "type 1"
        },
        {
          data: [{x:130,y:184},{x:40,y:142},{x:80,y:110}],
          name: "path feature",
          className: "path",
          color: "#eda64f",
          type: "path",
          filter: "type 2"
        },
        {
          data: [],
          name: "predicted disorder",
          className: "disorder",
          color: "#008B8D",
          type: "line",
          filter: "type 3",
          height: "5"
        }
      ],
    }
  },
  methods: {
    genRandom() {
      var randomData = [];
      for (var i=1;i<250;i++) {
        var count = Math.floor((Math.random() * 20) + 1);
        randomData.push({x: i*2, y:count});
      }
      this.featuresA[2].data = randomData;
    }
  },
  created () {
    this.genRandom()
  }
}
</script>

<style>

</style>
