<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1>欢迎使用 MCP Cloud</h1>
      <p>集成多种大模型能力的智能代理管理平台</p>
    </div>

    <el-row :gutter="20" class="stat-cards">
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="stat-card">
          <div slot="header">
            <i class="el-icon-s-cooperation"></i>
            <span>MCP 服务器</span>
          </div>
          <div class="card-content">
            <div class="stat-number">{{ stats.serverCount }}</div>
            <div class="stat-label">已连接服务器</div>
          </div>
          <el-button type="text" @click="$router.push('/mcp-servers')">管理服务器</el-button>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="stat-card">
          <div slot="header">
            <i class="el-icon-s-custom"></i>
            <span>智能代理</span>
          </div>
          <div class="card-content">
            <div class="stat-number">{{ stats.agentCount }}</div>
            <div class="stat-label">已创建代理</div>
          </div>
          <el-button type="text" @click="$router.push('/agents')">管理代理</el-button>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="stat-card">
          <div slot="header">
            <i class="el-icon-key"></i>
            <span>SDK 密钥</span>
          </div>
          <div class="card-content">
            <div class="stat-number">{{ stats.keyCount }}</div>
            <div class="stat-label">活跃密钥</div>
          </div>
          <el-button type="text" @click="$router.push('/sdk-keys')">管理密钥</el-button>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="8" :lg="6">
        <el-card shadow="hover" class="stat-card">
          <div slot="header">
            <i class="el-icon-chat-dot-round"></i>
            <span>对话</span>
          </div>
          <div class="card-content">
            <div class="stat-number">{{ stats.chatCount }}</div>
            <div class="stat-label">本月对话次数</div>
          </div>
          <el-button type="text" @click="startNewChat">开始新对话</el-button>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-section">
      <el-col :xs="24" :lg="16">
        <el-card shadow="hover" class="recent-card">
          <div slot="header">
            <span>最近活跃的代理</span>
            <el-button style="float: right; padding: 3px 0" type="text" @click="$router.push('/agents')">
              查看全部
            </el-button>
          </div>
          <el-table :data="recentAgents" style="width: 100%">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="model" label="模型"></el-table-column>
            <el-table-column prop="chat_count" label="对话量"></el-table-column>
            <el-table-column prop="last_active" label="最近活跃">
              <template slot-scope="scope">
                {{ formatDate(scope.row.last_active) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template slot-scope="scope">
                <el-button size="mini" @click="viewAgent(scope.row)">详情</el-button>
                <el-button size="mini" type="primary" @click="chatWithAgent(scope.row)">聊天</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :xs="24" :lg="8">
        <el-card shadow="hover" class="quick-actions">
          <div slot="header">
            <span>快速操作</span>
          </div>
          <div class="action-list">
            <el-button type="primary" icon="el-icon-plus" @click="$router.push('/agents/create')">
              创建新代理
            </el-button>
            <el-button type="success" icon="el-icon-connection" @click="$router.push('/mcp-servers/create')">
              添加MCP服务器
            </el-button>
            <el-button type="info" icon="el-icon-key" @click="$router.push('/sdk-keys')">
              管理SDK密钥
            </el-button>
            <el-button type="warning" icon="el-icon-user" @click="$router.push('/profile')">
              账户设置
            </el-button>
          </div>

          <div class="docs-section">
            <h3>快速文档</h3>
            <ul>
              <li><a href="#" target="_blank">入门指南</a></li>
              <li><a href="#" target="_blank">API文档</a></li>
              <li><a href="#" target="_blank">SDK使用说明</a></li>
              <li><a href="#" target="_blank">常见问题</a></li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      loading: false
    }
  },
  computed: {
    ...mapGetters('dashboard', [
      'dashboardStats',
      'recentAgents'
    ]),
    stats() {
      return this.dashboardStats
    }
  },
  created() {
    this.fetchDashboardData()
  },
  methods: {
    ...mapActions('dashboard', [
      'fetchDashboardStats',
      'fetchRecentAgents'
    ]),
    async fetchDashboardData() {
      this.loading = true
      try {
        await Promise.all([
          this.fetchDashboardStats(),
          this.fetchRecentAgents(5)
        ])
      } catch (error) {
        this.$message.error('获取仪表盘数据失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    viewAgent(agent) {
      this.$router.push(`/agents/${agent.id}`)
    },
    chatWithAgent(agent) {
      this.$router.push(`/chat/${agent.id}`)
    },
    startNewChat() {
      // 假设我们会导航到代理选择页面
      this.$router.push('/chat')
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-section {
  text-align: center;
  margin-bottom: 30px;
}

.welcome-section h1 {
  margin-bottom: 10px;
  font-size: 28px;
  color: #303133;
}

.welcome-section p {
  font-size: 16px;
  color: #606266;
}

.stat-cards {
  margin-bottom: 30px;
}

.stat-card {
  height: 100%;
}

.stat-card .el-card__header {
  display: flex;
  align-items: center;
  padding: 12px 20px;
}

.stat-card .el-card__header i {
  margin-right: 8px;
  font-size: 18px;
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.content-section {
  margin-bottom: 20px;
}

.recent-card {
  margin-bottom: 20px;
}

.quick-actions {
  height: 100%;
}

.action-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.docs-section {
  margin-top: 20px;
}

.docs-section h3 {
  font-size: 16px;
  margin-bottom: 10px;
}

.docs-section ul {
  padding-left: 20px;
}

.docs-section li {
  margin-bottom: 5px;
}

.docs-section a {
  color: #409EFF;
  text-decoration: none;
}

.docs-section a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .stat-cards > div {
    margin-bottom: 15px;
  }
}
</style> 