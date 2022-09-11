
<template>
    <div id="new_cube_wrapper">
        <div id="cube_form" class="card-4">
            <h3 class="card-4">New Filter</h3>

            <button id="close_btn" @click="onClose" class="card-4">X</button>

            <div class="vis_item card-4 selected" @click="onSelectDimens" ref="dims">
                <h4>Dimensions</h4>
                <img src="https://cdn-icons-png.flaticon.com/512/2125/2125009.png"/>
            </div>
            <div class="vis_item card-4" @click="onSelectFreq" ref="freq_items">
                <h4>Frequent-itemsets</h4>
                 <img src="https://cdn-icons-png.flaticon.com/512/2125/2125009.png"/>
            </div>
            <br/>
            <Button id="save-type" txt="Select Type" @click="onAddFilter()"></Button>
        </div>
    </div>
</template>

<script>
import Button from '../ui/Button.vue';
import TextInput from '../ui/TextInput.vue';
import LogSelector from '../LogSelector.vue';
import DimSelector from '../DimSelector.vue';
import Select from '../ui/Select.vue';
import SelectDimen from '../ui/SelectDimen.vue';
import { mapActions, mapGetters } from 'vuex';
// import { defineComponent } from '@vue/composition-api'
export default {
    data(){
        return {
            active : "name",
            type1: undefined,
            selections:[]
        }
    },
    name: 'FilterTypeDialog',
    components: {
    Button,
    TextInput,
    LogSelector,
    DimSelector,
    Select,
    SelectDimen
},
props: {
        // txt: String,
        // color: String
        dimens: Object
    },
     computed: {
        ...mapGetters({
            currDimens: 'main/currDimens',
            currCube: 'main/specCube',
        }),
        dimValues(){
            let freqAll = JSON.parse(this.currCube['freq_all']);
            return Set(Object.keys(freqAll[this.type1 + ',' + this.type2][this.dim1 + ',' + this.dim2]).map(x => x.split(',')[0]))
        }

    },
    methods: {
        ...mapActions({
            getDims: 'main/getCubeDimens'
        }),
        created(){
            this.type = 'dims';
        },
        onSelectDimens(){
            this.$refs['dims'].classList.add('selected');
            this.$refs['freq_items'].classList.remove('selected');
            this.type = 'dims';
        },
        onSelectFreq(){
            this.$refs['dims'].classList.remove('selected');
            this.$refs['freq_items'].classList.add('selected');
            this.type = 'freq_items';
        },
        onClose(){
            this.$emit('close-new-filter-type')
        },
        onAddFilter(){
            console.log("works");
            if(this.type === undefined){
                this.$emit('filter-type-selected', "dims")
            }else{
                this.$emit('filter-type-selected', this.type)
            }
        },
    },
    emits:['filter-type-selected', 'close-new-filter-type'],
    created(){
        this.active = "name";
        this.overviewTables = {0:{}}
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
        position: fixed;
        width: 100%;
        top:0px;
        left:0px;
        padding-top: 100px;
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
        background: #CCCCCC;
        border-radius: 10px;
        padding-bottom:  10px;
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
    .filter_attr {
        width: fit-content;
        display: inline-block;
        margin: 20px 0;
    }
    label{
        display: block;
    }
    #logs_table{
        width: calc(100% - 40px);
        background: white;
        /* border-radius: 10px; */

    }

    .cube-table-wrapper{
    width: 95%;
    overflow-y: auto;    /* Trigger vertical scroll    */
    overflow-x: auto;  /* Hide the horizontal scroll */
    background:  #DDDDDD;
    height:400px;
    margin: 20px auto 0 auto;
    /* border-radius: 10px;
    -webkit-border-radius: 10px;
-moz-border-radius: 10px; */
    overflow-x: scroll;
    overflow-y: scroll;
}
.cube-table{
	border: 1px solid #888888;
	/* border-radius: 10px; */
}
.cube-table-wrapper td, .cube-table-wrapper th{
	width: 100px;
	text-align: center;
	border: 1px solid #888888;
}
.cube-table-wrapper th{
	background: #00549F;
    color: white;
}

.table_heading{
	background-color: #00549F;
    color: #ffffff;
    text-align: center;
    font-weight: bold;
    padding-bottom: 5px;
    font-family: 'Roboto', sans-serif;
    padding: 5px;
}
#save-type{
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);

}

.vis_item{
    width:160px;
    height: 160px;
    display: inline-block;
    background: #ffffff;
    margin: 20px 10px 0 10px;
    border-radius: 10px;
}
.vis_item img{
    width:80px;
    height: 80px;
}
.vis_item:hover, .selected{
    background: #EEEEEE;
}
</style>
