import { logsService , cubesService, analysesService, visService} from '@/api'

const namespaced = true;

const state = {
  logs: [],
  cubes: [],
  spec_log: {},
  spec_cube: {},
  analyses: [], //used for AnalysisView, to hold all the opened analyses
  curr_analysis: "",
  curr_analysis_vis_data: [],
  curr_analysis_filter_data: {},
  curr_dimens: {},
  perf: {}
};

const getters = {
  logs: state => state.logs,
  cubes: state => state.cubes,
  specLog: state => state.spec_log,
  specCube: state => state.spec_cube,
  analyses: state => state.analyses,
  currAnalysis: state => state.curr_analysis,
  currDimens: state => state.curr_dimens,
  currAnalysisVisData: state => state.curr_analysis_vis_data,
  currAnalysisFilterData: state => state.curr_analysis_filter_data,
  perf: state => state.perf
};

const actions = {
  async getPerfor({ dispatch, commit }){
    console.log("Server Calling function was performance");
    await cubesService.post('/performance')
      .then((data) =>{
        console.log("Got logs from server")
        commit('setPerf', data)
      })
      .catch((error) => {
        console.log(error)
        });
  },
  async getLogs({ dispatch, commit }) {
    console.log("Server Calling function was triggered");
    await logsService.post('/all')
      .then((logs) =>{
        console.log("Got logs from server")
        commit('setLogs', logs)
      })
      .catch((error) => {
        console.log(error)
        });
  },
  async getSpecLog({dispatch, commit}, logname){
    await logsService.post('/get/'+logname)
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        commit('setSpecLog', data)
      }
      // return data;
    })
    .catch((error) => {
      console.log(error)
      // return data;
      })
    
  },
  async uploadLog({dispatch, commit}, log){
    console.log("Server FKT for Upload");
    // await authService.get('/logs')
    let formData = new FormData();
    formData.append('file', log);
    await logsService.post('/add', formData)
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        commit('setLogs', data) 
      }
    })
    .catch((error) => {
      console.log(error)
      })
    await dispatch('getLogs')
  },
  async getCubes({ dispatch, commit }) {
    console.log("Server Calling function For all Cubes was triggered");
    await cubesService.post('/all')
      .then((cubes) =>{
        console.log("Got cubes from server")
        commit('setCubes', cubes)
      })
      .catch((error) => {
        console.log(error)
        });
  },
  async getSpecCube({dispatch, commit}, cubename){
    console.log(cubename)
    await cubesService.post('/get/'+cubename)
    .then(({data}) =>{
      console.log(data)
      // if(!("error" in data) && 
      // !("msg" in data && data['msg'] == "Token has expired")){
        commit('setSpecCube', data)
      // }
      // return data;
    })
    .catch((error) => {
      console.log(error)
      // return data;
      })
    
  },
  async createCube({dispatch, commit}, cube){// await authService.get('/logs')
    let formData = new FormData();
    formData.append('name', cube.name);
    formData.append('logname', cube.logname);
    formData.append('dimens', cube.dimens);
    
    console.log("Server FKT for Create Cube");
    console.log(cube);
    console.log(formData);
    await cubesService.post('/add', JSON.stringify(cube))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
      }
    })
    .catch((error) => {
      console.log(error)
      })
    await dispatch('getCubes')
  },

  async getAnalyses({dispatch, commit}, cube){// await authService.get('/logs')
    let formData = new FormData();
    formData.append('name', cube.name);
    formData.append('logname', cube.logname);
    formData.append('dimens', cube.dimens);
    
    console.log("Server FKT for Create Cube");
    console.log(cube);
    console.log(formData);
    await cubesService.post('/add', JSON.stringify(cube))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
      }
    })
    .catch((error) => {
      console.log(error)
      })
    await dispatch('getCubes')
  },

  async getSpecAnalysis({dispatch, commit}, cube){// await authService.get('/logs')
    // let formData = new FormData();
    // formData.append('name', cube.name);
    // formData.append('logname', cube.logname);
    // formData.append('dimens', cube.dimens);
    
    console.log("Server FKT for get Analysis");
    console.log(cube);
    console.log(formData);
    await cubesService.post('/add', JSON.stringify(cube))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
      }
    })
    .catch((error) => {
      console.log(error)
      })
    await dispatch('getCubes')
  },

  async createAnalysis({dispatch, commit}, analysis){// await authService.get('/logs')
    let formData = new FormData();
    formData.append('name', analysis.name);
    formData.append('logname', analysis.logname);
    formData.append('cube', analysis.cube);
    
    console.log("Server FKT for Create Analysis");
    console.log(analysis);
    console.log(formData);
    await analysesService.post('/add', JSON.stringify(analysis))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('getSpecCube', state.spec_cube.cube)
      }
    })
    .catch((error) => {
      console.log(error)
      })
    
  },

  async delAnalysis({dispatch, commit}, analysis){
    let formData = new FormData();
    formData.append('name', analysis.name);
    formData.append('cube', analysis.cube);
    formData.append('log', analysis.log);
    
    console.log("Server FKT for Deleting Analysis" + analysis.name);
    console.log(analysis);
    console.log(formData);
    await analysesService.post('/delete/' + analysis.name, JSON.stringify(analysis))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('getSpecCube', state.spec_cube.cube)
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async delLog({dispatch, commit}, log){
    console.log("Server FKT for Deleting Log" + log);
    await logsService.post('/delete/' + log,{})
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('getLogs');
        commit('setSpecLog', {});
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async delCube({dispatch, commit}, cube){
    console.log("Server FKT for Deleting Cube" + cube);
    await cubesService.post('/delete/' + cube, )
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('getCubes');
        commit('setSpecCube', {});
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },


  async setAFilters({dispatch, commit}, object){// await authService.get('/logs')
    let formData = new FormData();
    console.log("Server FKT for Adding a filter");
    console.log(object['analysis'])
    console.log(object["filter"]);

    await analysesService.post('/set/' + object['analysis'] + '/filters' , JSON.stringify({"new_filter": object["filter"]}))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('openAnalysis', state.curr_analysis.name)
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async setAVis({dispatch, commit}, analysis){// await authService.get('/logs')
    let formData = new FormData();
    console.log("Server FKT for Adding a visualisation");
    console.log(analysis);
    console.log(formData);

    await analysesService.post('/set/' + analysis.name + '/visualisations' , JSON.stringify(analysis))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        dispatch('openAnalysis', state.curr_analysis.name)
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async openAnalysis({commit}, newAnalyses){
    console.log(newAnalyses)
    await analysesService.post('/get/'+newAnalyses , JSON.stringify({}))
    .then(({data}) =>{
      console.log(data)
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('openAnalysis', data)
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async getCubeDimens({commit}, params){
    console.log(params.cubename)
    console.log(params.dim1)
    console.log(params.dim2)
    console.log(params.mat)
    await cubesService.post('/get/'+params.cubename+'/dim' , JSON.stringify(params))
    .then(({data}) =>{
      console.log(JSON.parse(data))
      console.log(typeof(data))
      data = JSON.parse(data)
      console.log(typeof(data))
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('setCurrDimens', data)
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async getFlattenedLog({commit}, params){ //TODO index of abnalysis 
    console.log(params);
    let reqData = { 'analysisname': params["analysisname"] };
    console.log(reqData);
    console.log(JSON.stringify(reqData))
    await visService.post('/log', JSON.stringify(reqData))
    .then(({data}) =>{
      console.log(data)
      // console.log(JSON.parse(data['data']))
      // console.log(typeof(data))
      // data = JSON.parse(data['data'])
      console.log(data['data'])
      console.log(typeof(data['data']))
      try{
        data = JSON.parse(data['data'])
      }catch(error){
        console.log(error)
      }
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('setCurAVisLog', {'data': data, 'index': params.vis_index})
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async getDFG({commit}, params){
    console.log(params);
    // TODO ADD FUTHER PARAMS
    let reqData = { 'analysisname': params["analysisname"], 'vis_index': params['vis_index']}; 
    console.log(reqData);
    console.log(JSON.stringify(reqData))
    await visService.post('/dfg', JSON.stringify(reqData))
    .then(({data}) =>{
      console.log(data)
      // console.log(JSON.parse(data['data']))
      // console.log(typeof(data))
      // data = JSON.parse(data['data'])
      console.log(data['data'])
      console.log(typeof(data['data']))
      // try{
      //   data = JSON.parse(data['data')
      // }catch(error){
      //   console.log(error)
      // }
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('setCurAVisDFG', {'data': data['data'], 'index': params.vis_index})
      }
    })
    .catch((error) => {
      console.log(error)
      })
  },

  async getFreqItems({commit}, params){
    console.log(params);
    
    // TODO ADD FUTHER PARAMS
    let reqData = { 'analysisname': params["analysisname"], 'index': params["vis_index"]};
    
    await visService.post('/freq_itemsets', JSON.stringify(reqData))
    .then(({data}) =>{
      console.log("Return Freq Items")
      console.log(data['result'])
      // console.log(JSON.parse(data['data']))
      // console.log(typeof(data))
      // data = JSON.parse(data['data'])
      
      // console.log(data['data'])
      // console.log(typeof(data['data']))

      console.log(data['result']['freq_itemsets'])
      
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('setCurAVisFreqItems', {'data': data.result.freq_itemsets, 'index': params.vis_index})
      }
    })
    .catch((error) => {
      console.log(error)
      })

  },

  async getFreqItemsInFilter({commit}, params){
    console.log(params);
    
    // TODO ADD FUTHER PARAMS
    let reqData = { 'analysisname': params["analysisname"], 'attrs': params['attrs'],'set_size': params['set_size'], 'min_supp': params['min_supp']};
    
    await analysesService.post('/freq_itemsets', JSON.stringify(reqData))
    .then(({data}) =>{
      console.log("Return Freq Items")
      console.log(data['result'])

      console.log(data['result']['freq_itemsets'])
      
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setCurrAFilterData', {'data': data.result.freq_itemsets, 'index': params.vis_index})
        commit('setCurrAFilterData', {'data': data.result.freq_itemsets, 'index': params.vis_index})
      }
    })
    .catch((error) => {
      console.log(error)
      })

  },
  resetCurrAFilterData({commit}){
    resetCurrAFilterData
    commit('resetCurrAFilterData')
  },
  async getAssRules({commit}, params){
    console.log(params);
    
    // TODO ADD FUTHER PARAMS
    let reqData = { 'analysisname': params["analysisname"], 'index': params["vis_index"]};
    
    await visService.post('/assoc_rules', JSON.stringify(reqData))
    .then(({data}) =>{
      console.log("Return Association Rules")
      console.log(data['result'])
      // console.log(JSON.parse(data['data']))
      // console.log(typeof(data))
      // data = JSON.parse(data['data'])
      
      // console.log(data['data'])
      // console.log(typeof(data['data']))

      console.log(data['result']['assoc_rules'])
      
      if(!("error" in data) && 
      !("msg" in data && data['msg'] == "Token has expired")){
        // commit('setLogs', data) 
        // dispatch('getSpecCube', state.spec_cube.cube)
        commit('setCurAVisAssocRules', {'data': data.result.assoc_rules, 'index': params.vis_index})
      }
    })
    .catch((error) => {
      console.log(error)
      })
  }
};

const mutations = {
  setLogs(state, logs) {
    state.logs = logs.data.logs;
  },
  setPerf(state, perf){
    state.perf = perf.data.stats;
  },
  setSpecLog(state, log) {
    state.spec_log = log;
    print("No Log set ")
  },
  setSpecCube(state, cube) {
    cube.analyses = JSON.parse(cube.analyses)
    console.log(cube)
    console.log(typeof(cube.dimens))
    state.spec_cube = cube;
  },
  setCurrAFilterData(state, obj){
    console.log('Saved Folowing Data:')
    console.log(obj)
    state.curr_analysis_filter_data = obj['data'];
  },
  resetCurrAFilterData(state){
    state.curr_analysis_filter_data = {}
  },
  // logoutUserState(state) {
  setCubes(state, cubes){
    state.cubes = cubes.data.cubes;
  },
  openAnalysis(state, specAnalysis){
    console.log("BlBla");
    console.log(this.analysesState);
    let analysisName = specAnalysis.name;
    let temp =  state.analyses.map(x => x);
    console.log(temp);
    if(!temp.includes(analysisName)){
      temp.push(analysisName);
    }
    console.log(temp);
    state.analyses = temp;
    state.curr_analysis = specAnalysis;
    // let newVisData = []
    state.curr_analysis_vis_data = state.curr_analysis.visualisations.map(x => {})
    console.log(state.curr_analysis);
    console.log("Init Vis Data");
    console.log(state.curr_analysis_vis_data);
  },
  closeAnalysis(state, specAnalysis){
      console.log("Close Analysis")
      let analysisName = specAnalysis.name;
      // state.curr_analusis = analysis;
      let index = state.analyses.indexOf(analysisName);
      if(state.curr_analusis === analysisName){
        if(index - 1 >= 0){
          index -= 1;
        }else if( index + 1 <state.curr_analusis.length){
          index += 1;
        }else{
          state.curr_analusis = "";
        }
      }
      state.analyses = state.analyses.filter( e => e!== analysisName);
  },
  setCurrDimens(state, dimens){
    state.curr_dimens = dimens;
    console.log(state.curr_dimens)
    console.log(typeof(state.curr_dimens))
    // console.log(getters.currDimen1Values())
  },
  setCurAVisLog(state, obj){
    console.log("Flat Log Response")
    console.log(obj)
    state.curr_analysis_vis_data[obj['index']] = obj['data']
  },
  setCurAVisDFG(state, obj){
    console.log("DFG Response")
    console.log(obj)
    state.curr_analysis_vis_data[obj['index']] = obj['data']
  },
  setCurAVisFreqItems(state, obj){
    console.log("Freq Itemsets Response")
    console.log(obj)
    state.curr_analysis_vis_data[obj['index']] = obj['data']
  },
  setCurAVisAssocRules(state, obj){
    console.log("Assoc. Rules Response")
    console.log(obj)
    state.curr_analysis_vis_data[obj['index']] = obj['data']
  }
};

export default {
  namespaced,
  state,
  getters,
  actions,
  mutations
};