<template lang="html">
    <div>
        <p>MyFeatureViewerText</p>
    </div>
    <div id="myfv"> </div>
</template>

<script>
import { createFeature } from 'feature-viewer';

export default {
   name: 'MyFeatureViewer', 
   props: {
    options: {
        type: Object,
        required: true,
        default() { 
            return {
                showAxis: true, showSequence: true,
                brushActive: true, toolbar:true,
                bubbleHelp: true, zoomMax:20 
            } 
        }
    },
    featuresA: {
        type: Array,
        required: true,
        default(){ 
            return [
                {
                    data: [{x:20,y:32},{x:46,y:100},{x:123,y:167}],
                    name: "default feature",
                    className: "default ft",
                    color: "#005572",
                    type: "rect",
                    filter: "default"
                }
            ]
        }   
    }
   },
   mounted() {
    var ft = new createFeature(500,"#myfv", this.options);
    console.log("MyFeatureViewer line 16")
    console.log("MyFeatureViewer", ft);
    this.featuresA.forEach(element => {
        console.log(element);
        ft.addFeature(element); 
    });
   }
}
</script>
<style lang="css" scoped>
    
</style>

