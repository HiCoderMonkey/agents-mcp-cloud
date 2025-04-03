<template>
  <div class="reset-container">
    <div class="reset-box">
      <h2>重置密码</h2>
      <el-form :model="resetForm" :rules="rules" ref="resetForm" label-width="100px">
        <el-form-item label="邮箱" prop="email" v-if="step === 1">
          <el-input v-model="resetForm.email" placeholder="请输入注册邮箱"></el-input>
        </el-form-item>
        <el-form-item v-if="step === 1">
          <el-button type="primary" @click="requestReset" :loading="loading">发送重置链接</el-button>
          <router-link to="/login">
            <el-button>返回登录</el-button>
          </router-link>
        </el-form-item>

        <div v-if="step === 2">
          <el-form-item label="重置令牌" prop="token">
            <el-input v-model="resetForm.token" placeholder="请输入收到的重置令牌"></el-input>
          </el-form-item>
          <el-form-item label="新密码" prop="password">
            <el-input v-model="resetForm.password" type="password" placeholder="请输入新密码"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input v-model="resetForm.confirmPassword" type="password" placeholder="请再次输入新密码"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitReset" :loading="loading">重置密码</el-button>
            <el-button @click="step = 1">返回</el-button>
          </el-form-item>
        </div>

        <div v-if="step === 3" class="success-message">
          <i class="el-icon-success"></i>
          <p>密码重置成功！</p>
          <router-link to="/login">
            <el-button type="primary">返回登录</el-button>
          </router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  data() {
    // 密码验证
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.resetForm.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    return {
      step: 1, // 1: 输入邮箱, 2: 重置密码, 3: 成功
      loading: false,
      resetForm: {
        email: '',
        token: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ],
        token: [
          { required: true, message: '请输入重置令牌', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, validator: validatePass2, trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    async requestReset() {
      this.$refs.resetForm.validateField('email', async (error) => {
        if (!error) {
          this.loading = true
          try {
            // 在这里调用API，发送重置密码请求
            // await this.$store.dispatch('requestPasswordReset', this.resetForm.email)
            this.$message.success('重置链接已发送到您的邮箱，请检查')
            this.step = 2
          } catch (error) {
            this.$message.error(error.message || '发送重置链接失败，请稍后重试')
          } finally {
            this.loading = false
          }
        }
      })
    },
    async submitReset() {
      this.$refs.resetForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            // 在这里调用API，提交重置密码
            // await this.$store.dispatch('resetPassword', {
            //   token: this.resetForm.token,
            //   password: this.resetForm.password
            // })
            this.$message.success('密码重置成功')
            this.step = 3
          } catch (error) {
            this.$message.error(error.message || '重置密码失败，请稍后重试')
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.reset-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.reset-box {
  width: 450px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #303133;
}

.success-message {
  text-align: center;
  padding: 20px 0;
}

.success-message i {
  font-size: 64px;
  color: #67c23a;
}

.success-message p {
  margin: 20px 0;
  font-size: 18px;
}
</style> 