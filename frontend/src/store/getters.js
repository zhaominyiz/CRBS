export const username = state => {
    if (state.token)
        return JSON.parse(atob(state.token.split('.')[1]))['sub']
    return ''
}

export const name = state => {
    if (state.token)
        return JSON.parse(atob(state.token.split('.')[1]))['name']
    return ''
}