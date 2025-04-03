<template>
  <div class="sdk-keys-container">
    <div class="page-header">
      <h2>SDK密钥管理</h2>
      <el-button type="primary" @click="openCreateDialog">创建密钥</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="sdkKeys"
      border
      style="width: 100%">
      <el-table-column
        prop="id"
        label="ID"
        width="80">
      </el-table-column>
      <el-table-column
        prop="name"
        label="名称"
        min-width="120">
      </el-table-column>
      <el-table-column
        prop="agent_name"
        label="关联代理"
        min-width="120">
      </el-table-column>
      <el-table-column
        prop="key"
        label="密钥"
        min-width="180">
        <template slot-scope="scope">
          <div class="key-display">
            <span>{{ maskKey(scope.row.key) }}</span>
            <el-button type="text" icon="el-icon-view" @click="toggleKeyVisibility(scope.row)"></el-button>
            <el-button type="text" icon="el-icon-document-copy" @click="copyKey(scope.row.key)"></el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="created_at"
        label="创建时间"
        width="180">
        <template slot-scope="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column
        prop="is_active"
        label="状态"
        width="100">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            @change="updateKeyStatus(scope.row)">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="120">
        <template slot-scope="scope">
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建密钥对话框 -->
    <el-dialog title="创建SDK密钥" :visible.sync="dialogVisible">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="为此密钥添加名称，例如: 测试密钥"></el-input>
        </el-form-item>
        <el-form-item label="关联代理" prop="agent_id">
          <el-select v-model="form.agent_id" placeholder="选择关联的代理" style="width: 100%">
            <el-option
              v-for="agent in agents"
              :key="agent.id"
              :label="agent.name"
              :value="agent.id">
            </el-option>
          </el-select>
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
  name: 'SDKKeys',
  data() {
    return {
      dialogVisible: false,
      newKeyDialogVisible: false,
      form: {
        name: '',
        agent_id: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入密钥名称', trigger: 'blur' }
        ],
        agent_id: [
          { required: true, message: '请选择关联的代理', trigger: 'change' }
        ]
      },
      submitLoading: false,
      visibleKeys: new Set() // 跟踪哪些key应该显示完整内容
    }
  },
  computed: {
    ...mapGetters({
      sdkKeys: 'sdkKeys/sdkKeyList',
      loading: 'sdkKeys/loading',
      totalKeys: 'sdkKeys/totalKeys',
      newKey: 'sdkKeys/newKey',
      agents: 'agents/agentList'
    })
  },
  created() {
    this.fetchKeys()
    this.fetchAgents()
  },
  methods: {
    ...mapActions({
      fetchAllSDKKeys: 'sdkKeys/fetchAllSDKKeys',
      createSDKKey: 'sdkKeys/createSDKKey',
      deleteSDKKey: 'sdkKeys/deleteSDKKey',
      updateSDKKeyStatus: 'sdkKeys/updateSDKKeyStatus',
      clearNewKey: 'sdkKeys/clearNewKey',
      fetchAgents: 'agents/fetchAgents'
    }),
    async fetchKeys() {
      try {
        await this.fetchAllSDKKeys()
      } catch (error) {
        this.$message.error('获取SDK密钥列表失败')
        console.error(error)
      }
    },
    openCreateDialog() {
      this.form = {
        name: '',
        agent_id: ''
      }
      this.dialogVisible = true
    },
    async createKey() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          this.submitLoading = true
          try {
            await this.createSDKKey(this.form)
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
          await this.deleteSDKKey(row.id)
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
          id: key.id,
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
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString()
    }
  }
}
</script>

<style scoped>
.sdk-keys-container {
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
</style> 