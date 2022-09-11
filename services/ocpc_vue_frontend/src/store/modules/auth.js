import { authService, logsService, cubesService, analysesService, visService} from '@/api'

const namespaced = true;

const state = {
  user: {
  },
  logs: [],
  isLoggedIn: false
};

const getters = {
  isLoggedIn: state => state.isLoggedIn,
  user: state => state.user,
  logs: state => state.logs
};

const actions = {
  async registerUser({ dispatch }, user) {
    await authService.get('/signup', user)
      .then(() =>{
        // await dispatch('fetchUser')
      })
  },
  async loginUser({ dispatch , commit}, usr) {
    console.log("User in store");
    console.log(usr);
    let returnData = null
    await authService.post('/login', JSON.stringify(usr))
    .then(({ data }) => {
      console.log(data)
      const result = data
      localStorage.setItem('jwt', result.access_token);
      localStorage.setItem('jwt_refresh', result.refresh_token);
      
      authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
      logsService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
      cubesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
      analysesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
      visService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`

      console.log("DOOOOOOONE STORING")
      console.log(localStorage.getItem('jwt'))
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        commit('setUser', data)  
      }
      returnData = result
    })
    return returnData
    // await dispatch('fetchUser')
  },
  async fetchUser({ commit }) {
    await authService.get('/user')
      .then(({ data }) => {
        console.log(data)
        if(!("error" in data) && 
        !("msg" in data && data['msg'] == "Token has expired")){
          commit('setUser', data)  
        }
      })
  },
  async logoutUser({ commit }) {
    await authService.post('/logout');
    localStorage.removeItem('jwt');
    localStorage.removeItem('jwt_refresh');
    commit('logoutUserState');
  },
  actionIsLoggedIn({commit}, isLoggedIn){
    commit('setIsLoggedIn', isLoggedIn)
  },
};

const mutations = {
  setUser(state, user) {
    state.isLoggedIn = true;
    state.user = user;
  },
  logoutUserState(state) {
    state.isLoggedIn = false;
    localStorage.removeItem('jwt');
    localStorage.removeItem('jwt_refresh');
    state.user = {};
  },
  setLogs(state, data) {
    // state.isLoggedIn = true;
    state.logs = data["logs"];
  },
  setIsLoggedIn(state, data){
    state.isLoggedIn = data;
  }
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};