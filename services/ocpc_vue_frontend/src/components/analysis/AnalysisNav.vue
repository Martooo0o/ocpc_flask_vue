<template>
    <div id="wrap">
        <ul>
            <li class="item" :key="analysis" v-for="analysis in this.analysesState">
                <div @click="onClick(analysis)" v-bind:class="{'nav_btn_wrap': true,
                 'selected': this.currentAnalysis.name === analysis}">
                    <label>{{analysis}}</label>
                    <button class="card-4">X</button>
                </div >
            </li>
            <!-- <li>
                <div class="nav_btn_wrap">
                    <label>New Analysis</label>
                    <button class="card-4">+</button>
                </div >
            </li>  -->
             <!-- <li>
                    <div class="nav_btn_wrap selected">
                        <label>Analysis 1</label>
                        <button class="card-4">X</button>
                    </div >
                </li>
                <li>
                    <div class="nav_btn_wrap">
                        <label>Analysis 1 vs. Analysis 2</label>
                        <button class="card-4">X</button>
                    </div >
                </li> -->
        </ul>
    </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
export default {
    name: "AnalysisNav",
    props: {
        analysies: Array
    },
    computed: {
        ...mapGetters({
            analysesState: 'main/analyses',
            currentAnalysis: 'main/currAnalysis'
        }), 
    },
    methods: {
        ...mapActions({
            openAnalysis: 'main/openAnalysis',
        }),
        async onClick(analysis){
            await this.openAnalysis(analysis);
        }
    }
}
</script>
<style scoped>
#wrap{
     background: #888888;
}
ul {
   list-style-type: none;
   margin: 0;
   border-bottom: 1px solid black;
   width: fit-content;
   padding: 0;
}
li{
    display: inline-block;
    border-left: 1px solid black;
    border-right: none;
    background: #CCCCCC;
}
li:hover{
    background: #E6B656;
}
li:hover label{
    color: white;
}
li:last-child{
    border-right: 1px solid black;
}
.nav_btn_wrap{
    padding: 5px;
}
.nav_btn_wrap label{
    margin: 0 10px;
}
.selected{
    background: #E6B656;
}
.selected label{
    color: white;
    font-weight: bold;
}
button{
    background: white;
    border-radius: 25px;
    border: none;
}
button:hover{
    background: red;
    color: white;
}

</style>
