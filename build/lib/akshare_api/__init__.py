# -*- coding: utf-8 -*-
"""
AKShare API调用 - 完整股票数据接口汇总
基于AKShare股票数据接口完整文档编写
包含98个股票相关的数据接口调用方法
支持自动安装和启动AKTools服务
"""

import requests
import pandas as pd
from typing import Optional, Union, Dict, Any
from .service_manager import AKToolsServiceManager, ensure_service_running


class AKShareAPIError(Exception):
    """AKShare API异常类"""
    pass


class AKShareAPI:
    """AKShare API客户端类"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8080", auto_start_service: bool = True):
        """
        初始化AKShare API客户端
        
        Args:
            base_url: API基础URL，默认为本地AKTools服务
            auto_start_service: 是否自动启动AKTools服务
        """
        self.base_url = base_url.rstrip('/')
        self.auto_start_service = auto_start_service
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AKShare-API/1.0.0',
            'Accept': 'application/json',
        })
        
        # 如果启用自动服务管理，确保服务正在运行
        if auto_start_service and self.base_url.startswith("http://127.0.0.1"):
            port = int(self.base_url.split(':')[-1]) if ':' in self.base_url else 8080
            ensure_service_running(port=port)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        发起API请求
        
        Args:
            endpoint: API端点
            params: 请求参数
            
        Returns:
            pandas.DataFrame: 返回的数据
            
        Raises:
            AKShareAPIError: API请求失败时抛出异常
        """
        url = f"{self.base_url}/api/public/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                return pd.DataFrame()
                
            return pd.DataFrame(data)
            
        except requests.exceptions.ConnectionError as e:
            # 如果是连接错误且启用了自动服务管理，尝试重启服务
            if self.auto_start_service and self.base_url.startswith("http://127.0.0.1"):
                print("⚠️  检测到服务连接失败，正在尝试重启AKTools服务...")
                port = int(self.base_url.split(':')[-1]) if ':' in self.base_url else 8080
                if ensure_service_running(port=port):
                    print("✅ 服务重启成功，正在重试请求...")
                    # 重试请求
                    try:
                        response = self.session.get(url, params=params, timeout=30)
                        response.raise_for_status()
                        data = response.json()
                        return pd.DataFrame(data) if data else pd.DataFrame()
                    except Exception as retry_e:
                        raise AKShareAPIError(f"重试请求失败: {retry_e}")
                else:
                    raise AKShareAPIError(f"无法启动AKTools服务，请手动检查: {e}")
            else:
                raise AKShareAPIError(f"API连接失败: {e}")
        except requests.exceptions.RequestException as e:
            raise AKShareAPIError(f"API请求失败: {e}")
        except Exception as e:
            raise AKShareAPIError(f"数据处理失败: {e}")
    
    def get_service_status(self) -> dict:
        """获取AKTools服务状态"""
        from .service_manager import get_service_manager
        port = int(self.base_url.split(':')[-1]) if ':' in self.base_url else 8080
        manager = get_service_manager(port=port, auto_start=False)
        return manager.get_service_status()
    
    def restart_service(self) -> bool:
        """重启AKTools服务"""
        from .service_manager import get_service_manager
        port = int(self.base_url.split(':')[-1]) if ':' in self.base_url else 8080
        manager = get_service_manager(port=port, auto_start=False)
        return manager.restart_service()
    
    def stop_service(self):
        """停止AKTools服务"""
        from .service_manager import get_service_manager
        port = int(self.base_url.split(':')[-1]) if ':' in self.base_url else 8080
        manager = get_service_manager(port=port, auto_start=False)
        manager.stop_service()
    
    # =============================================================================
    # 1. A股数据接口 (47个)
    # =============================================================================
    
    # 1.1 股票市场总貌 (5个)
    def stock_sse_summary(self) -> pd.DataFrame:
        """获取上海证券交易所总貌数据"""
        return self._make_request("stock_sse_summary")
    
    def stock_szse_summary(self) -> pd.DataFrame:
        """获取深圳证券交易所总貌数据"""
        return self._make_request("stock_szse_summary")
    
    def stock_szse_area_summary(self) -> pd.DataFrame:
        """获取深圳证券交易所地区交易排序数据"""
        return self._make_request("stock_szse_area_summary")
    
    def stock_szse_sector_summary(self, symbol: str = "当年") -> pd.DataFrame:
        """获取深圳证券交易所股票行业成交数据"""
        return self._make_request("stock_szse_sector_summary", {"symbol": symbol})
    
    def stock_sse_deal_daily(self) -> pd.DataFrame:
        """获取上海证券交易所每日概况数据"""
        return self._make_request("stock_sse_deal_daily")
    
    # 1.2 个股信息查询 (2个)
    def stock_individual_info_em(self, symbol: str) -> pd.DataFrame:
        """获取个股信息查询-东方财富"""
        return self._make_request("stock_individual_info_em", {"symbol": symbol})
    
    def stock_individual_basic_info_xq(self, symbol: str) -> pd.DataFrame:
        """获取个股信息查询-雪球"""
        return self._make_request("stock_individual_basic_info_xq", {"symbol": symbol})
    
    # 1.3 行情报价 (1个)
    def stock_bid_ask_em(self, symbol: str) -> pd.DataFrame:
        """获取行情报价-东方财富"""
        return self._make_request("stock_bid_ask_em", {"symbol": symbol})
    
    # 1.4 实时行情数据 (10个)
    def stock_zh_a_spot_em(self) -> pd.DataFrame:
        """获取沪深京A股实时行情-东方财富"""
        return self._make_request("stock_zh_a_spot_em")
    
    def stock_sh_a_spot_em(self) -> pd.DataFrame:
        """获取沪A股实时行情-东方财富"""
        return self._make_request("stock_sh_a_spot_em")
    
    def stock_sz_a_spot_em(self) -> pd.DataFrame:
        """获取深A股实时行情-东方财富"""
        return self._make_request("stock_sz_a_spot_em")
    
    def stock_bj_a_spot_em(self) -> pd.DataFrame:
        """获取京A股实时行情-东方财富"""
        return self._make_request("stock_bj_a_spot_em")
    
    def stock_new_a_spot_em(self) -> pd.DataFrame:
        """获取新股实时行情-东方财富"""
        return self._make_request("stock_new_a_spot_em")
    
    def stock_cy_a_spot_em(self) -> pd.DataFrame:
        """获取创业板实时行情-东方财富"""
        return self._make_request("stock_cy_a_spot_em")
    
    def stock_kc_a_spot_em(self) -> pd.DataFrame:
        """获取科创板实时行情-东方财富"""
        return self._make_request("stock_kc_a_spot_em")
    
    def stock_zh_ab_comparison_em(self) -> pd.DataFrame:
        """获取AB股比价-东方财富"""
        return self._make_request("stock_zh_ab_comparison_em")
    
    def stock_zh_a_spot(self) -> pd.DataFrame:
        """获取沪深京A股实时行情-新浪"""
        return self._make_request("stock_zh_a_spot")
    
    def stock_individual_spot_xq(self, symbol: str) -> pd.DataFrame:
        """获取个股实时行情-雪球"""
        return self._make_request("stock_individual_spot_xq", {"symbol": symbol})
    
    # 1.5 历史行情数据 (3个)
    def stock_zh_a_hist(self, symbol: str, period: str = "daily", 
                       start_date: str = "20210301", end_date: str = "20210616", 
                       adjust: str = "", timeout: Optional[int] = None) -> pd.DataFrame:
        """获取历史行情数据-东方财富"""
        params = {
            "symbol": symbol,
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust,
        }
        if timeout is not None:
            params["timeout"] = timeout
        return self._make_request("stock_zh_a_hist", params)
    
    def stock_zh_a_daily(self, symbol: str, start_date: str = "20201103", 
                        end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取历史行情数据-新浪"""
        return self._make_request("stock_zh_a_daily", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_zh_a_hist_tx(self, symbol: str, start_date: str = "20201103", 
                          end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取历史行情数据-腾讯"""
        return self._make_request("stock_zh_a_hist_tx", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    # 1.6 分时数据 (5个)
    def stock_zh_a_minute(self, symbol: str, period: str = "1", adjust: str = "") -> pd.DataFrame:
        """获取分时数据-新浪"""
        return self._make_request("stock_zh_a_minute", {
            "symbol": symbol,
            "period": period,
            "adjust": adjust
        })
    
    def stock_zh_a_hist_min_em(self, symbol: str, period: str = "1", 
                              start_date: str = "2021-09-01 09:30:00", 
                              end_date: str = "2021-09-01 15:00:00", 
                              adjust: str = "") -> pd.DataFrame:
        """获取分时数据-东方财富"""
        return self._make_request("stock_zh_a_hist_min_em", {
            "symbol": symbol,
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_intraday_em(self, symbol: str) -> pd.DataFrame:
        """获取日内分时数据-东方财富"""
        return self._make_request("stock_intraday_em", {"symbol": symbol})
    
    def stock_intraday_sina(self, symbol: str) -> pd.DataFrame:
        """获取日内分时数据-新浪"""
        return self._make_request("stock_intraday_sina", {"symbol": symbol})
    
    def stock_zh_a_hist_pre_min_em(self, symbol: str) -> pd.DataFrame:
        """获取盘前数据-东方财富"""
        return self._make_request("stock_zh_a_hist_pre_min_em", {"symbol": symbol})
    
    # 1.7 历史分笔数据 (1个)
    def stock_zh_a_tick_tx(self, symbol: str, trade_date: str = "20210316") -> pd.DataFrame:
        """获取历史分笔数据-腾讯"""
        return self._make_request("stock_zh_a_tick_tx", {
            "symbol": symbol,
            "trade_date": trade_date
        })
    
    # 1.8 其他A股相关接口 (20个)
    def stock_zh_growth_comparison_em(self, symbol: str) -> pd.DataFrame:
        """获取股票成长性比较-东方财富"""
        return self._make_request("stock_zh_growth_comparison_em", {"symbol": symbol})
    
    def stock_zh_valuation_comparison_em(self, symbol: str) -> pd.DataFrame:
        """获取股票估值比较-东方财富"""
        return self._make_request("stock_zh_valuation_comparison_em", {"symbol": symbol})
    
    def stock_zh_dupont_comparison_em(self, symbol: str) -> pd.DataFrame:
        """获取股票杜邦分析比较-东方财富"""
        return self._make_request("stock_zh_dupont_comparison_em", {"symbol": symbol})
    
    def stock_zh_scale_comparison_em(self, symbol: str) -> pd.DataFrame:
        """获取股票规模比较-东方财富"""
        return self._make_request("stock_zh_scale_comparison_em", {"symbol": symbol})
    
    def stock_zh_a_cdr_daily(self, symbol: str, start_date: str = "20201103", 
                            end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取CDR历史数据-新浪"""
        return self._make_request("stock_zh_a_cdr_daily", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_financial_abstract(self, symbol: str) -> pd.DataFrame:
        """获取财务报表数据"""
        return self._make_request("stock_financial_abstract", {"symbol": symbol})
    
    def stock_financial_analysis_indicator(self, symbol: str) -> pd.DataFrame:
        """获取财务指标数据"""
        return self._make_request("stock_financial_analysis_indicator", {"symbol": symbol})
    
    def stock_yjbb_em(self, date: str = "20220331") -> pd.DataFrame:
        """获取业绩报表数据"""
        return self._make_request("stock_yjbb_em", {"date": date})
    
    def stock_hsgt_fund_flow_summary_em(self) -> pd.DataFrame:
        """获取沪深港通资金流向"""
        return self._make_request("stock_hsgt_fund_flow_summary_em")
    
    def stock_individual_fund_flow_rank(self) -> pd.DataFrame:
        """获取个股资金流向"""
        return self._make_request("stock_individual_fund_flow_rank")
    
    def stock_profit_forecast_em(self) -> pd.DataFrame:
        """获取东方财富盈利预测"""
        return self._make_request("stock_profit_forecast_em")
    
    def stock_profit_forecast_ths(self) -> pd.DataFrame:
        """获取同花顺盈利预测"""
        return self._make_request("stock_profit_forecast_ths")
    
    def stock_board_concept_cons_ths(self) -> pd.DataFrame:
        """获取同花顺概念板块指数"""
        return self._make_request("stock_board_concept_cons_ths")
    
    def stock_board_concept_name_em(self) -> pd.DataFrame:
        """获取东方财富概念板块"""
        return self._make_request("stock_board_concept_name_em")
    
    def stock_board_concept_hist_em(self, symbol: str, period: str = "daily", 
                                   start_date: str = "20220101", 
                                   end_date: str = "20250227", 
                                   adjust: str = "") -> pd.DataFrame:
        """获取概念板块历史行情"""
        return self._make_request("stock_board_concept_hist_em", {
            "symbol": symbol,
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_board_industry_name_ths(self) -> pd.DataFrame:
        """获取同花顺行业一览表"""
        return self._make_request("stock_board_industry_name_ths")
    
    def stock_board_industry_name_em(self) -> pd.DataFrame:
        """获取东方财富行业板块"""
        return self._make_request("stock_board_industry_name_em")
    
    def stock_hot_rank_em(self) -> pd.DataFrame:
        """获取股票热度排行"""
        return self._make_request("stock_hot_rank_em")
    
    def stock_market_activity_em(self) -> pd.DataFrame:
        """获取盘口异动数据"""
        return self._make_request("stock_market_activity_em")
    
    def stock_board_change_em(self) -> pd.DataFrame:
        """获取板块异动详情"""
        return self._make_request("stock_board_change_em")
    
    # =============================================================================
    # 2. B股数据接口 (4个)
    # =============================================================================
    
    def stock_zh_b_spot_em(self) -> pd.DataFrame:
        """获取B股实时行情-东方财富"""
        return self._make_request("stock_zh_b_spot_em")
    
    def stock_zh_b_spot(self) -> pd.DataFrame:
        """获取B股实时行情-新浪"""
        return self._make_request("stock_zh_b_spot")
    
    def stock_zh_b_daily(self, symbol: str, start_date: str = "20201103", 
                        end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取B股历史行情数据-新浪"""
        return self._make_request("stock_zh_b_daily", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_zh_b_minute(self, symbol: str, period: str = "1", adjust: str = "") -> pd.DataFrame:
        """获取B股分时数据-新浪"""
        return self._make_request("stock_zh_b_minute", {
            "symbol": symbol,
            "period": period,
            "adjust": adjust
        })
    
    # =============================================================================
    # 3. 港股数据接口 (3个)
    # =============================================================================
    
    def stock_hk_spot_em(self) -> pd.DataFrame:
        """获取港股实时行情-东方财富"""
        return self._make_request("stock_hk_spot_em")
    
    def stock_hk_spot(self) -> pd.DataFrame:
        """获取港股实时行情-新浪"""
        return self._make_request("stock_hk_spot")
    
    def stock_hk_daily(self, symbol: str, start_date: str = "20201103", 
                      end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取港股历史行情数据-新浪"""
        return self._make_request("stock_hk_daily", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    # =============================================================================
    # 4. 美股数据接口 (3个)
    # =============================================================================
    
    def stock_us_spot(self) -> pd.DataFrame:
        """获取美股实时行情-新浪"""
        return self._make_request("stock_us_spot")
    
    def stock_us_spot_em(self) -> pd.DataFrame:
        """获取美股实时行情-东方财富"""
        return self._make_request("stock_us_spot_em")
    
    def stock_us_daily(self, symbol: str, start_date: str = "20201103", 
                      end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
        """获取美股历史行情数据-新浪"""
        return self._make_request("stock_us_daily", {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    # =============================================================================
    # 5. 高级功能接口 (36个)
    # =============================================================================
    
    # 5.1 涨停板行情接口 (3个)
    def stock_zt_pool_em(self) -> pd.DataFrame:
        """获取涨停股池"""
        return self._make_request("stock_zt_pool_em")
    
    def stock_zt_pool_previous_em(self) -> pd.DataFrame:
        """获取昨日涨停股池"""
        return self._make_request("stock_zt_pool_previous_em")
    
    def stock_dt_pool_em(self) -> pd.DataFrame:
        """获取跌停股池"""
        return self._make_request("stock_dt_pool_em")
    
    # 5.2 龙虎榜接口 (2个)
    def stock_lhb_detail_em(self, start_date: str = "20230403", 
                           end_date: str = "20230417") -> pd.DataFrame:
        """获取龙虎榜详情"""
        return self._make_request("stock_lhb_detail_em", {
            "start_date": start_date,
            "end_date": end_date
        })
    
    def stock_lhb_stock_statistic_em(self) -> pd.DataFrame:
        """获取个股上榜统计"""
        return self._make_request("stock_lhb_stock_statistic_em")
    
    # 5.3 机构相关接口 (5个)
    def stock_institute_visit_em(self) -> pd.DataFrame:
        """获取机构调研统计"""
        return self._make_request("stock_institute_visit_em")
    
    def stock_institute_visit_detail_em(self) -> pd.DataFrame:
        """获取机构调研详细"""
        return self._make_request("stock_institute_visit_detail_em")
    
    def stock_institute_hold_detail(self, stock: str, quarter: str) -> pd.DataFrame:
        """获取机构持股详情"""
        return self._make_request("stock_institute_hold_detail", {
            "stock": stock,
            "quarter": quarter
        })
    
    def stock_institute_recommend(self, symbol: str) -> pd.DataFrame:
        """获取机构推荐池"""
        return self._make_request("stock_institute_recommend", {"symbol": symbol})
    
    def stock_institute_recommend_detail(self, symbol: str) -> pd.DataFrame:
        """获取股票评级记录"""
        return self._make_request("stock_institute_recommend_detail", {"symbol": symbol})
    
    # 5.4 研报资讯接口 (6个)
    def stock_research_report_em(self, symbol: str) -> pd.DataFrame:
        """获取个股研报"""
        return self._make_request("stock_research_report_em", {"symbol": symbol})
    
    def stock_info_cjzc_em(self) -> pd.DataFrame:
        """获取财经早餐"""
        return self._make_request("stock_info_cjzc_em")
    
    def stock_info_global_em(self) -> pd.DataFrame:
        """获取全球财经快讯-东方财富"""
        return self._make_request("stock_info_global_em")
    
    def stock_info_global_sina(self) -> pd.DataFrame:
        """获取全球财经快讯-新浪财经"""
        return self._make_request("stock_info_global_sina")
    
    def stock_news_em(self, symbol: str) -> pd.DataFrame:
        """获取个股新闻-东方财富"""
        return self._make_request("stock_news_em", {"symbol": symbol})
    
    def stock_news_main_cx(self) -> pd.DataFrame:
        """获取财经内容精选-财新网"""
        return self._make_request("stock_news_main_cx")
    
    # 5.5 互动易接口 (3个)
    def stock_irm_cninfo(self, symbol: str) -> pd.DataFrame:
        """获取互动易-提问"""
        return self._make_request("stock_irm_cninfo", {"symbol": symbol})
    
    def stock_irm_ans_cninfo(self, symbol: str) -> pd.DataFrame:
        """获取互动易-回答"""
        return self._make_request("stock_irm_ans_cninfo", {"symbol": symbol})
    
    def stock_sns_sseinfo(self, symbol: str) -> pd.DataFrame:
        """获取上证e互动"""
        return self._make_request("stock_sns_sseinfo", {"symbol": symbol})
    
    # 5.6 其他高级功能接口 (17个)
    def stock_zyjs_ths(self, symbol: str) -> pd.DataFrame:
        """获取主营介绍-同花顺"""
        return self._make_request("stock_zyjs_ths", {"symbol": symbol})
    
    def stock_zygc_em(self, symbol: str) -> pd.DataFrame:
        """获取主营构成-东方财富"""
        return self._make_request("stock_zygc_em", {"symbol": symbol})
    
    def stock_gsrl_gsdt_em(self, date: str) -> pd.DataFrame:
        """获取公司动态-东方财富"""
        return self._make_request("stock_gsrl_gsdt_em", {"date": date})
    
    def stock_dividend_cninfo(self, symbol: str) -> pd.DataFrame:
        """获取历史分红-巨潮资讯"""
        return self._make_request("stock_dividend_cninfo", {"symbol": symbol})
    
    def stock_financial_report_sina(self, stock: str, indicator: str) -> pd.DataFrame:
        """获取财务报表-新浪"""
        return self._make_request("stock_financial_report_sina", {
            "stock": stock,
            "indicator": indicator
        })
    
    def stock_yjkb_em(self, date: str) -> pd.DataFrame:
        """获取业绩快报-东方财富"""
        return self._make_request("stock_yjkb_em", {"date": date})
    
    def stock_yjyg_em(self, date: str) -> pd.DataFrame:
        """获取业绩预告-东方财富"""
        return self._make_request("stock_yjyg_em", {"date": date})
    
    def stock_yysj_em(self, symbol: str, date: str) -> pd.DataFrame:
        """获取预约披露时间-东方财富"""
        return self._make_request("stock_yysj_em", {
            "symbol": symbol,
            "date": date
        })
    
    def stock_board_concept_cons_em(self, symbol: str) -> pd.DataFrame:
        """获取概念板块成分股-东方财富"""
        return self._make_request("stock_board_concept_cons_em", {"symbol": symbol})
    
    def stock_board_industry_cons_em(self, symbol: str) -> pd.DataFrame:
        """获取行业板块成分股-东方财富"""
        return self._make_request("stock_board_industry_cons_em", {"symbol": symbol})
    
    def stock_board_industry_hist_em(self, symbol: str, period: str = "daily", 
                                    start_date: str = "20220101", 
                                    end_date: str = "20250227", 
                                    adjust: str = "") -> pd.DataFrame:
        """获取行业板块指数-东方财富"""
        return self._make_request("stock_board_industry_hist_em", {
            "symbol": symbol,
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "adjust": adjust
        })
    
    def stock_hot_follow_xq(self, symbol: str) -> pd.DataFrame:
        """获取股票热度-雪球关注排行榜"""
        return self._make_request("stock_hot_follow_xq", {"symbol": symbol})
    
    def stock_hot_rank_detail_em(self, symbol: str) -> pd.DataFrame:
        """获取历史趋势及粉丝特征-东方财富"""
        return self._make_request("stock_hot_rank_detail_em", {"symbol": symbol})
    
    def stock_hot_rank_detail_xq(self, symbol: str) -> pd.DataFrame:
        """获取个股人气榜-实时变动"""
        return self._make_request("stock_hot_rank_detail_xq", {"symbol": symbol})
    
    def stock_hot_rank_latest_em(self) -> pd.DataFrame:
        """获取个股人气榜-最新排名"""
        return self._make_request("stock_hot_rank_latest_em")
    
    def stock_hot_keyword_em(self) -> pd.DataFrame:
        """获取热门关键词-东方财富"""
        return self._make_request("stock_hot_keyword_em")
    
    def stock_hot_search_em(self) -> pd.DataFrame:
        """获取热搜股票-东方财富"""
        return self._make_request("stock_hot_search_em")
    
    def stock_hot_related_em(self, symbol: str) -> pd.DataFrame:
        """获取相关股票-东方财富"""
        return self._make_request("stock_hot_related_em", {"symbol": symbol})


# 创建全局实例
api = AKShareAPI()

# 为了向后兼容，提供函数式接口
def stock_sse_summary() -> pd.DataFrame:
    """获取上海证券交易所总貌数据"""
    return api.stock_sse_summary()

def stock_szse_summary() -> pd.DataFrame:
    """获取深圳证券交易所总貌数据"""
    return api.stock_szse_summary()

def stock_szse_area_summary() -> pd.DataFrame:
    """获取深圳证券交易所地区交易排序数据"""
    return api.stock_szse_area_summary()

def stock_szse_sector_summary(symbol: str = "当年") -> pd.DataFrame:
    """获取深圳证券交易所股票行业成交数据"""
    return api.stock_szse_sector_summary(symbol)

def stock_sse_deal_daily() -> pd.DataFrame:
    """获取上海证券交易所每日概况数据"""
    return api.stock_sse_deal_daily()

def stock_individual_info_em(symbol: str) -> pd.DataFrame:
    """获取个股信息查询-东方财富"""
    return api.stock_individual_info_em(symbol)

def stock_individual_basic_info_xq(symbol: str) -> pd.DataFrame:
    """获取个股信息查询-雪球"""
    return api.stock_individual_basic_info_xq(symbol)

def stock_bid_ask_em(symbol: str) -> pd.DataFrame:
    """获取行情报价-东方财富"""
    return api.stock_bid_ask_em(symbol)

def stock_zh_a_spot_em() -> pd.DataFrame:
    """获取沪深京A股实时行情-东方财富"""
    return api.stock_zh_a_spot_em()

def stock_sh_a_spot_em() -> pd.DataFrame:
    """获取沪A股实时行情-东方财富"""
    return api.stock_sh_a_spot_em()

def stock_sz_a_spot_em() -> pd.DataFrame:
    """获取深A股实时行情-东方财富"""
    return api.stock_sz_a_spot_em()

def stock_bj_a_spot_em() -> pd.DataFrame:
    """获取京A股实时行情-东方财富"""
    return api.stock_bj_a_spot_em()

def stock_new_a_spot_em() -> pd.DataFrame:
    """获取新股实时行情-东方财富"""
    return api.stock_new_a_spot_em()

def stock_cy_a_spot_em() -> pd.DataFrame:
    """获取创业板实时行情-东方财富"""
    return api.stock_cy_a_spot_em()

def stock_kc_a_spot_em() -> pd.DataFrame:
    """获取科创板实时行情-东方财富"""
    return api.stock_kc_a_spot_em()

def stock_zh_ab_comparison_em() -> pd.DataFrame:
    """获取AB股比价-东方财富"""
    return api.stock_zh_ab_comparison_em()

def stock_zh_a_spot() -> pd.DataFrame:
    """获取沪深京A股实时行情-新浪"""
    return api.stock_zh_a_spot()

def stock_individual_spot_xq(symbol: str) -> pd.DataFrame:
    """获取个股实时行情-雪球"""
    return api.stock_individual_spot_xq(symbol)

def stock_zh_a_hist(symbol: str, period: str = "daily", 
                   start_date: str = "20210301", end_date: str = "20210616", 
                   adjust: str = "", timeout: Optional[int] = None) -> pd.DataFrame:
    """获取历史行情数据-东方财富"""
    return api.stock_zh_a_hist(symbol, period, start_date, end_date, adjust, timeout)

def stock_zh_a_daily(symbol: str, start_date: str = "20201103", 
                    end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
    """获取历史行情数据-新浪"""
    return api.stock_zh_a_daily(symbol, start_date, end_date, adjust)

def stock_zh_a_hist_tx(symbol: str, start_date: str = "20201103", 
                      end_date: str = "20201116", adjust: str = "") -> pd.DataFrame:
    """获取历史行情数据-腾讯"""
    return api.stock_zh_a_hist_tx(symbol, start_date, end_date, adjust)

def stock_zh_a_minute(symbol: str, period: str = "1", adjust: str = "") -> pd.DataFrame:
    """获取分时数据-新浪"""
    return api.stock_zh_a_minute(symbol, period, adjust)

def stock_zh_a_hist_min_em(symbol: str, period: str = "1", 
                          start_date: str = "2021-09-01 09:30:00", 
                          end_date: str = "2021-09-01 15:00:00", 
                          adjust: str = "") -> pd.DataFrame:
    """获取分时数据-东方财富"""
    return api.stock_zh_a_hist_min_em(symbol, period, start_date, end_date, adjust)

def stock_intraday_em(symbol: str) -> pd.DataFrame:
    """获取日内分时数据-东方财富"""
    return api.stock_intraday_em(symbol)

def stock_intraday_sina(symbol: str) -> pd.DataFrame:
    """获取日内分时数据-新浪"""
    return api.stock_intraday_sina(symbol)

def stock_zh_a_hist_pre_min_em(symbol: str) -> pd.DataFrame:
    """获取盘前数据-东方财富"""
    return api.stock_zh_a_hist_pre_min_em(symbol)

def stock_zh_a_tick_tx(symbol: str, trade_date: str = "20210316") -> pd.DataFrame:
    """获取历史分笔数据-腾讯"""
    return api.stock_zh_a_tick_tx(symbol, trade_date)

# 导出所有函数和类
__all__ = [
    'AKShareAPI',
    'AKShareAPIError',
    'api',
    # A股数据接口
    'stock_sse_summary',
    'stock_szse_summary',
    'stock_szse_area_summary',
    'stock_szse_sector_summary',
    'stock_sse_deal_daily',
    'stock_individual_info_em',
    'stock_individual_basic_info_xq',
    'stock_bid_ask_em',
    'stock_zh_a_spot_em',
    'stock_sh_a_spot_em',
    'stock_sz_a_spot_em',
    'stock_bj_a_spot_em',
    'stock_new_a_spot_em',
    'stock_cy_a_spot_em',
    'stock_kc_a_spot_em',
    'stock_zh_ab_comparison_em',
    'stock_zh_a_spot',
    'stock_individual_spot_xq',
    'stock_zh_a_hist',
    'stock_zh_a_daily',
    'stock_zh_a_hist_tx',
    'stock_zh_a_minute',
    'stock_zh_a_hist_min_em',
    'stock_intraday_em',
    'stock_intraday_sina',
    'stock_zh_a_hist_pre_min_em',
    'stock_zh_a_tick_tx',
    # B股数据接口
    'stock_zh_b_spot_em',
    'stock_zh_b_spot',
    'stock_zh_b_daily',
    'stock_zh_b_minute',
    # 港股数据接口
    'stock_hk_spot_em',
    'stock_hk_spot',
    'stock_hk_daily',
    # 美股数据接口
    'stock_us_spot',
    'stock_us_spot_em',
    'stock_us_daily',
    # 高级功能接口
    'stock_zt_pool_em',
    'stock_zt_pool_previous_em',
    'stock_dt_pool_em',
    'stock_lhb_detail_em',
    'stock_lhb_stock_statistic_em',
    'stock_institute_visit_em',
    'stock_institute_visit_detail_em',
    'stock_institute_hold_detail',
    'stock_institute_recommend',
    'stock_institute_recommend_detail',
    'stock_research_report_em',
    'stock_info_cjzc_em',
    'stock_info_global_em',
    'stock_info_global_sina',
    'stock_news_em',
    'stock_news_main_cx',
    'stock_irm_cninfo',
    'stock_irm_ans_cninfo',
    'stock_sns_sseinfo',
    'stock_zyjs_ths',
    'stock_zygc_em',
    'stock_gsrl_gsdt_em',
    'stock_dividend_cninfo',
    'stock_financial_report_sina',
    'stock_yjkb_em',
    'stock_yjyg_em',
    'stock_yysj_em',
    'stock_board_concept_cons_em',
    'stock_board_industry_cons_em',
    'stock_board_industry_hist_em',
    'stock_hot_follow_xq',
    'stock_hot_rank_detail_em',
    'stock_hot_rank_detail_xq',
    'stock_hot_rank_latest_em',
    'stock_hot_keyword_em',
    'stock_hot_search_em',
    'stock_hot_related_em',
    'stock_zh_growth_comparison_em',
    'stock_zh_valuation_comparison_em',
    'stock_zh_dupont_comparison_em',
    'stock_zh_scale_comparison_em',
    'stock_zh_a_cdr_daily',
    'stock_financial_abstract',
    'stock_financial_analysis_indicator',
    'stock_hsgt_fund_flow_summary_em',
    'stock_individual_fund_flow_rank',
    'stock_profit_forecast_em',
    'stock_profit_forecast_ths',
    'stock_board_concept_cons_ths',
    'stock_board_concept_name_em',
    'stock_board_concept_hist_em',
    'stock_board_industry_name_ths',
    'stock_board_industry_name_em',
    'stock_hot_rank_em',
    'stock_market_activity_em',
    'stock_board_change_em',
]
