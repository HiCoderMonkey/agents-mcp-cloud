import { 
  getMCPServers, 
  getMCPServerById, 
  createMCPServer, 
  updateMCPServer, 
  deleteMCPServer,
  testMCPServerConnection,
  getMCPServerStatus
} from '@/api/mcp-servers'

const state = {
  servers: [],
  currentServer: null,
  loading: false,
  totalServers: 0,
  connectionStatus: null
}

const mutations = {
  SET_SERVERS(state, { servers, total }) {
    state.servers = servers
    state.totalServers = total
  },
  SET_CURRENT_SERVER(state, server) {
    state.currentServer = server
  },
  ADD_SERVER(state, server) {
    state.servers.unshift(server)
    state.totalServers++
  },
  UPDATE_SERVER(state, updatedServer) {
    const index = state.servers.findIndex(server => server.id === updatedServer.id)
    if (index !== -1) {
      state.servers.splice(index, 1, updatedServer)
    }
    if (state.currentServer && state.currentServer.id === updatedServer.id) {
      state.currentServer = updatedServer
    }
  },
  REMOVE_SERVER(state, serverId) {
    state.servers = state.servers.filter(server => server.id !== serverId)
    state.totalServers--
    if (state.currentServer && state.currentServer.id === serverId) {
      state.currentServer = null
    }
  },
  SET_LOADING(state, isLoading) {
    state.loading = isLoading
  },
  SET_CONNECTION_STATUS(state, status) {
    state.connectionStatus = status
  }
}

const actions = {
  // 获取MCP服务器列表
  async fetchMCPServerList({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const response = await getMCPServers(params)
      const servers = response.data
      commit('SET_SERVERS', {
        servers: Array.isArray(servers) ? servers : [],
        total: Array.isArray(servers) ? servers.length : 0
      })
      return response
    } catch (error) {
      console.error('获取MCP服务器列表失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取单个MCP服务器详情
  async fetchMCPServerById({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await getMCPServerById(id)
      commit('SET_CURRENT_SERVER', response.data)
      return response.data
    } catch (error) {
      console.error('获取MCP服务器详情失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建MCP服务器
  async createMCPServer({ commit }, serverData) {
    commit('SET_LOADING', true)
    try {
      const response = await createMCPServer(serverData)
      commit('ADD_SERVER', response.data)
      return response.data
    } catch (error) {
      console.error('创建MCP服务器失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新MCP服务器
  async updateMCPServer({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await updateMCPServer(id, data)
      commit('UPDATE_SERVER', response.data)
      return response.data
    } catch (error) {
      console.error('更新MCP服务器失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除MCP服务器
  async deleteMCPServer({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await deleteMCPServer(id)
      commit('REMOVE_SERVER', id)
      return true
    } catch (error) {
      console.error('删除MCP服务器失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 测试MCP服务器连接
  async testConnection({ commit }, id) {
    commit('SET_LOADING', true)
    commit('SET_CONNECTION_STATUS', null)
    try {
      const response = await testMCPServerConnection(id)
      commit('SET_CONNECTION_STATUS', response.data)
      return response.data
    } catch (error) {
      console.error('测试连接失败:', error)
      commit('SET_CONNECTION_STATUS', { success: false, message: error.message || '连接失败' })
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取MCP服务器状态
  async getServerStatus({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await getMCPServerStatus(id)
      // 更新服务器对象中的状态信息
      const statusInfo = response.data
      if (state.currentServer && state.currentServer.id === id) {
        commit('SET_CURRENT_SERVER', {
          ...state.currentServer,
          status: statusInfo
        })
      }
      return statusInfo
    } catch (error) {
      console.error('获取服务器状态失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  }
}

const getters = {
  serverList: state => state.servers,
  currentServer: state => state.currentServer,
  loading: state => state.loading,
  totalServers: state => state.totalServers,
  connectionStatus: state => state.connectionStatus
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 