<script>
export default {
      name: "TextInput",
      props: {
          placeholder: String,
          input: String
      },
      methods: {
        setData(text){
          this.obj = text;
        }
      },
      data(){
        return {
          obj: ""
        }
      },
      created(){
        if(this.input != null){
          this.obj = this.input;  
        }
      }
  }
</script>

<template>
            <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet">
            <div class="form__group">
                <input v-model="obj" type="text" class="form__input" id="name" :placeholder="placeholder" required="" />
                <label for="name" class="form__label">{{placeholder}}</label>
            </div>
</template>

<style scoped>
.form__group{
  width: calc(100% - 30px);
}
.form__label {
  font-family: 'Roboto', sans-serif;
  font-size: 0.8rem;
  margin-left: 2rem;
  margin-top: 0.7rem;
  display: block;
  transition: all 0.3s;
  transform: translateY(0rem);
}

.form__input {
  font-family: 'Roboto', sans-serif;
  color: #333;
  font-size: 0.8rem;
	margin: 0 auto;
  padding: 0.8rem 1rem;
  border-radius: 0.2rem;
  background-color: rgb(255, 255, 255);
  border: none;
  width: calc(100% - 30px);
  margin: 0 15px;
  display: block;
  border-bottom: 0.3rem solid transparent;
  transition: all 0.3s;
}

.form__input:placeholder-shown + .form__label {
  opacity: 0;
  visibility: hidden;
  -webkit-transform: translateY(-4rem);
  transform: translateY(-4rem);
}


</style>
