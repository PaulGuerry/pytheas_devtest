<template lang="html">
    <progress :value="currentPercent" max="100" class="rounded">Loading...</progress>
</template>
<script>

export default {
    name: 'ProgressComponent',
    props: {
    currentCount: {
        type: Number,
        required: true,
        default: 0 
        },
    currentPercent: {
        type: Number,
        required: true,
        default: 0
        }
    },
    mounted() {
        //setTimeout is required so that the browser renders before the function fired on emission in the parent component runs
        //source: https://stackoverflow.com/questions/47634258/what-is-nexttick-and-what-does-it-do-in-vue-js/47636157#47636157
        setTimeout(() => {this.$emit('emittedCount', this.currentCount + 1), 50})
    }
}
</script>
<style scoped lang="css">
    progress {
        border-radius: 7px; 
        width: 80%;
        height: 12px;
        margin-left: 0%;
        box-shadow: 1px 1px 4px rgba( 0, 0, 0, 0.2 );
    }
    progress::-webkit-progress-bar {
        background-color: gray;
        border-radius: 7px;
    }
    progress::-webkit-progress-value {
        background-color: #3b82f6;
        border-radius: 7px;
        box-shadow: 1px 1px 5px 3px #a5b4fc;
    }
</style>