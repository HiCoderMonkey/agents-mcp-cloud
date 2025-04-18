<template>
  <div class="server-form-container">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑MCP服务器' : '创建MCP服务器' }}</h2>
      <div>
        <el-button @click="goBack">返回</el-button>
        <el-button v-if="isEdit" type="success" @click="testConnection">测试连接</el-button>
      </div>
    </div>

    <el-card class="form-card">
      <el-form 
        :model="form" 
        :rules="rules" 
        ref="form" 
        label-width="120px"
        v-loading="loading">
        <!-- MCP服务名称 -->
        <el-form-item label="服务名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入MCP服务名称"></el-input>
        </el-form-item>

        <!-- MCP服务描述 -->
        <el-form-item label="服务描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入MCP服务描述"
          ></el-input>
        </el-form-item>

        <!-- MCP配置内容 -->
        <el-form-item label="配置内容" prop="config">
          <json-editor v-model="form.config" height="400px"></json-editor>
          <div class="form-tips">请输入JSON格式的配置内容</div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="submitLoading">
            {{ isEdit ? '保存修改' : '创建服务器' }}
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 连接测试结果对话框 -->
    <el-dialog
      title="连接测试结果"
      :visible.sync="connectionDialogVisible"
      width="30%">
      <div v-if="connectionStatus">
        <div v-if="connectionStatus.success" class="connection-success">
          <i class="el-icon-success"></i>
          <p>连接成功!</p>
          <div class="connection-details">
            <p><strong>服务器版本:</strong> {{ connectionStatus.version || '未知' }}</p>
            <p><strong>消息:</strong> {{ connectionStatus.message }}</p>
          </div>
        </div>
        <div v-else class="connection-error">
          <i class="el-icon-error"></i>
          <p>连接失败!</p>
          <div class="connection-details">
            <p><strong>错误信息:</strong> {{ connectionStatus.message }}</p>
          </div>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="connectionDialogVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import JsonEditor from '@/components/JsonEditor'

export default {
  name: 'MCPServerForm',
  components: {
    JsonEditor
  },
  data() {
    return {
      form: {
        name: '',
        host: '',
        port: 8080,
        api_key: '',
        description: '',
        is_active: true,
        config: {}
      },
      rules: {
        name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        host: [
          { required: true, message: '请输入主机地址', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '请输入端口号', trigger: 'blur' },
          { type: 'number', message: '端口必须为数字', trigger: 'blur' }
        ],
        api_key: [
          { required: true, message: '请输入API密钥', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '请输入服务描述', trigger: 'blur' }
        ],
        config: [
          { required: true, message: '请输入配置内容', trigger: 'blur' },
          { 
            validator: (rule, value, callback) => {
              if (!value || Object.keys(value).length === 0) {
                callback(new Error('配置内容不能为空'));
              } else {
                // 验证config是否包含必要的mcpServers字段
                if (!value.mcpServers || Object.keys(value.mcpServers).length === 0) {
                  callback(new Error('配置必须包含至少一个mcpServers服务'));
                } else {
                  // 验证每个服务是否包含必要的字段
                  for (const serverName in value.mcpServers) {
                    const server = value.mcpServers[serverName];
                    if (!server.command) {
                      callback(new Error(`服务 ${serverName} 缺少command字段`));
                      return;
                    }
                    if (!Array.isArray(server.args)) {
                      callback(new Error(`服务 ${serverName} 缺少args数组字段`));
                      return;
                    }
                  }
                  callback();
                }
              }
            },
            trigger: 'blur'
          }
        ]
      },
      submitLoading: false,
      connectionDialogVisible: false
    }
  },
  computed: {
    ...mapGetters({
      loading: 'mcpServers/loading',
      currentServer: 'mcpServers/currentServer',
      connectionStatus: 'mcpServers/connectionStatus'
    }),
    isEdit() {
      return !!this.$route.params.id
    },
    serverId() {
      return this.$route.params.id
    }
  },
  created() {
    if (this.isEdit) {
      this.fetchServerDetails()
    }
  },
  methods: {
    ...mapActions({
      fetchMCPServerById: 'mcpServers/fetchMCPServerById',
      createMCPServer: 'mcpServers/createMCPServer',
      updateMCPServer: 'mcpServers/updateMCPServer',
      testServerConnection: 'mcpServers/testConnection'
    }),
    async fetchServerDetails() {
      try {
        await this.fetchMCPServerById(this.serverId)
        // 填充表单数据
        this.form = {
          name: this.currentServer.name,
          host: this.currentServer.host,
          port: this.currentServer.port,
          api_key: this.currentServer.api_key || '',
          description: this.currentServer.description || '',
          is_active: this.currentServer.is_active
        }
      } catch (error) {
        this.$message.error('获取服务器详情失败')
        console.error(error)
      }
    },
    async submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          this.submitLoading = true
          try {
            if (this.isEdit) {
              await this.updateMCPServer({
                id: this.serverId,
                data: this.form
              })
              this.$message.success('更新成功')
            } else {
              await this.createMCPServer(this.form)
              this.$message.success('创建成功')
              this.resetForm()
            }
            // 成功后返回列表页
            if (this.isEdit) {
              this.goBack()
            }
          } catch (error) {
            const errorMsg = error.response?.data?.detail || '操作失败'
            this.$message.error(this.isEdit ? `更新失败: ${errorMsg}` : `创建失败: ${errorMsg}`)
            console.error(error)
          } finally {
            this.submitLoading = false
          }
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
    },
    goBack() {
      this.$router.push('/mcp-servers')
    },
    async testConnection() {
      if (!this.isEdit) return
      
      try {
        await this.testServerConnection(this.serverId)
        this.connectionDialogVisible = true
      } catch (error) {
        this.$message.error('测试连接失败')
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>
.server-form-container {
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

.form-card {
  margin-bottom: 20px;
}

.el-form {
  max-width: 800px;
  margin: 0 auto;
}

.switch-label {
  margin-left: 10px;
  color: #606266;
}

.connection-success {
  text-align: center;
  color: #67C23A;
}

.connection-error {
  text-align: center;
  color: #F56C6C;
}

.connection-success i,
.connection-error i {
  font-size: 48px;
  margin-bottom: 10px;
}

.connection-details {
  margin-top: 15px;
  text-align: left;
  padding: 10px;
  border-radius: 4px;
  background-color: #f5f7fa;
}
</style> 