import { login, logout, getUserInfo } from '@/api/auth'

const state = {
  token: localStorage.getItem('token') || '',
  user: JSON.parse(localStorage.getItem('user') || '{}'),
  loading: false
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
  },
  SET_USER(state, user) {
    state.user = user
  },
  SET_LOADING(state, isLoading) {
    state.loading = isLoading
  },
  CLEAR_AUTH(state) {
    state.token = ''
    state.user = {}
  }
}

const actions = {
  // 用户登录
  async login({ commit }, userInfo) {
    commit('SET_LOADING', true)
    try {
      const response = await login(userInfo)
      const { access_token, user } = response.data
      
      // 保存到状态和本地存储
      commit('SET_TOKEN', access_token)
      commit('SET_USER', user)
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(user))
      
      return Promise.resolve(response)
    } catch (error) {
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 用户退出登录
  async logout({ commit }) {
    try {
      await logout()
    } catch (error) {
      console.error('退出登录API调用失败:', error)
    } finally {
      // 无论API是否成功，都清除本地状态
      commit('CLEAR_AUTH')
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  },
  
  // 获取用户信息
  async getUserInfo({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await getUserInfo()
      commit('SET_USER', response.data)
      localStorage.setItem('user', JSON.stringify(response.data))
      return response.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
      if (error.response && error.response.status === 401) {
        // 如果是未授权错误，清除认证状态
        commit('CLEAR_AUTH')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.user,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 