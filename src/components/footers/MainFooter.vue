<template lang="html">
    <footer class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-12 py-20 max-w-[1200px] 
                   mx-auto gap-10 border-t px-5" >
        <div class="flex flex-col gap-4 md:col-span-2">
            <router-link to="/about">
                <h4 class="text-3x1 font-bold text-gray-700"> Contact </h4>
            </router-link>
        </div>
        <div class="flex flex-col gap-4 md:col-span-5">
           <h4 class="text-3x1 font-bold text-gray-700"> Please cite </h4>
            <div class="flex flex-col gap-3">
                <a href="https://doi.org/10.5582/irdr.2024.01043" class="text-gray-500 font-semibold  hover:text-blue-700 transition duration-300 ease-in-out"> Percheron <span class="italic"> et al. </span>  Intractable Rare Dis Res  (2024) </a>
            </div> 
        </div>
        <div class="flex flex-col gap-4 md:col-span-3">
            <h4 class="text-3x1 font-bold text-gray-700">
                <router-link to="/sources">
                    Sources
                </router-link>
            </h4>
        </div>
        <div class="flex flex-col gap-4 md:col-span-2">
            <h4 class="text-3x1 font-bold text-gray-700">
                Sponsors
            </h4>
            <a href="https://mirumpharma.com/">
                <img style="height:60px; width:auto;" src="https://companieslogo.com/img/orig/MIRM_BIG-64e8aaee.png?t=1644879644">
            </a>
        </div> 
    </footer>
    <div class="bg-blue-600 text-white text-center py-3 px-5">
        <p style="display:inline-block;"> &copy; PytheasDB by GGS 2025. Supported by Mirum. </p>
    </div>
</template>
<script>
export default {
    
}
</script>
<style lang="">
    
</style>