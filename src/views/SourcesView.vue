<template lang="html">
    <div class="w-full grid grid-cols-1 place-items-center mx-auto">
        <router-link to="/">
            <img class="w-[200px] h-auto md:w-[200px] lg:w-[300px] " src="@/assets/PYTHEAS_Logo.svg">
        </router-link>
        <p  class="text-xl  text-gray-400 my-10"> References </p>
        <table class="text-sm text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                <tr>
                    <th scope="col" class="px-6 py-1 text-left">
                        ARTICLE
                    </th>
                    <th scope="col" class="px-6 py-1 text-left">
                        DISEASE
                    </th>
                    <th scope="col" class="px-6 py-1 text-left">
                        DOI
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-none dark:bg-gray-800 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
                v-for="(el, i) in DOIarray" :key="i">
                    <td class="px-6 py-0 text-left">
                        {{ el.articlenumber }}
                    </td>
                    <td class="px-6 py-0 text-left">
                        {{ el.disease }}
                    </td>
                    <td class="px-6 py-0 text-left">
                        <a :href="el.articledoi"> {{ el.articledoi }} </a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>
import myArticleDOIs from '@/assets/article_DOIs.json'


export default {
    name: "SourcesView",
    components: {},
    data() {
        return {
            DOIarray: myArticleDOIs
        }
    },
    mounted() {},
    methods: {}
}   
</script>
<style lang="">
    
</style>