
<template>
    <div id="wrap">
        <!-- <div id="dimens">Dimensions</div>
        <div class="vertical_line"></div>
        <div id="values_wrapper">Value-Pairs</div>
        <div class="vertical_line"></div>
        <div id="mat">Materialisation</div> -->

        <div class="item" :key="filter" v-for="filter in filters">
            <ItemFilter v-if="filter['type'] === 'dims'" class="item_a" @select-filter="onSelect" :filter="filter"></ItemFilter>
            <ItemFItemsFilter :filter="filter" v-if="filter['type'] === 'freq_items'" ></ItemFItemsFilter>
            <!-- <div class="line"></div> -->
        </div>
    </div>
</template>

<script>
import Button from '@/components/ui/Button.vue';
import TextInput from '@/components/ui/TextInput.vue';
import LogSelector from '../LogSelector.vue';
import ItemAnalysis from './ItemAnalysis.vue';
import ItemFilter from './ItemFilter.vue';
import ItemFItemsFilter from './ItemFItemsFilter.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
            filters : []
        }
    },
    components: {
    Button,
    TextInput,
    LogSelector,
    ItemAnalysis,
    ItemFilter,
    ItemFItemsFilter
},
props: {
        filters: Array,
    },
    computed: {
        ...mapGetters({
            analysesState: 'main/analyses',
        })
    },
    methods: {
        ...mapActions({
        openAnalysis: 'main/openAnalysis',
    }),
        async onSelect(analysis){
            await this.openAnalysis(analysis)
            .then(() => {
            console.log("Analysis Edited");
            this.$router.push('/analyses');
            })
            .catch((error) => {
            console.log(error)
            })
        },
        onNewAnalysis(){
           this.$emit('new-analysis')
        }
    },
    emits:['create_analysis', ],
    created(){
        console.log(this.analyses)
    }
}
</script>

<style scoped>

   #wrap{
       width: calc( 100% - 42px);
       /* border: 2px solid #E6B656; */
       border-radius: 10px;
       margin: 0 20px;
       
       position: relative;
       padding: 0px 0 10px 0;
   }
   #dimens{ 
    display: inline-block;
    padding: 10px;
    border-radius: 10px;
    width: 150px;
    position: absolute;
    left: 0;
    top: 0;
    margin-left: 20px;
    font-size: small;
}
#values_wrapper{
     display: inline-block;
    padding: 10px;
    width: calc(100% - 260px);
    position: absolute;
    font-size: small;
    left: 50%;
    top:0;
    transform: translateX(-50%);
}

#mat{
    display: inline-block;
    padding: 10px;
    border-radius: 10px;
    float: right;
    position: absolute;
    right: 0;
    top: 0px;
    width: 100px;
    text-align: center;
    margin-right: 20px;
    font-size: small;
}
   h3{
       border-bottom-right-radius: 10px;
       border-bottom-left-radius: 10px;
       margin: 0 auto;
   }
   #no_analyses{
    position:relative;
    left: 50%;
    display: block;
    width: fit-content;
    transform: translateX(-50%);
    margin-bottom: 20px;
   }
   
   /* #left_headline{
       border-top-left-radius: 5px
   } */
   #create_analysis{
       position: absolute;
       right: 5px;
       top: 5px;
   }
   .item{
       position: relative;
       width: 100%;
       margin: 30px 0 0 0;
   }
   .item_a{
       margin: 10px 10px;
   }
   /* .item:first-of-type .item_a{
       margin: 0 0 10px 0;
   }
   .item:last-of-type .item_a{
       margin: 10px 0 0px 0;
   } */
    .line{
        width: calc(100% - 20px);
        background: #cccccc;
        height: 1px;
        position: absolute;
        bottom: 0px;
        left: 50%;
        transform: translateX(-50%);
        margin: 0 0 0 10px;
        display: block;
    }

    #wrap .item:last-of-type .line{
        display: none;
    }
</style>
<style >
/* #items_wrapper .item:last-of-type .line{
        display: none;
    } */
</style>
