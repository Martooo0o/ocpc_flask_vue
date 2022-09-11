<template>
    <button id="wrapper_btn" @click="onClick()">
        <div class="fck_btn_centering">
            <div id="filter_attrs_wrap">
                <label>Materialisation</label>
                <div id="mat" class="card-4">{{mat}}</div>
                <div class="line"></div>
                <label>Dimensions</label>
                <div id="dimens" class="card-4">
                    <div class="dim1 " :style="dim1Style">
                        <dim class="inner_dim1">
                            {{dim1}}
                        </dim>
                    </div>
                    <div class="dim2">
                        <dim class="inner_dim2">
                            {{dim2}}
                        </dim>
                    </div>
                </div>
            </div>
            <div class="vert_line"></div>
            <div id="values_wrapper">
                <label id="label_values">Pair-Values</label> 
                <div class="item card-4" :key="pair" v-for="pair in dimValues">
                    <div class="left_item" :style="dim1ValueStyle">{{pair.split(',')[0]}}</div>
                    <div class="right_item" >{{pair.split(',')[1]}}</div>
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
export default {
    name: "ItemFilter",
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
    components: { Button },
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
.fck_btn_centering{
    min-height: 100px;
    height: fit-content;
}
#wrapper_btn:nth-of-type(){
    border-radius: 10px;
}
#wrapper_btn:hover{
    background: #888888;
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
#filter_attrs_wrap label{
    display: inline-block;
    width: 100%;
    text-align: center;
    padding: 10px 0;
}
#dimens{
    display: inline-block;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    width: 190px;
    margin: 0 20px 10px 20px;
    height: 33px;
    /* position: absolute;
    left: 20px;
    top: 15px; */
}
#mat{
    background: #E6B656;
    display: inline-block;
    padding: 10px 0;
    color: white;
    font-weight: bolder;
    border-radius: 10px;
    /* position: absolute;
    top: 15px; */
    width: 190px;
    margin: 0 20px;
    text-align: center;
}

.dim1{
    background: #56e6a0;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
    display: inline-block;
    width: 75px;
    padding: 10px;
    overflow: hidden;
}
.inner_dim1{
  /* animation properties */
  -moz-transform: translateX(100%);
  -webkit-transform: translateX(100%);
  transform: translateX(100%);
  
  -moz-animation: my-animation 15s linear infinite;
  -webkit-animation: my-animation 15s linear infinite;
  animation: my-animation 15s linear infinite;
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
.inner_dim2{
  /* animation properties */
  -moz-transform: translateX(100%);
  -webkit-transform: translateX(100%);
  transform: translateX(100%);
  
  -moz-animation: my-animation 15s linear infinite;
  -webkit-animation: my-animation 15s linear infinite;
  animation: my-animation 15s linear infinite;
}
.dim2{
    background: #CCCCCC;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    display: inline-block;
    width: 75px;
    padding: 10px;
    overflow: hidden;
}

/* Values */
#label_values{
    display: inline-block;
    margin: 10px 0;
    width: 100%;
    text-align: center;
}
.item{
    display: inline-block;
     font-weight: bold;
    border-radius: 10px;
    margin-right: 10px;
    margin-bottom: 10px;
}
.left_item, .right_item{
    display: inline-block;
}
.left_item{
    background: #E6B65680;
    
    padding: 10px;
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}
.right_item{
    background: #CCCCCC80;
    padding: 10px;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}
#delete_btn{
    width: 30px;
    height: 30px;
    border-radius: 10px;
    
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

 .line{
        width: calc(100% - 40px);
        background: #cccccc;
        height: 1px;
        bottom: 0px;
        margin: 10px 20px 0 20px;
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
