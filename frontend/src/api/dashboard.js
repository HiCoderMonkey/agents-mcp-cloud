import request from './config'

// 获取仪表盘统计数据
export function getDashboardStats() {
  return request({
    url: '/dashboard/stats',
    method: 'get'
  })
}

// 获取最近活跃的代理
export function getRecentAgents(limit = 5) {
  return request({
    url: '/dashboard/recent-agents',
    method: 'get',
    params: { limit }
  })
}

// 获取系统使用统计
export function getSystemUsage() {
  return request({
    url: '/dashboard/system-usage',
    method: 'get'
  })
}

// 获取聊天统计数据（按时间）
export function getChatStats(timeRange) {
  return request({
    url: '/dashboard/chat-stats',
    method: 'get',
    params: { time_range: timeRange }
  })
} 