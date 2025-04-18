import { 
  getAgents, 
  getAgentById, 
  createAgent, 
  updateAgent, 
  deleteAgent,
  getAgentChatHistory,
  getAgentSDKKeys,
  createAgentSDKKey,
  deleteAgentSDKKey,
  updateAgentSDKKeyStatus
} from '@/api/agents'
import request from '@/utils/request'

const state = {
  agents: [],
  currentAgent: null,
  chatHistory: [],
  sdkKeys: [],
  loading: false,
  totalAgents: 0
}

const mutations = {
  SET_AGENTS(state, { agents, total }) {
    state.agents = agents
    state.totalAgents = total
  },
  SET_CURRENT_AGENT(state, agent) {
    state.currentAgent = agent
  },
  SET_CHAT_HISTORY(state, history) {
    state.chatHistory = history
  },
  SET_SDK_KEYS(state, keys) {
    state.sdkKeys = keys
  },
  ADD_SDK_KEY(state, key) {
    state.sdkKeys.unshift(key)
  },
  REMOVE_SDK_KEY(state, keyId) {
    state.sdkKeys = state.sdkKeys.filter(key => key.id !== keyId)
  },
  UPDATE_SDK_KEY_STATUS(state, { keyId, isActive }) {
    const key = state.sdkKeys.find(k => k.id === keyId)
    if (key) {
      key.is_active = isActive
    }
  },
  ADD_AGENT(state, agent) {
    state.agents.unshift(agent)
    state.totalAgents++
  },
  UPDATE_AGENT(state, updatedAgent) {
    const index = state.agents.findIndex(agent => agent.id === updatedAgent.id)
    if (index !== -1) {
      state.agents.splice(index, 1, updatedAgent)
    }
    if (state.currentAgent && state.currentAgent.id === updatedAgent.id) {
      state.currentAgent = updatedAgent
    }
  },
  REMOVE_AGENT(state, agentId) {
    state.agents = state.agents.filter(agent => agent.id !== agentId)
    state.totalAgents--
    if (state.currentAgent && state.currentAgent.id === agentId) {
      state.currentAgent = null
    }
  },
  SET_LOADING(state, isLoading) {
    state.loading = isLoading
  }
}

const actions = {
  // 获取代理列表
  async fetchAgents({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const response = await getAgents(params)
      const agents = response.data
      commit('SET_AGENTS', {
        agents: Array.isArray(agents) ? agents : [],
        total: Array.isArray(agents) ? agents.length : 0
      })
      return agents
    } catch (error) {
      console.error('获取代理列表失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取单个代理详情
  async fetchAgentById({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await getAgentById(id)
      commit('SET_CURRENT_AGENT', response.data)
      return response.data
    } catch (error) {
      console.error('获取代理详情失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建新代理
  async createAgent({ commit }, agentData) {
    commit('SET_LOADING', true)
    try {
      const response = await createAgent(agentData)
      commit('ADD_AGENT', response.data)
      return response.data
    } catch (error) {
      console.error('创建代理失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新代理信息
  async updateAgent({ commit }, { id, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await updateAgent(id, data)
      commit('UPDATE_AGENT', response.data)
      return response.data
    } catch (error) {
      console.error('更新代理失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除代理
  async deleteAgent({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await deleteAgent(id)
      commit('REMOVE_AGENT', id)
      return true
    } catch (error) {
      console.error('删除代理失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取代理聊天历史
  async fetchAgentChatHistory({ commit }, { id, params }) {
    commit('SET_LOADING', true)
    try {
      const response = await getAgentChatHistory(id, params)
      commit('SET_CHAT_HISTORY', response.data.items || [])
      return response.data
    } catch (error) {
      console.error('获取聊天历史失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取代理的SDK密钥
  async fetchAgentSDKKeys({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await getAgentSDKKeys(id)
      commit('SET_SDK_KEYS', response.data)
      return response.data
    } catch (error) {
      console.error('获取SDK密钥失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 为代理创建新的SDK密钥
  async createSDKKey({ commit }, { agentId, data }) {
    commit('SET_LOADING', true)
    try {
      const response = await createAgentSDKKey(agentId, data)
      commit('ADD_SDK_KEY', response.data)
      return response.data
    } catch (error) {
      console.error('创建SDK密钥失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除代理的SDK密钥
  async deleteSDKKey({ commit }, { agentId, keyId }) {
    commit('SET_LOADING', true)
    try {
      await deleteAgentSDKKey(agentId, keyId)
      commit('REMOVE_SDK_KEY', keyId)
      return true
    } catch (error) {
      console.error('删除SDK密钥失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新代理的SDK密钥状态
  async updateSDKKeyStatus({ commit }, { agentId, keyId, isActive }) {
    commit('SET_LOADING', true)
    try {
      await updateAgentSDKKeyStatus(agentId, keyId, isActive)
      commit('UPDATE_SDK_KEY_STATUS', { keyId, isActive })
      return true
    } catch (error) {
      console.error('更新SDK密钥状态失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },

  // 发送消息到Agent
  async sendMessage(_, { agentId, message }) {
    const response = await request({
      url: `/agents/${agentId}/send`,
      method: 'post',
      data: { message }
    })
    return response.data
  },

  // 获取与Agent的聊天历史
  async getChatHistory(_, { agentId, skip = 0, limit = 20 }) {
    const response = await request({
      url: `/agents/${agentId}/history`,
      method: 'get',
      params: { skip, limit }
    })
    return response.data
  }
}

const getters = {
  agentList: state => state.agents,
  currentAgent: state => state.currentAgent,
  chatHistory: state => state.chatHistory,
  sdkKeys: state => state.sdkKeys,
  loading: state => state.loading,
  totalAgents: state => state.totalAgents
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 