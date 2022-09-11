<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">New Analysis</h3>

            <button id="close_btn" @click="onClose()" class="card-4">X</button>

            <br>
            <div class="contents_wrap">
                <TextInput ref="analysisName" placeholder='Analysis Name'></TextInput>
                <h4>Type</h4>
                <div id="types_wrapper" >
                    <div class="type_wrapper selected_type" ref="single_type">
                        <h5>Single</h5>
                        <img id="img" src="@/assets/cube.png" alt="">
                    </div>
                    <div class="type_wrapper" ref="comparison_type">
                        <h5>Comparison</h5>
                        <img id="img" src="@/assets/cube.png" alt=""/>
                        <p id="coming_soon">Coming Soon</p>
                    </div>
                </div>
            </div>
           
            <Button id="btn" @click="onCreateAnalysis()" txt="Create Analysis"></Button>
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
    name: 'NewCubeDialog',
    components: {
    Button,
    TextInput,
    LogSelector,
    DimSelector
},
props: {
        // txt: String,
        // color: String
        logname: String,
        cubename: String
    },
    computed: {
        ...mapGetters({
            specLog: 'main/specLog',
        })
    },
    methods: {
        ...mapActions({
            createAnalysis: 'main/createAnalysis'
        }),
        async onCreateAnalysis(){
            let name = this.$refs['analysisName'].obj
            console.log(name)
            let type = this.$refs['single_type'].classList.contains('selected_type')?'single':'comparison';
            console.log(type)
            await this.createAnalysis(
                {name: name,
                type: type,
                logname: this.logname,
                cube: this.cubename})
            .then(() => {
            console.log("Donec Creating Analysis")
            this.$emit('close-new-analysis')
            })
            .catch((error) => {
            console.log(error)
            this.$emit('close-new-analysis')
            })
        },  
        onClose(){
            this.$emit('close-new-analysis')
        }
    },
    emits:['create-analysis', 'close-new-analysis'],
    created(){
        this.active = "name";
        this.new_cube_name = "";
        this.selected_log = "";
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
