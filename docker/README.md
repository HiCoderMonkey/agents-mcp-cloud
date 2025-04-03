# Docker依赖组件

本目录包含了MCP Agents Cloud项目所需的Docker依赖组件，目前支持：

- MySQL 8.0数据库

## 前置条件

在使用这些依赖组件前，请确保已安装：

1. [Docker](https://docs.docker.com/get-docker/) (20.10.0+)
2. [Docker Compose](https://docs.docker.com/compose/install/) (2.0.0+)

## MySQL数据库安装与配置

### 快速开始

1. 启动MySQL服务：

```bash
# 进入docker目录
cd docker

# 启动MySQL服务
docker-compose up -d mysql
```

2. 检查MySQL服务状态：

```bash
docker-compose ps
```

服务正常启动后，输出中的`Status`应显示为`Up`状态。

### 连接数据库

MySQL服务将在本地63307端口启动，您可以使用以下信息连接：

- 主机: localhost 或 127.0.0.1
- 端口: 63307
- 默认数据库: mcp_agents (还有 mcp_agents_dev, mcp_agents_test, mcp_agents_prod)
- 用户名: mcp_user
- 密码: mcp_password

也可以使用root用户连接（仅用于管理目的）：
- 用户名: root
- 密码: password

### 配置应用使用数据库

在 `config-*.yml` 文件中配置数据库连接：

```yaml
database:
  url: "mysql+pymysql://mcp_user:mcp_password@localhost:63307/mcp_agents_dev"
  # 其他数据库配置...
```

不同环境使用不同的数据库：
- 开发环境: mcp_agents_dev
- 测试环境: mcp_agents_test
- 生产环境: mcp_agents_prod

### 数据持久化

MySQL数据将持久化存储在主机路径 `/appdata/share/agents-mcp-cloud/mysql/data` 中。请确保该目录存在且具有适当的权限。

> 注意：请确保 `/appdata/share/agents-mcp-cloud/mysql/data` 目录存在，并且运行Docker的用户有写入权限。

如需完全重置数据库，可以备份并删除该目录中的内容：

```bash
# 停止服务
docker-compose down

# 清空数据目录
sudo rm -rf /appdata/share/agents-mcp-cloud/mysql/data/*

# 重新启动服务
docker-compose up -d mysql
```

### 自定义配置

- MySQL配置文件位于 `mysql/conf/my.cnf`
- 初始化脚本位于 `mysql/init/01-init.sql`

如果修改这些文件，需要重启或重建MySQL容器才能生效：

```bash
# 重新创建并启动MySQL容器
docker-compose up -d --force-recreate mysql
```

## 停止服务

```bash
# 停止MySQL服务
docker-compose stop mysql

# 停止所有服务并移除容器
docker-compose down
```

## 常见问题

### 端口冲突

如果63307端口已被占用，可以编辑`docker-compose.yml`修改端口映射：

```yaml
ports:
  - "33306:3306"  # 将本地33306端口映射到容器的3306端口
```

然后更新配置文件中的数据库连接URL。

### 连接问题

如果无法连接到MySQL，请检查：

1. MySQL容器是否正常运行：`docker-compose ps`
2. 查看MySQL日志：`docker-compose logs mysql`
3. 确认本地防火墙是否阻止了63307端口
4. 检查网络模式是否合适：当前使用"bridge"模式

### 数据目录权限问题

如果容器无法启动或出现权限错误，请检查数据目录：

```bash
# 查看目录权限
ls -la /appdata/share/agents-mcp-cloud/mysql/data

# 修改目录权限
sudo chown -R 999:999 /appdata/share/agents-mcp-cloud/mysql/data
```

> 提示: 999:999 是MySQL容器内部的mysql用户ID。

### 性能优化

默认配置适用于开发环境。如果在生产环境使用，建议根据服务器硬件情况调整`my.cnf`中的参数，特别是内存相关的配置如`innodb_buffer_pool_size`。 