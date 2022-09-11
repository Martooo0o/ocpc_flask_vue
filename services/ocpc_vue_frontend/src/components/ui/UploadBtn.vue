<template>
 <div id="wrapper">
        <input type="file" @change="uploadFile" ref="file">
        <button class="btn" @click="chooseFiles" ref="fileBtn">+ Upload Log</button>
  </div>
</template>

<script>
  export default {
      name: "UploadButton",
      props: {
          txt: String,
          color: String
      },
      data: ()=> {
        {fileObj: null}
      },
      methods: {
          onClick(){
              console.log("Click")
          },
          chooseFiles(){
            this.$refs.file.click();
            // document.getElementById("fileUpload").click();
          },
          uploadFile() {
            this.fileObj = this.$refs.file.files[0];
            console.log("UploadBtn: File Uploaded");
            console.log(this.$refs.file);
            this.$emit('log-uploaded', this.fileObj)
          },
      },
      emits: ['log-uploaded']
  }

</script>

<style scoped>
input{
  display: none;
}
button{
  width: 100%;
}
</style>
