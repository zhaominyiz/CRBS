import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuex from 'vuex';
import VueResource from 'vue-resource';
import axios from 'axios'
import router from './router';       // 路由列表
import store from './store';
import iView from 'iview';
import 'iview/dist/styles/iview.css';    // 使用 CSS

import App from './App.vue'

Vue.use(VueRouter)
Vue.use(Vuex)
Vue.use(VueResource);
Vue.use(iView)

if (process.env.NODE_ENV === 'production') {
  Vue.config.silent = true
  Vue.config.devtools = false
  Vue.http.options.root = 'http://localhost:8666'
} else {
  Vue.http.options.root = 'http://localhost:8666'
}
// Vue.prototype.$http=axios
Vue.prototype.$ajax = axios
Vue.http.options.emulateJSON = true;
Vue.http.interceptors.push(function (request, next) {
  // modify request
  if (store.state.token)
    request.headers.set('Authorization', `Bearer ${store.state.token}`);
  next((response) => {
    if (response.status == 401) {
      // 登录状态失败
      store.commit('clearToken')
      vm.$Notice.error({
        title: '登录状态无效, 请登录',
      })
      vm.$router.push('/')
    }
  });
});

var vm = new Vue({
  router,
  store,
  el: '#app',
  render: h => h(App)
})
