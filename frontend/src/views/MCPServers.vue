<template>
  <div class="mcp-servers-container">
    <div class="page-header">
      <h2>MCP服务器管理</h2>
      <el-button type="primary" @click="dialogVisible = true">添加服务器</el-button>
    </div>

    <!-- 服务器列表 -->
    <el-table
      v-loading="loading"
      :data="servers"
      border
      style="width: 100%">
      <el-table-column
        prop="name"
        label="名称"
        width="180">
      </el-table-column>
      <el-table-column
        prop="address"
        label="地址"
        width="180">
      </el-table-column>
      <el-table-column
        prop="port"
        label="端口">
      </el-table-column>
      <el-table-column
        prop="status"
        label="状态">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status === 'online' ? 'success' : (scope.row.status === 'offline' ? 'danger' : 'warning')">
            {{ statusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="is_active"
        label="激活状态">
        <template slot-scope="scope">
          <el-switch
            v-model="scope.row.is_active"
            @change="updateServerStatus(scope.row)">
          </el-switch>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="200">
        <template slot-scope="scope">
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

    <!-- 添加/编辑服务器对话框 -->
    <el-dialog :title="isEdit ? '编辑服务器' : '添加服务器'" :visible.sync="dialogVisible">
      <el-form :model="serverForm" :rules="rules" ref="serverForm" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="serverForm.name"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="serverForm.address"></el-input>
        </el-form-item>
        <el-form-item label="端口" prop="port">
          <el-input v-model.number="serverForm.port" type="number"></el-input>
        </el-form-item>
        <el-form-item label="API密钥" prop="api_key">
          <el-input v-model="serverForm.api_key"></el-input>
        </el-form-item>
        <el-form-item label="激活状态" prop="is_active">
          <el-switch v-model="serverForm.is_active"></el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveServer" :loading="saveLoading">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MCPServers',
  data() {
    return {
      loading: false,
      saveLoading: false,
      dialogVisible: false,
      isEdit: false,
      servers: [],
      serverForm: this.getEmptyServerForm(),
      rules: {
        name: [
          { required: true, message: '请输入服务器名称', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入服务器地址', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '请输入端口号', trigger: 'blur' },
          { type: 'number', message: '端口必须为数字', trigger: 'blur' }
        ],
        api_key: [
          { required: true, message: '请输入API密钥', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchServers()
  },
  methods: {
    getEmptyServerForm() {
      return {
        name: '',
        address: '',
        port: 8080,
        api_key: '',
        is_active: true
      }
    },
    statusText(status) {
      const statusMap = {
        'online': '在线',
        'offline': '离线',
        'error': '错误'
      }
      return statusMap[status] || status
    },
    async fetchServers() {
      this.loading = true
      try {
        // 这里应该调用API获取服务器列表
        // const response = await this.$store.dispatch('fetchServers')
        // this.servers = response.data

        // 模拟数据
        this.servers = [
          { id: 1, name: '测试服务器1', address: '192.168.1.100', port: 8080, api_key: '******', status: 'online', is_active: true },
          { id: 2, name: '测试服务器2', address: '192.168.1.101', port: 8080, api_key: '******', status: 'offline', is_active: false }
        ]
      } catch (error) {
        this.$message.error('获取服务器列表失败')
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    handleEdit(row) {
      this.isEdit = true
      this.serverForm = { ...row }
      this.dialogVisible = true
    },
    async handleDelete(row) {
      this.$confirm('确认删除该服务器?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          // 调用API删除服务器
          // await this.$store.dispatch('deleteServer', row.id)
          this.$message.success('删除成功')
          this.fetchServers()
        } catch (error) {
          this.$message.error('删除失败')
        }
      }).catch(() => {})
    },
    async saveServer() {
      this.$refs.serverForm.validate(async (valid) => {
        if (valid) {
          this.saveLoading = true
          try {
            if (this.isEdit) {
              // 更新服务器
              // await this.$store.dispatch('updateServer', this.serverForm)
              this.$message.success('更新成功')
            } else {
              // 创建服务器
              // await this.$store.dispatch('createServer', this.serverForm)
              this.$message.success('创建成功')
            }
            this.dialogVisible = false
            this.fetchServers()
          } catch (error) {
            this.$message.error(this.isEdit ? '更新失败' : '创建失败')
          } finally {
            this.saveLoading = false
          }
        }
      })
    },
    async updateServerStatus(row) {
      try {
        // 更新服务器状态
        // await this.$store.dispatch('updateServerStatus', { id: row.id, is_active: row.is_active })
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
.mcp-servers-container {
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