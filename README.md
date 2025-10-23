# AKShare API

[![PyPI version](https://badge.fury.io/py/akshare-api.svg)](https://badge.fury.io/py/akshare-api)
[![Python Support](https://img.shields.io/pypi/pyversions/akshare-api.svg)](https://pypi.org/project/akshare-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/akshare-api)](https://pepy.tech/project/akshare-api)

基于AKTools公开API的AKShare股票数据接口Python调用库，提供完整的股票数据获取功能。
**支持自动安装和启动AKTools服务，无需手动配置！**

## ✨ 特性

- 🎯 **接口完整**: 涵盖AKShare文档中所有股票相关的数据接口（共98个接口）
- 🌍 **市场全面**: 支持A股、B股、港股、美股等多个市场
- 🔥 **功能丰富**: 包含实时行情、历史数据、基本面分析、资金流向等高级功能
- 🚀 **调用简便**: 通过封装的Python方法，一行代码即可获取数据
- ⚙️ **参数灵活**: 支持多种参数配置，满足不同分析需求
- 🛡️ **错误处理**: 内置异常处理机制，确保程序稳定运行
- 📊 **数据格式**: 统一返回pandas.DataFrame格式，便于数据分析
- 📚 **文档详细**: 每个接口都包含完整的参数说明和使用示例
- 🔧 **自动服务管理**: 自动安装和启动AKTools服务，无需手动配置
- 🔄 **智能重连**: 连接失败时自动重启服务并重试请求

## 📦 安装

### 从PyPI安装（推荐）

```bash
pip install akshare-api
```

### 从源码安装

```bash
git clone https://github.com/JoshuaMaoJH/akshare-api.git
cd akshare-api
pip install -e .
```

## 🚀 快速开始

### 基础使用（推荐）

```python
from akshare_api import stock_zh_a_spot_em, stock_zh_a_hist

# 获取A股实时行情（自动启动AKTools服务）
spot_data = stock_zh_a_spot_em()
print(f"共获取到 {len(spot_data)} 只股票数据")

# 获取历史行情数据
hist_data = stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240131")
print(hist_data.head())
```

### 面向对象使用

```python
from akshare_api import AKShareAPI

# 创建API客户端（自动启动AKTools服务）
api = AKShareAPI(base_url="http://127.0.0.1:8080")

# 获取数据
data = api.stock_zh_a_spot_em()
print(data.head())

# 查看服务状态
status = api.get_service_status()
print(f"服务状态: {status}")
```

### 手动服务管理

```python
from akshare_api import AKShareAPI

# 禁用自动服务管理
api = AKShareAPI(auto_start_service=False)

# 手动管理服务
api.start_service()  # 启动服务
api.restart_service()  # 重启服务
api.stop_service()  # 停止服务
```

### 命令行工具

```bash
# 测试API连接（自动启动服务）
akshare-api --test-connection

# 列出所有可用接口
akshare-api --list-interfaces

# 服务管理
akshare-api --start-service      # 启动服务
akshare-api --stop-service       # 停止服务
akshare-api --restart-service    # 重启服务
akshare-api --service-status     # 查看服务状态

# 指定API基础URL
akshare-api --base-url http://localhost:8080 --test-connection
```

## 📊 支持的接口

### 接口统计总览

| 分类 | 接口数量 | 说明 |
|------|----------|------|
| **A股数据接口** | 47个 | 包含市场总貌、个股信息、实时行情、历史数据、分时数据等 |
| **B股数据接口** | 4个 | B股实时行情、历史数据、分时数据 |
| **港股数据接口** | 3个 | 港股实时行情、历史数据 |
| **美股数据接口** | 3个 | 美股实时行情、历史数据 |
| **高级功能接口** | 36个 | 基本面数据、资金流向、概念板块、行业分析等 |
| **其他功能接口** | 5个 | 股票比较分析相关接口 |
| **总计** | **98个** | **完整的股票数据接口库** |

### 🏢 A股数据接口 (47个)

#### 市场总貌 (5个)
- `stock_sse_summary()` - 上海证券交易所总貌数据
- `stock_szse_summary()` - 深圳证券交易所总貌数据
- `stock_szse_area_summary()` - 深圳证券交易所地区交易排序
- `stock_szse_sector_summary()` - 深圳证券交易所股票行业成交数据
- `stock_sse_deal_daily()` - 上海证券交易所每日概况数据

#### 个股信息查询 (2个)
- `stock_individual_info_em()` - 个股信息查询-东方财富
- `stock_individual_basic_info_xq()` - 个股信息查询-雪球

#### 实时行情数据 (10个)
- `stock_zh_a_spot_em()` - 沪深京A股实时行情-东方财富
- `stock_sh_a_spot_em()` - 沪A股实时行情-东方财富
- `stock_sz_a_spot_em()` - 深A股实时行情-东方财富
- `stock_bj_a_spot_em()` - 京A股实时行情-东方财富
- `stock_new_a_spot_em()` - 新股实时行情-东方财富
- `stock_cy_a_spot_em()` - 创业板实时行情-东方财富
- `stock_kc_a_spot_em()` - 科创板实时行情-东方财富
- `stock_zh_ab_comparison_em()` - AB股比价-东方财富
- `stock_zh_a_spot()` - 沪深京A股实时行情-新浪
- `stock_individual_spot_xq()` - 个股实时行情-雪球

#### 历史行情数据 (3个)
- `stock_zh_a_hist()` - 历史行情数据-东方财富
- `stock_zh_a_daily()` - 历史行情数据-新浪
- `stock_zh_a_hist_tx()` - 历史行情数据-腾讯

#### 分时数据 (5个)
- `stock_zh_a_minute()` - 分时数据-新浪
- `stock_zh_a_hist_min_em()` - 分时数据-东方财富
- `stock_intraday_em()` - 日内分时数据-东方财富
- `stock_intraday_sina()` - 日内分时数据-新浪
- `stock_zh_a_hist_pre_min_em()` - 盘前数据-东方财富

### 🌍 其他市场数据接口

#### B股数据接口 (4个)
- `stock_zh_b_spot_em()` - B股实时行情-东方财富
- `stock_zh_b_spot()` - B股实时行情-新浪
- `stock_zh_b_daily()` - B股历史行情数据-新浪
- `stock_zh_b_minute()` - B股分时数据-新浪

#### 港股数据接口 (3个)
- `stock_hk_spot_em()` - 港股实时行情-东方财富
- `stock_hk_spot()` - 港股实时行情-新浪
- `stock_hk_daily()` - 港股历史行情数据-新浪

#### 美股数据接口 (3个)
- `stock_us_spot()` - 美股实时行情-新浪
- `stock_us_spot_em()` - 美股实时行情-东方财富
- `stock_us_daily()` - 美股历史行情数据-新浪

### 🔥 高级功能接口 (36个)

#### 涨停板行情 (3个)
- `stock_zt_pool_em()` - 涨停股池
- `stock_zt_pool_previous_em()` - 昨日涨停股池
- `stock_dt_pool_em()` - 跌停股池

#### 龙虎榜 (2个)
- `stock_lhb_detail_em()` - 龙虎榜详情
- `stock_lhb_stock_statistic_em()` - 个股上榜统计

#### 机构相关 (5个)
- `stock_institute_visit_em()` - 机构调研统计
- `stock_institute_visit_detail_em()` - 机构调研详细
- `stock_institute_hold_detail()` - 机构持股详情
- `stock_institute_recommend()` - 机构推荐池
- `stock_institute_recommend_detail()` - 股票评级记录

#### 研报资讯 (6个)
- `stock_research_report_em()` - 个股研报
- `stock_info_cjzc_em()` - 财经早餐
- `stock_info_global_em()` - 全球财经快讯-东方财富
- `stock_info_global_sina()` - 全球财经快讯-新浪财经
- `stock_news_em()` - 个股新闻-东方财富
- `stock_news_main_cx()` - 财经内容精选-财新网

## 📖 详细使用说明

### 🔧 服务管理API

#### 服务状态管理

```python
from akshare_api import AKShareAPI

api = AKShareAPI()

# 获取服务状态
status = api.get_service_status()
print(f"服务运行状态: {status['running']}")
print(f"服务端口: {status['port']}")
print(f"基础URL: {status['base_url']}")
if status['response_time']:
    print(f"响应时间: {status['response_time']:.2f}ms")

# 重启服务
if api.restart_service():
    print("服务重启成功")
else:
    print("服务重启失败")

# 停止服务
api.stop_service()
print("服务已停止")
```

#### 全局服务管理

```python
from akshare_api.service_manager import get_service_manager, ensure_service_running

# 获取全局服务管理器
manager = get_service_manager(port=8080, auto_start=True)

# 确保服务正在运行
if ensure_service_running(port=8080):
    print("服务正在运行")
else:
    print("服务启动失败")
```

### 📊 高级功能示例

#### 涨停板数据

```python
from akshare_api import stock_zt_pool_em, stock_zt_pool_previous_em, stock_dt_pool_em

# 获取涨停股池
zt_data = stock_zt_pool_em()
print(f"今日涨停股票: {len(zt_data)} 只")

# 获取昨日涨停股池
prev_zt_data = stock_zt_pool_previous_em()
print(f"昨日涨停股票: {len(prev_zt_data)} 只")

# 获取跌停股池
dt_data = stock_dt_pool_em()
print(f"今日跌停股票: {len(dt_data)} 只")
```

#### 龙虎榜数据

```python
from akshare_api import stock_lhb_detail_em, stock_lhb_stock_statistic_em

# 获取龙虎榜详情
lhb_detail = stock_lhb_detail_em(
    start_date="20240403", 
    end_date="20240417"
)

# 获取个股上榜统计
lhb_stats = stock_lhb_stock_statistic_em()
```

#### 机构相关数据

```python
from akshare_api import stock_institute_visit_em, stock_institute_recommend

# 获取机构调研统计
institute_visit = stock_institute_visit_em()

# 获取机构推荐池
institute_recommend = stock_institute_recommend(symbol="000001")
```

#### 分时数据

```python
from akshare_api import stock_zh_a_hist_min_em, stock_intraday_em

# 获取分时数据
minute_data = stock_zh_a_hist_min_em(
    symbol="000001",
    period="1",
    start_date="2024-01-01 09:30:00",
    end_date="2024-01-01 15:00:00"
)

# 获取日内分时数据
intraday_data = stock_intraday_em(symbol="000001")
```

### 💾 数据保存示例

```python
from akshare_api import stock_zh_a_spot_em

# 获取数据
spot_data = stock_zh_a_spot_em()

# 保存为CSV文件
spot_data.to_csv('stock_data.csv', index=False, encoding='utf-8-sig')

# 保存为Excel文件
spot_data.to_excel('stock_data.xlsx', index=False)

# 保存为JSON文件
spot_data.to_json('stock_data.json', orient='records', force_ascii=False, indent=2)
```

### 🔄 批量数据获取

```python
import time
from akshare_api import stock_zh_a_hist

def batch_get_stock_data(symbols, start_date, end_date):
    """批量获取多只股票的历史数据"""
    results = {}
    for symbol in symbols:
        try:
            df = stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date)
            results[symbol] = df
            print(f"成功获取 {symbol} 的数据，共 {len(df)} 条记录")
            time.sleep(0.5)  # 避免请求过于频繁
        except Exception as e:
            print(f"获取 {symbol} 数据失败: {e}")
    return results

# 使用示例
symbols = ["000001", "000002", "600000", "600036"]
data_dict = batch_get_stock_data(symbols, "20240101", "20240131")
```

### 🛡️ 错误处理

```python
from akshare_api import stock_zh_a_spot_em, AKShareAPIError

try:
    data = stock_zh_a_spot_em()
    if data.empty:
        print("未获取到数据")
    else:
        print(f"获取到 {len(data)} 条数据")
except AKShareAPIError as e:
    print(f"API错误: {e}")
    print("提示: 服务会自动尝试重启")
except Exception as e:
    print(f"未知错误: {e}")
```

### 🎯 完整示例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 完整使用示例
"""

from akshare_api import (
    stock_zh_a_spot_em,
    stock_zh_a_hist,
    stock_sse_summary,
    stock_zt_pool_em,
    AKShareAPI,
    AKShareAPIError
)

def main():
    """主函数"""
    print("=== AKShare API 完整使用示例 ===\n")
    
    try:
        # 1. 基础使用 - 自动启动服务
        print("1. 获取A股实时行情...")
        spot_data = stock_zh_a_spot_em()
        print(f"   获取到 {len(spot_data)} 只股票数据")
        
        # 2. 面向对象使用
        print("\n2. 面向对象使用...")
        api = AKShareAPI()
        
        # 查看服务状态
        status = api.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        # 获取历史数据
        print("\n3. 获取历史数据...")
        hist_data = stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240131")
        print(f"   获取到 {len(hist_data)} 条历史数据")
        
        # 获取涨停板数据
        print("\n4. 获取涨停板数据...")
        zt_data = stock_zt_pool_em()
        print(f"   今日涨停股票: {len(zt_data)} 只")
        
        # 数据分析
        print("\n5. 数据分析...")
        if '涨跌幅' in spot_data.columns:
            up_stocks = len(spot_data[spot_data['涨跌幅'] > 0])
            print(f"   上涨股票: {up_stocks} 只")
        
        print("\n✅ 所有示例运行完成！")
        
    except AKShareAPIError as e:
        print(f"❌ API错误: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")

if __name__ == "__main__":
    main()
```

## ⚙️ 配置

### 环境要求

- **Python版本**: 3.7 及以上
- **依赖包**: requests, pandas, numpy, aktools
- **网络**: 需要网络连接获取数据

### API基础URL配置

```python
from akshare_api import AKShareAPI

# 使用默认URL（自动启动服务）
api = AKShareAPI()

# 自定义URL（自动启动服务）
api = AKShareAPI(base_url="http://127.0.0.1:8080")

# 禁用自动服务管理
api = AKShareAPI(auto_start_service=False)

# 使用远程服务
api = AKShareAPI(base_url="http://your-server:8080", auto_start_service=False)
```

## 🛠️ 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
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

### Q: 首次使用需要手动安装AKTools吗？
A: **不需要！** 库会自动检测并安装最新版AKTools，无需手动操作。

### Q: 如何解决API连接失败？
A: 库会自动尝试重启服务，如果仍然失败，请检查：
1. 网络连接是否正常
2. 防火墙是否阻止了端口8080
3. 是否有其他程序占用了端口8080

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

### Q: 如何禁用自动服务管理？
A: 在创建API客户端时设置参数：

```python
from akshare_api import AKShareAPI

# 禁用自动服务管理
api = AKShareAPI(auto_start_service=False)
```

### Q: 如何查看服务状态？
A: 使用服务状态API：

```python
from akshare_api import AKShareAPI

api = AKShareAPI()
status = api.get_service_status()
print(f"服务状态: {status}")
```

### Q: 如何手动管理服务？
A: 使用服务管理方法：

```python
from akshare_api import AKShareAPI

api = AKShareAPI(auto_start_service=False)

# 启动服务
api.start_service()

# 重启服务
api.restart_service()

# 停止服务
api.stop_service()
```

## 🤝 贡献

欢迎对本项目提出建议或贡献代码：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证进行授权，详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢 [AKShare](https://github.com/akfamily/akshare) 项目提供的数据接口
- 感谢 [AKTools](https://github.com/akfamily/aktools) 项目提供的API服务

## 📞 联系方式

- 项目地址：https://github.com/JoshuaMaoJH/akshare-api
- 问题反馈：https://github.com/JoshuaMaoJH/akshare-api/issues
- 文档地址：https://github.com/JoshuaMaoJH/akshare-api#readme

如有任何问题或建议，欢迎通过Issue与我们联系。

## 📈 更新日志

### v1.1.0 (2024-01-15)

**重大更新：自动服务管理功能**

#### ✨ 新增功能
- 🔧 **自动服务管理**: 自动安装和启动AKTools服务，无需手动配置
- 🔄 **智能重连**: 连接失败时自动重启服务并重试请求
- 🛠️ **服务管理API**: 提供完整的服务状态监控和管理功能
- 🖥️ **增强命令行工具**: 新增服务管理命令
- 📊 **服务状态监控**: 实时监控服务运行状态和响应时间

#### 🔧 技术改进
- 新增 `AKToolsServiceManager` 服务管理器类
- 集成自动服务管理到主API类
- 添加 `auto_start_service` 参数控制自动服务管理
- 完善错误处理和重试机制
- 支持跨平台服务管理

#### 📚 文档更新
- 更新README.md，添加自动服务管理说明
- 新增详细使用示例和常见问题解答
- 更新安装和使用指南

#### 🔄 向后兼容
- 所有原有API接口保持不变
- 函数式调用方式完全兼容
- 默认启用自动服务管理，可通过参数禁用

### v1.0.0 (2024-01-01)

**初始版本发布**

#### ✨ 新增功能
- 🎉 **完整接口库**: 包含所有98个AKShare接口
- 🌍 **多市场支持**: 支持A股、B股、港股、美股数据接口
- 🔥 **高级功能**: 涨停板、龙虎榜、机构调研、研报资讯等高级功能接口
- 📊 **接口统计**: 完整的接口分类统计和使用说明
- 🐍 **Python封装**: 面向对象和函数式两种调用方式
- 🛠️ **CLI工具**: 命令行工具支持接口列表和连接测试
- 📚 **完整文档**: 详细的API文档和使用示例

#### 📈 接口数量
- **A股数据接口**: 47个（市场总貌、实时行情、历史数据、分时数据等）
- **B股数据接口**: 4个（实时行情、历史数据、分时数据）
- **港股数据接口**: 3个（实时行情、历史数据）
- **美股数据接口**: 3个（实时行情、历史数据）
- **高级功能接口**: 36个（基本面、资金流向、概念板块等）
- **其他功能接口**: 5个（比较分析、特殊功能等）

---

**🎉 现在您可以直接使用AKShare API，无需任何手动配置！**
