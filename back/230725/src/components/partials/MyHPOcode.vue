<template>

<div class="container my-10">
    <div class="row">
        <div class="col">
            <template v-for="(item, index) in convertHPOcodes(HPOcodes)" :key="item.level">
                <p> HP:{{ HPOcodes[index] }}, {{ item.slice().reverse()[this.branchLevel].label }} (HP:{{ item.slice().reverse()[this.branchLevel].code }})</p>
            </template>
        </div>
    </div>
</div>



</template>


<script>
import hpoData from '@/assets/hp.json'
export default {
    name: "HPOcode",
    data() {
        return {
            HPOedgeData: hpoData.graphs[0].edges,
            HPOnodeData: hpoData.graphs[0].nodes
        }
    },
    methods: {
        findHPOedges(HPOcode) {
            let result = [];
            let edge = [];
            let i = 0;
            result.push({"code": HPOcode, "label": this.findHPOnode(HPOcode), "level": i});
            while (HPOcode != "0000001") {
                edge = this.HPOedgeData.filter((element) => element.sub.includes(HPOcode));
                HPOcode = edge[0].obj.substring(34);
                i++;
                result.push({"code": edge[0].obj.substring(34), "label": this.findHPOnode(HPOcode), "level": i});
            }
            result.map(element => {element.level = Math.abs(element.level - result.length) - 1});
            //console.table(result);
            return result;
        },
        findHPOnode(HPOcode) {
            let node = this.HPOnodeData.filter((element) => element.id.includes(HPOcode));
            return node[0].lbl
        },
        convertHPOcodes(HPOcodes){
            let result = [];
            for (let i = 0; i < HPOcodes.length; i++) {
                result.push(this.findHPOedges(HPOcodes[i]));
                //console.table(result[i].slice().reverse()[this.branchLevel])
            } 
            return result
        }
    },
    props: {
    HPOcodes: {
        type: Array,
        required: true,
        default (){ return ["0000952", "0000989"] } 
        },
    branchLevel: {
        type: Number,
        required: true,
        default: 4
        }
    },
}

</script>


<style>

</style>