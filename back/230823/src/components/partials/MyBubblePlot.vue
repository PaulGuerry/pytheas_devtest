<template lang="html">


    <div class="w-full grid place-items-center"> 
        <div class="w-3/4 chart-container">
            <VuePlotly :data="bubbleData" :layout="bubbleLayout" :config="plotConfig"></VuePlotly>
        </div>
    </div>
        
</template>

<script>
import { VuePlotly } from 'vue3-plotly';

export default {
    name: "BubblePlot",
    components: { VuePlotly },
    data: () => ({
            plotConfig:{displayModeBar: false} 
    }),
    props: {
        bubbleData: {
            type: Array,
            required: true,
            default: () => [{
                type: 'scatter',
                x: [1, 2, 3],
                y: [10, 10, 10],
                mode: 'markers',
                marker: {
                    size: [14, 200, 2000],
                    color: ["#0284c788", "#f9731688", "#05966988"],
                    sizemode: 'area',
                    sizeref: 0.05
                },
                hoverinfo: 'none'
            }],
        },
        bubbleLayout: {
            type: Object,
            required: true,
            default: () => ({
                title: false,
                showlegend: false,
                yaxis: {
                    showgrid: false,
                    zeroline: false,
                    showticklabels: false,
                    range: [9.5, 10.5]
                },
                xaxis: {
                    showgrid: false,
                    zeroline: false,
                    showticklabels: false,
                    range:[0, 4]
                },
                autosize: true,
                margin: {t: 10, b: 10, l: 10, r: 10}
            })
        }
    }
}
</script>

<style lang="">
    
</style>