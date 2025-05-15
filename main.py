import os
import json
import requests
from typing import Dict, List, Any, Optional

# 插件信息
PLUGIN_NAME = "tushare-sina-news"
PLUGIN_VERSION = "1.0.0"
PLUGIN_DESCRIPTION = "Tushare新浪财经新闻API插件，用于获取财经相关新闻内容"

# API配置
TUSHARE_API_URL = "https://api.tushare.pro"
TUSHARE_TOKEN = "YOUR_TUSHARE_TOKEN"  # 在实际使用时替换为环境变量

class TushareSinaNewsPlugin:
    def __init__(self):
        self.token = os.environ.get("TUSHARE_TOKEN", TUSHARE_TOKEN)
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def manifest(self) -> Dict[str, Any]:
        """返回插件清单，描述插件功能和工具"""
        return {
            "name": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "description": PLUGIN_DESCRIPTION,
            "logo": "https://example.com/logo.png",  # 可替换为实际logo URL
            "publisher": "Your Name",
            "contact_email": "your.email@example.com",
            "legal_info_url": "https://example.com/legal",
            
            # 定义工具
            "tools": [
                {
                    "name": "get_sina_news",
                    "description": "获取新浪财经新闻",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "新闻开始日期 (YYYYMMDD格式)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "新闻结束日期 (YYYYMMDD格式)"
                            },
                            "category": {
                                "type": "string",
                                "description": "新闻类别，可选值: 财经, 科技, 社会, 国际等",
                                "default": "财经"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "返回条数限制",
                                "default": 10
                            }
                        },
                        "required": ["start_date"]
                    }
                }
            ]
        }
    
    def get_sina_news(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        获取新浪财经新闻
        
        Args:
            params: 包含查询参数的字典
                - start_date: 开始日期 (YYYYMMDD)
                - end_date: 结束日期 (YYYYMMDD) (可选)
                - category: 新闻类别 (可选)
                - limit: 返回条数 (可选)
                
        Returns:
            包含新闻列表的结果字典
        """
        try:
            # 准备API请求参数
            request_params = {
                "api_name": "news_sina",
                "token": self.token,
                "params": {
                    "start_date": params.get("start_date"),
                    "end_date": params.get("end_date", params.get("start_date")),
                    "src": params.get("category", "财经")
                },
                "fields": "title,content,pub_time,author,url"
            }
            
            # 添加限制条数
            limit = params.get("limit", 10)
            
            # 发送API请求
            response = requests.post(
                TUSHARE_API_URL,
                headers=self.headers,
                json=request_params
            )
            
            # 检查响应
            if response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"API请求失败: {response.status_code}",
                    "data": []
                }
            
            # 解析响应
            result = response.json()
            if result.get("code") != 0:
                return {
                    "status": "error",
                    "message": f"API返回错误: {result.get('msg')}",
                    "data": []
                }
            
            # 提取数据
            data = result.get("data", {})
            items = data.get("items", [])
            
            # 限制返回条数
            if limit and len(items) > limit:
                items = items[:limit]
            
            return {
                "status": "success",
                "message": "成功获取新闻数据",
                "data": items
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"处理请求时出错: {str(e)}",
                "data": []
            }

# 创建插件实例
plugin = TushareSinaNewsPlugin()

# 插件入口点函数
def execute_tool(tool_name: str, tool_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行插件工具
    
    Args:
        tool_name: 工具名称
        tool_params: 工具参数
        
    Returns:
        工具执行结果
    """
    if tool_name == "get_sina_news":
        return plugin.get_sina_news(tool_params)
    else:
        return {
            "status": "error",
            "message": f"未知工具: {tool_name}",
            "data": []
        }
