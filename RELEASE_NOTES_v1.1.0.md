# AKShare API v1.1.0 发布说明

## 🎉 重大更新：自动服务管理功能

### ✨ 新增功能

#### 🔧 自动服务管理
- **自动安装AKTools**: 首次使用时自动检测并安装最新版AKTools
- **自动启动服务**: 无需手动启动AKTools服务，API调用时自动启动
- **智能重连机制**: 连接失败时自动重启服务并重试请求
- **服务状态监控**: 实时监控服务运行状态和响应时间

#### 🛠️ 服务管理API
- `api.get_service_status()` - 获取服务状态
- `api.start_service()` - 启动服务
- `api.restart_service()` - 重启服务
- `api.stop_service()` - 停止服务

#### 🖥️ 增强的命令行工具
- `akshare-api --start-service` - 启动AKTools服务
- `akshare-api --stop-service` - 停止AKTools服务
- `akshare-api --restart-service` - 重启AKTools服务
- `akshare-api --service-status` - 查看服务状态

### 🚀 使用方式

#### 基础使用（推荐）
```python
from akshare_api import stock_zh_a_spot_em

# 自动启动AKTools服务，无需手动配置
data = stock_zh_a_spot_em()
print(f"获取到 {len(data)} 条数据")
```

#### 面向对象使用
```python
from akshare_api import AKShareAPI

# 创建API客户端（自动启动服务）
api = AKShareAPI()

# 获取数据
data = api.stock_zh_a_spot_em()

# 查看服务状态
status = api.get_service_status()
print(f"服务状态: {status}")
```

#### 手动服务管理
```python
from akshare_api import AKShareAPI

# 禁用自动服务管理
api = AKShareAPI(auto_start_service=False)

# 手动管理服务
api.start_service()
api.restart_service()
api.stop_service()
```

### 🔄 向后兼容

- 所有原有API接口保持不变
- 函数式调用方式完全兼容
- 默认启用自动服务管理，可通过参数禁用

### 📦 依赖更新

- 新增 `aktools>=1.0.0` 依赖
- 自动处理AKTools的安装和更新

### 🐛 修复

- 修复了连接失败时的错误处理
- 改进了服务启动的稳定性
- 优化了错误提示信息

### 📚 文档更新

- 更新了README.md，添加自动服务管理说明
- 新增自动服务管理示例文件
- 更新了安装和使用指南

### 🧪 测试

- 新增自动服务管理功能测试
- 完善了错误处理测试
- 添加了性能测试

## 🎯 升级建议

### 从 v1.0.0 升级

1. **安装新版本**:
   ```bash
   pip install akshare-api --upgrade
   ```

2. **无需修改代码**: 现有代码完全兼容

3. **享受新功能**: 自动服务管理功能自动生效

### 首次使用

1. **安装包**:
   ```bash
   pip install akshare-api
   ```

2. **直接使用**: 无需手动安装AKTools或启动服务
   ```python
   from akshare_api import stock_zh_a_spot_em
   data = stock_zh_a_spot_em()  # 自动启动服务
   ```

## 🔮 未来计划

- 支持多端口服务管理
- 添加服务健康检查
- 支持服务配置持久化
- 添加更多监控指标

## 🙏 致谢

感谢所有用户的反馈和建议，特别是关于简化AKTools服务管理的需求。

---

**注意**: 此版本向后兼容，现有用户可以直接升级使用。
