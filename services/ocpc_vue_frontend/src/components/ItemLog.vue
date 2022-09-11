<template>
    <button  @click="onClick()">
        <img src="https://cdn-icons-png.flaticon.com/512/2125/2125009.png" alt="">
        <h4>{{name}}</h4>

    </button>
</template>

<script>
import Button from './ui/Button.vue';
import MenuPopup from './MenuPopup.vue';
export default {
    name: "ItemLog",
    props: {
        name: String,
        selected: Boolean
    },
    methods: {
        onClick(name) {
            console.log("Selected ItemLog: " +this.name)
            this.$emit('select-log', this.name)
        },
    },
    components: { Button, MenuPopup },
    emits: ['select-log']
}
</script>

<style scoped>
    img{
        width: 30px;
        height: 30px;
        float: left;
        display: inline-block;
    }
    h4{
        margin:0;
        width: fit-content;
        display: inline-block;
        padding: 9px;
    }
    button{
        background: none;
        border: none;
        border-radius: 0px;
        position: absolute;
        left: 5px;
        justify-content: start;
    }
    #drop{
        position: absolute;
        top: -30px;
        right: -30px;
    }
</style>
