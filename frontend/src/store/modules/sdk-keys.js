import { 
  getAllSDKKeys, 
  getSDKKeyById, 
  createSDKKey, 
  deleteSDKKey, 
  updateSDKKeyStatus 
} from '@/api/sdk-keys'

const state = {
  sdkKeys: [],
  totalKeys: 0,
  currentKey: null,
  loading: false,
  newKey: null // 新创建的密钥，用于显示给用户
}

const mutations = {
  SET_SDK_KEYS(state, { keys, total }) {
    state.sdkKeys = keys
    state.totalKeys = total
  },
  SET_CURRENT_KEY(state, key) {
    state.currentKey = key
  },
  SET_NEW_KEY(state, key) {
    state.newKey = key
  },
  ADD_SDK_KEY(state, key) {
    state.sdkKeys.unshift(key)
    state.totalKeys++
  },
  REMOVE_SDK_KEY(state, keyId) {
    state.sdkKeys = state.sdkKeys.filter(key => key.id !== keyId)
    state.totalKeys--
    if (state.currentKey && state.currentKey.id === keyId) {
      state.currentKey = null
    }
  },
  UPDATE_SDK_KEY_STATUS(state, { keyId, isActive }) {
    const key = state.sdkKeys.find(k => k.id === keyId)
    if (key) {
      key.is_active = isActive
    }
    if (state.currentKey && state.currentKey.id === keyId) {
      state.currentKey.is_active = isActive
    }
  },
  SET_LOADING(state, isLoading) {
    state.loading = isLoading
  }
}

const actions = {
  // 获取所有SDK密钥
  async fetchAllSDKKeys({ commit }, params) {
    commit('SET_LOADING', true)
    try {
      const response = await getAllSDKKeys(params)
      commit('SET_SDK_KEYS', {
        keys: response.data.items,
        total: response.data.total
      })
      return response.data
    } catch (error) {
      console.error('获取SDK密钥列表失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 获取单个SDK密钥详情
  async fetchSDKKeyById({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      const response = await getSDKKeyById(id)
      commit('SET_CURRENT_KEY', response.data)
      return response.data
    } catch (error) {
      console.error('获取SDK密钥详情失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 创建新的SDK密钥
  async createSDKKey({ commit }, data) {
    commit('SET_LOADING', true)
    try {
      const response = await createSDKKey(data)
      commit('ADD_SDK_KEY', {
        ...response.data,
        key: '***************' // 隐藏实际密钥
      })
      commit('SET_NEW_KEY', response.data.key) // 保存完整密钥，用于一次性显示
      return response.data
    } catch (error) {
      console.error('创建SDK密钥失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 删除SDK密钥
  async deleteSDKKey({ commit }, id) {
    commit('SET_LOADING', true)
    try {
      await deleteSDKKey(id)
      commit('REMOVE_SDK_KEY', id)
      return true
    } catch (error) {
      console.error('删除SDK密钥失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 更新SDK密钥状态
  async updateSDKKeyStatus({ commit }, { id, isActive }) {
    commit('SET_LOADING', true)
    try {
      await updateSDKKeyStatus(id, isActive)
      commit('UPDATE_SDK_KEY_STATUS', { keyId: id, isActive })
      return true
    } catch (error) {
      console.error('更新SDK密钥状态失败:', error)
      return Promise.reject(error)
    } finally {
      commit('SET_LOADING', false)
    }
  },
  
  // 清除新创建的密钥（用户已查看后）
  clearNewKey({ commit }) {
    commit('SET_NEW_KEY', null)
  }
}

const getters = {
  sdkKeyList: state => state.sdkKeys,
  currentKey: state => state.currentKey,
  newKey: state => state.newKey,
  loading: state => state.loading,
  totalKeys: state => state.totalKeys
}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters
} 