#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 市场分析示例
"""

import pandas as pd
import numpy as np
from akshare_api import (
    stock_zh_a_spot_em,
    stock_sse_summary,
    stock_szse_summary,
    stock_zt_pool_em,
    stock_dt_pool_em,
    stock_hot_rank_em,
    stock_board_concept_name_em,
    stock_board_industry_name_em,
    AKShareAPIError
)


def market_overview_analysis():
    """市场总貌分析"""
    print("=== 市场总貌分析 ===\n")
    
    try:
        # 获取上海证券交易所总貌
        sse_summary = stock_sse_summary()
        if not sse_summary.empty:
            print("上海证券交易所总貌:")
            print(sse_summary)
            print()
        
        # 获取深圳证券交易所总貌
        szse_summary = stock_szse_summary()
        if not szse_summary.empty:
            print("深圳证券交易所总貌:")
            print(szse_summary)
            print()
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def stock_market_analysis():
    """股票市场分析"""
    print("=== 股票市场分析 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        print(f"总股票数: {len(spot_data)}")
        
        # 分析涨跌情况
        if '涨跌幅' in spot_data.columns:
            # 基本统计
            up_stocks = len(spot_data[spot_data['涨跌幅'] > 0])
            down_stocks = len(spot_data[spot_data['涨跌幅'] < 0])
            flat_stocks = len(spot_data[spot_data['涨跌幅'] == 0])
            
            print(f"上涨股票: {up_stocks} 只 ({up_stocks/len(spot_data)*100:.1f}%)")
            print(f"下跌股票: {down_stocks} 只 ({down_stocks/len(spot_data)*100:.1f}%)")
            print(f"平盘股票: {flat_stocks} 只 ({flat_stocks/len(spot_data)*100:.1f}%)")
            print(f"平均涨跌幅: {spot_data['涨跌幅'].mean():.2f}%")
            print(f"涨跌幅标准差: {spot_data['涨跌幅'].std():.2f}%")
            
            # 涨跌幅分布
            print(f"\n涨跌幅分布:")
            print(f"涨幅 > 10%: {len(spot_data[spot_data['涨跌幅'] > 10])} 只")
            print(f"涨幅 5%-10%: {len(spot_data[(spot_data['涨跌幅'] > 5) & (spot_data['涨跌幅'] <= 10)])} 只")
            print(f"涨幅 0%-5%: {len(spot_data[(spot_data['涨跌幅'] > 0) & (spot_data['涨跌幅'] <= 5)])} 只")
            print(f"跌幅 0%-5%: {len(spot_data[(spot_data['涨跌幅'] >= -5) & (spot_data['涨跌幅'] < 0)])} 只")
            print(f"跌幅 5%-10%: {len(spot_data[(spot_data['涨跌幅'] >= -10) & (spot_data['涨跌幅'] < -5)])} 只")
            print(f"跌幅 > 10%: {len(spot_data[spot_data['涨跌幅'] < -10])} 只")
        
        # 成交量分析
        if '成交量' in spot_data.columns:
            print(f"\n成交量分析:")
            print(f"总成交量: {spot_data['成交量'].sum():,.0f}")
            print(f"平均成交量: {spot_data['成交量'].mean():,.0f}")
            print(f"成交量中位数: {spot_data['成交量'].median():,.0f}")
            
            # 成交量前10
            volume_top10 = spot_data.nlargest(10, '成交量')
            print(f"\n成交量前10的股票:")
            print(volume_top10[['代码', '名称', '成交量', '涨跌幅']].to_string(index=False))
        
        # 成交额分析
        if '成交额' in spot_data.columns:
            print(f"\n成交额分析:")
            print(f"总成交额: {spot_data['成交额'].sum():,.0f} 万元")
            print(f"平均成交额: {spot_data['成交额'].mean():,.0f} 万元")
            
            # 成交额前10
            amount_top10 = spot_data.nlargest(10, '成交额')
            print(f"\n成交额前10的股票:")
            print(amount_top10[['代码', '名称', '成交额', '涨跌幅']].to_string(index=False))
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def limit_up_down_analysis():
    """涨跌停分析"""
    print("=== 涨跌停分析 ===\n")
    
    try:
        # 获取涨停股池
        zt_data = stock_zt_pool_em()
        if not zt_data.empty:
            print(f"涨停股票: {len(zt_data)} 只")
            print("涨停股票列表:")
            print(zt_data.head(10))
            print()
        
        # 获取跌停股池
        dt_data = stock_dt_pool_em()
        if not dt_data.empty:
            print(f"跌停股票: {len(dt_data)} 只")
            print("跌停股票列表:")
            print(dt_data.head(10))
            print()
        
        # 涨停跌停对比
        zt_count = len(zt_data) if not zt_data.empty else 0
        dt_count = len(dt_data) if not dt_data.empty else 0
        
        if zt_count + dt_count > 0:
            print(f"涨跌停对比:")
            print(f"涨停: {zt_count} 只 ({zt_count/(zt_count+dt_count)*100:.1f}%)")
            print(f"跌停: {dt_count} 只 ({dt_count/(zt_count+dt_count)*100:.1f}%)")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def hot_stocks_analysis():
    """热门股票分析"""
    print("=== 热门股票分析 ===\n")
    
    try:
        # 获取股票热度排行
        hot_data = stock_hot_rank_em()
        if not hot_data.empty:
            print(f"热门股票排行: {len(hot_data)} 只")
            print("热门股票前10:")
            print(hot_data.head(10))
            print()
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def sector_analysis():
    """板块分析"""
    print("=== 板块分析 ===\n")
    
    try:
        # 获取概念板块
        concept_data = stock_board_concept_name_em()
        if not concept_data.empty:
            print(f"概念板块数量: {len(concept_data)}")
            print("概念板块前10:")
            print(concept_data.head(10))
            print()
        
        # 获取行业板块
        industry_data = stock_board_industry_name_em()
        if not industry_data.empty:
            print(f"行业板块数量: {len(industry_data)}")
            print("行业板块前10:")
            print(industry_data.head(10))
            print()
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def market_sentiment_analysis():
    """市场情绪分析"""
    print("=== 市场情绪分析 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty or '涨跌幅' not in spot_data.columns:
            print("未获取到有效数据")
            return
        
        # 计算市场情绪指标
        up_ratio = len(spot_data[spot_data['涨跌幅'] > 0]) / len(spot_data) * 100
        down_ratio = len(spot_data[spot_data['涨跌幅'] < 0]) / len(spot_data) * 100
        avg_change = spot_data['涨跌幅'].mean()
        
        print(f"市场情绪指标:")
        print(f"上涨比例: {up_ratio:.1f}%")
        print(f"下跌比例: {down_ratio:.1f}%")
        print(f"平均涨跌幅: {avg_change:.2f}%")
        
        # 情绪判断
        if up_ratio > 60 and avg_change > 1:
            sentiment = "乐观"
        elif up_ratio > 50 and avg_change > 0:
            sentiment = "谨慎乐观"
        elif up_ratio < 40 and avg_change < -1:
            sentiment = "悲观"
        elif up_ratio < 50 and avg_change < 0:
            sentiment = "谨慎悲观"
        else:
            sentiment = "中性"
        
        print(f"市场情绪: {sentiment}")
        
        # 涨跌幅分布
        print(f"\n涨跌幅分布:")
        ranges = [
            (10, float('inf'), "涨幅>10%"),
            (5, 10, "涨幅5%-10%"),
            (0, 5, "涨幅0%-5%"),
            (-5, 0, "跌幅0%-5%"),
            (-10, -5, "跌幅5%-10%"),
            (-float('inf'), -10, "跌幅>10%")
        ]
        
        for min_val, max_val, label in ranges:
            if max_val == float('inf'):
                count = len(spot_data[spot_data['涨跌幅'] > min_val])
            elif min_val == -float('inf'):
                count = len(spot_data[spot_data['涨跌幅'] < max_val])
            else:
                count = len(spot_data[(spot_data['涨跌幅'] > min_val) & (spot_data['涨跌幅'] <= max_val)])
            print(f"{label}: {count} 只")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def comprehensive_market_analysis():
    """综合市场分析"""
    print("=== 综合市场分析 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        print(f"市场概况:")
        print(f"总股票数: {len(spot_data)}")
        
        if '涨跌幅' in spot_data.columns:
            up_count = len(spot_data[spot_data['涨跌幅'] > 0])
            down_count = len(spot_data[spot_data['涨跌幅'] < 0])
            avg_change = spot_data['涨跌幅'].mean()
            
            print(f"上涨股票: {up_count} 只 ({up_count/len(spot_data)*100:.1f}%)")
            print(f"下跌股票: {down_count} 只 ({down_count/len(spot_data)*100:.1f}%)")
            print(f"平均涨跌幅: {avg_change:.2f}%")
        
        # 获取涨停跌停数据
        try:
            zt_data = stock_zt_pool_em()
            dt_data = stock_dt_pool_em()
            
            zt_count = len(zt_data) if not zt_data.empty else 0
            dt_count = len(dt_data) if not dt_data.empty else 0
            
            print(f"涨停股票: {zt_count} 只")
            print(f"跌停股票: {dt_count} 只")
            
        except:
            print("涨停跌停数据获取失败")
        
        # 市场强度分析
        if '涨跌幅' in spot_data.columns:
            strong_up = len(spot_data[spot_data['涨跌幅'] > 5])
            strong_down = len(spot_data[spot_data['涨跌幅'] < -5])
            
            print(f"强势上涨(>5%): {strong_up} 只")
            print(f"强势下跌(<-5%): {strong_down} 只")
            
            # 市场强度评分
            strength_score = (up_count - down_count) / len(spot_data) * 100
            print(f"市场强度评分: {strength_score:.1f}")
            
            if strength_score > 20:
                strength_level = "强势"
            elif strength_score > 10:
                strength_level = "较强"
            elif strength_score > -10:
                strength_level = "平衡"
            elif strength_score > -20:
                strength_level = "较弱"
            else:
                strength_level = "弱势"
            
            print(f"市场强度: {strength_level}")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


if __name__ == "__main__":
    print("AKShare API 市场分析示例\n")
    
    # 运行各种分析
    market_overview_analysis()
    print("\n" + "="*50 + "\n")
    
    stock_market_analysis()
    print("\n" + "="*50 + "\n")
    
    limit_up_down_analysis()
    print("\n" + "="*50 + "\n")
    
    hot_stocks_analysis()
    print("\n" + "="*50 + "\n")
    
    sector_analysis()
    print("\n" + "="*50 + "\n")
    
    market_sentiment_analysis()
    print("\n" + "="*50 + "\n")
    
    comprehensive_market_analysis()
    
    print("\n所有分析完成！")
