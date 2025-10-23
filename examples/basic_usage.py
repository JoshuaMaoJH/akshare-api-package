#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 基础使用示例
"""

import pandas as pd
from akshare_api import (
    stock_zh_a_spot_em,
    stock_zh_a_hist,
    stock_sse_summary,
    stock_zt_pool_em,
    AKShareAPI,
    AKShareAPIError
)


def basic_usage_example():
    """基础使用示例"""
    print("=== AKShare API 基础使用示例 ===\n")
    
    try:
        # 1. 获取A股实时行情
        print("1. 获取A股实时行情...")
        spot_data = stock_zh_a_spot_em()
        print(f"   获取到 {len(spot_data)} 只股票数据")
        if not spot_data.empty:
            print(f"   前5只股票:")
            print(spot_data.head())
        print()
        
        # 2. 获取上海证券交易所总貌
        print("2. 获取上海证券交易所总貌...")
        sse_summary = stock_sse_summary()
        print(f"   获取到 {len(sse_summary)} 条总貌数据")
        if not sse_summary.empty:
            print(sse_summary.head())
        print()
        
        # 3. 获取涨停股池
        print("3. 获取涨停股池...")
        zt_data = stock_zt_pool_em()
        print(f"   今日涨停股票 {len(zt_data)} 只")
        if not zt_data.empty:
            print(zt_data.head())
        print()
        
        # 4. 获取历史行情数据
        print("4. 获取历史行情数据...")
        hist_data = stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240131")
        print(f"   获取到 {len(hist_data)} 条历史数据")
        if not hist_data.empty:
            print(hist_data.head())
        print()
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def object_oriented_example():
    """面向对象使用示例"""
    print("=== 面向对象使用示例 ===\n")
    
    try:
        # 创建API客户端
        api = AKShareAPI(base_url="http://127.0.0.1:8080")
        
        # 获取数据
        print("1. 获取A股实时行情...")
        spot_data = api.stock_zh_a_spot_em()
        print(f"   获取到 {len(spot_data)} 只股票数据")
        
        print("2. 获取创业板实时行情...")
        cy_data = api.stock_cy_a_spot_em()
        print(f"   创业板股票 {len(cy_data)} 只")
        
        print("3. 获取科创板实时行情...")
        kc_data = api.stock_kc_a_spot_em()
        print(f"   科创板股票 {len(kc_data)} 只")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def data_analysis_example():
    """数据分析示例"""
    print("=== 数据分析示例 ===\n")
    
    try:
        # 获取实时行情数据
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        print(f"总股票数: {len(spot_data)}")
        
        # 分析涨跌情况
        if '涨跌幅' in spot_data.columns:
            up_stocks = len(spot_data[spot_data['涨跌幅'] > 0])
            down_stocks = len(spot_data[spot_data['涨跌幅'] < 0])
            flat_stocks = len(spot_data[spot_data['涨跌幅'] == 0])
            
            print(f"上涨股票: {up_stocks} 只")
            print(f"下跌股票: {down_stocks} 只")
            print(f"平盘股票: {flat_stocks} 只")
            print(f"平均涨跌幅: {spot_data['涨跌幅'].mean():.2f}%")
        
        # 筛选涨幅大于5%的股票
        if '涨跌幅' in spot_data.columns:
            high_gain_stocks = spot_data[spot_data['涨跌幅'] > 5]
            print(f"\n涨幅大于5%的股票有 {len(high_gain_stocks)} 只")
            if not high_gain_stocks.empty:
                print("涨幅前10的股票:")
                print(high_gain_stocks.head(10))
        
        # 按成交量排序
        if '成交量' in spot_data.columns:
            volume_sorted = spot_data.sort_values('成交量', ascending=False)
            print(f"\n成交量前10的股票:")
            print(volume_sorted.head(10))
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def batch_data_example():
    """批量数据获取示例"""
    print("=== 批量数据获取示例 ===\n")
    
    import time
    
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
    print(f"批量获取股票 {symbols} 的历史数据...")
    data_dict = batch_get_stock_data(symbols, "20240101", "20240131")
    
    print(f"\n成功获取 {len(data_dict)} 只股票的数据")


def save_data_example():
    """数据保存示例"""
    print("=== 数据保存示例 ===\n")
    
    try:
        # 获取实时行情数据
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        # 保存为CSV文件
        csv_file = "stock_data.csv"
        spot_data.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"数据已保存到 {csv_file}")
        
        # 保存为Excel文件
        excel_file = "stock_data.xlsx"
        spot_data.to_excel(excel_file, index=False)
        print(f"数据已保存到 {excel_file}")
        
        # 保存为JSON文件
        json_file = "stock_data.json"
        spot_data.to_json(json_file, orient='records', force_ascii=False, indent=2)
        print(f"数据已保存到 {json_file}")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


if __name__ == "__main__":
    print("AKShare API 使用示例\n")
    
    # 运行各种示例
    basic_usage_example()
    print("\n" + "="*50 + "\n")
    
    object_oriented_example()
    print("\n" + "="*50 + "\n")
    
    data_analysis_example()
    print("\n" + "="*50 + "\n")
    
    batch_data_example()
    print("\n" + "="*50 + "\n")
    
    save_data_example()
    
    print("\n所有示例运行完成！")
