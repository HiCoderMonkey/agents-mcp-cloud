<template>
  <div class="mcp-servers-container">
    <div class="page-header">
      <h2>MCP服务管理</h2>
      <el-button type="primary" @click="goToCreate">添加MCP服务</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="servers"
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
        min-width="150">
      </el-table-column>
      <el-table-column
        prop="description"
        label="描述"
        min-width="200"
        show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        label="配置内容"
        min-width="180">
        <template slot-scope="scope">
          <el-popover
            placement="top"
            width="400"
            trigger="hover">
            <pre>{{ formatJSON(scope.row.config) }}</pre>
            <el-button slot="reference" size="mini" type="text">查看配置</el-button>
          </el-popover>
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
        label="操作"
        width="180">
        <template slot-scope="scope">
          <el-button
            size="mini"
            @click="goToDetail(scope.row)">查看</el-button>
          <el-button
            size="mini"
            type="primary"
            @click="goToEdit(scope.row)">编辑</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="totalServers > 0"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-sizes="[10, 20, 50, 100]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="totalServers"
      class="pagination">
    </el-pagination>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'MCPServers',
  data() {
    return {
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    ...mapGetters({
      servers: 'mcpServers/serverList',
      loading: 'mcpServers/loading',
      totalServers: 'mcpServers/totalServers'
    })
  },
  created() {
    this.fetchServers()
    console.log('Component created, servers state:', this.$store.state.mcpServers.servers)
  },
  methods: {
    ...mapActions({
      fetchMCPServerList: 'mcpServers/fetchMCPServerList',
      deleteMCPServer: 'mcpServers/deleteMCPServer'
    }),
    async fetchServers() {
      try {
        await this.fetchMCPServerList({
          page: this.currentPage,
          size: this.pageSize
        })
        console.log('Servers after fetch:', this.servers)
        console.log('Total servers:', this.totalServers)
      } catch (error) {
        this.$message.error('获取MCP服务列表失败')
        console.error(error)
      }
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.fetchServers()
    },
    handleCurrentChange(page) {
      this.currentPage = page
      this.fetchServers()
    },
    goToCreate() {
      this.$router.push('/mcp-servers/create')
    },
    goToDetail(row) {
      this.$router.push(`/mcp-servers/${row.id}`)
    },
    goToEdit(row) {
      this.$router.push(`/mcp-servers/${row.id}/edit`)
    },
    async handleDelete(row) {
      this.$confirm('确定要删除该MCP服务吗？删除后将无法恢复。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await this.deleteMCPServer(row.id)
          this.$message.success('删除成功')
        } catch (error) {
          this.$message.error('删除失败')
          console.error(error)
        }
      }).catch(() => {})
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return date.toLocaleString()
    },
    formatJSON(json) {
      return JSON.stringify(json, null, 2)
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

.pagination {
  margin-top: 20px;
  text-align: right;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 300px;
  overflow: auto;
}
</style> 