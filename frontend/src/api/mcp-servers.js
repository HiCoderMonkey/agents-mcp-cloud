import request from './config'

// 获取所有MCP服务器
export function getMCPServers(params) {
  return request({
    url: '/mcp-servers',
    method: 'get',
    params
  })
}

// 获取单个MCP服务器详情
export function getMCPServerById(id) {
  return request({
    url: `/mcp-servers/${id}`,
    method: 'get'
  })
}

// 创建新MCP服务器
export function createMCPServer(data) {
  return request({
    url: '/mcp-servers',
    method: 'post',
    data
  })
}

// 更新MCP服务器信息
export function updateMCPServer(id, data) {
  return request({
    url: `/mcp-servers/${id}`,
    method: 'put',
    data
  })
}

// 删除MCP服务器
export function deleteMCPServer(id) {
  return request({
    url: `/mcp-servers/${id}`,
    method: 'delete'
  })
}

// 测试MCP服务器连接
export function testMCPServerConnection(id) {
  return request({
    url: `/mcp-servers/${id}/test-connection`,
    method: 'post'
  })
}

// 获取MCP服务器状态
export function getMCPServerStatus(id) {
  return request({
    url: `/mcp-servers/${id}/status`,
    method: 'get'
  })
} 