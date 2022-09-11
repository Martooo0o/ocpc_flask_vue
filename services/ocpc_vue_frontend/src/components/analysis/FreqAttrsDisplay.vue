
<template>
    <div id="left_right_wrap">
        <div class="item" :key="dimen" v-for="dimen in Object.keys(getDimens)">
            <h4>{{dimen}}</h4>
            <div class="item_wrapper" :key="dimenVal" v-for="dimenVal in getDimens[dimen]">
                {{dimenVal}}
            </div>
        </div>
        <div id="edit_btn" @click="this.$emit('edit-freq-attrs')"><p>Attributes</p></div>
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import TextInput from '../ui/TextInput.vue';
import LogSelector from '../LogSelector.vue';
// import { defineComponent } from '@vue/composition-api'
export default {
    // data(){
    //      return {
    //         dimens: this.dimens
    //     }
    // },
    name: 'FreqAttrsDisplay',
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
    emits:['edit-freq-attrs'],
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
       width: calc( 100% - 10px);
       height: calc(100% - 10px);
       /* border: 2px solid #E6B656; */
        align-content: flex-start;
       margin: 10px 0px 0px 10px;
       border-radius: 10px;
       background: #DDDDDD;
       overflow-x: scroll;
       position:relative;
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

   #edit_btn{
    width: 30px;
    height: 100%;
    position: absolute;
    right: 0px;
    writing-mode: vertical-rl;
    text-orientation: sideways;
    transform: rotate(180deg);
    background: #E6B656;
    border-bottom-right-radius: 10px;
    border-top-right-radius: 10px;
   }
   #edit_btn p{
    margin: 0 auto;
    width: fit-content;
    padding: 0;
    color: white;
    font-weight: bold;
    transform: translateX(-5px)
   }
   #edit_btn:hover{
    background: #F6C666;
   }

   /* #left_headline{
       border-top-left-radius: 5px
   } */
</style>
