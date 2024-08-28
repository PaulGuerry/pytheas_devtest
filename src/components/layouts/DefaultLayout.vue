<template lang="html">
       <MainHeader /> 
       <slot></slot>
       <MainFooter />
</template>
<script>
import MainFooter from '../footers/MainFooter.vue';
import MainHeader from '../headers/MainHeader.vue';

export default {
    components: { MainHeader, MainFooter }
}
</script>
<style lang="css">
    
</style>