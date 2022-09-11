<template>
    <button id="wrapper_btn" @click="onClick()">
        <div class="fck_btn_centering">
            <div id="filter_attrs_wrap">
                <label>Attributes</label>
                <!-- <div id="mat" class="card-4">
                    </div> -->
                <!-- Dim Display might need to e modified to a VerticalDimDisplay -->
                 <VertDimDispaly :dimens="this.filter['attrs']"></VertDimDispaly>
            </div>
            <div class="vert_line"></div>
            <div id="values_wrapper">
                <label id="label_values">Sets</label>
                 <div class="table_wrapper">
                    <table class="freq_items_table" ref="table"  v-if="this.filter!==undefined">
                        <thead v-if="this.filter['selections']!==undefined && this.filter['selections'].length">
                            <tr>
                                <!-- <td>Set Size</td> -->
                                <!-- <td>Set</td> -->
                                <!-- <td>Support</td> -->
                            </tr>
                        </thead>
                        <tbody>
                            <tr :key="set" v-for="set in this.filter['selections']">
                                <!-- <td :key="column" v-for="column in Object.keys(data)">{{data[column][row]}}</td> -->
                                <!-- <td>{{set[0]}}</td> -->
                                <td>{{set}}</td>
                                <!-- <td>{{set[2]}}</td> -->
                            </tr> 
                        </tbody>
                    </table>
                </div>
                
            </div>
            <div class="vert_line2"></div>
            <div id="controls_wrapper">
                <div class="arrow-up"></div>
                <span class="dot"></span>
                <div class="arrow-down"></div>
            </div>
             <div class="close_btn card-4">
                <p>X</p>
            </div>
        </div>
    </button>
</template>

<script>
import Button from '../ui/Button.vue';
import DimDispaly from '../DimDispaly.vue';
import VertDimDispaly from '../VertDimDispaly.vue';
export default {
    name: "ItemFItemsFilter",
    props: {
        filter: Object
    },
    methods: {
        onClick(name) {
            console.log("Selected ItemLog: " +this.name)
            this.$emit('select-analysis', this.name)
        },
    },
    created(){
        this.randomColor = Math.floor(Math.random()*16777215).toString(16);
        console.log(this.randomColor)
        console.log(this.filter)
    },
    computed: {
        dimValues(){
            return this.filter.selections
        },
        dim1(){
            console.log(this.filter)
            console.log(this.filter.dim1)
            if(this.filter.dim1.substring(0, 7) == 'object_'){
                return this.filter.dim1.substring(7)  
            }else{
                return this.filter.dim1     
            }
        },
        dim2(){
            if(this.filter.dim2.substring(0, 7) == 'object_'){
                return this.filter.dim2.substring(7);  
            }else{
                return this.filter.dim2;     
            }
        },
        mat(){
            return this.filter.mat
        },
        dim1Style(){
            return {
                background: '#'+this.randomColor
            };
        },
        dim1ValueStyle(){
            return {
                background: '#'+this.randomColor + '66'
            };
        }
    },
    components: { Button, DimDispaly, VertDimDispaly },
    emits: ['select-analysis']
}
</script>

<style scoped>
#wrapper_btn{
         background: none;
        border: none;
        position: relative;
        width: calc(100% - 20px);
        height: fit-content;
        border-radius: 10px;
        margin: 0 10px;
        background: #EEEEEE;
    }
#wrapper_btn:nth-of-type(){
    border-radius: 10px;
}
#wrapper_btn:hover{
    background: #888888;
}
#dimens{
    display: inline-block;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    width: 190px;
    position: absolute;
    left: 20px;
    top: 15px;
    height: 33px;
}
/* for Firefox */
@-moz-keyframes my-animation {
  from { -moz-transform: translateX(100%); }
  to { -moz-transform: translateX(-100%); }
}

/* for Chrome */
@-webkit-keyframes my-animation {
  from { -webkit-transform: translateX(100%); }
  to { -webkit-transform: translateX(-100%); }
}

@keyframes my-animation {
  from {
    -moz-transform: translateX(100%);
    -webkit-transform: translateX(100%);
    transform: translateX(100%);
  }
  to {
    -moz-transform: translateX(-100%);
    -webkit-transform: translateX(-100%);
    transform: translateX(-100%);
  }

}
#filter_attrs_wrap{
    width: 230px;
    display: inline-block;
    vertical-align: top;
}
#values_wrapper{
    display: inline-block;
    width: calc(100% - 320px);
    position: relative;
    margin: 0 10px;
    text-align: start;
    /* top: 10px;
    left: 230px; */

}
#controls_wrapper{
    width: 60px;
    height: 100%;
    display: inline-block;
    position: relative;
    /* top: 50%;
    transform: translateY(-50%); */
    margin: 30px 0 0 10px;
    vertical-align: top;
}
.vert_line{
    position: absolute;
    width: 1px;
    background: #cccccc;
    margin: 10px 5px;
    display: inline-block;
    height: calc(100% - 20px);
    left: 230px;
}
.vert_line2{
    position: absolute;
    width: 1px;
    background: #cccccc;
    margin: 10px 5px;
    display: inline-block;
    height: calc(100% - 20px);
    left: calc(100% - 80px);
}
#filter_attrs_wrap label, #values_wrapper label{
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 10px 0;
}

#mat{
    background: #E6B656;
    display: inline-block;
    padding: 10px;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    float: right;
    position: absolute;
    right: 20px;
    top: 15px;
    width: 100px;
    text-align: center;
}
.item{
    display: inline-block;
     font-weight: bold;
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
}


.arrow-up {
  width: 0; 
  height: 0; 
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-top: 20px solid #E6B656;
  transform: rotate(180deg);
  margin: 10px 10px 5px 10px;
  display: block;
}

.dot {
    position: relative;
    display: block;
    height: 25px;
    width: 25px;
    background-color: #bbb;
    border-radius: 50%;
    margin: 5px 0;
    left: 50%;
    transform: translateX(-50%);
}

.arrow-down {
  width: 0; 
  height: 0; 
  border-left: 20px solid transparent;
  border-right: 20px solid transparent;
  border-top: 20px solid #E6B656;
  margin: 5px 10px 10px 10px;
  display: block;
}


.close_btn{
    background: red;
    color: white;
    position: absolute;
    right: -15px;
    top: -15px;
    padding: 10px;
    height: 20px;
    width: 20px;
    border-radius: 20px;
}
.close_btn p{
    padding: 0;
    margin: 0 auto;
    display: block;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.close_btn:hover{
    background: white;
    color: red;
}
</style>
