# AKShare API 安装和使用说明

## 📦 安装方法

### 方法1：从PyPI安装（推荐）

```bash
pip install akshare-api
```

### 方法2：从源码安装

```bash
# 克隆仓库
git clone https://github.com/JoshuaMaoJH/akshare-api.git
cd akshare-api

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

### 方法3：直接使用源码

```bash
# 下载源码文件
# 将 akshare_api 目录复制到您的项目中
# 直接导入使用
```

## 🚀 快速开始

### 1. 基础使用

```python
from akshare_api import stock_zh_a_spot_em

# 获取A股实时行情
data = stock_zh_a_spot_em()
print(data.head())
```

### 2. 面向对象使用

```python
from akshare_api import AKShareAPI

# 创建API客户端
api = AKShareAPI(base_url="http://127.0.0.1:8080")

# 获取数据
data = api.stock_zh_a_spot_em()
print(data.head())
```

### 3. 命令行使用

```bash
# 测试API连接
akshare-api --test-connection

# 列出所有接口
akshare-api --list-interfaces

# 指定API基础URL
akshare-api --base-url http://localhost:8080 --test-connection
```

## 🔧 配置

### 环境要求

- Python 3.7 及以上版本
- AKTools服务已启动（默认端口8080）

### API基础URL配置

```python
from akshare_api import AKShareAPI

# 使用默认URL
api = AKShareAPI()

# 自定义URL
api = AKShareAPI(base_url="http://your-server:8080")
```

## 📊 使用示例

### 获取市场总貌

```python
from akshare_api import stock_sse_summary, stock_szse_summary

# 获取上海证券交易所总貌
sse_data = stock_sse_summary()
print(sse_data)

# 获取深圳证券交易所总貌
szse_data = stock_szse_summary()
print(szse_data)
```

### 获取实时行情

```python
from akshare_api import stock_zh_a_spot_em, stock_cy_a_spot_em

# 获取所有A股实时行情
all_stocks = stock_zh_a_spot_em()
print(f"共获取到 {len(all_stocks)} 只股票数据")

# 获取创业板实时行情
cy_stocks = stock_cy_a_spot_em()
print(f"创业板股票 {len(cy_stocks)} 只")
```

### 获取历史数据

```python
from akshare_api import stock_zh_a_hist

# 获取历史行情数据
hist_data = stock_zh_a_hist(
    symbol="000001", 
    start_date="20240101", 
    end_date="20240131"
)
print(hist_data.head())
```

### 数据分析

```python
import pandas as pd
from akshare_api import stock_zh_a_spot_em

# 获取实时行情数据
spot_data = stock_zh_a_spot_em()

# 数据分析
print(f"总股票数: {len(spot_data)}")
print(f"上涨股票: {len(spot_data[spot_data['涨跌幅'] > 0])}")
print(f"下跌股票: {len(spot_data[spot_data['涨跌幅'] < 0])}")
print(f"平均涨跌幅: {spot_data['涨跌幅'].mean():.2f}%")

# 保存数据
spot_data.to_csv('stock_data.csv', index=False, encoding='utf-8-sig')
```

## 🛠️ 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/
```

### 代码格式化

```bash
black akshare_api/
```

### 类型检查

```bash
mypy akshare_api/
```

## 📝 注意事项

### 数据源限制
- **新浪财经**: 重复运行函数会被暂时封IP，建议增加时间间隔
- **东方财富**: 数据质量高，访问无限制，推荐使用
- **腾讯证券**: 数据稳定，但接口相对较少

### 参数格式
- **日期格式**: 通常使用"YYYYMMDD"格式，如"20210301"
- **分时数据**: 使用"YYYY-MM-DD HH:MM:SS"格式
- **股票代码**: A股使用6位数字，如"000001"

### 复权数据说明
- **不复权**: 默认返回原始价格数据
- **前复权(qfq)**: 保持当前价格不变，调整历史价格
- **后复权(hfq)**: 保持历史价格不变，调整当前价格

## 🐛 常见问题

### Q: 如何解决API连接失败？
A: 请检查：
1. AKTools服务是否已启动
2. API基础URL是否正确
3. 网络连接是否正常

### Q: 如何获取更多股票数据？
A: 可以使用批量获取的方式，注意控制请求频率：

```python
import time
from akshare_api import stock_zh_a_hist

symbols = ["000001", "000002", "600000"]
for symbol in symbols:
    data = stock_zh_a_hist(symbol=symbol, start_date="20240101", end_date="20240131")
    print(f"获取 {symbol} 数据完成")
    time.sleep(0.5)  # 避免请求过于频繁
```

### Q: 如何处理数据为空的情况？
A: 检查返回的DataFrame是否为空：

```python
from akshare_api import stock_zh_a_spot_em

data = stock_zh_a_spot_em()
if data.empty:
    print("未获取到数据")
else:
    print(f"获取到 {len(data)} 条数据")
```

## 📞 支持

如果您在使用过程中遇到问题：

1. 查看本文档的常见问题部分
2. 查看项目的README.md文件
3. 在项目Issues中提问
4. 联系维护者

## 📚 相关资源

- [项目主页](https://github.com/JoshuaMaoJH/akshare-api)
- [PyPI页面](https://pypi.org/project/akshare-api/)
- [文档地址](https://github.com/JoshuaMaoJH/akshare-api#readme)
- [AKShare项目](https://github.com/akfamily/akshare)
- [AKTools项目](https://github.com/akfamily/aktools)
