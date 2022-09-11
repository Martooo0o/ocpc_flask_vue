
<template>
    <div id="left_right_wrap" class="card-4">
        <div id="left_wrap" class="wrap">
            <h3 id="left_headline" class="card-4">Attributes</h3>
            <div class="item_type" :key="`${ key }-${ index }`" v-for="(value, key, index) in this.nonSelectedAttrs" >
                <h5>{{key}}</h5>
                <div @click="dimSelected(key, attr)" class="item_attr" :key="attr" v-for="attr in this.nonSelectedAttrs[key]">
                    {{attr}}
                </div>
            </div> 
        </div>
        
        <div id="right_wrap" class="wrap">
            <h3 class="card-4">Selected</h3>
            <div class="item_type" :key="`${ key }-${ index }`" v-for="(value, key, index) in this.dim_selections" >
                <h5>{{key}}</h5>
                <div @click="dimUnselected(key, sel_value)" class="item_attr" :key="`${ sel_key }-${ sel_index }`" v-for="(sel_value, sel_key, sel_index) in this.dim_selections[key]">
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
    name: 'FreqDimSelector',
    components: {
    Button,
    TextInput,
    LogSelector
    },
    props: {
        attrs: Object, //all options available; key is object type or event, value is a list of attrs 
        selected: Object, //all selected options; key/values as in attrs
        notifySelection: Boolean
    },
    methods: {
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
             if(this.notifySelection !== undefined && this.notifySelection){
                this.$emit('selection-changed')
             }
        },
        dimUnselected(type, attr){
            console.log("clicki")
            console.log(type)
            console.log(attr)
            if(this.dim_selections[type] == null){
                console.log("No such attr has been selected")
                return
            }else{
                const index = this.dim_selections[type].indexOf(attr);
                if (index > -1) { // only splice array when item is found
                    this.dim_selections[type].splice(index, 1); // 2nd parameter means remove one item only
                }
            }  
            console.log(this.dim_selections)
            if(this.notifySelection !== undefined && this.notifySelection){
                this.$emit('selection-changed')
             }
        }
    },
    emits:['create_cube', 'selection-changed'],
    created(){
        console.log(this.attrs)
        console.log(this.selected)
        this.active = "name";
        this.dim_selections = this.selected;
        if(this.dim_selections === undefined){
                this.dim_selections = {}
        }
        console.log(this.dim_selections)
    },
     computed: {
        nonSelectedAttrs(){
            let nonSelected = {};
            let usedAttrs = this.attrs
            if(usedAttrs === undefined){
                usedAttrs = this.attrs['attrs']
            }
            console.log(usedAttrs)
            if(usedAttrs != undefined && this.dim_selections != undefined){
                console.log("INSIDE LOOP")
                for(let i = 0;i<Object.keys(usedAttrs).length;i++){
                    let key = Object.keys(usedAttrs)[i];
                        nonSelected[key] = [];
                        for(let j = 0;j<usedAttrs[key].length;j++){
                            console.log("INSIDE Inner LOOP")
                            let attr = usedAttrs[key][j]
                            if(this.dim_selections[key] === undefined || (this.dim_selections[key] != undefined && !this.dim_selections[key].includes(attr))){
                                nonSelected[key].push(attr);
                            }
                        }
                    
                }
            }
            console.log(nonSelected)
            return nonSelected;
        }
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
