import request from './config'

// 获取所有代理
export function getAgents(params) {
  return request({
    url: '/agents',
    method: 'get',
    params
  })
}

// 获取单个代理详情
export function getAgentById(id) {
  return request({
    url: `/agents/${id}`,
    method: 'get'
  })
}

// 创建新代理
export function createAgent(data) {
  return request({
    url: '/agents',
    method: 'post',
    data
  })
}

// 更新代理信息
export function updateAgent(id, data) {
  return request({
    url: `/agents/${id}`,
    method: 'put',
    data
  })
}

// 删除代理
export function deleteAgent(id) {
  return request({
    url: `/agents/${id}`,
    method: 'delete'
  })
}

// 获取代理的聊天历史
export function getAgentChatHistory(id, params) {
  return request({
    url: `/agents/${id}/chat-history`,
    method: 'get',
    params
  })
}

// 发送消息给代理
export function sendMessageToAgent(id, data) {
  return request({
    url: `/agents/${id}/chat`,
    method: 'post',
    data
  })
}

// 获取代理的SDK密钥
export function getAgentSDKKeys(id) {
  return request({
    url: `/agents/${id}/sdk-keys`,
    method: 'get'
  })
}

// 为代理创建新的SDK密钥
export function createAgentSDKKey(id, data) {
  return request({
    url: `/agents/${id}/sdk-keys`,
    method: 'post',
    data
  })
}

// 删除代理的SDK密钥
export function deleteAgentSDKKey(agentId, keyId) {
  return request({
    url: `/agents/${agentId}/sdk-keys/${keyId}`,
    method: 'delete'
  })
}

// 更新代理的SDK密钥状态
export function updateAgentSDKKeyStatus(agentId, keyId, isActive) {
  return request({
    url: `/agents/${agentId}/sdk-keys/${keyId}/status`,
    method: 'patch',
    data: { is_active: isActive }
  })
} 