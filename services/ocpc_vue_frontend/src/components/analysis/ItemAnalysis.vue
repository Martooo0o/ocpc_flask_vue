<template>
    <button id="wrapper_btn" @click="onClick()" >
        <img src="@/assets/graph.png" alt="">
        <h4>{{name}}</h4>
        <div id="toolbar">
            <div  @click.stop="openDelAnalysisDialog" id="clickable" class="close_btn card-4">
                <p>X</p>
            </div>
            <div id="creation_date">
                <label class="card-4">{{ceration_date}} 12.04.22</label>
            </div>
            
        </div>
            
        <h5>{{filters}} Filters: </h5>
    </button>
</template>

<script>
import Button from '../ui/Button.vue';
export default {
    name: "ItemAnalysis",
    props: {
        name: String
    },
    created(){
        this.randomColor = Math.floor(Math.random()*16777215).toString(16);
        console.log(this.randomColor)
        // this.$refs[''].addEventListener("click", function( e ){
        //         e = window.event || e; 
        //         if(this === e.target) {
        //             // put your code here
        //             console.log("Delete " + this.name + "?");
        //             this.$emit('delete-analysis', this.name);
        //         }
        // });
    },
    methods: {
        onClick(name) {
            console.log("Selected ItemLog: " +this.name)
            this.$emit('select-analysis', this.name)
        },
        openDelAnalysisDialog(){
            console.log("Delete " + this.name + "?");
            this.$emit('delete-analysis', this.name);
        },
        onDeleteAnalysis(){
            
        }  
    },
    components: { Button },
    emits: ['select-analysis', 'delete-analysis']
}
</script>

<style scoped>
#wrapper_btn{
        background: none;
        border: none;
        padding: 5px;
        position: relative;
        width: 100%;
        height: 130px;
        background: white;
        border-radius: 10px;
    }
#wrapper_btn:nth-of-type(){
    border-radius: 10px;
}
#wrapper_btn:hover{
    background: #888888;
}
    img{
        width: 100px;
        height: 100px;
        position: absolute;
        display: block;
        top: 50%;
        left: 20px;
        transform: translateY(-50%);
    }
    h4{
        margin:10px;
        width: fit-content;
        display: inline-block;
        color: gray;;
        position: absolute;
        top: 5px;
        left: 120px;
        font-size: 15px;
    }
    h5{
        margin:10px;
        width: fit-content;
        display: inline-block;
        color: gray;;
        position: absolute;
        top: 30px;
        left: 120px;
        font-size: 10px;
    }
    label{
    margin-left: 20px;
    width: fit-content;
    color: white;
    display: inline-block;
    margin: 0 10px 0 20px;
    width: fit-content;
    padding: 5px 10px;
    background-color: #E6B656;
    width: fit-content;
    z-index: 5;
    border-radius: 10px;
}
#creation_date{
    /* position: absolute;
    right: 0px;
    top:10px */
    display: inline-block;
    float: right;
}
#toolbar{
    display: block;
    width: 100%;
    position: absolute;
    right: -15px;
    top: -15px;
    margin-top: 20px;
    margin-right: 20px;
}
.close_btn{
    background: red;
    color: white;
    /* position: absolute;
    right: -15px;
    top: -15px; */
    /* padding: 10px; */
    height: 23px;
    width: 23px;
    border-radius: 20px;
    display: inline-block;
    float: right;
    position: relative;
}
.close_btn p{
    padding: 0;
    margin: 0 auto;
    display: block;
    position: absolute;
    top: 50%;
    left: 50%;
    /* display: inline-block; */
    transform: translate(-50%, -50%);
}

.close_btn:hover{
    background: white;
    color: red;
}
    
    
</style>
