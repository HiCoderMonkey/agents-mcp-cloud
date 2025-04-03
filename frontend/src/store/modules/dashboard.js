import { 
  getDashboardStats, 
  getRecentAgents, 
  getSystemUsage, 
  getChatStats 
} from '@/api/dashboard'

const state = {
  stats: {
    serverCount: 0,
    agentCount: 0,
    keyCount: 0,
    chatCount: 0
  },
  recentAgents: [],
  systemUsage: {},
  chatStats: {},
  loading: false
}

const mutations = {
  SET_STATS(state, stats) {
    state.stats = stats
  },
  SET_RECENT_AGENTS(state, agents) {
    state.recentAgents = agents
  },
  SET_SYSTEM_USAGE(state, usage) {
    state.systemUsage = usage
  },
  SET_CHAT_STATS(state, stats) {
    state.chatStats = stats
  },
  SET_LOADING(state, isLoading) {
    state.loading = isLoading
  }
}

const actions = {
  // 获取仪表盘统计数据
  async fetchDashboardStats({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await getDashboardStats()
      commit('SET_STATS', response.data)
      return response.data
    } catch (error) {
      console.error('获取仪表盘统计数据失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取最近活跃的代理
  async fetchRecentAgents({ commit }, limit) {
    commit('SET_LOADING', true)
    try {
      const response = await getRecentAgents(limit)
      commit('SET_RECENT_AGENTS', response.data)
      return response.data
    } catch (error) {
      console.error('获取最近活跃代理失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取系统使用统计
  async fetchSystemUsage({ commit }) {
    commit('SET_LOADING', true)
    try {
      const response = await getSystemUsage()
      commit('SET_SYSTEM_USAGE', response.data)
      return response.data
    } catch (error) {
      console.error('获取系统使用统计失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取聊天统计数据
  async fetchChatStats({ commit }, timeRange) {
    commit('SET_LOADING', true)
    try {
      const response = await getChatStats(timeRange)
      commit('SET_CHAT_STATS', response.data)
      return response.data
    } catch (error) {
      console.error('获取聊天统计数据失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取所有仪表盘数据
  async fetchAllDashboardData({ dispatch }) {
    await Promise.all([
      dispatch('fetchDashboardStats'),
      dispatch('fetchRecentAgents', 5),
      dispatch('fetchSystemUsage')
    ])
  }
}

const getters = {
  dashboardStats: state => state.stats,
  recentAgents: state => state.recentAgents,
  systemUsage: state => state.systemUsage,
  chatStats: state => state.chatStats,
  loading: state => state.loading
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 