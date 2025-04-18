import json
from typing import Any, Sequence, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource, ErrorData, TextResourceContents, \
    BlobResourceContents
from mcp.shared.exceptions import McpError

from .searXNG_client import SearXNGClient


class SearXNGServer:
    """
    SearXNG MCP服务器
    提供搜索功能，通过MCP接口供模型使用
    """

    def __init__(self, instance_url: str = "https://your-searxng-instance.com"):
        """
        初始化SearXNG服务器

        参数:
        - instance_url: SearXNG实例URL
        """
        self.searxng_client = SearXNGClient(instance_url=instance_url)

    async def search(self, query: str, categories: Optional[List[str]] = None,
                     engines: Optional[List[str]] = None,
                     language: str = "zh",
                     max_results: int = 10,
                     time_range: Optional[str] = None) -> Dict[str, Any]:
        """
        执行搜索并返回格式化的结果

        参数:
        - query: 搜索查询
        - categories: 搜索类别列表 (例如 ['general', 'images', 'news'])
        - engines: 搜索引擎列表 (例如 ['google', 'bing', 'duckduckgo'])
        - language: 搜索语言代码
        - max_results: 最大结果数量
        - time_range: 时间范围过滤 ('day', 'week', 'month', 'year')

        返回:
        - 结构化的搜索结果
        """
        # 设置默认搜索参数
        if categories is None:
            categories = ["general"]
        if engines is None:
            engines = ["google", "bing", "duckduckgo"]

        # 使用SearXNG客户端执行搜索
        search_results = self.searxng_client.search(
            query=query,
            categories=categories,
            engines=engines,
            language=language,
            max_results=max_results,
            time_range=time_range,
            safesearch=1
        )

        return search_results

    def format_search_results(self, search_results: Dict[str, Any]) -> str:
        """
        将搜索结果格式化为文本输出

        参数:
        - search_results: 搜索结果字典

        返回:
        - 格式化的搜索结果文本
        """
        # 构建格式化输出
        output = []
        # 添加内容结果
        content_items = search_results.get('content', [])
        if content_items:
            for item in content_items:
                output.append(f"[{item.get('index', '')}] {item.get('result', '')}")
            output.append("")

        return "\n".join(output)


async def serve(instance_url: str = "https://your-searxng-instance.com"):
    """
    启动SearXNG MCP服务器

    参数:
    - instance_url: SearXNG实例URL
    """
    server = Server("SearXNGServer")
    searxng_server = SearXNGServer(instance_url=instance_url)

    @server.list_resources()
    async def handle_list_resources():
        """列出可用的搜索资源"""
        return [
            {
                "uri": "searxng://web/search",
                "name": "网络搜索",
                "description": "使用SearXNG在网络上搜索信息",
                "mimeType": "application/json",
            }
        ]

    @server.read_resource()
    async def handle_read_resource(uri: str) -> List[TextResourceContents | BlobResourceContents]:
        """读取指定的搜索资源"""
        if uri.startswith("searxng://"):
            # 创建一个文本资源内容对象
            return [
                TextResourceContents(
                    uri=uri,
                    mimeType="application/json",
                    text=json.dumps({"message": "此功能暂未实现"}, ensure_ascii=False)
                )
            ]
        raise ValueError(f"不支持的URI: {uri}")

    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """列出可用的搜索工具"""
        return [
            Tool(
                name="web_search",
                description="使用SearXNG搜索网络信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索查询",
                        },
                        "categories": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "搜索类别，例如 ['general', 'images', 'news']",
                        },
                        "engines": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "搜索引擎，例如 ['google', 'bing', 'duckduckgo']",
                        },
                        "language": {
                            "type": "string",
                            "description": "搜索语言代码",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "最大结果数量",
                        },
                        "time_range": {
                            "type": "string",
                            "description": "时间范围过滤 ('day', 'week', 'month', 'year')",
                        }
                    },
                    "required": ["query"],
                }
            )
        ]

    @server.call_tool()
    async def call_tool(
            name: str, arguments: Dict[str, Any]
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """处理工具调用请求"""
        try:
            if name == "web_search":
                query = arguments.get("query")
                if not query:
                    raise ValueError("缺少必要参数: query")

                categories = arguments.get("categories")
                engines = arguments.get("engines")
                language = arguments.get("language", "zh")
                max_results = arguments.get("max_results", 10)
                time_range = arguments.get("time_range")

                search_results = await searxng_server.search(
                    query=query,
                    categories=categories,
                    engines=engines,
                    language=language,
                    max_results=max_results,
                    time_range=time_range
                )

                formatted_results = searxng_server.format_search_results(search_results)

                return [TextContent(type="text", text=formatted_results)]

            return [TextContent(type="text", text=f"不支持的工具: {name}")]

        except Exception as e:
            error = ErrorData(message=f"搜索服务错误: {str(e)}", code=-32603)
            raise McpError(error)
        
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
