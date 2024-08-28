<template>

<div class="container my-10">
    <div class="row">
        <div class="col">
            <p class="my-2 italic">Branch of HPO tree leading down to the selected term.</p>
        </div>
        <div class="col">
            <table class="table table-hover text-center table-striped">
                <thead class="bg-light my-4">
                    <tr>
                        <th>HPO Code</th>
                        <th>Label</th>
                        <th>Branch level</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in findHPOedges().slice().reverse()" :key="item.code">
                        <td> {{ item.code }} </td>
                        <td> {{ item.label }} </td>
                        <td> {{ item.level }} </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>



</template>


<script>
import hpoData from '@/assets/hp.json'
export default {
    name: "HPOlist",
    data() {
        return {
            HPOedgeData: hpoData.graphs[0].edges,
            HPOnodeData: hpoData.graphs[0].nodes
        }
    },
    methods: {
        findHPOedges() {
            let result = [];
            let edge = [];
            let HPOcode = this.HPOcode;
            let i = 0;
            result.push({"code": this.HPOcode, "label": this.findHPOnode(this.HPOcode), "level": i});
            while (HPOcode != "0000001") {
                edge = this.HPOedgeData.filter((element) => element.sub.includes(HPOcode));
                HPOcode = edge[0].obj.substring(34);
                i++;
                result.push({"code": edge[0].obj.substring(34), "label": this.findHPOnode(HPOcode), "level": i});
            }
            result.map(element => {element.level = Math.abs(element.level - result.length) - 1});
            return result;
        },
        findHPOnode(HPOcode) {
            let node = this.HPOnodeData.filter((element) => element.id.includes(HPOcode));
            return node[0].lbl
        }
    },
    props: {
    HPOcode: {
        type: String,
        required: true,
        default: "0001396" 
        }
    },
}

</script>


<style>

</style>