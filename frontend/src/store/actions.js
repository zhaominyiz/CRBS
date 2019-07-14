import Vue from 'vue'
import axios from 'axios'
/**
 * @description 此文件主要定义一些HTTP协议的发包函数
 * @copyright 南京理工大学 剁椒鱼头队
 * @author 赵珉怿
 */
/**
 * @method
 * @description 用于登录的发包函数
 * @param {string} userName 用户名
 * @param {string} password 密码
 */
export const login = ({commit, state,}, payload) => {
  var userName = payload['userName']
  var password = payload['password']
  var vm = payload['vm']
  Vue.http.post('api/login', {userName, password}).then(
    (response) => {
      var data = response.body
      //获取返回的信息 具体见前后端定义的文档
      var msg = response.data.msg
      if (msg === 'SUCCESS') {
        //将结果存入Session中
        sessionStorage.setItem('username', response.data.username)
        vm.$Message.success('登录成功!');
        var t = setTimeout(function () {
          window.location.reload();
        }, 2000);
      } else if (msg === 'SERVE_ERROR') {
        vm.$Message.error('服务器错误!');
      } else if (msg === 'INPUT_DATAERROR') {
        vm.$Message.error('输入数据错误!');
      } else if (msg === 'ACCOUNT_ERROR') {
        vm.$Message.error('无此账号!');
      } else {
        vm.$Message.error('密码错误!');
      }
    },
    (response) => {
      vm.$Message.error('网络错误!');
    }
  )

}
/**
 * @method
 * @description 用于登出的函数
 */
export const logout = ({commit, state}) => {
  commit('clearToken')
}
/**
 * @method
 * @description 用于注册的发包函数
 * @param {string} userName 用户名
 * @param {string} password 密码
 */
export const signup = ({commit, state,}, payload) => {
  var userName = payload['userName']
  var password = payload['password']
  // alert(userName+password)
  var vm = payload['vm']
  Vue.http.post('api/signup', {userName, password}).then(
    (response) => {
      // var data = JSON.stringify(response.data)
      var data = response.body
      var msg = response.data.msg
      // alert(msg)
      if (msg === 'SUCCESS') {
        // commit('saveToken', data['token'])
        sessionStorage.setItem('username', response.data.username)
        vm.$Message.success('注册成功!');
      } else if (msg === 'SERVE_ERROR') {
        vm.$Message.error('服务器错误!');
      } else if (msg === 'INPUT_DATAERROR') {
        vm.$Message.error('输入数据错误!');
      } else if (msg === 'ACCOUNT_ERROR') {
        vm.$Message.error('已有该账号！');
      } else {
        vm.$Message.error('密码错误!');
      }
    },
    (response) => {
      vm.$Message.error('网络错误!');
    }
  )

}
