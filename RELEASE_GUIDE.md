# AKShare API 发布指南

本指南将帮助您将 AKShare API 包发布到 PyPI（Python Package Index）。

## 📋 发布前准备

### 1. 检查包结构

确保您的包结构如下：

```
akshare_api_package/
├── akshare_api/
│   ├── __init__.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_akshare_api.py
├── examples/
│   ├── basic_usage.py
│   ├── market_analysis.py
│   └── data_visualization.py
├── docs/
│   └── README.md
├── README.md
├── LICENSE
├── requirements.txt
├── pyproject.toml
├── setup.py
└── MANIFEST.in
```

### 2. 更新版本号

在 `pyproject.toml` 和 `setup.py` 中更新版本号：

```toml
# pyproject.toml
version = "1.0.0"
```

```python
# setup.py
version="1.0.0"
```

### 3. 更新文档

确保 `README.md` 中的信息是最新的，包括：
- 功能描述
- 安装说明
- 使用示例
- 更新日志

## 🚀 发布步骤

### 1. 安装构建工具

```bash
pip install build twine
```

### 2. 构建包

```bash
cd akshare_api_package
python -m build
```

这将创建 `dist/` 目录，包含：
- `akshare_api-1.0.0-py3-none-any.whl` (wheel包)
- `akshare_api-1.0.0.tar.gz` (源码包)

### 3. 检查包

```bash
twine check dist/*
```

### 4. 上传到测试PyPI

首先上传到测试PyPI进行验证：

```bash
twine upload --repository testpypi dist/*
```

您需要：
1. 在 https://test.pypi.org/account/register/ 注册账户
2. 创建API token
3. 配置认证信息

### 5. 测试安装

```bash
pip install --index-url https://test.pypi.org/simple/ akshare-api
```

### 6. 上传到正式PyPI

测试无误后，上传到正式PyPI：

```bash
twine upload dist/*
```

您需要：
1. 在 https://pypi.org/account/register/ 注册账户
2. 创建API token
3. 配置认证信息

## 🔧 配置认证

### 方法1：使用配置文件

创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers = pypi testpypi

[pypi]
username = __token__
password = pypi-your-api-token-here

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-your-test-api-token-here
```

### 方法2：使用环境变量

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-api-token-here
```

### 方法3：命令行参数

```bash
twine upload --username __token__ --password pypi-your-api-token-here dist/*
```

## 📝 发布检查清单

- [ ] 包结构正确
- [ ] 版本号已更新
- [ ] README.md 内容完整
- [ ] LICENSE 文件存在
- [ ] 所有测试通过
- [ ] 代码格式化完成
- [ ] 类型检查通过
- [ ] 文档更新完成
- [ ] 包构建成功
- [ ] 包检查通过
- [ ] 测试PyPI上传成功
- [ ] 测试安装成功
- [ ] 正式PyPI上传成功

## 🔄 版本管理

### 语义化版本

遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范：

- **主版本号**：不兼容的API修改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

### 版本更新示例

```bash
# 1.0.0 -> 1.0.1 (bug修复)
# 1.0.1 -> 1.1.0 (新功能)
# 1.1.0 -> 2.0.0 (破坏性更改)
```

## 🐛 常见问题

### 1. 包名冲突

如果包名已存在，需要：
- 更改包名
- 或者联系现有包的所有者

### 2. 认证失败

检查：
- API token是否正确
- 用户名是否为 `__token__`
- 密码是否为完整的API token

### 3. 构建失败

检查：
- `pyproject.toml` 语法是否正确
- 依赖是否正确安装
- Python版本是否兼容

### 4. 上传失败

检查：
- 网络连接
- PyPI服务状态
- 包大小是否超限

## 📚 相关资源

- [PyPI 官方文档](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine 文档](https://twine.readthedocs.io/)
- [Python 打包用户指南](https://packaging.python.org/guides/)
- [语义化版本规范](https://semver.org/)

## 🎉 发布后

发布成功后：

1. 在GitHub上创建Release
2. 更新项目文档
3. 通知用户更新
4. 监控包下载情况
5. 收集用户反馈

## 📞 支持

如果在发布过程中遇到问题，请：

1. 查看本文档的常见问题部分
2. 搜索相关错误信息
3. 在项目Issues中提问
4. 联系维护者

---

**注意**: 发布到PyPI是公开的，请确保您的代码质量和文档完整性。
