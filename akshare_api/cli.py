#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API命令行工具
支持自动管理AKTools服务
"""

import argparse
import sys
from typing import Optional
from . import AKShareAPI, AKShareAPIError
from .service_manager import AKToolsServiceManager, get_service_manager


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AKShare API命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  akshare-api --help                    # 显示帮助信息
  akshare-api --list-interfaces         # 列出所有可用接口
  akshare-api --test-connection         # 测试API连接
  akshare-api --start-service           # 启动AKTools服务
  akshare-api --stop-service            # 停止AKTools服务
  akshare-api --restart-service         # 重启AKTools服务
  akshare-api --service-status          # 查看服务状态
  akshare-api --base-url http://localhost:8080  # 指定API基础URL
        """
    )
    
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8080",
        help="API基础URL (默认: http://127.0.0.1:8080)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="AKTools服务端口 (默认: 8080)"
    )
    
    parser.add_argument(
        "--list-interfaces",
        action="store_true",
        help="列出所有可用的API接口"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="测试API连接"
    )
    
    parser.add_argument(
        "--start-service",
        action="store_true",
        help="启动AKTools服务"
    )
    
    parser.add_argument(
        "--stop-service",
        action="store_true",
        help="停止AKTools服务"
    )
    
    parser.add_argument(
        "--restart-service",
        action="store_true",
        help="重启AKTools服务"
    )
    
    parser.add_argument(
        "--service-status",
        action="store_true",
        help="查看AKTools服务状态"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="AKShare API 1.0.0"
    )
    
    args = parser.parse_args()
    
    # 服务管理命令
    if args.start_service:
        start_service(args.port)
        return
    
    if args.stop_service:
        stop_service(args.port)
        return
    
    if args.restart_service:
        restart_service(args.port)
        return
    
    if args.service_status:
        show_service_status(args.port)
        return
    
    # 创建API客户端
    try:
        api = AKShareAPI(base_url=args.base_url, auto_start_service=True)
    except Exception as e:
        print(f"错误: 无法创建API客户端: {e}")
        sys.exit(1)
    
    # 列出所有接口
    if args.list_interfaces:
        list_interfaces()
        return
    
    # 测试连接
    if args.test_connection:
        test_connection(api)
        return
    
    # 如果没有指定任何操作，显示帮助
    parser.print_help()


def list_interfaces():
    """列出所有可用的API接口"""
    print("AKShare API 可用接口列表:")
    print("=" * 50)
    
    interfaces = [
        # A股数据接口
        ("A股数据接口", [
            "stock_sse_summary - 上海证券交易所总貌数据",
            "stock_szse_summary - 深圳证券交易所总貌数据",
            "stock_szse_area_summary - 深圳证券交易所地区交易排序",
            "stock_szse_sector_summary - 深圳证券交易所股票行业成交数据",
            "stock_sse_deal_daily - 上海证券交易所每日概况数据",
            "stock_individual_info_em - 个股信息查询-东方财富",
            "stock_individual_basic_info_xq - 个股信息查询-雪球",
            "stock_bid_ask_em - 行情报价-东方财富",
            "stock_zh_a_spot_em - 沪深京A股实时行情-东方财富",
            "stock_sh_a_spot_em - 沪A股实时行情-东方财富",
            "stock_sz_a_spot_em - 深A股实时行情-东方财富",
            "stock_bj_a_spot_em - 京A股实时行情-东方财富",
            "stock_new_a_spot_em - 新股实时行情-东方财富",
            "stock_cy_a_spot_em - 创业板实时行情-东方财富",
            "stock_kc_a_spot_em - 科创板实时行情-东方财富",
            "stock_zh_ab_comparison_em - AB股比价-东方财富",
            "stock_zh_a_spot - 沪深京A股实时行情-新浪",
            "stock_individual_spot_xq - 个股实时行情-雪球",
            "stock_zh_a_hist - 历史行情数据-东方财富",
            "stock_zh_a_daily - 历史行情数据-新浪",
            "stock_zh_a_hist_tx - 历史行情数据-腾讯",
            "stock_zh_a_minute - 分时数据-新浪",
            "stock_zh_a_hist_min_em - 分时数据-东方财富",
            "stock_intraday_em - 日内分时数据-东方财富",
            "stock_intraday_sina - 日内分时数据-新浪",
            "stock_zh_a_hist_pre_min_em - 盘前数据-东方财富",
            "stock_zh_a_tick_tx - 历史分笔数据-腾讯",
        ]),
        
        # B股数据接口
        ("B股数据接口", [
            "stock_zh_b_spot_em - B股实时行情-东方财富",
            "stock_zh_b_spot - B股实时行情-新浪",
            "stock_zh_b_daily - B股历史行情数据-新浪",
            "stock_zh_b_minute - B股分时数据-新浪",
        ]),
        
        # 港股数据接口
        ("港股数据接口", [
            "stock_hk_spot_em - 港股实时行情-东方财富",
            "stock_hk_spot - 港股实时行情-新浪",
            "stock_hk_daily - 港股历史行情数据-新浪",
        ]),
        
        # 美股数据接口
        ("美股数据接口", [
            "stock_us_spot - 美股实时行情-新浪",
            "stock_us_spot_em - 美股实时行情-东方财富",
            "stock_us_daily - 美股历史行情数据-新浪",
        ]),
        
        # 高级功能接口
        ("高级功能接口", [
            "stock_zt_pool_em - 涨停股池",
            "stock_zt_pool_previous_em - 昨日涨停股池",
            "stock_dt_pool_em - 跌停股池",
            "stock_lhb_detail_em - 龙虎榜详情",
            "stock_lhb_stock_statistic_em - 个股上榜统计",
            "stock_institute_visit_em - 机构调研统计",
            "stock_institute_visit_detail_em - 机构调研详细",
            "stock_institute_hold_detail - 机构持股详情",
            "stock_institute_recommend - 机构推荐池",
            "stock_institute_recommend_detail - 股票评级记录",
            "stock_research_report_em - 个股研报",
            "stock_info_cjzc_em - 财经早餐",
            "stock_info_global_em - 全球财经快讯-东方财富",
            "stock_info_global_sina - 全球财经快讯-新浪财经",
            "stock_news_em - 个股新闻-东方财富",
            "stock_news_main_cx - 财经内容精选-财新网",
            "stock_irm_cninfo - 互动易-提问",
            "stock_irm_ans_cninfo - 互动易-回答",
            "stock_sns_sseinfo - 上证e互动",
        ]),
    ]
    
    for category, interface_list in interfaces:
        print(f"\n{category}:")
        print("-" * len(category))
        for interface in interface_list:
            print(f"  {interface}")
    
    print(f"\n总计: 98个接口")
    print("\n使用示例:")
    print("  from akshare_api import stock_zh_a_spot_em")
    print("  data = stock_zh_a_spot_em()")
    print("  print(data.head())")


def start_service(port: int):
    """启动AKTools服务"""
    print(f"正在启动AKTools服务 (端口: {port})...")
    manager = get_service_manager(port=port, auto_start=False)
    if manager.start_service():
        print("✅ AKTools服务启动成功!")
    else:
        print("❌ AKTools服务启动失败!")
        sys.exit(1)


def stop_service(port: int):
    """停止AKTools服务"""
    print(f"正在停止AKTools服务 (端口: {port})...")
    manager = get_service_manager(port=port, auto_start=False)
    manager.stop_service()
    print("✅ AKTools服务已停止!")


def restart_service(port: int):
    """重启AKTools服务"""
    print(f"正在重启AKTools服务 (端口: {port})...")
    manager = get_service_manager(port=port, auto_start=False)
    if manager.restart_service():
        print("✅ AKTools服务重启成功!")
    else:
        print("❌ AKTools服务重启失败!")
        sys.exit(1)


def show_service_status(port: int):
    """显示服务状态"""
    print(f"AKTools服务状态 (端口: {port}):")
    print("-" * 40)
    
    manager = get_service_manager(port=port, auto_start=False)
    status = manager.get_service_status()
    
    print(f"运行状态: {'✅ 运行中' if status['running'] else '❌ 未运行'}")
    print(f"端口: {status['port']}")
    print(f"基础URL: {status['base_url']}")
    
    if status['process_id']:
        print(f"进程ID: {status['process_id']}")
    
    if status['response_time']:
        print(f"响应时间: {status['response_time']:.2f}ms")


def test_connection(api: AKShareAPI):
    """测试API连接"""
    print("测试API连接...")
    print(f"API基础URL: {api.base_url}")
    
    try:
        # 尝试获取一个简单的接口
        data = api.stock_sse_summary()
        if not data.empty:
            print("✅ API连接成功!")
            print(f"获取到 {len(data)} 条数据")
        else:
            print("⚠️  API连接成功，但返回数据为空")
    except AKShareAPIError as e:
        print(f"❌ API连接失败: {e}")
        print("\n请检查:")
        print("1. AKTools服务是否已启动")
        print("2. API基础URL是否正确")
        print("3. 网络连接是否正常")
        print("\n提示: 可以使用 'akshare-api --start-service' 启动服务")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
