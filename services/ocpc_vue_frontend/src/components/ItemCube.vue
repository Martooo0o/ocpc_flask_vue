<template>
    <button @click="onClick()">
        <img id="img" src="@/assets/cube.png" alt="">
        <h5>{{cubename}}</h5>

        <MenuPopup id="drop" displayVal="none"></MenuPopup>
    </button>
</template>

<script>
import Button from './ui/Button.vue';
import MenuPopup from './MenuPopup.vue';
export default {
    name: "ItemCube",
    props: {
        cubename: String
    },
    methods: {
        onClick(name) {
            console.log("Selected ItemCube: " +this.cubename)
            this.$emit('select-cube', this.cubename)
        },
    },
    components: { Button, MenuPopup },
    emits: ['select-cube']
}
</script>

<style scoped>
    img{
        width: 35px;
        height: 35px;
        display: inline-block;
        float: left;
    }
    h5{
        margin:0;
    }
    button{
        background: none;
        border: none;
        border-radius: 0px;
        position: relative;
        width: 100%;
        display: block;
    }
    #drop{
        position: absolute;
        top: -30px;
        right: -30px;
    }
</style>
