<template>
  <div class="login-container">
    <el-card class="login-card">
      <div slot="header">
        <h2>登录到MCP Agents Cloud</h2>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginForm" label-width="0px">
        <el-form-item prop="email">
          <el-input v-model="loginForm.email" prefix-icon="el-icon-user" placeholder="电子邮箱"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" placeholder="密码" show-password></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading" style="width: 100%">登录</el-button>
        </el-form-item>
        <div class="form-footer">
          <router-link to="/register">没有账户？注册</router-link>
          <router-link to="/reset-password">忘记密码？</router-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      loginForm: {
        email: '',
        password: ''
      },
      loading: false,
      rules: {
        email: [
          { required: true, message: '请输入电子邮箱', trigger: 'blur' },
          { type: 'email', message: '请输入有效的电子邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          // 构建表单数据，适配后端API格式
          const formData = new FormData()
          formData.append('username', this.loginForm.email)
          formData.append('password', this.loginForm.password)
          
          this.$store.dispatch('login', formData)
            .then(() => {
              this.$message.success('登录成功')
              // 如果有重定向参数，则跳转到该路径
              const redirectPath = this.$route.query.redirect || '/'
              this.$router.push(redirectPath)
            })
            .catch(error => {
              console.error(error)
              this.$message.error('登录失败：' + (error.response?.data?.detail || '未知错误'))
            })
            .finally(() => {
              this.loading = false
            })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}
.login-card {
  width: 400px;
  max-width: 100%;
}
.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}
</style> 