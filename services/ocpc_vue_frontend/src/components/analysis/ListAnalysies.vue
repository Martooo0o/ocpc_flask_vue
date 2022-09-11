
<template>
    <div id="wrapper" class="card-4">
        <h3 id="left_headline" class="card-4">Analyses</h3>

        <Button id="create_analysis" @click="onNewAnalysis()" txt="+ Create Analysis"></Button>
        <div id="items_wrapper">
            <div class="item" :key="analysis" v-for="analysis in analyses">
                <ItemAnalysis @delete-analysis="openDelAnalysisDialog" class="item_a" @select-analysis="onSelect" :name="analysis"></ItemAnalysis>

                 <div class="line"></div>
            </div>
        </div>
        <label id="no_analyses" v-if="analyses.length == 0">No Analyses</label>
    </div>
   
      
</template>

<script>
import Button from '@/components/ui/Button.vue';
import TextInput from '@/components/ui/TextInput.vue';
import LogSelector from '../LogSelector.vue';
import ItemAnalysis from './ItemAnalysis.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
            analyses : []
        }
    },
    components: {
    Button,
    TextInput,
    LogSelector,
    ItemAnalysis
},
props: {
        analyses: Array,
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
        },
        openDelAnalysisDialog(name){
            console.log("Delete " + name + "?");
            this.$emit('delete-analysis', name);
        },  
    },
    emits:['create_analysis','delete-analysis'],
    created(){
        console.log(this.analyses)
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
       width: calc(100% - 20px);
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
        width: 90%;
        background: #E6B656;
        height: 2px;
        position: absolute;
        bottom: 0px;
        left: 50%;
        transform: translateX(-50%);
    }
</style>
<style >
#items_wrapper .item:last-of-type .line{
        display: none;
    }
</style>
