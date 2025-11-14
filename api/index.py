"""
Vercel serverless function entry point for Telegram webhook
"""
import json
from webhook import webhook_handler


def handler(request):
    """Vercel serverless function handler."""
    # Convert Vercel request to async-compatible format
    import asyncio
    
    # Get request body
    if hasattr(request, 'body'):
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
    else:
        body = request.get_json() if hasattr(request, 'get_json') else {}
    
    # Create a simple request-like object
    class SimpleRequest:
        async def json(self):
            return body
    
    # Run async handler
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    result = loop.run_until_complete(webhook_handler(SimpleRequest()))
    return result

