<template>
  <div class="agent-detail-container" v-loading="loading">
    <div class="page-header">
      <div class="title-section">
        <el-button icon="el-icon-back" @click="$router.push('/agents')">返回</el-button>
        <h2>{{ agent.name }}</h2>
        <el-tag type="success" v-if="agent.is_active">激活</el-tag>
        <el-tag type="info" v-else>未激活</el-tag>
      </div>
      <div>
        <el-button type="primary" @click="handleEdit">编辑</el-button>
        <el-button type="success" @click="startChat">开始聊天</el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="info">
        <el-card class="detail-card">
          <div slot="header">基本信息</div>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="名称">{{ agent.name }}</el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(agent.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="模型">{{ agent.model }}</el-descriptions-item>
            <el-descriptions-item label="温度">{{ agent.temperature }}</el-descriptions-item>
            <el-descriptions-item label="最大Token">{{ agent.max_tokens }}</el-descriptions-item>
            <el-descriptions-item label="服务器">{{ serverName }}</el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">{{ agent.description }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="SDK密钥" name="keys">
        <el-card class="detail-card">
          <div slot="header" class="sdk-header">
            <span>SDK密钥</span>
            <el-button size="small" type="primary" @click="openCreateDialog">创建密钥</el-button>
          </div>
          <el-table :data="sdkKeys" border style="width: 100%">
            <el-table-column prop="name" label="名称"></el-table-column>
            <el-table-column prop="key" label="密钥" width="180">
              <template slot-scope="scope">
                <div class="key-display">
                  <span>{{ maskKey(scope.row.key) }}</span>
                  <el-button type="text" icon="el-icon-view" @click="toggleKeyVisibility(scope.row)"></el-button>
                  <el-button type="text" icon="el-icon-document-copy" @click="copyKey(scope.row.key)"></el-button>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180">
              <template slot-scope="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="状态" width="80">
              <template slot-scope="scope">
                <el-switch v-model="scope.row.is_active" @change="updateKeyStatus(scope.row)"></el-switch>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="聊天记录" name="chats">
        <el-card class="detail-card">
          <div slot="header">最近聊天记录</div>
          <el-empty v-if="chatHistory.length === 0" description="暂无聊天记录"></el-empty>
          <div v-else class="chat-list">
            <div v-for="chat in chatHistory" :key="chat.id" class="chat-item">
              <div class="chat-time">{{ formatDate(chat.created_at) }}</div>
              <div class="chat-preview">
                <div class="message user">用户: {{ chat.user_message }}</div>
                <div class="message agent">助手: {{ chat.agent_message }}</div>
              </div>
              <el-button type="text" @click="viewChat(chat)">查看详情</el-button>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 创建SDK密钥对话框 -->
    <el-dialog title="创建SDK密钥" :visible.sync="dialogVisible">
      <el-form :model="form" :rules="rules" ref="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="为此密钥添加名称，例如: 测试密钥"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="createKey" :loading="submitLoading">创建</el-button>
      </div>
    </el-dialog>

    <!-- 新创建的密钥展示对话框 -->
    <el-dialog title="请保存您的密钥" :visible.sync="newKeyDialogVisible" :close-on-click-modal="false">
      <div class="new-key-display">
        <p class="warning">请立即保存您的密钥，它不会再次显示！</p>
        <div class="key-value">{{ newKey }}</div>
        <el-button type="primary" @click="copyKey(newKey)">复制密钥</el-button>
      </div>
      <div slot="footer">
        <el-button type="primary" @click="newKeyDialogVisible = false">我已保存密钥</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'AgentDetail',
  data() {
    return {
      dialogVisible: false,
      newKeyDialogVisible: false,
      activeTab: 'info',
      form: {
        name: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入密钥名称', trigger: 'blur' }
        ]
      },
      submitLoading: false,
      visibleKeys: new Set() // 跟踪哪些key应该显示完整内容
    }
  },
  computed: {
    ...mapGetters({
      agent: 'agents/currentAgent',
      loading: 'agents/loading',
      sdkKeys: 'agents/sdkKeys',
      chatHistory: 'agents/chatHistory',
      newKey: 'agents/newKey'
    }),
    agentId() {
      return this.$route.params.id
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    ...mapActions({
      fetchAgentById: 'agents/fetchAgentById',
      fetchAgentSDKKeys: 'agents/fetchAgentSDKKeys',
      fetchAgentChatHistory: 'agents/fetchAgentChatHistory',
      createSDKKey: 'agents/createSDKKey',
      deleteSDKKey: 'agents/deleteSDKKey',
      updateSDKKeyStatus: 'agents/updateSDKKeyStatus'
    }),
    async fetchData() {
      try {
        await this.fetchAgentById(this.agentId)
        await this.fetchAgentSDKKeys(this.agentId)
        if (this.activeTab === 'chats') {
          await this.fetchChatHistory()
        }
      } catch (error) {
        this.$message.error('获取代理详情失败')
        console.error(error)
      }
    },
    async fetchChatHistory() {
      try {
        await this.fetchAgentChatHistory({
          id: this.agentId,
          params: { limit: 50 }
        })
      } catch (error) {
        this.$message.error('获取聊天历史失败')
        console.error(error)
      }
    },
    handleTabChange(tab) {
      if (tab === 'chats' && (!this.chatHistory || this.chatHistory.length === 0)) {
        this.fetchChatHistory()
      }
    },
    openCreateDialog() {
      this.form = { name: '' }
      this.dialogVisible = true
    },
    async createKey() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          this.submitLoading = true
          try {
            await this.createSDKKey({
              agentId: this.agentId,
              data: this.form
            })
            this.dialogVisible = false
            this.newKeyDialogVisible = true
          } catch (error) {
            this.$message.error('创建密钥失败')
            console.error(error)
          } finally {
            this.submitLoading = false
          }
        }
      })
    },
    async handleDelete(row) {
      this.$confirm('确定要删除该密钥吗？删除后将无法恢复。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await this.deleteSDKKey({
            agentId: this.agentId,
            keyId: row.id
          })
          this.$message.success('删除成功')
        } catch (error) {
          this.$message.error('删除失败')
          console.error(error)
        }
      }).catch(() => {})
    },
    async updateKeyStatus(key) {
      try {
        await this.updateSDKKeyStatus({
          agentId: this.agentId,
          keyId: key.id,
          isActive: key.is_active
        })
        this.$message.success('状态更新成功')
      } catch (error) {
        this.$message.error('状态更新失败')
        // 回滚UI状态
        key.is_active = !key.is_active
        console.error(error)
      }
    },
    handleEdit() {
      this.$router.push(`/agents/${this.agent.id}/edit`)
    },
    startChat() {
      this.$router.push(`/chat/${this.agent.id}`)
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString()
    },
    toggleKeyVisibility(key) {
      if (this.visibleKeys.has(key.id)) {
        this.visibleKeys.delete(key.id)
      } else {
        this.visibleKeys.add(key.id)
      }
    },
    maskKey(key) {
      const id = this.sdkKeys.find(k => k.key === key)?.id
      if (this.visibleKeys.has(id)) {
        return key
      }
      return key.substring(0, 7) + '...' + key.substring(key.length - 4)
    },
    copyKey(key) {
      // 复制密钥到剪贴板
      navigator.clipboard.writeText(key).then(() => {
        this.$message.success('已复制到剪贴板')
      })
    },
    viewChat(chat) {
      // 跳转到聊天详情页面
      this.$router.push(`/chat/${this.agent.id}?session=${chat.id}`)
    }
  }
}
</script>

<style scoped>
.agent-detail-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

h2 {
  margin: 0;
}

.detail-card {
  margin-bottom: 20px;
}

.sdk-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.key-display {
  display: flex;
  align-items: center;
  gap: 5px;
}

.new-key-display {
  text-align: center;
  padding: 20px;
}

.warning {
  color: #E6A23C;
  font-weight: bold;
  margin-bottom: 15px;
}

.key-value {
  background: #f5f7fa;
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  margin-bottom: 15px;
  word-break: break-all;
}

.chat-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.chat-item {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 15px;
}

.chat-time {
  color: #909399;
  margin-bottom: 10px;
}

.chat-preview {
  margin-bottom: 10px;
}

.message {
  margin-bottom: 5px;
}

.message.user {
  color: #409EFF;
}

.message.agent {
  color: #67C23A;
}
</style> 