<template lang="html">
    <header class="hidden lg:block">
        <nav class="flex items-center justify-between py-5 px-10">
            <router-link to="/">
                <img class="w-[50px] h-auto md:w-[100px] lg:w-[200px] " src="@/assets/PYTHEAS_Logo.svg">
            </router-link>
            
            <div class="flex gap-8 ">
                <router-link to="/" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Home
                </router-link>
                <router-link to="/diseases" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Diseases
                </router-link>
                <router-link to="/genes" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Genes
                </router-link>
                <router-link to="/compare" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Compare
                </router-link>
                <router-link to="/sources" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Sources
                </router-link>
                <router-link to="/about" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    About
                </router-link>
            </div>
            <div class="relative">
                <label class="relative block">
                    <span class="sr-only"> Search </span>
                    <span class="absolute inset-y-0 left-0 flex items-center pl-3 pr-8">
                        <font-awesome-icon icon="fa-solid fa-search" class="text-gray-400" />
                    </span>
                    <input class="placeholder:italic placeholder:text-slate-400 block bg-white 
                    w-full border border-slate-300 rounded-md py-2 pl-12 pr-3 shadow-sm
                    focus:outline-none focus:border-sky-500 focus:ring-sky-500 focus:ring-1 sm:text-sm"  
                    type="text" name="search" placeholder="Search for diseases...">
                </label>
            </div>
        </nav>
    </header>
    <header class="block lg:hidden">
        <nav class="flex items-center justify-between py-5 px-10">
            <router-link to="/">
                <img class="w-[50px] h-auto md:w-[100px] lg:w-[200px] " src="@/assets/PYTHEAS_Logo.svg">
            </router-link>
            
            <div class="flex gap-8 ">
                <router-link to="/diseases" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Diseases
                </router-link>
                <router-link to="/genes" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Genes
                </router-link>
                <router-link to="/compare" class="font-[400] text-lg hover:text-blue-700 transition duration-300 ease-in-out">
                    Compare
                </router-link>
            </div>
        </nav>
    </header>
</template>
<script>
export default {
    name: "MainHeader"
}
</script>
<style lang="css">
    
</style>