"""
Script to set up the Telegram webhook after deploying to Vercel.
Run this script after your bot is deployed to Vercel.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
VERCEL_URL = os.getenv('VERCEL_URL', 'https://your-app.vercel.app')

if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found in environment variables")
    exit(1)

# Set webhook URL
webhook_url = f"{VERCEL_URL}/webhook"
set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

print(f"Setting webhook to: {webhook_url}")

response = requests.post(set_webhook_url, json={"url": webhook_url})

if response.status_code == 200:
    result = response.json()
    if result.get('ok'):
        print("✅ Webhook set successfully!")
        print(f"Webhook URL: {webhook_url}")
    else:
        print(f"❌ Error setting webhook: {result.get('description')}")
else:
    print(f"❌ HTTP Error: {response.status_code}")
    print(response.text)

