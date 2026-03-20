<template lang="html">
    <div class="w-full grid grid-cols-6 place-items-center mx-auto">
        <p  class="text-xl col-start-2 col-span-4 text-gray-400 my-10"> Sample sizes </p>
        <div class="w-full col-start-2 col-span-4 place-items-center mx-auto">
                <table class="w-full text-sm text-gray-500 dark:text-gray-400">
                    <thead class="text-sm text-gray-700 uppercase bg-white dark:bg-gray-700 dark:text-gray-400 rounded-full">
                        <tr>
                            <th scope="col" class="px-6 py-1 text-center">
                                Proportion in the general population (<i>p</i><sub>0</sub>)
                            </th>
                            <th scope="col" class="px-6 py-1 text-center">
                                Proportion in the studied disease (<i>p</i><sub>1</sub>)
                            </th>
                            <th scope="col" class="px-6 py-1 text-center">
                                Type I error rate (alpha)
                            </th>
                            <th scope="col" class="px-6 py-1 text-center">
                                Type II error rate (beta)
                            </th>
                            <th scope="col" class="px-6 py-1 text-center">
                                Required sample size
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-none ">
                            <td class="px-6 py-10 text-center">
                                <input class="px-6 border-none text-center" @input="updatep0" v-model="p0"/>
                            </td>
                            <td class="px-6 py-6 text-center">
                                <input class="px-6 border-none text-center" @input="updatep1" v-model="p1"/>
                            </td>
                            <td class="px-6 py-6 text-center">
                                <input class="px-6 border-none  text-center" @input="updatealpha" v-model="alpha"/>
                            </td>
                            <td class="px-6 py-6 text-center">
                                <input class="px-6 border-none  text-center" @input="updatebeta" v-model="beta"/>
                            </td>
                            <td class="px-6 py-6 border-none text-center">
                                {{ N1 }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
</template>


<script>


export default {
    name: "SampleSizeView",
    components: {},
    data() {
      return this.initialState()
    },
    mounted() {
      return this.calculateN1()
    },
    methods: {
        initialState() {
            return {
                p0: 0.05, p1: 0.15, alpha: 0.05, beta: 0.05, N1: null 
                }
        },
        updatep0() {
            this.calculateN1()
            return this.p0
        },
        updatep1() {
            this.calculateN1()
            return this.p1
        },
        updatealpha() {
            this.calculateN1()
            return this.alpha
        },
        updatebeta() {
            this.calculateN1()
            return this.beta
        },
        calculateN1(){
                var qnorm = function(p) {
                    // ALGORITHM AS 111, APPL.STATIST., VOL.26, 118-121, 1977.
                    // Computes z = invNorm(p)
            
                    p = parseFloat(p);
                    var split = 0.42;
            
                    var a0 = 2.50662823884;
                    var a1 = -18.61500062529;
                    var a2 = 41.39119773534;
                    var a3 = -25.44106049637;
                    var b1 = -8.47351093090;
                    var b2 = 23.08336743743;
                    var b3 = -21.06224101826;
                    var b4 =  3.13082909833;
                    var c0 = -2.78718931138;
                    var c1 = -2.29796479134;
                    var c2 =  4.85014127135;
                    var c3 =  2.32121276858;
                    var d1 =  3.54388924762;
                    var d2 =  1.63706781897;
            
                    var q = p - 0.5;
            
                    var r, ppnd;
            
                    if (Math.abs(q) <= split) {
                      r = q * q;
                      ppnd = q * (((a3*r+a2)*r+a1)*r+a0)/((((b4*r+b3)*r+b2)*r+b1)*r+1);
                    } else {
                      r = p;
                      if (q > 0) r = 1 - p;
                      if (r > 0) {
                        r = Math.sqrt(-Math.log(r));
                        ppnd = (((c3*r+c2)*r+c1)*r+c0)/((d2*r+d1)*r+1);
                        if (q < 0) ppnd = -ppnd;
                      }
                      else {
                        ppnd = 0;
                      }
                    }
            
                    return ppnd;
                }
                var z_alpha = qnorm(1-this.alpha/2)
                var z_beta = qnorm(1-this.beta)
                //console.log("z_alpha =", z_alpha)
                var q0 = 1 - this.p0
                var q1 = 1 - this.p1
                this.N1 = this.p0 * q0 * ( z_alpha + z_beta * Math.sqrt(this.p1*q1/(this.p0*q0)))**2 / (this.p1 - this.p0)**2
                this.N1 = Math.round(this.N1)

                return this.N1
            }
        }
}   
</script>
<style lang="">
    
</style>
