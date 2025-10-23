#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API 测试文件
"""

import pytest
import pandas as pd
from akshare_api import (
    AKShareAPI,
    AKShareAPIError,
    stock_zh_a_spot_em,
    stock_sse_summary,
    stock_zt_pool_em
)


class TestAKShareAPI:
    """AKShare API测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.api = AKShareAPI()
    
    def test_api_initialization(self):
        """测试API初始化"""
        assert self.api.base_url == "http://127.0.0.1:8080"
        assert self.api.session is not None
    
    def test_api_initialization_custom_url(self):
        """测试自定义URL的API初始化"""
        custom_api = AKShareAPI(base_url="http://custom:8080")
        assert custom_api.base_url == "http://custom:8080"
    
    def test_make_request_invalid_endpoint(self):
        """测试无效端点的请求"""
        with pytest.raises(AKShareAPIError):
            self.api._make_request("invalid_endpoint")
    
    def test_make_request_with_params(self):
        """测试带参数的请求"""
        # 这个测试需要实际的API服务运行
        try:
            result = self.api._make_request("stock_sse_summary")
            assert isinstance(result, pd.DataFrame)
        except AKShareAPIError:
            # 如果没有API服务运行，跳过这个测试
            pytest.skip("API服务未运行")


class TestStockFunctions:
    """股票函数测试类"""
    
    def test_stock_zh_a_spot_em(self):
        """测试A股实时行情函数"""
        try:
            result = stock_zh_a_spot_em()
            assert isinstance(result, pd.DataFrame)
        except AKShareAPIError:
            pytest.skip("API服务未运行")
    
    def test_stock_sse_summary(self):
        """测试上交所总貌函数"""
        try:
            result = stock_sse_summary()
            assert isinstance(result, pd.DataFrame)
        except AKShareAPIError:
            pytest.skip("API服务未运行")
    
    def test_stock_zt_pool_em(self):
        """测试涨停股池函数"""
        try:
            result = stock_zt_pool_em()
            assert isinstance(result, pd.DataFrame)
        except AKShareAPIError:
            pytest.skip("API服务未运行")


class TestDataValidation:
    """数据验证测试类"""
    
    def test_dataframe_structure(self):
        """测试DataFrame结构"""
        try:
            data = stock_zh_a_spot_em()
            if not data.empty:
                assert isinstance(data, pd.DataFrame)
                assert len(data) > 0
        except AKShareAPIError:
            pytest.skip("API服务未运行")
    
    def test_data_types(self):
        """测试数据类型"""
        try:
            data = stock_zh_a_spot_em()
            if not data.empty:
                # 检查是否有必要的列
                expected_columns = ['代码', '名称']
                for col in expected_columns:
                    if col in data.columns:
                        assert data[col].dtype == 'object'
        except AKShareAPIError:
            pytest.skip("API服务未运行")


class TestErrorHandling:
    """错误处理测试类"""
    
    def test_api_error_raising(self):
        """测试API错误抛出"""
        api = AKShareAPI()
        
        with pytest.raises(AKShareAPIError):
            api._make_request("nonexistent_endpoint")
    
    def test_invalid_symbol_handling(self):
        """测试无效股票代码处理"""
        api = AKShareAPI()
        
        try:
            # 使用无效的股票代码
            result = api.stock_individual_info_em("INVALID")
            # 应该返回空的DataFrame而不是抛出异常
            assert isinstance(result, pd.DataFrame)
        except AKShareAPIError:
            # 如果API抛出异常，这也是可以接受的
            pass


class TestIntegration:
    """集成测试类"""
    
    def test_multiple_api_calls(self):
        """测试多次API调用"""
        try:
            # 连续调用多个API
            spot_data = stock_zh_a_spot_em()
            sse_data = stock_sse_summary()
            zt_data = stock_zt_pool_em()
            
            # 验证所有调用都返回DataFrame
            assert isinstance(spot_data, pd.DataFrame)
            assert isinstance(sse_data, pd.DataFrame)
            assert isinstance(zt_data, pd.DataFrame)
            
        except AKShareAPIError:
            pytest.skip("API服务未运行")
    
    def test_api_performance(self):
        """测试API性能"""
        import time
        
        try:
            start_time = time.time()
            data = stock_zh_a_spot_em()
            end_time = time.time()
            
            # API调用应该在合理时间内完成（比如30秒内）
            assert end_time - start_time < 30
            
            if not data.empty:
                print(f"API调用耗时: {end_time - start_time:.2f}秒")
                print(f"获取数据量: {len(data)}条")
                
        except AKShareAPIError:
            pytest.skip("API服务未运行")


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
