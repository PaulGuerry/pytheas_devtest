<template>

<DefaultLayout>

  <router-view/>
  
</DefaultLayout>


</template>

<script>
import DefaultLayout from './components/layouts/DefaultLayout.vue';


export default {
  name: 'App',
  components: {
    DefaultLayout,
  },
}
</script>

<style>

</style>
