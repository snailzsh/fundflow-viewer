import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

def get_fund_flow_data(period='today'):
    """
    获取东方财富网行业资金流向数据
    period: 'today' - 今日排行, '5day' - 5日排行, '10day' - 10日排行
    """
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    
    # 根据不同时间段设置不同参数
    if period == 'today':
        sort_field = 'f62'  # 今日主力净流入
        period_name = "今日排行"
    elif period == '5day':
        sort_field = 'f164'  # 5日主力净流入
        period_name = "5日排行"
    elif period == '10day':
        sort_field = 'f174'  # 10日主力净流入
        period_name = "10日排行"
    else:
        raise ValueError("period must be one of 'today', '5day', '10day'")
    
    params = {
        'pn': 1,  # 页码
        'pz': 20,  # 每页数量，获取前20名
        'po': 1,  # 按净流入降序排序
        'np': 1,
        'ut': 'b2884a393a59ad64002292a3e90d46a5',
        'fltt': 2,
        'invt': 2,
        'fid': sort_field,
        'fs': 'm:90+t:2',  # 行业板块
        'fields': 'f1,f2,f3,f12,f13,f14,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f2,f3,f12,f13,f14,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f128,f136,f115,f152,f124,f164,f165,f174,f175,f275,f276,f277,f278,f279,f280,f281,f282'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        if data['data'] and data['data']['diff']:
            result = []
            for i, item in enumerate(data['data']['diff'], 1):
                if period == 'today':
                    main_net_inflow = item['f62']  # 今日主力净流入
                    main_net_inflow_pct = item['f184']  # 今日主力净流入占比
                    super_large_inflow = item['f66']  # 今日超大单净流入
                    super_large_inflow_pct = item['f69']  # 今日超大单净流入占比
                    large_inflow = item['f72']  # 今日大单净流入
                    large_inflow_pct = item['f75']  # 今日大单净流入占比
                    medium_inflow = item['f78']  # 今日中单净流入
                    medium_inflow_pct = item['f81']  # 今日中单净流入占比
                    small_inflow = item['f84']  # 今日小单净流入
                    small_inflow_pct = item['f87']  # 今日小单净流入占比
                elif period == '5day':
                    main_net_inflow = item['f164']  # 5日主力净流入
                    main_net_inflow_pct = item['f165']  # 5日主力净流入占比
                    super_large_inflow = item['f275']  # 5日超大单净流入
                    super_large_inflow_pct = item['f276']  # 5日超大单净流入占比
                    large_inflow = item['f277']  # 5日大单净流入
                    large_inflow_pct = item['f278']  # 5日大单净流入占比
                    medium_inflow = item['f279']  # 5日中单净流入
                    medium_inflow_pct = item['f280']  # 5日中单净流入占比
                    small_inflow = item['f281']  # 5日小单净流入
                    small_inflow_pct = item['f282']  # 5日小单净流入占比
                elif period == '10day':
                    main_net_inflow = item['f174']  # 10日主力净流入
                    main_net_inflow_pct = item['f175']  # 10日主力净流入占比
                    super_large_inflow = 0  # API中没有提供10日超大单数据，用0代替
                    super_large_inflow_pct = 0
                    large_inflow = 0
                    large_inflow_pct = 0
                    medium_inflow = 0
                    medium_inflow_pct = 0
                    small_inflow = 0
                    small_inflow_pct = 0
                
                # 将数值转换为亿元单位，并保留两位小数
                main_net_inflow = round(main_net_inflow / 100000000, 2)
                super_large_inflow = round(super_large_inflow / 100000000, 2)
                large_inflow = round(large_inflow / 100000000, 2)
                medium_inflow = round(medium_inflow / 100000000, 2)
                small_inflow = round(small_inflow / 100000000, 2)
                
                # 获取行业板块代码
                sector_code = item['f12']
                
                # 获取概念资金流和主力净流入最大股
                concept_flow, top_stock = get_sector_detail(sector_code, period)
                
                result.append({
                    '序号': i,
                    '行业板块': item['f14'],  # 行业名称
                    '涨跌幅': round(item['f3'] / 100, 2),  # 涨跌幅
                    '主力净流入': main_net_inflow,
                    '主力净流入占比': round(main_net_inflow_pct / 100, 2),
                    '超大单净流入': super_large_inflow,
                    '超大单净流入占比': round(super_large_inflow_pct / 100, 2),
                    '大单净流入': large_inflow,
                    '大单净流入占比': round(large_inflow_pct / 100, 2),
                    '中单净流入': medium_inflow,
                    '中单净流入占比': round(medium_inflow_pct / 100, 2),
                    '小单净流入': small_inflow,
                    '小单净流入占比': round(small_inflow_pct / 100, 2),
                    '概念资金流': concept_flow,
                    '主力净流入最大股': top_stock
                })
            
            return {
                'status': 'success',
                'period': period_name,
                'data': result
            }
        else:
            return {
                'status': 'error',
                'message': '未获取到数据'
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

def get_sector_detail(sector_code, period='today'):
    """
    获取行业板块的概念资金流和主力净流入最大股
    sector_code: 行业板块代码
    period: 'today' - 今日, '5day' - 5日, '10day' - 10日
    """
    try:
        # 获取概念资金流 - 使用行业板块资金流作为概念资金流
        concept_flow = 0
        
        # 获取行业内主力净流入最大股
        top_stock_url = "https://push2.eastmoney.com/api/qt/clist/get"
        
        # 根据不同时间段设置不同参数
        if period == 'today':
            sort_field = 'f62'  # 今日主力净流入
        elif period == '5day':
            sort_field = 'f164'  # 5日主力净流入
        elif period == '10day':
            sort_field = 'f174'  # 10日主力净流入
        
        stock_params = {
            'pn': 1,  # 页码
            'pz': 1,  # 只取第一名
            'po': 1,  # 按净流入降序排序
            'np': 1,
            'ut': 'b2884a393a59ad64002292a3e90d46a5',
            'fltt': 2,
            'invt': 2,
            'fid': sort_field,
            'fs': f'b:{sector_code}+f:!50',  # 按行业板块筛选，排除B股等
            'fields': 'f12,f14,f62'  # 股票代码、名称和主力净流入
        }
        
        stock_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        stock_response = requests.get(top_stock_url, params=stock_params, headers=stock_headers)
        stock_data = stock_response.json()
        
        top_stock = ""
        if stock_data.get('data') and stock_data['data'].get('diff') and len(stock_data['data']['diff']) > 0:
            stock_item = stock_data['data']['diff'][0]
            top_stock = f"{stock_item['f14']}({stock_item['f12']})"
        
        return concept_flow, top_stock
    except Exception as e:
        print(f"获取行业详情出错: {e}")
        return 0, ""

def get_all_fund_flow_data():
    """获取所有时间段的资金流向数据"""
    today_data = get_fund_flow_data('today')
    time.sleep(1)  # 避免请求过于频繁
    five_day_data = get_fund_flow_data('5day')
    time.sleep(1)
    ten_day_data = get_fund_flow_data('10day')
    
    return {
        'today': today_data,
        '5day': five_day_data,
        '10day': ten_day_data
    }

if __name__ == '__main__':
    # 测试
    data = get_all_fund_flow_data()
    print(json.dumps(data, ensure_ascii=False, indent=2)) 