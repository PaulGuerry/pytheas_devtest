<template lang="html">
    <div  class="w-full py-4 text-xl text-gray-600 col-start-1 col-span-4"> 
        <table class="w-full text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1 text-center w-1/3">
                        SPECIES
                    </th>
                    <th scope="col" class="px-6 py-1 text-center w-1/3">
                        GENE
                    </th>
                    <th scope="col" class="px-6 py-1 text-center w-1/3">
                        UNIPROT
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                    v-for="(el, i) in this.orthologArray" :key="i">
                    <td class="px-6 py-2 text-center italic">
                        <a :href="el.link">{{ el.species }} </a>
                    </td>
                    <td class="px-6 py-2 text-center italic"> 
                       <a :href="el.link">{{ el.gene }} </a>
                    </td>
                    <td class="px-6 py-2 text-center" :href="el.uniprot.link">
                       <a :href="el.uniprot.link"> {{ el.uniprot.code }} </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
        
</template>
<script>

import myDiseaseStats from '@/assets/hp_disease_stats.json'

export default {
    name: "ShowOrthologTable",
    data() {
        return this.initialState()
    },
    mounted() { 
        this.reset();
        this.gatherStats();    
    },
    methods: {
        reset() {
            Object.assign(this.$data, this.initialState())
        },
        initialState() {
            return {
                diseaseArray: myDiseaseStats,
                orthologArray: [],

            }
        },
        gatherStats() {
            var stats_disease = this.diseaseArray.filter((item) => {return (item.gene == this.propData.gene)})
            this.orthologArray = stats_disease[0].animals
        }
    },
    props: {
        propData: {
            type: Object,
            required: true,
            default: () => ({gene: "KIF12", branchLevel: 3, disease: "PFIC8"}) 
        }
    },

}
</script>

<style lang="">
    
</style>