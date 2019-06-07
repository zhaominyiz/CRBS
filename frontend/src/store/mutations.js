export const syncRouter = (state, route) => {
  state.route = route
}

export const saveToken = (state, token) => {
    localStorage.setItem('token', token)
    state.token = token;
}

export const clearToken = (state) => {
  localStorage.setItem('token', '')
  state.token = ''
}