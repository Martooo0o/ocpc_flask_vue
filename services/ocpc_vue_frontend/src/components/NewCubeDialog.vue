<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">New Cube</h3>

            <button id="close_btn" @click="onClose()" class="card-4">X</button>

            <nav class="card-4">
                <a :class="{active: active==='name'}" @click="onSelectNav('name')">Name</a>
                <a :class="{active: active==='log'}" @click="onSelectNav('log')">Log</a>
                <a :class="{active: active==='dim'}" @click="onSelectNav('dim')">Dimensions</a>
            </nav>

            <br>
            <div class="contents_wrap">
                <TextInput ref="cubeName" :input="new_cube_name" placeholder='Cube Name' v-if="active === 'name'"></TextInput>
                <LogSelector @select-log="onLogSelected" v-else-if="active === 'log'" :logs="logs"></LogSelector>
                <DimSelector ref="selections" v-else-if="active === 'dim'" :log="specLog"></DimSelector>
            </div>
            <Button id="btn" @click="onCreateCube()" txt="Create Cube"></Button>
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
        logs: Array,
    },
    computed: {
        ...mapGetters({
            specLog: 'main/specLog',
        })
    },
    methods: {
        ...mapActions({
            getSpecLog: 'main/getSpecLog'
        }),
        onCreateCube(){
            if(this.active === 'name'){
                this.active = "log";
                this.new_cube_name = this.$refs['cubeName'].obj;
                console.log(this.new_cube_name)
            }else if(this.active === 'log'){
                if(this.selected_log != null){
                    this.getSpecLog(this.selected_log);
                    console.log(this.specLog)
                    this.active = "dim";   
                }else{
                    // TODO display error
                }
            }else{
                console.log(this.$refs['selections'].dim_selections)
                this.$emit('create_cube', this.new_cube_name, this.selected_log, this.$refs['selections'].dim_selections)
            }
        },
        onLogSelected(log){
            this.selected_log = log
        },
        onSelectNav(nav){
            this.active = nav;
            // if(nav === 'name'){
            //     console.log(this.$refs['cubeName'])
            //     this.$refs['cubeName'].obj = this.new_cube_name;
            // }
        },
        onClose(){
            this.$emit('close-new-cube')
        }
    },
    emits:['create_cube'],
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
    #home_icon{
        width: 20px;
        height: 20px;
    }
    header{
        display: flex;
        justify-content: space-between;
        align-content: center;
        margin: 0 0 20px 0;
        background-color: #333333;
        vertical-align: middle;
        position: fixed;
        width: 100%;
        top:0px;
        z-index: 10;
    }
    #ocel_logo{
        widows: 100px;
        height: 100px;
        scale: 0.75;
    }

    nav {
    width: fit-content;
    font-size: 20px;
    text-align: center;
    position: relative;
    height: 59px;
    border-radius: 10px;
    display: block;
    border: 2px solid #E6B656;
    padding: 0;
    margin: 20px auto 0 auto;
    background: #E6B656;
    }
    nav a:nth-of-type(3n+1){
        border-top-left-radius: 10px;
        border-bottom-left-radius: 10px;
    }
    nav a:nth-last-of-type(3n+1){
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }

    nav a{
        background-color: white;
        width: 100px;
        text-decoration: none;
        color: lighgray;
        margin: 0;
        position: relative;
        top: 50%;
        -ms-transform: translateY(-50%);
        transform: translateY(-50%);
        display: inline-block;
        padding: 1rem 2rem;
        border-left: 1px solid var(--color-border); 
    }

    nav a.active {
    color: var(green);
    font-weight: bolder;
    background-color: #E6B656;
    color: white;
    }

    nav a:hover {
    background-color: #E6B656;
    color:white;
    }

    nav a:first-of-type {
    border: 0;
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
    /* #contents_wrap{
        margin-bottom: 40px;
    } */
    #btn{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
    }

    /* Inout design */

</style>
