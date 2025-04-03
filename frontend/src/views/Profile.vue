<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <div slot="header">
        <span>个人资料</span>
      </div>
      <el-form :model="profile" :rules="rules" ref="profileForm" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="profile.username"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profile.email"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="updateProfile" :loading="loading">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="password-card">
      <div slot="header">
        <span>修改密码</span>
      </div>
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordForm" label-width="120px">
        <el-form-item label="当前密码" prop="oldPassword">
          <el-input v-model="passwordForm.oldPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input v-model="passwordForm.newPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirmPassword">
          <el-input v-model="passwordForm.confirmPassword" type="password"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="changePassword" :loading="pwdLoading">修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'Profile',
  data() {
    // 确认密码验证
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.passwordForm.newPassword) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      loading: false,
      pwdLoading: false,
      profile: {
        username: '',
        email: ''
      },
      passwordForm: {
        oldPassword: '',
        newPassword: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
        ]
      },
      passwordRules: {
        oldPassword: [
          { required: true, message: '请输入当前密码', trigger: 'blur' }
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能小于6个字符', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, validator: validatePass, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    ...mapGetters(['currentUser'])
  },
  created() {
    this.loadUserProfile()
  },
  methods: {
    loadUserProfile() {
      if (this.currentUser) {
        this.profile.username = this.currentUser.username
        this.profile.email = this.currentUser.email
      }
    },
    async updateProfile() {
      this.$refs.profileForm.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            // 此处调用API更新用户信息
            // await this.$store.dispatch('updateProfile', this.profile)
            this.$message.success('个人资料已更新')
          } catch (error) {
            this.$message.error(error.message || '更新个人资料失败')
          } finally {
            this.loading = false
          }
        }
      })
    },
    async changePassword() {
      this.$refs.passwordForm.validate(async (valid) => {
        if (valid) {
          this.pwdLoading = true
          try {
            // 此处调用API修改密码
            // await this.$store.dispatch('changePassword', this.passwordForm)
            this.$message.success('密码已更新')
            this.passwordForm = {
              oldPassword: '',
              newPassword: '',
              confirmPassword: ''
            }
          } catch (error) {
            this.$message.error(error.message || '修改密码失败')
          } finally {
            this.pwdLoading = false
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-card, .password-card {
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 0 15px;
  }
}
</style> 