#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台内容采集器
从必应、36kr、百度、知乎采集指定主题的内容
"""

import requests
from urllib.parse import quote
import json
import re
from typing import List, Dict, Optional
import time


class ContentCollector:
    """多平台内容采集器"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def collect_from_bing(self, topic: str, count: int = 5) -> List[Dict]:
        """
        从必应搜索采集内容
        注意：实际使用中可能需要使用Bing Search API
        """
        results = []
        try:
            # 使用必应搜索页面（简化版本，实际可能需要API）
            search_url = f"https://www.bing.com/search?q={quote(topic)}&first=1&count={count}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # 简单的结果提取（实际解析需要根据页面结构调整）
            # 这里仅提供框架，真实场景建议使用官方API
            print(f"[必应] 已搜索主题: {topic}")
            print(f"[必应] 搜索URL: {search_url}")
            
            # 模拟返回结果（实际使用时需要解析HTML）
            results.append({
                'platform': '必应',
                'topic': topic,
                'title': f'必应搜索结果: {topic}',
                'url': search_url,
                'snippet': '请查看搜索链接获取详细内容',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            print(f"[必应] 采集失败: {str(e)}")
        
        return results
    
    def collect_from_36kr(self, topic: str, count: int = 5) -> List[Dict]:
        """
        从36kr采集内容
        使用36kr的搜索功能
        """
        results = []
        try:
            # 36kr搜索URL
            search_url = f"https://so.36kr.com?q={quote(topic)}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            print(f"[36kr] 已搜索主题: {topic}")
            print(f"[36kr] 搜索URL: {search_url}")
            
            # 尝试提取部分可见内容
            # 注意：36kr可能有反爬机制，实际使用需要更复杂的处理
            results.append({
                'platform': '36kr',
                'topic': topic,
                'title': f'36kr搜索结果: {topic}',
                'url': search_url,
                'snippet': '请查看搜索链接获取详细内容',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            print(f"[36kr] 采集失败: {str(e)}")
        
        return results
    
    def collect_from_baidu(self, topic: str, count: int = 5) -> List[Dict]:
        """
        从百度搜索采集内容
        注意：百度有严格的反爬机制，建议使用百度API
        """
        results = []
        try:
            search_url = f"https://www.baidu.com/s?wd={quote(topic)}&rn={count}"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            print(f"[百度] 已搜索主题: {topic}")
            print(f"[百度] 搜索URL: {search_url}")
            
            results.append({
                'platform': '百度',
                'topic': topic,
                'title': f'百度搜索结果: {topic}',
                'url': search_url,
                'snippet': '请查看搜索链接获取详细内容',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            print(f"[百度] 采集失败: {str(e)}")
        
        return results
    
    def collect_from_zhihu(self, topic: str, count: int = 5) -> List[Dict]:
        """
        从知乎采集内容
        使用知乎搜索
        """
        results = []
        try:
            # 知乎搜索URL
            search_url = f"https://www.zhihu.com/search?q={quote(topic)}&type=content"
            
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            print(f"[知乎] 已搜索主题: {topic}")
            print(f"[知乎] 搜索URL: {search_url}")
            
            results.append({
                'platform': '知乎',
                'topic': topic,
                'title': f'知乎搜索结果: {topic}',
                'url': search_url,
                'snippet': '请查看搜索链接获取详细内容',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
            
        except Exception as e:
            print(f"[知乎] 采集失败: {str(e)}")
        
        return results
    
    def collect_all(self, topic: str, count: int = 5) -> Dict:
        """
        从所有平台采集内容
        """
        print(f"\n{'='*60}")
        print(f"开始采集主题: {topic}")
        print(f"{'='*60}\n")
        
        all_results = {
            'topic': topic,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'results': {}
        }
        
        # 依次从各平台采集
        all_results['results']['bing'] = self.collect_from_bing(topic, count)
        time.sleep(1)  # 避免请求过快
        
        all_results['results']['36kr'] = self.collect_from_36kr(topic, count)
        time.sleep(1)
        
        all_results['results']['baidu'] = self.collect_from_baidu(topic, count)
        time.sleep(1)
        
        all_results['results']['zhihu'] = self.collect_from_zhihu(topic, count)
        
        print(f"\n{'='*60}")
        print("采集完成!")
        print(f"{'='*60}\n")
        
        return all_results
    
    def save_results(self, results: Dict, filename: str = 'collection_results.json'):
        """保存采集结果到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到: {filename}")
        except Exception as e:
            print(f"保存失败: {str(e)}")
    
    def display_results(self, results: Dict):
        """显示采集结果"""
        print("\n" + "="*60)
        print("采集结果概览")
        print("="*60)
        
        for platform, data in results['results'].items():
            print(f"\n【{platform.upper()}】")
            for item in data:
                print(f"  标题: {item['title']}")
                print(f"  链接: {item['url']}")
                print(f"  时间: {item['timestamp']}")
                print("-" * 40)


def main():
    """主函数"""
    collector = ContentCollector()
    
    # 获取用户输入的主题（支持命令行参数）
    import sys
    
    if len(sys.argv) > 1:
        topic = sys.argv[1].strip()
    else:
        topic = input("请输入要采集的主题: ").strip()
    
    if not topic:
        print("主题不能为空!")
        return
    
    # 获取结果数量
    if len(sys.argv) > 2:
        try:
            count = int(sys.argv[2])
        except ValueError:
            count = 5
    else:
        try:
            count = int(input("请输入每个平台期望的结果数量 (默认5): ").strip() or "5")
        except (ValueError, EOFError):
            count = 5
    
    # 执行采集
    results = collector.collect_all(topic, count)
    
    # 显示结果
    collector.display_results(results)
    
    # 保存结果
    save_filename = f"collection_{topic}_{time.strftime('%Y%m%d_%H%M%S')}.json"
    collector.save_results(results, save_filename)
    
    print("\n提示:")
    print("1. 由于各平台的反爬机制，本脚本主要提供搜索链接")
    print("2. 如需获取详细内容，建议访问对应链接或使用官方API")
    print("3. 请遵守各平台的使用条款和robots.txt协议")


if __name__ == "__main__":
    main()
