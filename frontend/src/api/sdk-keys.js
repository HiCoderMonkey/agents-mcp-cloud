import request from './config'

// 获取所有SDK密钥
export function getAllSDKKeys(params) {
  return request({
    url: '/sdk-keys',
    method: 'get',
    params
  })
}

// 获取单个SDK密钥详情
export function getSDKKeyById(id) {
  return request({
    url: `/sdk-keys/${id}`,
    method: 'get'
  })
}

// 创建新的SDK密钥
export function createSDKKey(data) {
  return request({
    url: '/sdk-keys',
    method: 'post',
    data
  })
}

// 删除SDK密钥
export function deleteSDKKey(id) {
  return request({
    url: `/sdk-keys/${id}`,
    method: 'delete'
  })
}

// 更新SDK密钥状态
export function updateSDKKeyStatus(id, isActive) {
  return request({
    url: `/sdk-keys/${id}/status`,
    method: 'patch',
    data: { is_active: isActive }
  })
} 