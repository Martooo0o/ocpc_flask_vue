<template>

    <button class="btn" :style="{background: color}">{{txt}}</button>
</template>

<script>
export default {
    name: "Button",
    props: {
        txt: String,
        color: String
    },
    methods: {
        onClick(){
            console.log("Click")
        },
    }
}
</script>
