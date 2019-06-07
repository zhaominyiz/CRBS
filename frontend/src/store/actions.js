import Vue from 'vue'

export const login = ({ commit, state, }, payload) => {
    var username = payload['username']
    var password = payload['password']
    var vm = payload['vm']
    Vue.http.post('api/token/auth/', {username, password}).then(
        (Response) => {
            var data = Response.body
            commit('saveToken', data['token'])
            vm.$Message.success('登录成功!');
        },
        (Response) => {
            vm.$Message.error('认证失败!');
        }
    )
}

export const logout = ({commit, state}) => {
    commit('clearToken')
}