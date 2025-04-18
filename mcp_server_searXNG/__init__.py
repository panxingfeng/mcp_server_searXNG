from .SearXNGServer import serve


def main():
    """SearXNG MCP Server - Web search functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="给模型提供网络搜索能力的MCP服务器"
    )
    parser.add_argument("--instance-url", default="http://localhost:4000",
                        help="SearXNG实例URL，默认为https://your-searxng-instance.com")
    args = parser.parse_args()

    asyncio.run(serve(instance_url=args.instance_url))


if __name__ == "__main__":
    main()