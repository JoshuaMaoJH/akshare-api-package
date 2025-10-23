# AKShare API 文档

欢迎使用 AKShare API 文档！

## 目录

- [安装指南](installation.md)
- [快速开始](quickstart.md)
- [API参考](api_reference.md)
- [使用示例](examples.md)
- [常见问题](faq.md)
- [更新日志](changelog.md)

## 概述

AKShare API 是一个基于 AKTools 公开 API 的 Python 库，提供了完整的股票数据获取功能。它封装了 AKShare 文档中的所有股票相关数据接口，让您能够轻松获取 A股、B股、港股、美股等多个市场的实时行情、历史数据、基本面分析等数据。

## 主要特性

- 🎯 **接口完整**: 涵盖 98 个股票数据接口
- 🌍 **市场全面**: 支持多个市场的数据获取
- 🔥 **功能丰富**: 包含实时行情、历史数据、基本面分析等
- 🚀 **调用简便**: 一行代码即可获取数据
- 📊 **数据格式**: 统一返回 pandas.DataFrame 格式

## 快速开始

```python
from akshare_api import stock_zh_a_spot_em

# 获取A股实时行情
data = stock_zh_a_spot_em()
print(data.head())
```

## 安装

```bash
pip install akshare-api
```

## 许可证

本项目采用 MIT 许可证。
