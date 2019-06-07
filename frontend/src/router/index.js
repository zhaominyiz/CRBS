import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/index'
import newTask from "../components/newTask";
import History from "../components/history";
import userInfo from "../components/userInfo";
import detail from "../components/result";
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },{
      path:'/newTask',
      name:'newTask',
      component:newTask
    },{
      path:'/userInfo',
      name:'userInfo',
      component:userInfo
    },{
      path:'/history',
      name:'history',
      component:History
    },{
      path:'/detail',
      name:'detail',
      component:detail
    }
  ]
})

