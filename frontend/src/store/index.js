import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { login } from '@/api/auth'

import auth from './modules/auth'
import agents from './modules/agents'
import sdkKeys from './modules/sdk-keys'
import dashboard from './modules/dashboard'
import mcpServers from './modules/mcp-servers'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user')) || {},
    mcpServers: [],
    agents: [],
    sdkKeys: [],
    loading: false,
    error: null
  },
  getters: {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    currentUser: state => state.user,
    mcpServers: state => state.mcpServers,
    agents: state => state.agents,
    sdkKeys: state => state.sdkKeys,
    isLoading: state => state.loading,
    error: state => state.error
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
    },
    SET_LOADING(state, isLoading) {
      state.loading = isLoading
    },
    SET_ERROR(state, error) {
      state.error = error
    },
    CLEAR_ERROR(state) {
      state.error = null
    },
    SET_TOKEN(state, token) {
      state.token = token
    },
    SET_USER(state, user) {
      state.user = user
    }
  },
  actions: {
    async login({ commit, dispatch }, userInfo) {
      commit('SET_LOADING', true)
      try {
        const response = await login(userInfo)
        const { access_token, user } = response.data
        
        // 保存到状态和本地存储
        commit('SET_TOKEN', access_token)
        commit('SET_USER', user)
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))
        
        // 获取用户信息
        await dispatch('getUserInfo')
        
        return Promise.resolve(response)
      } catch (error) {
        return Promise.reject(error)
      } finally {
        commit('SET_LOADING', false)
      }
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
    },
    setLoading({ commit }, isLoading) {
      commit('SET_LOADING', isLoading)
    },
    setError({ commit }, error) {
      commit('SET_ERROR', error)
    },
    clearError({ commit }) {
      commit('CLEAR_ERROR')
    },
    getUserInfo({ commit }) {
      // Implementation of getUserInfo action
    }
  },
  modules: {
    auth,
    agents,
    sdkKeys,
    dashboard,
    mcpServers
  }
}) 