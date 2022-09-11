<template>
    <button :class="[first?'first':''], [last?'last':'']" :style="{background: color}">{{txt}}</button>
</template>

<script>

export default {
    name: "MenuPopItem",
    props: {
        txt: String,
        color: String,
        first: Boolean,
        last: Boolean
        // displayVal: String
    },
    methods: {
        onClick(){
            console.log("Click")
        },
    }
}
</script>
<style scoped>
    #popup_wrap{
        display: none;
    }
    button{
        margin: 0;
        border-radius: 0px;
    }
    .first{
        border-top-left-radius: 20px;
        border-top-right-radius: 20px;
    }
    .last{
        border-bottom-left-radius: 20px;
        border-bottom-right-radius: 20px;
    }
</style>
