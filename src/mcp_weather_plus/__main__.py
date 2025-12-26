import argparse
import sys
from mcp_weather_plus.server import serve

def main():
    parser = argparse.ArgumentParser(description="Weather MCP Server")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port for streamable-http mode (default: 8080)"
    )
    
    args = parser.parse_args()
    
    try:
        serve(mode=args.mode, port=args.port)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
