// import Vue from 'vue';
import Vuex from 'vuex';
import auth from './modules/auth';
import main from './modules/main';

// Vue.use(Vuex);

const store = new Vuex.Store({
  modules: {
    auth: auth, 
    main: main
  }
})

export default store

