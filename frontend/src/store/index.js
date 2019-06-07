import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


import * as getters from './getters'
import * as actions from './actions'
import * as mutations from './mutations'

const state = {
    token: '',
}

if (typeof localStorage === 'object') {
    try {
        localStorage.setItem('localStorage', 1);
        localStorage.removeItem('localStorage');
    } catch (e) {
        Storage.prototype._setItem = Storage.prototype.setItem;
        Storage.prototype.setItem = function() {};
        console.log('Your web browser does not support storing settings locally. In Safari, the most common cause of this is using "Private Browsing Mode". Some settings may not save or some features may not work properly for you.');
    }
}

state.token = localStorage.getItem('token') || state.token

const store = new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})

export default store