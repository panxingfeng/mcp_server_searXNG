import requests
from typing import List, Dict, Any, Optional
import logging

class SearXNGClient:
    """
    SearXNG 搜索客户端
    用于执行搜索并将结果格式化为指定的JSON格式
    """
    def __init__(self, instance_url: str = "https://your-searxng-instance.com"):
        """
        初始化SearXNG客户端

        参数:
        - instance_url: SearXNG实例URL
        """
        self.instance_url = instance_url
        self.logger = logging.getLogger(__name__)

    def search(self, query: str,
               categories: Optional[List[str]] = None,
               engines: Optional[List[str]] = None,
               language: str = "zh",
               max_results: int = 20,
               timeout: int = 30,
               pageno: int = 1,
               time_range: Optional[str] = None,
               safesearch: int = 0,
               format: str = "json",
               results_on_new_tab: Optional[int] = None,
               image_proxy: Optional[bool] = None,
               autocomplete: Optional[str] = None,
               theme: Optional[str] = None,
               enabled_plugins: Optional[List[str]] = None,
               disabled_plugins: Optional[List[str]] = None,
               enabled_engines: Optional[List[str]] = None,
               disabled_engines: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        执行搜索并返回格式化的结果

        参数:
        - query: 搜索查询
        - categories: 搜索类别列表 (例如 ['general', 'images', 'news'])
        - engines: 搜索引擎列表 (例如 ['google', 'bing', 'duckduckgo'])
        - language: 搜索语言代码
        - include_images: 是否包含图像结果
        - max_results: 最大结果数量
        - timeout: API请求超时时间(秒)
        - pageno: 搜索结果页码
        - time_range: 时间范围过滤 ('day', 'week', 'month', 'year')
        - safesearch: 安全搜索级别 (0=关闭, 1=中等, 2=严格)
        - format: 返回格式 ('json', 'csv', 'rss')
        - results_on_new_tab: 在新标签页打开结果 (0=否, 1=是)
        - image_proxy: 是否通过SearXNG代理图像
        - autocomplete: 自动完成服务
        - theme: 界面主题
        - enabled_plugins: 要启用的插件列表
        - disabled_plugins: 要禁用的插件列表
        - enabled_engines: 要启用的引擎列表
        - disabled_engines: 要禁用的引擎列表

        返回:
        - 结构化的搜索结果JSON
        """
        self.logger.info(f"开始搜索: {query}")

        # 构建查询参数
        params = {
            'q': query,
            'format': format,
            'language': language,
            'safesearch': safesearch,
            'pageno': pageno
        }

        # 添加可选参数
        if categories:
            params['categories'] = ','.join(categories)
        if engines:
            params['engines'] = ','.join(engines)
        if time_range:
            params['time_range'] = time_range
        if results_on_new_tab is not None:
            params['results_on_new_tab'] = results_on_new_tab
        if image_proxy is not None:
            params['image_proxy'] = 'True' if image_proxy else 'False'
        if autocomplete:
            params['autocomplete'] = autocomplete
        if theme:
            params['theme'] = theme
        if enabled_plugins:
            params['enabled_plugins'] = ','.join(enabled_plugins)
        if disabled_plugins:
            params['disabled_plugins'] = ','.join(disabled_plugins)
        if enabled_engines:
            params['enabled_engines'] = ','.join(enabled_engines)
        if disabled_engines:
            params['disabled_engines'] = ','.join(disabled_engines)

        # 请求URL
        url = f"{self.instance_url}/search"

        try:
            # 发送搜索请求
            self.logger.info(f"请求URL: {url} 参数: {params}")
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # 检查HTTP错误

            # 解析响应
            search_results = response.json()
            self.logger.info(f"获取到 {len(search_results.get('results', []))} 个结果")

            # 格式化结果
            return self._format_results(query, search_results, max_results)

        except requests.RequestException as e:
            self.logger.error(f"请求错误: {e}")
            # 返回空结果
            return self._format_results(query, {"results": []}, [], 0)

    def _format_results(self, query: str, search_data: Dict[str, Any],
                        max_results: int) -> Dict[str, Any]:
        """
        将搜索结果格式化为指定的JSON格式

        参数:
        - query: 原始查询
        - search_data: 搜索结果数据
        - image_results: 图像搜索结果数据
        - max_results: 最大结果数量

        返回:
        - 格式化的JSON结果
        """
        # 初始化结果列表
        formatted_results = []

        # 处理正常搜索结果
        results = search_data.get('results', [])
        for index, result in enumerate(results[:max_results]):
            # 获取内容并处理结尾的省略号
            content = result.get('content', '')

            # 添加到索引结果列表
            content_item = {
                "index": index,
                "result": content
            }

            formatted_results.append(content_item)

        # 构建最终结果
        final_result = {
            "query": query,
            "content": formatted_results,
        }

        return final_result
