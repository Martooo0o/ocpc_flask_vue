<template>
    <div id="inner_analysis_wrapper">
        <h3 class="card-4">{{this.currentAnalysis.name}}</h3>

        <div class="half card-4" style="margin-right: 10px">
            <label class="info_label">Source Cube:</label><span>{{this.currentAnalysis.cube.name}}</span>
        </div>
        <div class="half card-4">
            <label class="info_label">Source Log:</label><span>{{this.currentAnalysis.sourcelog}}</span>
        </div>

        <div class="headline_wrapper">
            <h4>Filters</h4>
            <div id="line"></div>
        </div>

        <ListFilters :filters="filters" v-if="filters.length !== 0"></ListFilters>
        
        <h5 v-if="filters.length == 0" >None</h5>
        <Button id="add_filter_btn" txt="Add Filter" @click="newFilter()"></Button>

        <FilterTypeDialog @close-new-filter-type="closeNewFilterType" @filter-type-selected="onFilterTypeSelected" v-if="new_filter_type"></FilterTypeDialog>
        <DimFilterDialog @close-new-filter="closeNewFiler" :dimens="this.currentAnalysis.cube.dimens" @create-filter="onCreateDimsFilter" v-if="new_filter"></DimFilterDialog>
        <ItemsetFilterDialog @new_params_for_fitems_filter="getFItemsForFilter" :tableData="aFilterData" @close-new-itemset-filter="closeNewItemsetFiler" :dimens="this.currentAnalysis.cube.dimens" @create-filter="onCreateFItemsFilter" v-if="new_itemset_filter"></ItemsetFilterDialog>

        <br>

        <div class="headline_wrapper">
            <h4>Visualisations</h4>
            <div id="line"></div>
        </div>

        <ListVisualisations 
            :visualisations="this.currentAnalysis.visualisations" 
            @new-vis="this.new_vis=true" 
            @get-flat-log="getFlatLog" 
            @get-dfg="getDFG" 
            @edit-freq-attrs="editFreqVisAttrs" 
            @get-freq-items="getFreqitems" 
            @get-ass-rules="getAssRules" 
            @dfg_props_changed="saveDFGProps"
            @fitems_props_changed="saveFItemsProps"
            @assoc_rules_props_changed="saveAssocRulesProps"
            ></ListVisualisations>

        <VisualisationsDialog v-if="new_vis" @close-new-vis="new_vis=false" @add-vis="onCreateVis"></VisualisationsDialog>

        <DialogFreqVisAttrs :index="this.editing_vis" v-if="edit_freq_attrs_vis" @save_item_attrs="saveFreqItemAttrs" @close-edit-freq-attrs="edit_freq_attrs_vis=false"></DialogFreqVisAttrs>

        <!-- <nav class="card-4">
            <a :class="{active: active==='logs'}" @click="onSelectNav('name')">Logs</a>
            <a :class="{active: active==='dfg'}" @click="onSelectNav('log')">DFG</a>
            <a :class="{active: active==='freq'}" @click="onSelectNav('dim')">Freq. I-sets</a>
        </nav> -->
    </div>
</template>

<script>
import AnalysisNav from './AnalysisNav.vue'
import Select from '../ui/Select.vue'
import Button from '../ui/Button.vue'
import DimFilterDialog from '../DimFilterDialog.vue'
import ListFilters from '../analysis/ListFilters.vue'
import ListVisualisations from '../analysis/ListVisualisations.vue'
import VisualisationsDialog from '../analysis/VisualisationsDialog.vue'
import ListItemsetFilters from '../analysis/ListItemsetFilters.vue'
import ItemsetFilterDialog from '../analysis/ItemsetFilterDialog.vue'
import { mapActions, mapGetters } from 'vuex';
import DialogFreqVisAttrs from './DialogFreqVisAttrs.vue'
import FilterTypeDialog from './FilterTypeDialog.vue'
// import { emit } from 'process';
export default {
  components: { AnalysisNav, Select, Button, DimFilterDialog, ListFilters, ListVisualisations, VisualisationsDialog, ItemsetFilterDialog, ListItemsetFilters, DialogFreqVisAttrs, FilterTypeDialog},
    name: "Analysis",
    props: {
        txt: String,
        color: String
    },
    computed: {
        ...mapGetters({
            currentAnalysis: 'main/currAnalysis',
            currCube: 'main/specCube',
            aFilterData: 'main/currAnalysisFilterData',
        }),
        filters(){
            console.log(this.currentAnalysis.filters)
            return this.currentAnalysis.filters
        }
    },
    methods: {
        ...mapActions({
            setFilters: 'main/setAFilters',
            setVis: 'main/setAVis',
            getFLog: 'main/getFlattenedLog',
            getDFGServer: 'main/getDFG',
            getFreqItemsServer: 'main/getFreqItemsInFilter',
            getAssRulesServer: 'main/getAssRules'
        }),
        onClick(){
            console.log("Click")
        },
        onFilterTypeSelected(fType){
            //stop the new filter type dialog
            this.new_filter_type = false;
            if(fType === 'dims'){
                this.new_filter = true;
            }
            else if(fType === 'freq_items'){
                this.new_itemset_filter = true;
            }
        },
        closeNewFilterType(){
            this.new_filter_type = false;
        },
        newFilter(){
            this.new_filter_type = true;
        },
        newItemsetFilter(){
            this.new_itemset_filter = true;
        },
        async getFItemsForFilter(params){
            this.new_filter = false;
            console.log(params)
            // let newF = {'type': 'dims', 'mat': mat, 'selections': selections, 'type_dim1': type1,'dim1': dim1, 'type_dim2': type2, 'dim2': dim2}
            await this.getFreqItemsServer(Object.assign({},{"analysisname": this.currentAnalysis.name}, params))
        },
        async onCreateDimsFilter(type1, dim1, type2, dim2, selections, mat){
            this.new_filter = false;
            let newF = {'type': 'dims', 'mat': mat, 'selections': selections, 'type_dim1': type1,'dim1': dim1, 'type_dim2': type2, 'dim2': dim2}
            await this.setFilters({"analysis": this.currentAnalysis.name,
                "filter": newF})
        },
        async onCreateFItemsFilter(params){ // CHECK WHAT PARAMS ARE NEEDED FOR HERE
            this.new_itemset_filter = false;
            let newF = {'type': 'freq_items', 'selections': params['selections'], 'attrs': params['attrs']}
            await this.setFilters({"analysis": this.currentAnalysis.name,
                "filter": newF})
        },
        async onCreateVis(type){
            this.new_vis = false;
            console.log(type)

            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }
            console.log(eA)
            let newV = {'type': type}
            
            if(type === 'dfg'){
                newV['dfg_type'] = 'Frequency'
                newV['edge_threshold'] = 0
                newV['act_threshold'] = 0
            }else if(type === 'freq_items'){
                newV['attrs'] = {}
                newV['set_size'] = 0
                newV['min_supp'] = 0.01
            }else if(type === 'ass_rules'){
                newV['attrs'] = {}
                newV['set_size'] = 0
                newV['min_supp'] = 0.01
                newV['min_conf'] = 0.01
                newV['min_lift'] = 0.01
            }

            eA['visualisations'].push(newV)
            console.log(eA)
            // eA['visualisations'] = JSON.stringify(eA['visualisations'])
            // console.log(eA)

            await this.setVis(eA)
        },
        async saveFreqItemAttrs(selections){
            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
                console.log("SOMETHING IS WRONG NO VISUALISATIONS FOUND")
                return ;
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }
            console.log(eA)
            console.log("The Index: " + this.editing_vis)

            eA['visualisations'][this.editing_vis]['attrs'] = selections;

            this.edit_freq_attrs_vis = false;

            await this.setVis(eA)
        },
        async saveFItemsProps(params, index){
            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
                console.log("SOMETHING IS WRONG NO VISUALISATIONS FOUND")
                return ;
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }
            console.log(eA)
            console.log("The Index: " + index)
            
            if(Object.keys(params).includes('set_size')){
                eA['visualisations'][index]['set_size'] = params['set_size'];
            }
            if(Object.keys(params).includes('min_supp')){
                eA['visualisations'][index]['min_supp'] = params['min_supp'];
            }

            this.edit_freq_attrs_vis = false;

            await this.setVis(eA)
        },
        async saveAssocRulesProps(params, index){
            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
                console.log("SOMETHING IS WRONG NO VISUALISATIONS FOUND")
                return ;
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }
            console.log(eA)
            console.log("The Index: " + index)
            
            if(Object.keys(params).includes('set_size')){
                eA['visualisations'][index]['set_size'] = params['set_size'];
            }
            if(Object.keys(params).includes('min_supp')){
                eA['visualisations'][index]['min_supp'] = params['min_supp'];
            }
            if(Object.keys(params).includes('min_conf')){
                eA['visualisations'][index]['min_conf'] = params['min_conf'];
            }
            if(Object.keys(params).includes('min_lift')){
                eA['visualisations'][index]['min_lift'] = params['min_lift'];
            }

            this.edit_freq_attrs_vis = false;

            await this.setVis(eA)
        },
        async saveDFGProps(params, index){
            let eA = {}
            eA['name'] = this.currentAnalysis['name']
            if(this.currentAnalysis['visualisations'] == []){
                eA['visualisations'] = []
                console.log("SOMETHING IS WRONG NO VISUALISATIONS FOUND")
                return ;
            }else{
                console.log(this.currentAnalysis['visualisations'])
                eA['visualisations'] = this.currentAnalysis['visualisations']
                console.log(typeof(eA['visualisations']))
            }
            console.log(eA)
            console.log("The Index: " + index)
            if(Object.keys(params).includes('act_threshold')){
                eA['visualisations'][index]['act_threshold'] = params['act_threshold'];
            }
            if(Object.keys(params).includes('edge_threshold')){
                eA['visualisations'][index]['edge_threshold'] = params['edge_threshold'];
            }
            if(Object.keys(params).includes('dfg_type')){
                eA['visualisations'][index]['dfg_type'] = params['dfg_type'];
            }

            this.edit_freq_attrs_vis = false;

            await this.setVis(eA)
        },
        
        closeNewFiler(){
            this.new_filter = false;
        },
        closeNewItemsetFiler(){
            this.new_itemset_filter = false;
        },
        async getFlatLog(index){
            console.log(index)
            let params = {'analysisname': this.currentAnalysis.name, 'vis_index': index}
            console.log(params)
            await this.getFLog(params)

            // commit('setCurAVisLog', {'data': data, 'index': params.vis_index})
        },
        async getDFG(index){
            console.log(index)
            let params = {'analysisname': this.currentAnalysis.name, 'vis_index': index}
            console.log(params)
            await this.getDFGServer(params)
        },
        editFreqVisAttrs(index){
            console.log('show freq vis attrs')
            this.edit_freq_attrs_vis = true;
            this.editing_vis = index;
        },
        async getFreqitems(index){
            console.log(index)
            let params = {'analysisname': this.currentAnalysis.name, 'vis_index': index}
            console.log(params)
            await this.getFreqItemsServer(params)
        },
        async getAssRules(index){
            console.log(index)
            let params = {'analysisname': this.currentAnalysis.name, 'vis_index': index}
            console.log(params)
            await this.getAssRulesServer(params)
        }
    },
    created(){
        console.log(this.currentAnalysis)
        this.new_filter_type = false;
        this.new_filter = false;
        this.new_vis = false;
        this.new_itemset_filter = false;
        this.edit_freq_attrs_vis = false;

        //used for visualisations that require a popup to selet certain properties (FreqItemsVis, AssocRulesVis)
        this.editing_vis = -1; 
    },
    data() {
        return {
            new_filter_type: this.new_filter_type,
            new_filter: this.new_filter,
            new_vis: this.new_vis,
            new_itemset_filter: this.new_itemset_filter,
            edit_freq_attrs_vis: this.edit_freq_attrs_vis,
            editing_vis: this.editing_vis
        }
	},
}
</script>

<style scoped>
h3{
    border-bottom-right-radius: 10px;
    border-bottom-left-radius: 10px;
    margin: 0 auto;
    min-width: 100px;
    max-width: 150px;
    text-align: center;
}

h5{
    margin: 5px 0 10px 0;
}
.info_label{
    width: fit-content;
    color: black;
    display: inline-block;
    width: fit-content;
    padding: 5px 10px;
    background-color: #CCCCCC;
    width: fit-content;
    z-index: 5;
    border-radius: 8px;
    padding: 10px 10px;
}
span{
    margin-left: 20px;
    margin-right: 20px;
}
.half{
    width: calc( 50% - 30px);
    display: inline-block;
    border: 1px solid#CCCCCC;
    border-radius: 10px;
    position: relative;
    text-align: left;
    margin: 20px 0 0px 0;
}
#inner_analysis_wrapper{
    height: fit-content;
}
h4{
    position: absolute;
    top: 0;
    left: 40px;
}
#line{
    height: 1px;
    width: calc( 100% - 252px );
    background: #E6B656;
    position: absolute;
    left: 220px;
    top: 30px;
}

nav {
    width: fit-content;
    font-size: 20px;
    text-align: center;
    position: relative;
    height: 43px;
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
        padding: 0.5rem 2rem;
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
    .headline_wrapper{
        display: block;
        position: relative;
        height: 50px;
    }

    #add_filter_btn{
        margin-top: 20px;
    }
</style>
