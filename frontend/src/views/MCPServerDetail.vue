<template>
  <div class="server-detail-container">
    <div class="page-header">
      <h2>MCP服务详情</h2>
      <div>
        <el-button @click="$router.push('/mcp-servers')">返回</el-button>
        <el-button type="primary" @click="goToEdit">编辑</el-button>
        <el-button type="danger" @click="handleDelete">删除</el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :md="16">
        <el-card shadow="hover" v-loading="loading">
          <div slot="header">
            <span>基本信息</span>
          </div>
          <div v-if="server" class="server-info">
            <div class="info-item">
              <span class="label">ID:</span>
              <span class="value">{{ server.id }}</span>
            </div>
            <div class="info-item">
              <span class="label">名称:</span>
              <span class="value">{{ server.name }}</span>
            </div>
            <div class="info-item">
              <span class="label">描述:</span>
              <span class="value">{{ server.description || '无' }}</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间:</span>
              <span class="value">{{ formatDate(server.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">更新时间:</span>
              <span class="value">{{ formatDate(server.updated_at) }}</span>
            </div>
          </div>
          <div v-else class="empty-data">没有服务信息</div>
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card shadow="hover" class="agents-card">
          <div slot="header">
            <span>关联代理</span>
          </div>
          <div class="agents-content">
            <el-table
              :data="agents"
              style="width: 100%">
              <el-table-column
                prop="name"
                label="名称">
              </el-table-column>
              <el-table-column
                prop="model"
                label="模型">
              </el-table-column>
              <el-table-column
                label="操作"
                width="100">
                <template slot-scope="scope">
                  <el-button size="mini" @click="viewAgent(scope.row)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div v-if="!agents.length" class="empty-data">
              没有关联的代理
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="24">
        <el-card shadow="hover" class="config-card">
          <div slot="header">
            <span>配置内容</span>
            <el-button
              style="float: right; padding: 3px 0"
              type="text"
              @click="copyConfig">
              复制配置
            </el-button>
          </div>
          <div class="json-content">
            <pre>{{ formatJSON(server?.config) }}</pre>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 删除确认对话框 -->
    <el-dialog
      title="确认删除"
      :visible.sync="deleteDialogVisible"
      width="30%">
      <span>确定要删除此MCP服务吗？此操作不可撤销。</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete" :loading="deleteLoading">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'MCPServerDetail',
  data() {
    return {
      deleteDialogVisible: false,
      deleteLoading: false,
      agents: []
    }
  },
  computed: {
    ...mapGetters({
      server: 'mcpServers/currentServer',
      loading: 'mcpServers/loading'
    }),
    serverId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchServerDetails()
    this.fetchRelatedAgents()
  },
  methods: {
    ...mapActions({
      fetchMCPServerById: 'mcpServers/fetchMCPServerById',
      deleteMCPServer: 'mcpServers/deleteMCPServer'
    }),
    async fetchServerDetails() {
      try {
        await this.fetchMCPServerById(this.serverId)
      } catch (error) {
        this.$message.error('获取服务详情失败')
        console.error(error)
      }
    },
    async fetchRelatedAgents() {
      try {
        // 这里应该调用API获取与此MCP服务关联的代理
        // 模拟数据
        this.agents = [
          { id: 1, name: '客服助手', model: 'gpt-3.5-turbo' },
          { id: 2, name: '数据分析助手', model: 'gpt-4' }
        ]
      } catch (error) {
        console.error('获取关联代理失败:', error)
      }
    },
    viewAgent(agent) {
      this.$router.push(`/agents/${agent.id}`)
    },
    goToEdit() {
      this.$router.push(`/mcp-servers/${this.serverId}/edit`)
    },
    handleDelete() {
      this.deleteDialogVisible = true
    },
    async confirmDelete() {
      this.deleteLoading = true
      try {
        await this.deleteMCPServer(this.serverId)
        this.$message.success('删除成功')
        this.$router.push('/mcp-servers')
      } catch (error) {
        this.$message.error('删除失败')
        console.error(error)
      } finally {
        this.deleteLoading = false
        this.deleteDialogVisible = false
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '未知'
      const date = new Date(dateStr)
      return date.toLocaleString()
    },
    formatJSON(json) {
      if (!json) return '{}'
      return JSON.stringify(json, null, 2)
    },
    copyConfig() {
      if (!this.server || !this.server.config) return
      
      const configStr = JSON.stringify(this.server.config, null, 2)
      navigator.clipboard.writeText(configStr)
        .then(() => {
          this.$message.success('配置已复制到剪贴板')
        })
        .catch(err => {
          console.error('复制失败:', err)
          this.$message.error('复制失败')
        })
    }
  }
}
</script>

<style scoped>
.server-detail-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h2 {
  margin: 0;
}

.el-card {
  margin-bottom: 20px;
}

.server-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
}

.label {
  flex: 0 0 100px;
  font-weight: bold;
  color: #606266;
}

.value {
  flex: 1;
}

.empty-data {
  color: #909399;
  text-align: center;
  padding: 20px 0;
}

.agents-content {
  min-height: 100px;
}

.json-content {
  overflow: auto;
  max-height: 500px;
  background-color: #f8f8f8;
  border-radius: 4px;
  padding: 10px;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.config-card {
  margin-top: 10px;
}
</style> 