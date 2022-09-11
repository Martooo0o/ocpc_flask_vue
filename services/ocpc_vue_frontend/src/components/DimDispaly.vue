
<template>
    <div id="left_right_wrap" class="card-4">
        <h3 id="left_headline" class="card-4">Dimensions</h3>
        
        <div class="item" :key="dimen" v-for="dimen in Object.keys(getDimens)">
            <h4>{{dimen}}</h4>
            <div class="item_wrapper" :key="dimenVal" v-for="dimenVal in getDimens[dimen]">
                {{dimenVal}}
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
    // data(){
    //      return {
    //         dimens: this.dimens
    //     }
    // },
    name: 'DimDispaly',
    components: {
        Button,
        TextInput,
        LogSelector
    },
    props: {
        dimens: Object
    },
    methods: {
    },
    emits:['create_cube'],
    created(){
        this.active = "name";
        console.log(this.dimens)
    },
    computed:{
        getDimens(){
            if(this.dimens === undefined){
                return {}
            }else{
                return this.dimens;
            }
        }
    }
}

</script>

<style scoped>
   #left_right_wrap{
       width: calc( 100% - 42px);
       height: 300px;
       /* border: 2px solid #E6B656; */
        align-content: flex-start;
       margin: 0 20px 20px 20px;
       border-radius: 10px;
       background: #DDDDDD;
       overflow-y: scroll;
       overflow-x: hidden;
   }
    #left_wrap{
       border-right: 2px solid #E6B656;
       width: fit;
   }
   #right_wrap{
        width: calc( 50% - 1px);
   }
   h3{
       border-bottom-right-radius: 10px;
       border-bottom-left-radius: 10px;
       margin: 0 auto;
   }
   h4{
       margin: 10px auto;
       text-align: center;
   }
   .item{
       display: inline-block;
       background: white;
       height: calc(100% - 56px);
       overflow-y: auto;
       margin: 10px 0px 10px 10px;
       border-radius: 10px;
   }
   .item_wrapper{
       margin: 10px;
       padding: 5px;
       background: #CCCCCC;
       border-radius: 10px;
   }
   .item:last-of-type{
       margin: 10px
   }

   /* #left_headline{
       border-top-left-radius: 5px
   } */
</style>
