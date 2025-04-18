<template>
  <div class="chat-container">
    <!-- 聊天消息列表 -->
    <div class="chat-messages" ref="messageList">
      <div v-for="(message, index) in messages" 
           :key="index" 
           :class="['message', message.role]">
        <div class="message-content">
          <div class="message-header">
            <span class="role">{{ message.role === 'user' ? '用户' : 'AI' }}</span>
            <span class="time">{{ formatTime(message.created_at) }}</span>
          </div>
          <div class="message-text">{{ message.content }}</div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input">
      <el-input
        v-model="inputMessage"
        type="textarea"
        :rows="3"
        placeholder="请输入消息..."
        @keyup.enter.native.exact="sendMessage"
      >
      </el-input>
      <el-button 
        type="primary" 
        :loading="sending" 
        @click="sendMessage">
        发送
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentChat',
  props: {
    agentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      messages: [],
      inputMessage: '',
      sending: false
    }
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim() || this.sending) return

      const message = this.inputMessage.trim()
      this.inputMessage = ''
      this.sending = true

      // 添加用户消息到列表
      this.messages.push({
        role: 'user',
        content: message,
        created_at: new Date()
      })

      try {
        // 调用发送消息的 API
        const response = await this.$store.dispatch('agents/sendMessage', {
          agentId: this.agentId,
          message: message
        })

        // 添加 AI 回复到列表
        this.messages.push({
          role: 'assistant',
          content: response.content,
          created_at: new Date()
        })

        // 滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      } catch (error) {
        this.$message.error('发送消息失败：' + error.message)
      } finally {
        this.sending = false
      }
    },
    scrollToBottom() {
      const messageList = this.$refs.messageList
      messageList.scrollTop = messageList.scrollHeight
    },
    formatTime(date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleTimeString()
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  min-height: 300px;
  max-height: 500px;
}

.message {
  margin-bottom: 20px;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 8px;
  word-break: break-word;
}

.message.user .message-content {
  margin-left: auto;
  background-color: #409eff;
  color: white;
}

.message.assistant .message-content {
  margin-right: auto;
  background-color: white;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  font-size: 12px;
}

.message.user .message-header {
  color: #e8f3ff;
}

.message.assistant .message-header {
  color: #909399;
}

.chat-input {
  padding: 20px;
  background-color: white;
  border-top: 1px solid #ebeef5;
  display: flex;
  gap: 10px;
}

.chat-input .el-textarea {
  flex: 1;
}

.chat-input .el-button {
  align-self: flex-end;
}
</style> 