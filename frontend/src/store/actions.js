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
            }else if(msg==='SERVE_ERROR'){
              vm.$Message.error('服务器错误!');
            }else if(msg==='INPUT_DATAERROR'){
              vm.$Message.error('输入数据错误!');
            }else if(msg==='ACCOUNT_ERROR'){
              vm.$Message.error('无此账号!');
            }else{
              vm.$Message.error('密码错误!');
            }
        },
        (response) => {
          vm.$Message.error('网络错误!');
        }
    )

}

export const logout = ({commit, state}) => {
    commit('clearToken')
}

export const signup = ({ commit, state, }, payload) => {
    var userName = payload['userName']
    var password = payload['password']
    // alert(userName+password)
    var vm = payload['vm']
    Vue.http.post('api/signup', {userName, password}).then(
        (response) => {
            // var data = JSON.stringify(response.data)
            var data=response.body
            var msg =response.data.msg
            // alert(msg)
            if(msg==='SUCCESS') {
              // commit('saveToken', data['token'])
              sessionStorage.setItem('username', response.data.username)
              vm.$Message.success('注册成功!');
            }else if(msg==='SERVE_ERROR'){
              vm.$Message.error('服务器错误!');
            }else if(msg==='INPUT_DATAERROR'){
              vm.$Message.error('输入数据错误!');
            }else if(msg==='ACCOUNT_ERROR'){
              vm.$Message.error('已有该账号！');
            }else{
              vm.$Message.error('密码错误!');
            }
        },
        (response) => {
          vm.$Message.error('网络错误!');
        }
    )

}
