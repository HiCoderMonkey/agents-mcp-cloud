<template>
  <div class="agents-container">
    <div class="page-header">
      <h2>代理(Agent)管理</h2>
      <el-button type="primary" @click="dialogVisible = true">添加代理</el-button>
    </div>

    <!-- 代理列表 -->
    <el-table
      v-loading="loading"
      :data="agents"
      border
      style="width: 100%">
      <el-table-column
        prop="name"
        label="名称"
        width="180">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        prop="model"
        label="模型"
        width="120">
      </el-table-column>
      <el-table-column
        prop="llm_api_url"
        label="LLM地址"
        width="200"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        label="API密钥"
        width="100">
        <template slot-scope="scope">
          <el-tag size="small" type="info" v-if="scope.row.api_key">已设置</el-tag>
          <el-tag size="small" type="warning" v-else>未设置</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="关联服务器"
        min-width="200">
        <template slot-scope="scope">
          <el-tag
            v-for="serverId in scope.row.mcp_server_ids"
            :key="serverId"
            size="small"
            style="margin-right: 5px">
            {{ getServerName(serverId) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="is_active"
        label="状态"
        width="100">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            @change="updateAgentStatus(scope.row)">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="300">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="viewAgent(scope.row)">查看</el-button>
          <el-button
            size="mini"
            type="primary"
            @click="openChat(scope.row)">聊天</el-button>
          <el-button
            size="mini"
            @click="handleEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加分页组件 -->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 50, 100]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalAgents"
      class="pagination">
    </el-pagination>

    <!-- 添加/编辑代理对话框 -->
    <el-dialog :title="isEdit ? '编辑代理' : '添加代理'" :visible.sync="dialogVisible">
      <el-form 
        :model="agentForm" 
        :rules="rules" 
        ref="agentForm" 
        label-width="100px"
        label-position="left">
        <el-form-item label="名称" prop="name">
          <el-input v-model="agentForm.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="agentForm.description"></el-input>
        </el-form-item>
        <el-form-item label="模型" prop="model">
          <el-select v-model="agentForm.model" placeholder="请选择模型">
            <el-option label="glm-4-flash" value="glm-4-flash"></el-option>
            <el-option label="GPT-3.5" value="gpt-3.5-turbo"></el-option>
            <el-option label="GPT-4" value="gpt-4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="LLM地址" prop="llm_api_url">
          <el-input 
            v-model="agentForm.llm_api_url" 
            placeholder="例如: https://api.openai.com/v1">
          </el-input>
        </el-form-item>
        <el-form-item label="API密钥" prop="api_key">
          <el-input 
            v-model="agentForm.api_key" 
            type="password" 
            placeholder="请输入API密钥"
            show-password>
          </el-input>
        </el-form-item>
        <el-form-item label="温度" prop="temperature">
          <el-slider v-model="agentForm.temperature" :min="0" :max="1" :step="0.1"></el-slider>
        </el-form-item>
        <el-form-item label="最大Token" prop="max_tokens">
          <el-input-number v-model="agentForm.max_tokens" :min="100" :max="8000"></el-input-number>
        </el-form-item>
        <el-form-item label="服务器" prop="mcp_server_ids">
          <el-select 
            v-model="agentForm.mcp_server_ids" 
            multiple 
            collapse-tags
            placeholder="请选择MCP服务器">
            <el-option
              v-for="server in servers"
              :key="server.id"
              :label="server.name"
              :value="server.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="激活状态" prop="is_active">
          <el-switch v-model="agentForm.is_active"></el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveAgent" :loading="saveLoading">保存</el-button>
      </div>
    </el-dialog>

    <!-- 添加聊天对话框 -->
    <el-dialog
      title="聊天测试"
      :visible.sync="chatDialogVisible"
      width="60%"
      :before-close="handleChatClose">
      <agent-chat
        v-if="chatDialogVisible"
        :agent-id="currentAgentId">
      </agent-chat>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import AgentChat from '@/components/AgentChat.vue'

export default {
  name: 'Agents',
  components: {
    AgentChat
  },
  data() {
    return {
      saveLoading: false,
      dialogVisible: false,
      chatDialogVisible: false,  // 聊天对话框显示状态
      currentAgentId: null,      // 当前选中的Agent ID
      isEdit: false,
      currentPage: 1,
      pageSize: 10,
      localServers: [],
      agentForm: this.getEmptyAgentForm(),
      rules: {
        name: [
          { required: true, message: '请输入代理名称', trigger: 'blur' }
        ],
        model: [
          { required: true, message: '请选择模型', trigger: 'change' }
        ],
        llm_api_url: [
          { required: true, message: '请输入LLM服务接口地址', trigger: 'blur' },
          { type: 'url', message: '请输入有效的URL地址', trigger: 'blur' }
        ],
        api_key: [
          { required: true, message: '请输入API密钥', trigger: 'blur' },
          { min: 8, message: 'API密钥长度不能小于8个字符', trigger: 'blur' }
        ],
        mcp_server_ids: [
          { required: true, message: '请选择至少一个MCP服务器', trigger: 'change' },
          { type: 'array', min: 1, message: '请至少选择一个MCP服务器', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters({
      agents: 'agents/agentList',
      loading: 'agents/loading',
      totalAgents: 'agents/totalAgents'
    }),
    servers() {
      return this.localServers
    }
  },
  created() {
    this.fetchAgents()
    this.fetchMCPServers()
  },
  methods: {
    ...mapActions({
      fetchAgentList: 'agents/fetchAgents',
      createAgentAction: 'agents/createAgent',
      updateAgentAction: 'agents/updateAgent',
      deleteAgentAction: 'agents/deleteAgent',
      fetchMCPServerList: 'mcpServers/fetchMCPServerList'
    }),
    getEmptyAgentForm() {
      return {
        name: '',
        description: '',
        model: 'glm-4-flash',
        temperature: 0.7,
        max_tokens: 2048,
        mcp_server_ids: [],
        is_active: true,
        llm_api_url: 'https://open.bigmodel.cn/api/paas/v4/',
        api_key: ''
      }
    },
    async fetchAgents() {
      try {
        await this.fetchAgentList({
          skip: (this.currentPage - 1) * this.pageSize,
          limit: this.pageSize
        })
      } catch (error) {
        this.$message.error('获取代理列表失败')
        console.error(error)
      }
    },
    async fetchMCPServers() {
      try {
        const response = await this.fetchMCPServerList({
          page: 1,
          size: 100  // 获取较多数据，因为这是选择列表
        })
        // 确保我们使用正确的数据结构，并且保持ID的原始类型
        this.localServers = (response.items || []).map(server => ({
          ...server,
          id: server.id.toString()  // 确保ID是字符串类型
        }))
      } catch (error) {
        this.$message.error('获取服务器列表失败')
        console.error(error)
      }
    },
    viewAgent(row) {
      this.$router.push(`/agents/${row.id}`)
    },
    handleEdit(row) {
      this.isEdit = true
      this.agentForm = { ...row }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      this.$confirm('确认删除该代理?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await this.deleteAgentAction(row.id)
          this.$message.success('删除成功')
          this.fetchAgents()
        } catch (error) {
          this.$message.error('删除失败')
          console.error(error)
        }
      }).catch(() => {})
    },
    async saveAgent() {
      this.$refs.agentForm.validate(async (valid) => {
        if (valid) {
          this.saveLoading = true
          try {
            if (this.isEdit) {
              await this.updateAgentAction({
                id: this.agentForm.id,
                data: this.agentForm
              })
              this.$message.success('更新成功')
            } else {
              await this.createAgentAction(this.agentForm)
              this.$message.success('创建成功')
            }
            this.dialogVisible = false
            this.fetchAgents()
          } catch (error) {
            this.$message.error(this.isEdit ? '更新失败' : '创建失败')
            console.error(error)
          } finally {
            this.saveLoading = false
          }
        }
      })
    },
    async updateAgentStatus(row) {
      try {
        await this.updateAgentAction({
          id: row.id,
          data: { is_active: row.is_active }
        })
        this.$message.success('状态更新成功')
      } catch (error) {
        this.$message.error('状态更新失败')
        row.is_active = !row.is_active
      }
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.fetchAgents()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.fetchAgents()
    },
    getServerName(serverId) {
      const server = this.servers.find(s => s.id === serverId)
      return server ? server.name : '未知服务器'
    },
    openChat(agent) {
      this.currentAgentId = agent.id
      this.chatDialogVisible = true
    },
    handleChatClose(done) {
      this.currentAgentId = null
      done()
    }
  }
}
</script>

<style scoped>
.agents-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

h2 {
  margin: 0;
}

/* 添加表单样式 */
.el-form {
  padding: 20px;
}

.el-form-item {
  margin-bottom: 22px;
}

/* 让输入框占满可用宽度 */
.el-form-item :deep(.el-form-item__content) {
  display: flex;
  flex-direction: column;
}

.el-form-item :deep(.el-input),
.el-form-item :deep(.el-select),
.el-form-item :deep(.el-slider),
.el-form-item :deep(.el-input-number) {
  width: 100%;
}

/* 调整标签样式 */
.el-form-item :deep(.el-form-item__label) {
  padding: 0;
  line-height: 32px;
  color: #606266;
}

/* 调整对话框宽度 */
.el-dialog {
  min-width: 500px;
}

@media screen and (max-width: 768px) {
  .el-dialog {
    width: 90%;
  }
}

/* 添加聊天对话框样式 */
.el-dialog__body {
  padding: 0;
  height: 600px;
}
</style> 