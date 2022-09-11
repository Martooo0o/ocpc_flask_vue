
<template>
    <div class="item card-4" :key="visualisation" v-for="visualisation in listVisualisations">
         <div .class="dummy"></div>
         <div v-if="JSON.stringify(visualisation) === '{}'" class="item_a" id="new_vis" @click="this.$emit('new-vis')">
            <img src="@/assets/plus_icon-3.png"/>
         </div>
        <Visualisation v-if="JSON.stringify(visualisation) !== '{}'" class="item_a" 
        @select-filter="onSelect" :visualisation="visualisation" 
        @get-flat-log="getFlatLog" 
        @get-dfg="getDFG" 
        @edit-freq-attrs="editFreqAttrs(visualisation.index)" 
        @get-freq-items="getFreqItems"
        @get-ass-rules="getAssRules"
        @dfg_props_changed="(props) => this.$emit('dfg_props_changed', props, visualisation.index)"
        @fitems_props_changed="(props) => this.$emit('fitems_props_changed', props, visualisation.index)"
        @assoc_rules_props_changed="(props) => this.$emit('assoc_rules_props_changed', props, visualisation.index)"
        ></Visualisation>
        <!-- <div class="line"></div> -->
    </div>
</template>

<script>
import Button from '@/components/ui/Button.vue';
import TextInput from '@/components/ui/TextInput.vue';
import LogSelector from '../LogSelector.vue';
import ItemAnalysis from './ItemAnalysis.vue';
import ItemFilter from './ItemFilter.vue';
import Visualisation from './Visualisation.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",

        }
    },
    components: {
    Button,
    TextInput,
    LogSelector,
    ItemAnalysis,
    ItemFilter,
    Visualisation
},
props: {
        visualisations: Array,
    },
    computed: {
        ...mapGetters({
            analysesState: 'main/analyses',
        }),
        listVisualisations(){
            // ES6 way
            const listCopy = [...this.visualisations];
            
            //add index to obj to know where to store data when making calls
            for(var i = 0;i< this.visualisations.length;i++){
               listCopy[i]['index']=i;         
            }

            listCopy.push({})
            console.log(listCopy)
            return listCopy
        },
    },
    methods: {
        ...mapActions({
        openAnalysis: 'main/openAnalysis',
    }),
        editFreqAttrs(index){
            console.log(index)
            this.$emit('edit-freq-attrs', index)
        },
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
        },
        getFlatLog(index){
            console.log(index)
             this.$emit('get-flat-log', index)
        },
        getDFG(index){
            console.log(index)
            this.$emit('get-dfg', index)
        },
        getFreqItems(index){
            console.log(index)
            this.$emit('get-freq-items', index)
        },
        getAssRules(index){
            console.log(index)
            this.$emit('get-ass-rules', index)
        }
    },
    emits:['new-vis', 'get-flat-log', 'edit-freq-attrs', 'get-freq-items', 'dfg_props_changed'],
    created(){
        console.log(this.visualisations)
        console.log(typeof(this.visualisations))
    }
}
</script>

<style scoped>
   #wrapper{
       width: calc( 100% - 42px);
       /* border: 2px solid #E6B656; */
       border-radius: 10px;
       margin: 0 20px;
       background: #DDDDDD;
       padding-bottom: 2.5px;
       position: relative;
   }
   #items_wrapper{  
       margin: 20px 10px 10px 10px;
       border-radius: 10px;
       /* border: 2px solid #E6B656; */
       background: white;
       /* text-decoration-color: white; */
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
       width: calc(50% - 80px);
        /*  This adds wifht:height aspect ration of 1:1 */
       padding-top: calc(50% - 80px);
       background: #CCCCCC;
       margin: 20px;
       border-radius: 10px;
       display: inline-block;
   }

   .dummy {
        margin-top: 100%;
    }
   .item_a{
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: silver;
         border-radius: 10px;
   }
   #new_vis img{
       width: 150px;
       position: absolute;
       top: 50%;
       left: 50%;
       transform: translate(-50%, -50%);
   }
    #new_vis:hover{
        background: #999999 ;
   }

    @media only screen and (max-width: 800px) {
        .item {
            width: calc(100% - 80px);
            background: lightblue;
            padding-top: calc(100% - 80px);
        }
    }
</style>
<style >
#items_wrapper .item:last-of-type .line{
        display: none;
    }
</style>
