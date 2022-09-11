<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">Delete Analysis</h3>

            <button id="close_btn" @click="onClose()" class="card-4">X</button>

            <br>
            <div class="contents_wrap">
                <h5>Are you certain you want to delete Analysis "{{analysis}}"?</h5>
                <!-- <TextInput ref="analysisName" placeholder='Analysis Name'></TextInput> -->
                <!-- <h4>Type</h4> -->
                <Button id="btn" @click="deleteAnalysis()" txt="Delete Analysis"></Button>
            </div>
           
        </div>
    </div>
   
      
</template>

<script>
import Button from './ui/Button.vue';
import TextInput from './ui/TextInput.vue';
import LogSelector from './LogSelector.vue';
import DimSelector from './DimSelector.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
        }
    },
    name: 'DelAnalysisDialog',
    components: {
    Button,
    TextInput,
    LogSelector,
    DimSelector
},
props: {
        // txt: String,
        // color: String
        // logname: String,
        // cubename: String,
        log: String,
        cubename: String,
        analysis: String
    },
    computed: {
        ...mapGetters({
            specLog: 'main/specLog',
        })
    },
    methods: {
        ...mapActions({
            delAnalysis: 'main/delAnalysis',
        }),
        async deleteAnalysis(){
            // let name = this.$refs['analysisName'].obj
            console.log(this.analysis)
            console.log(this.log)
            // let type = this.$refs['single_type'].classList.contains('selected_type')?'single':'comparison';
            // console.log(type)
            await this.delAnalysis(
                {analysis: this.analysis,
                cube: this.cubename,
                log: this.log
                })
            .then(() => {
            console.log("Donec Deleting Analysis" + this.analysis)
            this.$emit('close-del-analysis')
            })
            .catch((error) => {
            console.log(error)
            this.$emit('close-del-analysis')
            })
        },  
        onClose(){
            this.$emit('close-del-analysis')
        }
    },
    emits:['close-del-analysis'],
    created(){
        this.dim_selected = {};
    }
}
</script>

<style scoped>
    h3{
        border-bottom-right-radius: 10px;
        border-bottom-left-radius: 10px;
        margin: 0 auto;
    }
    #close_btn{
        position: absolute;
        top: 10px;
        left: 10px;
        background: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        height: 40px;
        width: 40px;
        font-size: large;
        color: gray;
    }
    #close_btn:hover{
        position: absolute;
        top: 10px;
        left: 10px;
        font-weight: bolder;
        background: #E6B656;
        border: none;
        border-radius: 10px;
        padding: 10px;
        height: 40px;
        width: 40px;
        font-size: large;
        color: white;
    }

    #new_cube_wrapper{
        position: absolute;
        width: 100%;
        top:0px;
        left:0px;
        background: #33333399;
        height: calc(100% + 100px);
        z-index: 20;
        transform: translate(0, -100px);
    }
    #cube_form{
        position: relative;
        margin: 0 50px;
        height: fit-content;
        min-height: 470px;
        top: 120px;
        background: #999999;
        border-radius: 10px;
        padding-bottom:  100px;
    }
    #btn{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }
    h4{
        color: white;
        background: #E6B656;
        border-radius: 10px;
        padding: 5px;
        width: 120px;
        margin: 10px auto 10px auto;
    }
    img{
        width: 35px;
        height: 35px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .type_wrapper{
        width: 200px;
        display: inline-block;
        background: lightgray;
        border-radius: 10px;
        height: 200px;
        position: relative;
    }
    .type_wrapper:first-of-type{
        
        margin: 10px 10px 10px 20px;
    }
    .type_wrapper:last-of-type{
        margin: 10px 10px 10px 20px;
    }
    .selected_type{
        background: white;
    }
    #coming_soon{
        position: absolute;
        top:-30px;
        right: -50px;
        rotate: 45deg;
        background: #E6B656;
        border-radius: 10px;
        padding: 5px;
        color: white;
    }

    /* Inout design */

</style>
