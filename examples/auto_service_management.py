#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 自动服务管理示例
演示如何使用自动安装和启动AKTools服务的功能
"""

import time
from akshare_api import (
    stock_zh_a_spot_em,
    stock_zh_a_hist,
    stock_sse_summary,
    AKShareAPI,
    AKShareAPIError
)


def auto_service_demo():
    """自动服务管理演示"""
    print("=== AKShare API 自动服务管理演示 ===\n")
    
    try:
        # 1. 基础使用 - 自动启动服务
        print("1. 基础使用 - 自动启动AKTools服务...")
        spot_data = stock_zh_a_spot_em()
        print(f"   ✅ 成功获取到 {len(spot_data)} 只股票数据")
        print()
        
        # 2. 面向对象使用 - 查看服务状态
        print("2. 面向对象使用 - 查看服务状态...")
        api = AKShareAPI()
        status = api.get_service_status()
        print(f"   ✅ 服务状态: {'运行中' if status['running'] else '未运行'}")
        print(f"   📊 端口: {status['port']}")
        print(f"   🌐 基础URL: {status['base_url']}")
        if status['response_time']:
            print(f"   ⚡ 响应时间: {status['response_time']:.2f}ms")
        print()
        
        # 3. 获取历史数据
        print("3. 获取历史数据...")
        hist_data = stock_zh_a_hist(symbol="000001", start_date="20240101", end_date="20240131")
        print(f"   ✅ 成功获取到 {len(hist_data)} 条历史数据")
        print()
        
        # 4. 获取市场总貌
        print("4. 获取市场总貌...")
        sse_summary = stock_sse_summary()
        print(f"   ✅ 成功获取到 {len(sse_summary)} 条总貌数据")
        print()
        
        print("🎉 所有演示完成！AKTools服务自动管理功能正常工作。")
        
    except AKShareAPIError as e:
        print(f"❌ API错误: {e}")
    except Exception as e:
        print(f"❌ 未知错误: {e}")


def manual_service_management_demo():
    """手动服务管理演示"""
    print("=== 手动服务管理演示 ===\n")
    
    try:
        # 创建API客户端，禁用自动服务管理
        api = AKShareAPI(auto_start_service=False)
        
        # 检查初始状态
        print("1. 检查初始服务状态...")
        status = api.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        # 手动启动服务
        print("\n2. 手动启动服务...")
        if api.restart_service():
            print("   ✅ 服务启动成功")
        else:
            print("   ❌ 服务启动失败")
            return
        
        # 再次检查状态
        print("\n3. 检查服务状态...")
        status = api.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        # 测试数据获取
        print("\n4. 测试数据获取...")
        data = api.stock_zh_a_spot_em()
        print(f"   ✅ 成功获取到 {len(data)} 条数据")
        
        # 停止服务
        print("\n5. 停止服务...")
        api.stop_service()
        print("   ✅ 服务已停止")
        
        # 最终状态检查
        print("\n6. 最终状态检查...")
        status = api.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        print("\n🎉 手动服务管理演示完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


def error_handling_demo():
    """错误处理和自动重连演示"""
    print("=== 错误处理和自动重连演示 ===\n")
    
    try:
        # 创建API客户端
        api = AKShareAPI()
        
        print("1. 正常数据获取...")
        data = api.stock_zh_a_spot_em()
        print(f"   ✅ 成功获取到 {len(data)} 条数据")
        
        print("\n2. 模拟服务异常（停止服务）...")
        api.stop_service()
        
        print("\n3. 尝试获取数据（应该自动重启服务）...")
        # 这里会触发自动重连机制
        data = api.stock_zh_a_spot_em()
        print(f"   ✅ 自动重连成功，获取到 {len(data)} 条数据")
        
        print("\n🎉 错误处理和自动重连演示完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


def performance_test_demo():
    """性能测试演示"""
    print("=== 性能测试演示 ===\n")
    
    try:
        api = AKShareAPI()
        
        # 测试多个接口的调用性能
        interfaces = [
            ("A股实时行情", lambda: api.stock_zh_a_spot_em()),
            ("上交所总貌", lambda: api.stock_sse_summary()),
            ("创业板行情", lambda: api.stock_cy_a_spot_em()),
            ("科创板行情", lambda: api.stock_kc_a_spot_em()),
        ]
        
        print("测试多个接口的调用性能:")
        for name, func in interfaces:
            start_time = time.time()
            try:
                data = func()
                end_time = time.time()
                print(f"   {name}: {len(data)} 条数据, 耗时 {end_time - start_time:.2f}s")
            except Exception as e:
                print(f"   {name}: 失败 - {e}")
        
        print("\n🎉 性能测试完成！")
        
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == "__main__":
    print("AKShare API 自动服务管理功能演示\n")
    
    # 运行各种演示
    auto_service_demo()
    print("\n" + "="*60 + "\n")
    
    manual_service_management_demo()
    print("\n" + "="*60 + "\n")
    
    error_handling_demo()
    print("\n" + "="*60 + "\n")
    
    performance_test_demo()
    
    print("\n" + "="*60)
    print("🎊 所有演示完成！")
    print("\n💡 提示:")
    print("- 首次使用时会自动安装AKTools")
    print("- 服务会自动启动，无需手动配置")
    print("- 连接失败时会自动重试")
    print("- 支持手动服务管理")
    print("- 提供完整的错误处理机制")
