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
        width="250">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="viewAgent(scope.row)">查看</el-button>
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

    <!-- 添加/编辑代理对话框 -->
    <el-dialog :title="isEdit ? '编辑代理' : '添加代理'" :visible.sync="dialogVisible">
      <el-form :model="agentForm" :rules="rules" ref="agentForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="agentForm.name"></el-input>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input type="textarea" v-model="agentForm.description"></el-input>
        </el-form-item>
        <el-form-item label="模型" prop="model">
          <el-select v-model="agentForm.model" placeholder="请选择模型">
            <el-option label="GPT-3.5" value="gpt-3.5-turbo"></el-option>
            <el-option label="GPT-4" value="gpt-4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="温度" prop="temperature">
          <el-slider v-model="agentForm.temperature" :min="0" :max="1" :step="0.1"></el-slider>
        </el-form-item>
        <el-form-item label="最大Token" prop="max_tokens">
          <el-input-number v-model="agentForm.max_tokens" :min="100" :max="8000"></el-input-number>
        </el-form-item>
        <el-form-item label="服务器" prop="mcp_server_id">
          <el-select v-model="agentForm.mcp_server_id" placeholder="请选择MCP服务器">
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
  </div>
</template>

<script>
export default {
  name: 'Agents',
  data() {
    return {
      loading: false,
      saveLoading: false,
      dialogVisible: false,
      isEdit: false,
      agents: [],
      servers: [],
      agentForm: this.getEmptyAgentForm(),
      rules: {
        name: [
          { required: true, message: '请输入代理名称', trigger: 'blur' }
        ],
        model: [
          { required: true, message: '请选择模型', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.fetchAgents()
    this.fetchServers()
  },
  methods: {
    getEmptyAgentForm() {
      return {
        name: '',
        description: '',
        model: 'gpt-3.5-turbo',
        temperature: 0.7,
        max_tokens: 2048,
        mcp_server_id: null,
        is_active: true
      }
    },
    async fetchAgents() {
      this.loading = true
      try {
        // 这里应该调用API获取代理列表
        // const response = await this.$store.dispatch('fetchAgents')
        // this.agents = response.data

        // 模拟数据
        this.agents = [
          { id: 1, name: '客服助手', description: '用于回答客户问题的AI助手', model: 'gpt-3.5-turbo', temperature: 0.7, max_tokens: 2048, mcp_server_id: 1, is_active: true },
          { id: 2, name: '代码助手', description: '帮助编写和审查代码的AI助手', model: 'gpt-4', temperature: 0.5, max_tokens: 4096, mcp_server_id: 1, is_active: true }
        ]
      } catch (error) {
        this.$message.error('获取代理列表失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async fetchServers() {
      try {
        // 这里应该调用API获取服务器列表
        // const response = await this.$store.dispatch('fetchServers')
        // this.servers = response.data

        // 模拟数据
        this.servers = [
          { id: 1, name: '测试服务器1' },
          { id: 2, name: '测试服务器2' }
        ]
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
          // 调用API删除代理
          // await this.$store.dispatch('deleteAgent', row.id)
          this.$message.success('删除成功')
          this.fetchAgents()
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    },
    async saveAgent() {
      this.$refs.agentForm.validate(async (valid) => {
        if (valid) {
          this.saveLoading = true
          try {
            if (this.isEdit) {
              // 更新代理
              // await this.$store.dispatch('updateAgent', this.agentForm)
              this.$message.success('更新成功')
            } else {
              // 创建代理
              // await this.$store.dispatch('createAgent', this.agentForm)
              this.$message.success('创建成功')
            }
            this.dialogVisible = false
            this.fetchAgents()
          } catch (error) {
            this.$message.error(this.isEdit ? '更新失败' : '创建失败')
          } finally {
            this.saveLoading = false
          }
        }
      })
    },
    async updateAgentStatus(row) {
      try {
        // 更新代理状态
        // await this.$store.dispatch('updateAgentStatus', { id: row.id, is_active: row.is_active })
        this.$message.success('状态更新成功')
      } catch (error) {
        this.$message.error('状态更新失败')
        // 回滚UI状态
        row.is_active = !row.is_active
      }
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

h2 {
  margin: 0;
}
</style> 