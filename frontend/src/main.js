import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

Vue.config.productionTip = false

// 使用ElementUI
Vue.use(ElementUI)

// 配置axios
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1'
// 添加请求拦截器，在请求头添加token
axios.interceptors.request.use(
  config => {
    const token = store.state.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 添加axios到Vue原型，方便组件内使用
Vue.prototype.$axios = axios

// 创建Vue实例
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
