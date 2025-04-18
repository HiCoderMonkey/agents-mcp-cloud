<template>
  <div class="mcp-form-container">
    <el-form ref="mcpForm" :model="formData" :rules="rules" label-width="120px">
      <!-- MCP服务名称 -->
      <el-form-item label="服务名称" prop="name">
        <el-input v-model="formData.name" placeholder="请输入MCP服务名称"></el-input>
      </el-form-item>
      
      <!-- MCP服务描述 -->
      <el-form-item label="服务描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="3"
          placeholder="请输入MCP服务描述(可选)"
        ></el-input>
      </el-form-item>
      
      <!-- MCP配置内容 -->
      <el-form-item label="配置内容" prop="config">
        <json-editor v-model="formData.config" height="400px"></json-editor>
        <div class="form-tips">请输入JSON格式的配置内容</div>
      </el-form-item>
      
      <!-- 表单按钮 -->
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import JsonEditor from '@/components/JsonEditor'

export default {
  name: 'MCPServerForm',
  components: {
    JsonEditor
  },
  props: {
    initialData: {
      type: Object,
      default: () => ({
        name: '',
        description: '',
        config: {}
      })
    }
  },
  data() {
    return {
      formData: {
        name: '',
        description: '',
        config: {}
      },
      rules: {
        name: [
          { required: true, message: '请输入MCP服务名称', trigger: 'blur' },
          { min: 1, max: 100, message: '长度在1到100个字符之间', trigger: 'blur' }
        ],
        config: [
          { 
            required: true, 
            validator: (rule, value, callback) => {
              if (Object.keys(value).length === 0) {
                callback(new Error('配置内容不能为空'));
              } else {
                callback();
              }
            }, 
            trigger: 'blur' 
          }
        ]
      }
    }
  },
  created() {
    if (this.initialData) {
      this.formData = JSON.parse(JSON.stringify(this.initialData));
    }
  },
  methods: {
    submitForm() {
      this.$refs.mcpForm.validate(valid => {
        if (valid) {
          this.$emit('submit', this.formData);
        } else {
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.mcpForm.resetFields();
    }
  }
}
</script>

<style scoped>
.mcp-form-container {
  padding: 20px;
}
.form-tips {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style> 