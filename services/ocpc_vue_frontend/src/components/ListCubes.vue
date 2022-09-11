<template class="container">

    <div id="cubes_wrapper">
        <h3 class="card-4">Cubes</h3>
        <Button id="upload_log_btn" @click="onNewCube()" txt="+ Create Cube"></Button>
        <div id="items_wrapper">
            <div class="item" :key="cube" v-for="cube in cubes">
                <ItemCube  @select-cube="onSelect" :cubename="cube"></ItemCube>
            </div>
        </div>
         <label id="no_cubes" v-if="cubes.length == 0">No cubes</label>
    </div>
</template>

<script>
import ItemCube from './ItemCube.vue';
import Button from './ui/Button.vue';
export default {
    name: "ListCubes",
    props: {
        // txt: String,
        // color: String
        cubes: Array,
    },
    methods: {
        onSelect(cube){
            console.log("Selected ListCubes: " +cube)
            this.$emit('select-cube', cube)
        },
        onNewCube(){
            this.$emit('new-cube', true)
        }
    },
    components: {Button, ItemCube},
    emits: ['select-cube']
}
</script>

<style scoped>
.item{

    display: block;
    padding: 10px;
    margin-top: 10px;
    margin: 10px 10px 0px 10px
}
.item:first-of-type{
     margin-top: 50px;
}
.item:last-of-type{
     margin-bottom: 50px;
}

.item:hover{
    background: #999999;
    border-radius: 20px;
}
#upload_log_btn{
    position: absolute;
    z-index: 5;
    bottom: calc(10px);
    margin: 0 auto;
    width: calc(100% - 20px);
    left: 5px;
}
#items_wrapper{
  /* margin-top: 50px;  */
   position: relative;
    height: 100%;
     overflow: scroll;
}
#cubes_wrapper{
  display: inline-block;
  width: 100%;
  height: 50%;
  border-right: 2px solid gray;
  float: left;
  position: relative;
}
h3{
    color: white;
    background-color: #E6B656;
    margin: 0;
    width: fit-content;
    min-width: 120px;
    padding: 5px 10px;
    border-bottom-right-radius: 10px;
    position: fixed;
}
#no_cubes{
    position:absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
