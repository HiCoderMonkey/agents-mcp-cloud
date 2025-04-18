<template>
  <div class="mcp-server-page">
    <h1>{{ isEdit ? '编辑MCP服务' : '创建MCP服务' }}</h1>
    <mcp-server-form 
      :initialData="mcpData"
      @submit="handleSubmit"
    />
  </div>
</template>

<script>
import MCPServerForm from '@/components/MCPServerForm'
import { createMCPServer, updateMCPServer, getMCPServerById } from '@/api/mcp-servers'

export default {
  name: 'MCPServerCreateEdit',
  components: {
    MCPServerForm
  },
  data() {
    return {
      mcpData: {
        name: '',
        description: '',
        config: {}
      },
      isEdit: false
    }
  },
  created() {
    const id = this.$route.params.id;
    this.isEdit = !!id;
    
    if (this.isEdit) {
      this.fetchMCPServer(id);
    }
  },
  methods: {
    async fetchMCPServer(id) {
      try {
        const response = await getMCPServerById(id);
        this.mcpData = response.data;
      } catch (error) {
        this.$message.error('获取MCP服务信息失败');
        console.error(error);
      }
    },
    async handleSubmit(formData) {
      try {
        if (this.isEdit) {
          await updateMCPServer(this.$route.params.id, formData);
          this.$message.success('更新MCP服务成功');
        } else {
          await createMCPServer(formData);
          this.$message.success('创建MCP服务成功');
        }
        this.$router.push('/mcp-servers');
      } catch (error) {
        this.$message.error(this.isEdit ? '更新MCP服务失败' : '创建MCP服务失败');
        console.error(error);
      }
    }
  }
}
</script>

<style scoped>
.mcp-server-page {
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}
</style> 