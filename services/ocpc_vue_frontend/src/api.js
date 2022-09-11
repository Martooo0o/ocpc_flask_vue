import axios from 'axios';
// ROOT_API: process.env.ROOT_API,
let baseURL = process.env.ROOT_API;
console.log(baseURL);
if(baseURL === undefined){
  baseURL='http://localhost:5000';
  console.log("baseURL changed:");
  console.log(baseURL);
}
let authBURL = baseURL + "/auth";
let logsBURL = baseURL + "/logs";
let cubesBURL = baseURL + "/cubes";
let analysesBURL = baseURL + "/analyses";
let visBURL = baseURL + "/visualisations";

const authService = axios.create({
  baseURL : authBURL,
});

const logsService = axios.create({
  baseURL : logsBURL,
  headers: {
    Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    'Content-Type': 'multipart/form-data'
  }
});

const cubesService = axios.create({
  // baseURL: process.env.VUE_APP_AUTH_URL,
  baseURL : cubesBURL,
  // withCredentials: true,
  // xsrfCookieName: 'csrf_access_token',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    'Content-Type': 'multipart/form-data'
  }
});

const analysesService = axios.create({
  // baseURL: process.env.VUE_APP_AUTH_URL,
  baseURL : analysesBURL,
  // withCredentials: true,
  // xsrfCookieName: 'csrf_access_token',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    'Content-Type': 'multipart/form-data'
  }
});

const visService = axios.create({
  // baseURL: process.env.VUE_APP_AUTH_URL,
  baseURL : visBURL,
  // withCredentials: true,
  // xsrfCookieName: 'csrf_access_token',
  headers: {
    Authorization: `Bearer ${localStorage.getItem('jwt')}`,
    'Content-Type': 'multipart/form-data'
  }
});

const COOKIE_EXPIRED_MSG = 'Token has expired'
authService.interceptors.response.use((response) => {
  console.log(response)
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  console.log(error)
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        console.log("Token expired triggered")
        error.config.retry = true
        // authService.defaults.xsrfCookieName = 'jw';
        authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt_refresh')}`
        authService.defaults.headers['Content-Type'] = 'multipart/form-data'
        await authService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          // localStorage.setItem('jwt_refresh', result.refresh_token);
        })
        authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        // authService.defaults.xsrfCookieName = 'csrf_access_token';
        return authService(error.config)
      }
      break;
    case 404:
      router.push('/404');
      break;
    default:
      break;
  }
  return error.response;
});

logsService.interceptors.response.use((response) => {
  console.log(response)
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  console.log(error_message)
  console.log(error.responses)
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        error.config.retry = true
        // logsService.defaults.xsrfCookieName = 'csrf_refresh_token';
        authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt_refresh')}`
        await authService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          localStorage.setItem('jwt_refresh', result.refresh_token);
        }, async (error) => {
          console.log(error)
        })
        logsService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        // logsService.defaults.xsrfCookieName = 'csrf_access_token';
        return logsService(error.config)
      }
      break;
    case 404:
      router.push('/404');
      break;
    case 405:
        authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
          await authService.post('/refresh')
          .then(({ data }) => {
            console.log(data)
            const result = data
            localStorage.setItem('jwt', result.access_token);
            localStorage.setItem('jwt_refresh', result.refresh_token);
          })
        break;
    default:
      logsService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        await logsService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          localStorage.setItem('jwt_refresh', result.refresh_token);
        })
      break;
  }
  return error.response;
});

cubesService.interceptors.response.use((response) => {
  console.log(response)
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  console.log(error_message)
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        error.config.retry = true
        // cubesService.defaults.xsrfCookieName = 'csrf_refresh_token';
        cubesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt_refresh')}`
        await cubesService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          // localStorage.setItem('jwt_refresh', result.refresh_token);
        })
        cubesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        // cubesService.defaults.xsrfCookieName = 'csrf_access_token';
        return cubesService(error.config)
      }
      break;
    case 404:
      router.push('/404');
      break;
    default:
      break;
  }
  return error.response;
});

analysesService.interceptors.response.use((response) => {
  console.log(response)
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  console.log(error_message)
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        error.config.retry = true
        // analysesService.defaults.xsrfCookieName = 'csrf_refresh_token';
        analysesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt_refresh')}`
        await analysesService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          // localStorage.setItem('jwt_refresh', result.refresh_token);
        })
        analysesService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        // analysesService.defaults.xsrfCookieName = 'csrf_access_token';
        return analysesService(error.config)
      }
      break;
    case 404:
      router.push('/404');
      break;
    default:
      break;
  }
  return error.response;
});

visService.interceptors.response.use((response) => {
  console.log(response)
  return response
}, async (error) => {
  const error_message = error.response.data.msg
  console.log(error_message)
  switch (error.response.status) {
    case 401:
      if (!error.config.retry && error_message === COOKIE_EXPIRED_MSG) {
        error.config.retry = true
        // visService.defaults.xsrfCookieName = 'csrf_refresh_token';
        visService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt_refresh')}`
        await visService.post('/refresh')
        .then(({ data }) => {
          console.log(data)
          const result = data
          localStorage.setItem('jwt', result.access_token);
          // localStorage.setItem('jwt_refresh', result.refresh_token);
        })
        visService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
        // visService.defaults.xsrfCookieName = 'csrf_access_token';
        return analysesService(error.config)
      }
      break;
    case 404:
      router.push('/404');
      break;
    default:
      break;
  }
  return error.response;
});

export { authService, logsService, cubesService, analysesService, visService};