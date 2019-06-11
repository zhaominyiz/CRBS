import Vue from 'vue'
import axios from 'axios'
export const login = ({ commit, state, }, payload) => {
    var userName = payload['userName']
    var password = payload['password']
    // alert(userName+password)
    var vm = payload['vm']
    Vue.http.post('api/login', {userName, password}).then(
        (response) => {
            // var data = JSON.stringify(response.data)
            var data=response.body
            var msg =response.data.msg
            // alert(msg)
            if(msg==='SUCCESS') {
              // commit('saveToken', data['token'])
              sessionStorage.setItem('username', response.data.username)
              vm.$Message.success('登录成功!');
              var t = setTimeout(function(){window.location.reload();},2000);
            }else{
              vm.$Message.error('认证失败!');
            }
        },
        (response) => {
          vm.$Message.error('认证失败!');
        }
    )


}

export const logout = ({commit, state}) => {
    commit('clearToken')
}
