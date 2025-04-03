import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || {},
    mcpServers: [],
    agents: [],
    sdkKeys: []
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    currentUser: state => state.user,
    mcpServers: state => state.mcpServers,
    agents: state => state.agents,
    sdkKeys: state => state.sdkKeys
  },
  mutations: {
    auth_request(state) {
      state.status = 'loading'
    },
    auth_success(state, { token, user }) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error(state) {
      state.status = 'error'
    },
    logout(state) {
      state.status = ''
      state.token = ''
      state.user = {}
    },
    set_mcp_servers(state, mcpServers) {
      state.mcpServers = mcpServers
    },
    set_agents(state, agents) {
      state.agents = agents
    },
    set_sdk_keys(state, sdkKeys) {
      state.sdkKeys = sdkKeys
    }
  },
  actions: {
    login({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios.post('/auth/login', user)
          .then(resp => {
            const token = resp.data.access_token
            const user = resp.data.user
            // 存储token到localStorage
            localStorage.setItem('token', token)
            localStorage.setItem('user', JSON.stringify(user))
            // 设置axios默认Authorization头
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
            commit('auth_success', { token, user })
            resolve(resp)
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            reject(err)
          })
      })
    },
    register({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        axios.post('/users', user)
          .then(response => {
            resolve(response)
          })
          .catch(err => {
            commit('auth_error')
            reject(err)
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    },
    fetchMCPServers({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/mcp-servers')
          .then(response => {
            commit('set_mcp_servers', response.data)
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    fetchAgents({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/agents')
          .then(response => {
            commit('set_agents', response.data)
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    },
    fetchSDKKeys({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('/sdk-keys')
          .then(response => {
            commit('set_sdk_keys', response.data)
            resolve(response)
          })
          .catch(error => {
            reject(error)
          })
      })
    }
  },
  modules: {
  }
}) 