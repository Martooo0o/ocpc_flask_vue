
<template>
    <div id="left_right_wrap" class="card-4">
        <div id="left_wrap" class="wrap">
            <h3 id="left_headline" class="card-4">Attributes</h3>
            <div class="item_type" :key="`${ key }-${ index }`" v-for="(value, key, index) in log.attrs" >
                <h5>{{key}}</h5>
                <div @click="dimSelected(key, attr)" class="item_attr" :key="attr" v-for="attr in log.attrs[key]">
                    {{attr}}
                </div>
            </div> 
        </div>
        
        <div id="right_wrap" class="wrap">
            <h3 class="card-4">Selected</h3>
            <div class="item_type" :key="`${ key }-${ index }`" v-for="(value, key, index) in log.attrs" >
                <h5>{{key}}</h5>
                <div class="item_attr" :key="`${ sel_key }-${ sel_index }`" v-for="(sel_value, sel_key, sel_index) in this.dim_selections[key]">
                    {{sel_value}}
                </div>
            </div> 
        </div>
    </div>
   
      
</template>

<script>
import Button from './ui/Button.vue';
import TextInput from './ui/TextInput.vue';
import LogSelector from './LogSelector.vue';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
            dim_selections: this.dim_selections
        }
    },
    name: 'NewCubeDialog',
    components: {
    Button,
    TextInput,
    LogSelector
},
props: {
        // txt: String,
        // color: String
        log: Object,
    },
    methods: {
        onCreateCube(){
            if(this.active === 'name'){
                this.active = "log";
            }else if(this.active === 'log'){
                this.active = "dim";
            }else{
                this.$emit('create_cube', "cube")
            }
        },
        onSelectNav(nav){
            this.active = nav;
        },
        dimSelected(type, attr){
            console.log("clicki")
            console.log(type)
            console.log(attr)
            if(this.dim_selections[type] == null){
                this.dim_selections[type] = [];
                 console.log("Type is null")
            }
             this.dim_selections[type].push(attr);
             console.log(this.dim_selections)
        }
    },
    emits:['create_cube'],
    created(){
        this.active = "name";
        this.dim_selections = {};
    }
}
</script>

<style scoped>
   #left_right_wrap{
       width: calc( 100% - 42px);
       height: 300px;
       border: 2px solid #E6B656;
       margin: 0 20px 20px 20px;
       border-radius: 10px;
       background: white;
   }
   #left_right_wrap .wrap{
       display: inline-block;
       height: 100%;
   }
    #left_wrap{
       border-right: 2px solid #E6B656;
       width: calc( 50% - 1px);
       display: inline-block;
       float: left;
   }
   #right_wrap{
        width: calc( 50% - 1px);
         display: inline-block;
       clear: left;
   }
   h3{
       border-bottom-right-radius: 10px;
   }
   #left_headline{
       border-top-left-radius: 5px
   }
   h5{
       margin: 5px;
   }
   .item_type{
       display: block;
       width: 100%;
       height: fit-content;
       clear: both;
   }
   .item_attr{
       display: block;
       width: fit-content;
       height: fit-content;
       float: left;
       margin: 0px 5px 5px 5px;
       background: #E6B656;
       border-radius: 10px;
       padding: 5px;
   }
</style>
