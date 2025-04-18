import request from './config'

// 用户登录
export function login(data) {
  return request({
    url: '/auth/json-login',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
  })
}

// 用户退出登录
export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

// 获取当前用户信息
export function getUserInfo() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

// 用户注册
export function register(data) {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

// 重置密码请求
export function resetPasswordRequest(email) {
  return request({
    url: '/auth/reset-password-request',
    method: 'post',
    data: { email }
  })
}

// 使用新密码重置
export function resetPassword(data) {
  return request({
    url: '/auth/reset-password',
    method: 'post',
    data
  })
}

// 更新用户资料
export function updateProfile(data) {
  return request({
    url: '/users/me',
    method: 'put',
    data
  })
}

// 更改密码
export function changePassword(data) {
  return request({
    url: '/users/me/password',
    method: 'put',
    data
  })
} 