# mcp_server_searXNG

基于MCP技术的网络搜索功能服务器，使用[SearXNG]([https://searx.github.io/searx/](https://github.com/searxng/searxng))搜索引擎实现隐私友好的网络搜索功能。

## 功能特点

此服务器提供以下主要功能：

- 通过多个搜索引擎进行网络搜索
- 支持多种搜索类别（一般、图片、新闻等）
- 自定义搜索引擎选择
- 语言筛选
- 时间范围过滤
- 搜索结果数量控制

## 可用工具

- `web_search` - 使用SearXNG执行网络搜索
  - 必需参数:
    - `query` (string): 搜索查询内容
  - 可选参数:
    - `categories` (array): 搜索类别，例如 ['general', 'images', 'news']
    - `engines` (array): 搜索引擎，例如 ['google', 'bing', 'duckduckgo']
    - `language` (string): 搜索语言代码，默认为 "zh"
    - `max_results` (integer): 最大结果数量，默认为 10
    - `time_range` (string): 时间范围过滤 ('day', 'week', 'month', 'year')

## 安装方法

### 使用 pip 安装

```bash
# 安装
pip install mcp-server-searxng==0.2

# 获取最新版本
pip install --upgrade mcp_server_searxng
```

## 使用示例

### 配置为 MCP 服务

在您的 MCP 配置中添加：

```json
"mcpServers": {
  "searxng": {
    "command": "python",
    "args": ["-m", "mcp_server_searxng", "--instance-url=https://your-searxng-instance.com"]
  }
}
```

### 调用示例
1.
```json
{
  "name": "web_search",
  "arguments": {
    "query": "气候变化研究",
    "categories": ["general"],
    "engines": ["google"],
    "language": "zh",
    "max_results": 15,
    "time_range": "month"
  }
}
```

## 调试

您可以使用 MCP inspector 来调试服务器:

```bash
npx @modelcontextprotocol/inspector python -m mcp_server_searxng
```

## 实际效果展示

<table>
  <tr>
    <td align="center" width="50%">
      <img src="https://raw.githubusercontent.com/panxingfeng/mcp_server_searXNG/main/mcp_server_searxng测试.png" width="330" /><br>
      <em>inspector的测试</em>
    </td>
    <td align="center" width="50%">
      <img src="https://raw.githubusercontent.com/panxingfeng/mcp_server_searXNG/main/搜索工具测试.gif" width="330" /><br>
      <em>基于我自己<a href="https://github.com/panxingfeng/chat_mcp">chat_mcp</a>的测试</em>
    </td>
  </tr>
</table>

## 许可证
mcp_server_searXNG 使用 MIT 许可证。这意味着您可以自由使用、修改和分发此软件，但需遵守 MIT 许可证的条款和条件。详情请参阅项目仓库中的 LICENSE 文件。
