<template>

<div class="container my-10">
    <div class="row">
        <div class="col">
            <p class="pt-[5px] mt-10 mb-5 text-2xl text-left text-blue-700 font-light"> Patient list </p>
            <p class="my-2 italic">List of reported patients with variants of the selected gene.</p>
        </div>
        <div class="row">
            <div class="col">
                <table class="table table-hover text-center table-striped">
                    <thead class="bg-light my-4">
                        <tr>
                            <th>Gene</th>
                            <th>Patient</th>
                            <th>Sex</th>
                            <th>DOI</th>
                            <th>Lab findings at diagnosis</th>
                            <th>Symptoms</th>
                            <th>Transplant</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="patient in filteredPatientList" :key="patient.id">
                            <td> {{ patient.gene }} </td>
                            <td> {{ patient.patients }} </td>
                            <td> {{ patient.sex }} </td>
                            <td > <a :href="patient.doi"  class="hover:text-blue-700 transition duration-300 ease-in-out"> {{ patient.doi }} </a> </td>
                            <td> {{ patient.labfindingsatdiagnosis }} </td>
                            <td> {{ patient.symptoms }} </td>
                            <td> {{ patient.transplantorgan }} </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>



</template>


<script>
import myPatientData from '@/assets/patientData.json'
export default {
    name: "PatientList",
    data() {
        return {
            patientData: myPatientData
        }
    },
    computed: {
        filteredPatientList() {
            let tempList = this.patientData;
            console.log(this.gene)
            tempList = tempList.filter((item) => {return (item.gene == this.gene)
            })
            return tempList;
        },
    },
    props: {
    gene: {
        type: String,
        required: true,
        default: "ZFYVE19" 
        }
    },
}

</script>


<style>

</style>