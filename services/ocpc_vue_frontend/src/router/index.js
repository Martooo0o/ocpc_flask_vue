import {createRouter, createMemoryHistory} from 'vue-router'
import LogsView from '../views/LogsView'
import App from '../App'
import store from '../store'
import { authService } from '@/api'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/performance',
    name: 'performance',
    component: () => import('../views/PerformanceView.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    // next: 
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/profile',
    name: 'profile',
    components: {
      default: () => import('../views/ProfileView.vue'),
      // inspector: () => import('../components/LogInspector.vue'),
    }
  },

  // IN THE FOLOWING ROUTES 'INSPECTOR' IS THE SECONDARY ROUTER 

  {
    path: '/logs',
    name: 'logs',
    components: {
      default: () => import('../views/LogsView.vue'),
      inspector: () => import('../components/LogInspector.vue'),
    }
  },
  {
    path: '/cubes',
    name: 'cubes',
    // route level code-splitting
    // this generates a separate chunk (About.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    components: {
      default: () => import('../views/LogsView.vue'),
      inspector: () => import('../components/CubeInspector.vue'),
    }
  },
  {
    path: '/analyses',
    name: 'analyses',
    component: () => import('../views/AnalysisView.vue')
  }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

router.beforeEach(async (to, from, next) => {

  const nearestWithTitle = to.matched.slice().reverse().find(r => r.meta && r.meta.title);

  if (nearestWithTitle) document.title = nearestWithTitle.meta.title;

  if (
    // make sure the user is authenticated
    // !store.state.auth.isLoggedIn &&
    to.name !== 'login' && to.name !== 'home' && to.name !== 'register'
  ) {
    console.log('doing call');
    authService.defaults.headers.Authorization = `Bearer ${localStorage.getItem('jwt')}`
    const response = await authService.post('/check_jwt')
    .then(function(value){
      console.log(value);
      if(value.status !== 200){
        next('/login');
        // store.state.auth.actionIsLoggedIn(false);
        store.dispatch('auth/actionIsLoggedIn', false);
        localStorage.removeItem('jwt');
        localStorage.removeItem('jwt_refresh');
      }else{
        console.log(store.state.main.analyses === undefined)
        console.log(store.state.main.analyses.length == 0)
        store.dispatch('auth/actionIsLoggedIn', true);

        if(to.name === 'analyses' && (store.state.main.analyses === undefined || store.state.main.analyses.length == 0)){
          console.log("No Analyses are currently open")
          // TODO ADD POPUP INFORRMING USER THAT NO POPUPS ARE CURR OPEN
        }else{
          next();
        }
      }
    })
    .catch(function(err){
      console.log(err)
      next('/login')
      store.dispatch('auth/actionIsLoggedIn', false);
      localStorage.removeItem('jwt');
      localStorage.removeItem('jwt_refresh');
    });
    
    console.log('juust did call');
    console.log(response);
  
    console.log('doing noothiing');
    // next();
    
  }else{
    next();
  }
});

export default router 