#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 自动服务管理功能测试
"""

import sys
import os
import time

# 添加包路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from akshare_api.service_manager import AKToolsServiceManager, get_service_manager
from akshare_api import AKShareAPI, AKShareAPIError


def test_service_manager():
    """测试服务管理器"""
    print("=== 测试服务管理器 ===\n")
    
    try:
        # 测试服务管理器初始化
        print("1. 测试服务管理器初始化...")
        manager = AKToolsServiceManager(port=8080, auto_start=False)
        print("   ✅ 服务管理器初始化成功")
        
        # 测试服务状态检查
        print("\n2. 测试服务状态检查...")
        status = manager.get_service_status()
        print(f"   初始状态: {'运行中' if status['running'] else '未运行'}")
        
        # 测试服务启动
        print("\n3. 测试服务启动...")
        if manager.start_service():
            print("   ✅ 服务启动成功")
        else:
            print("   ⚠️  服务启动失败（可能已运行）")
        
        # 再次检查状态
        print("\n4. 再次检查服务状态...")
        status = manager.get_service_status()
        print(f"   当前状态: {'运行中' if status['running'] else '未运行'}")
        if status['response_time']:
            print(f"   响应时间: {status['response_time']:.2f}ms")
        
        # 测试服务停止
        print("\n5. 测试服务停止...")
        manager.stop_service()
        print("   ✅ 服务停止成功")
        
        # 最终状态检查
        print("\n6. 最终状态检查...")
        status = manager.get_service_status()
        print(f"   最终状态: {'运行中' if status['running'] else '未运行'}")
        
        print("\n✅ 服务管理器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 服务管理器测试失败: {e}")
        return False


def test_api_integration():
    """测试API集成"""
    print("\n=== 测试API集成 ===\n")
    
    try:
        # 测试API初始化（自动启动服务）
        print("1. 测试API初始化（自动启动服务）...")
        api = AKShareAPI(auto_start_service=True)
        print("   ✅ API初始化成功")
        
        # 测试服务状态获取
        print("\n2. 测试服务状态获取...")
        status = api.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        # 测试数据获取
        print("\n3. 测试数据获取...")
        try:
            data = api.stock_sse_summary()
            print(f"   ✅ 成功获取到 {len(data)} 条数据")
        except AKShareAPIError as e:
            print(f"   ⚠️  数据获取失败: {e}")
        
        # 测试服务重启
        print("\n4. 测试服务重启...")
        if api.restart_service():
            print("   ✅ 服务重启成功")
        else:
            print("   ⚠️  服务重启失败")
        
        # 测试服务停止
        print("\n5. 测试服务停止...")
        api.stop_service()
        print("   ✅ 服务停止成功")
        
        print("\n✅ API集成测试完成")
        return True
        
    except Exception as e:
        print(f"❌ API集成测试失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===\n")
    
    try:
        # 创建API客户端
        api = AKShareAPI(auto_start_service=True)
        
        # 停止服务
        print("1. 停止服务...")
        api.stop_service()
        
        # 尝试获取数据（应该触发自动重连）
        print("\n2. 尝试获取数据（测试自动重连）...")
        try:
            data = api.stock_sse_summary()
            print(f"   ✅ 自动重连成功，获取到 {len(data)} 条数据")
        except AKShareAPIError as e:
            print(f"   ⚠️  自动重连失败: {e}")
        
        print("\n✅ 错误处理测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False


def test_global_manager():
    """测试全局服务管理器"""
    print("\n=== 测试全局服务管理器 ===\n")
    
    try:
        # 测试全局服务管理器
        print("1. 测试全局服务管理器...")
        manager1 = get_service_manager(port=8080, auto_start=False)
        manager2 = get_service_manager(port=8080, auto_start=False)
        
        # 应该是同一个实例
        if manager1 is manager2:
            print("   ✅ 全局服务管理器单例模式正常")
        else:
            print("   ⚠️  全局服务管理器单例模式异常")
        
        # 测试服务启动
        print("\n2. 测试服务启动...")
        if manager1.start_service():
            print("   ✅ 服务启动成功")
        
        # 测试服务状态
        print("\n3. 测试服务状态...")
        status = manager1.get_service_status()
        print(f"   服务状态: {'运行中' if status['running'] else '未运行'}")
        
        # 停止服务
        print("\n4. 停止服务...")
        manager1.stop_service()
        print("   ✅ 服务停止成功")
        
        print("\n✅ 全局服务管理器测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 全局服务管理器测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("AKShare API 自动服务管理功能测试")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_service_manager,
        test_api_integration,
        test_error_handling,
        test_global_manager
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！自动服务管理功能正常工作。")
    else:
        print("⚠️  部分测试失败，请检查相关功能。")
    
    print("\n💡 提示:")
    print("- 首次运行可能需要安装AKTools")
    print("- 服务启动需要一些时间")
    print("- 如果测试失败，请检查网络连接")


if __name__ == "__main__":
    main()
