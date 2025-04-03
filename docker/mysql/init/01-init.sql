-- 创建开发环境数据库
CREATE DATABASE IF NOT EXISTS mcp_agents_dev CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON mcp_agents_dev.* TO 'mcp_user'@'%';

-- 创建测试环境数据库
CREATE DATABASE IF NOT EXISTS mcp_agents_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON mcp_agents_test.* TO 'mcp_user'@'%';

-- 创建生产环境数据库（在本地开发时可能用不到，但为完整性添加）
CREATE DATABASE IF NOT EXISTS mcp_agents_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON mcp_agents_prod.* TO 'mcp_user'@'%';

-- 刷新权限
FLUSH PRIVILEGES; 