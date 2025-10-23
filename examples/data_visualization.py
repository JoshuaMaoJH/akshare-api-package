#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 数据可视化示例
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from akshare_api import (
    stock_zh_a_spot_em,
    stock_zh_a_hist,
    stock_zt_pool_em,
    stock_dt_pool_em,
    AKShareAPIError
)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def plot_market_distribution():
    """绘制市场涨跌分布图"""
    print("=== 市场涨跌分布图 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty or '涨跌幅' not in spot_data.columns:
            print("未获取到有效数据")
            return
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 涨跌幅分布直方图
        ax1.hist(spot_data['涨跌幅'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title('股票涨跌幅分布')
        ax1.set_xlabel('涨跌幅 (%)')
        ax1.set_ylabel('股票数量')
        ax1.grid(True, alpha=0.3)
        
        # 涨跌比例饼图
        up_count = len(spot_data[spot_data['涨跌幅'] > 0])
        down_count = len(spot_data[spot_data['涨跌幅'] < 0])
        flat_count = len(spot_data[spot_data['涨跌幅'] == 0])
        
        labels = ['上涨', '下跌', '平盘']
        sizes = [up_count, down_count, flat_count]
        colors = ['red', 'green', 'gray']
        
        ax2.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('涨跌比例分布')
        
        plt.tight_layout()
        plt.savefig('market_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("市场分布图已保存为 market_distribution.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_volume_analysis():
    """绘制成交量分析图"""
    print("=== 成交量分析图 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty or '成交量' not in spot_data.columns:
            print("未获取到有效数据")
            return
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 成交量分布
        ax1.hist(spot_data['成交量'], bins=50, alpha=0.7, color='orange', edgecolor='black')
        ax1.set_title('成交量分布')
        ax1.set_xlabel('成交量')
        ax1.set_ylabel('股票数量')
        ax1.set_yscale('log')  # 使用对数坐标
        ax1.grid(True, alpha=0.3)
        
        # 成交量前20的股票
        top20_volume = spot_data.nlargest(20, '成交量')
        ax2.barh(range(len(top20_volume)), top20_volume['成交量'])
        ax2.set_yticks(range(len(top20_volume)))
        ax2.set_yticklabels(top20_volume['名称'], fontsize=8)
        ax2.set_title('成交量前20的股票')
        ax2.set_xlabel('成交量')
        
        plt.tight_layout()
        plt.savefig('volume_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("成交量分析图已保存为 volume_analysis.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_limit_up_down():
    """绘制涨跌停分析图"""
    print("=== 涨跌停分析图 ===\n")
    
    try:
        # 获取涨停跌停数据
        zt_data = stock_zt_pool_em()
        dt_data = stock_dt_pool_em()
        
        zt_count = len(zt_data) if not zt_data.empty else 0
        dt_count = len(dt_data) if not dt_data.empty else 0
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 涨跌停数量对比
        categories = ['涨停', '跌停']
        counts = [zt_count, dt_count]
        colors = ['red', 'green']
        
        bars = ax1.bar(categories, counts, color=colors, alpha=0.7)
        ax1.set_title('涨跌停数量对比')
        ax1.set_ylabel('股票数量')
        
        # 在柱状图上添加数值标签
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
        
        # 涨跌停比例饼图
        if zt_count + dt_count > 0:
            ax2.pie([zt_count, dt_count], labels=['涨停', '跌停'], 
                   colors=['red', 'green'], autopct='%1.1f%%', startangle=90)
            ax2.set_title('涨跌停比例')
        else:
            ax2.text(0.5, 0.5, '无涨跌停数据', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('涨跌停比例')
        
        plt.tight_layout()
        plt.savefig('limit_up_down.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("涨跌停分析图已保存为 limit_up_down.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_historical_data(symbol="000001"):
    """绘制历史数据图表"""
    print(f"=== {symbol} 历史数据图表 ===\n")
    
    try:
        # 获取历史数据
        hist_data = stock_zh_a_hist(symbol=symbol, start_date="20240101", end_date="20241231")
        
        if hist_data.empty:
            print("未获取到历史数据")
            return
        
        # 创建图形
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # 价格走势图
        if '收盘' in hist_data.columns:
            ax1.plot(hist_data.index, hist_data['收盘'], label='收盘价', color='blue', linewidth=2)
            ax1.set_title(f'{symbol} 价格走势')
            ax1.set_ylabel('价格')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # 成交量图
        if '成交量' in hist_data.columns:
            ax2.bar(hist_data.index, hist_data['成交量'], alpha=0.7, color='orange')
            ax2.set_title(f'{symbol} 成交量')
            ax2.set_ylabel('成交量')
            ax2.set_xlabel('日期')
            ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'historical_data_{symbol}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"历史数据图表已保存为 historical_data_{symbol}.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_correlation_analysis():
    """绘制相关性分析图"""
    print("=== 相关性分析图 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        # 选择数值列进行相关性分析
        numeric_columns = []
        for col in ['涨跌幅', '成交量', '成交额', '换手率', '市盈率', '市净率']:
            if col in spot_data.columns:
                numeric_columns.append(col)
        
        if len(numeric_columns) < 2:
            print("数值列不足，无法进行相关性分析")
            return
        
        # 计算相关性矩阵
        corr_data = spot_data[numeric_columns].corr()
        
        # 创建热力图
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('股票指标相关性分析')
        plt.tight_layout()
        plt.savefig('correlation_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("相关性分析图已保存为 correlation_analysis.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_market_heatmap():
    """绘制市场热力图"""
    print("=== 市场热力图 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty or '涨跌幅' not in spot_data.columns:
            print("未获取到有效数据")
            return
        
        # 按涨跌幅排序，选择前50只股票
        top50 = spot_data.nlargest(50, '涨跌幅')
        
        # 创建热力图数据
        heatmap_data = top50[['涨跌幅']].T
        
        # 创建热力图
        plt.figure(figsize=(20, 6))
        sns.heatmap(heatmap_data, cmap='RdYlGn', center=0, 
                   yticklabels=['涨跌幅'], xticklabels=top50['名称'],
                   cbar_kws={'label': '涨跌幅 (%)'})
        plt.title('涨幅前50股票热力图')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('market_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("市场热力图已保存为 market_heatmap.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


def plot_comprehensive_dashboard():
    """绘制综合仪表板"""
    print("=== 综合仪表板 ===\n")
    
    try:
        # 获取A股实时行情
        spot_data = stock_zh_a_spot_em()
        
        if spot_data.empty:
            print("未获取到数据")
            return
        
        # 创建综合仪表板
        fig = plt.figure(figsize=(20, 12))
        
        # 1. 涨跌比例饼图
        ax1 = plt.subplot(2, 3, 1)
        if '涨跌幅' in spot_data.columns:
            up_count = len(spot_data[spot_data['涨跌幅'] > 0])
            down_count = len(spot_data[spot_data['涨跌幅'] < 0])
            flat_count = len(spot_data[spot_data['涨跌幅'] == 0])
            
            labels = ['上涨', '下跌', '平盘']
            sizes = [up_count, down_count, flat_count]
            colors = ['red', 'green', 'gray']
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax1.set_title('涨跌比例')
        
        # 2. 涨跌幅分布直方图
        ax2 = plt.subplot(2, 3, 2)
        if '涨跌幅' in spot_data.columns:
            ax2.hist(spot_data['涨跌幅'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.set_title('涨跌幅分布')
            ax2.set_xlabel('涨跌幅 (%)')
            ax2.set_ylabel('股票数量')
            ax2.grid(True, alpha=0.3)
        
        # 3. 成交量前20
        ax3 = plt.subplot(2, 3, 3)
        if '成交量' in spot_data.columns:
            top20_volume = spot_data.nlargest(20, '成交量')
            ax3.barh(range(len(top20_volume)), top20_volume['成交量'])
            ax3.set_yticks(range(len(top20_volume)))
            ax3.set_yticklabels(top20_volume['名称'], fontsize=8)
            ax3.set_title('成交量前20')
            ax3.set_xlabel('成交量')
        
        # 4. 市场统计信息
        ax4 = plt.subplot(2, 3, 4)
        ax4.axis('off')
        
        stats_text = f"""
        市场统计信息
        
        总股票数: {len(spot_data)}
        """
        
        if '涨跌幅' in spot_data.columns:
            up_count = len(spot_data[spot_data['涨跌幅'] > 0])
            down_count = len(spot_data[spot_data['涨跌幅'] < 0])
            avg_change = spot_data['涨跌幅'].mean()
            
            stats_text += f"""
        上涨股票: {up_count} 只
        下跌股票: {down_count} 只
        平均涨跌幅: {avg_change:.2f}%
            """
        
        if '成交量' in spot_data.columns:
            total_volume = spot_data['成交量'].sum()
            avg_volume = spot_data['成交量'].mean()
            
            stats_text += f"""
        总成交量: {total_volume:,.0f}
        平均成交量: {avg_volume:,.0f}
            """
        
        ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace')
        
        # 5. 涨跌幅箱线图
        ax5 = plt.subplot(2, 3, 5)
        if '涨跌幅' in spot_data.columns:
            ax5.boxplot(spot_data['涨跌幅'])
            ax5.set_title('涨跌幅箱线图')
            ax5.set_ylabel('涨跌幅 (%)')
            ax5.grid(True, alpha=0.3)
        
        # 6. 成交量分布
        ax6 = plt.subplot(2, 3, 6)
        if '成交量' in spot_data.columns:
            ax6.hist(spot_data['成交量'], bins=30, alpha=0.7, color='orange', edgecolor='black')
            ax6.set_title('成交量分布')
            ax6.set_xlabel('成交量')
            ax6.set_ylabel('股票数量')
            ax6.set_yscale('log')
            ax6.grid(True, alpha=0.3)
        
        plt.suptitle('AKShare API 综合仪表板', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("综合仪表板已保存为 comprehensive_dashboard.png")
        
    except AKShareAPIError as e:
        print(f"API错误: {e}")
    except Exception as e:
        print(f"未知错误: {e}")


if __name__ == "__main__":
    print("AKShare API 数据可视化示例\n")
    
    # 运行各种可视化
    plot_market_distribution()
    print("\n" + "="*50 + "\n")
    
    plot_volume_analysis()
    print("\n" + "="*50 + "\n")
    
    plot_limit_up_down()
    print("\n" + "="*50 + "\n")
    
    plot_historical_data("000001")
    print("\n" + "="*50 + "\n")
    
    plot_correlation_analysis()
    print("\n" + "="*50 + "\n")
    
    plot_market_heatmap()
    print("\n" + "="*50 + "\n")
    
    plot_comprehensive_dashboard()
    
    print("\n所有可视化完成！")
