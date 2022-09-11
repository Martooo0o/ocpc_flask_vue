<template>
    <div id="popup_wrap" :style="{display: displayVal }">
        <!-- <button @click="onClickDelete()" class="btn">De</button>
        <button @click="onClickExport()" class="btn">{{txt}}</button> -->
        <!-- <button @click="onClick()" class="btn">{{txt}}</button> -->
        <MenuPopItem txt="Delete" color="red" first="True"></MenuPopItem>
        <MenuPopItem txt="Export" color="black"></MenuPopItem>
        <MenuPopItem txt="Select" color="black" last="True"></MenuPopItem>
    </div>
</template>

<script>
import MenuPopItem from "./MenuPopItem.vue";

export default {
    name: "MenuPopup",
    props: {
        // txt: String,
        // color: String
        displayVal: String
    },
    methods: {
        onClick() {
            console.log("Click");
        },
    },
    components: { MenuPopItem }
}
</script>
<style scoped>
    #popup_wrap{
        display: none;
    }
</style>
