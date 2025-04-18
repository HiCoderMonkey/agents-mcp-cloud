<template>
  <div class="json-editor">
    <el-input
      type="textarea"
      v-model="jsonContent"
      :rows="15"
      @input="onInput"
      placeholder="请输入JSON格式的配置内容"
      style="width: 100%;"
    ></el-input>
    <div class="editor-actions">
      <el-button size="mini" type="text" @click="formatJSON">格式化</el-button>
      <el-button size="mini" type="text" @click="insertSampleJSON">插入示例</el-button>
      <span v-if="error" class="error-message">{{ error }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'JsonEditor',
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
    height: {
      type: String,
      default: '300px'
    }
  },
  data() {
    return {
      jsonContent: '{}',
      error: null
    }
  },
  watch: {
    value: {
      deep: true,
      handler(val) {
        // 只有当外部传入值变化且与当前内容不同时才更新，避免循环
        try {
          const currentValue = this.jsonContent ? JSON.parse(this.jsonContent) : {};
          if (JSON.stringify(val) !== JSON.stringify(currentValue)) {
            this.jsonContent = JSON.stringify(val, null, 2);
          }
        } catch (e) {
          // 如果当前内容不是有效的JSON，直接更新
          this.jsonContent = JSON.stringify(val || {}, null, 2);
        }
      },
      immediate: true
    }
  },
  methods: {
    onInput(value) {
      try {
        if (value.trim()) {
          const parsed = JSON.parse(value);
          this.$emit('input', parsed);
          this.error = null;
        } else {
          this.$emit('input', {});
          this.error = null;
        }
      } catch (e) {
        this.error = '无效的JSON格式';
        // 不更新父组件值，等待用户修复
      }
    },
    formatJSON() {
      try {
        if (this.jsonContent.trim()) {
          const obj = JSON.parse(this.jsonContent);
          this.jsonContent = JSON.stringify(obj, null, 2);
          this.error = null;
        }
      } catch (e) {
        this.error = '无效的JSON格式，无法格式化';
      }
    },
    insertSampleJSON() {
      this.jsonContent = JSON.stringify({
        mcpServers: {
          weather: {
              command: "uv",
              args: [
                  "--directory",
                  "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
                  "run",
                  "weather.py"
              ]
          }
        }
      }, null, 2);
      this.onInput(this.jsonContent);
    }
  }
}
</script>

<style scoped>
.json-editor {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 1px;
}
.editor-actions {
  padding: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9f9f9;
}
.error-message {
  color: #f56c6c;
  font-size: 12px;
  margin-left: auto;
}
</style> 