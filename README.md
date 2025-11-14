# Gujarati Translation Telegram Bot

A Telegram bot that translates text and file contents to Gujarati language.

## Features

- ✅ Translate text messages to Gujarati
- ✅ Translate text from files (.txt, .docx, .pdf)
- ✅ Support for multiple file formats
- ✅ Automatic language detection
- ✅ Handles large files by splitting into chunks

## Prerequisites

- Python 3.8 or higher
- A Telegram Bot Token (get it from [@BotFather](https://t.me/BotFather))

## Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a Telegram Bot Token:**
   - Open Telegram and search for [@BotFather](https://t.me/BotFather)
   - Send `/newbot` command
   - Follow the instructions to create a new bot
   - Copy the bot token you receive

4. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```bash
   BOT_TOKEN=your_bot_token_here
   ```
   
   Or export it directly:
   ```bash
   export BOT_TOKEN=your_bot_token_here
   ```

5. **Run the bot:**
   ```bash
   python bot.py
   ```

## Usage

1. Start a conversation with your bot on Telegram
2. Send `/start` to begin
3. Send any text message or file (.txt, .docx, .pdf)
4. The bot will translate the content to Gujarati

## Supported File Types

- `.txt` - Plain text files
- `.docx` - Microsoft Word documents
- `.pdf` - PDF documents

## Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show help information

## Notes

- The bot uses Google Translate API (via googletrans library) for translation
- Large files will be split into multiple messages due to Telegram's message length limit (4096 characters)
- The bot automatically detects the source language

## Troubleshooting

- **Bot not responding:** Make sure the BOT_TOKEN is set correctly
- **Translation errors:** Check your internet connection as the bot uses Google Translate API
- **File processing errors:** Ensure the file contains readable text and is in a supported format

## Deployment to Vercel

This bot is configured to deploy to Vercel as a serverless function.

### Prerequisites for Vercel Deployment

- A Vercel account (sign up at [vercel.com](https://vercel.com))
- Vercel CLI installed (optional, you can also deploy via GitHub)

### Deployment Steps

1. **Install Vercel CLI (if using CLI):**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel:**
   
   **Option A: Using Vercel CLI**
   ```bash
   vercel
   ```
   Follow the prompts to link your project and deploy.
   
   **Option B: Using GitHub (Recommended)**
   - Push your code to a GitHub repository
   - Go to [vercel.com](https://vercel.com) and import your repository
   - Vercel will automatically detect the Python project

3. **Set Environment Variables in Vercel:**
   - Go to your project settings in Vercel Dashboard
   - Navigate to "Environment Variables"
   - Add the following variable:
     - **Key:** `BOT_TOKEN`
     - **Value:** `8320163074:AAGR1DKtfQP743DWU8_uzy_PrTArwqkV7bQ` (your bot token)
   - Make sure to add it for all environments (Production, Preview, Development)

4. **Get Your Vercel Deployment URL:**
   - After deployment, Vercel will provide you with a URL like: `https://your-project.vercel.app`
   - Copy this URL

5. **Set Up the Webhook:**
   
   After deployment, you need to tell Telegram where to send updates. You can do this in two ways:
   
   **Option A: Using the setup script**
   ```bash
   # Set your Vercel URL in .env or export it
   export VERCEL_URL=https://your-project.vercel.app
   python setup_webhook.py
   ```
   
   **Option B: Using curl**
   ```bash
   curl -X POST "https://api.telegram.org/bot8320163074:AAGR1DKtfQP743DWU8_uzy_PrTArwqkV7bQ/setWebhook?url=https://your-project.vercel.app/webhook"
   ```
   
   Replace `https://your-project.vercel.app` with your actual Vercel deployment URL.

6. **Verify Webhook is Set:**
   ```bash
   curl "https://api.telegram.org/bot8320163074:AAGR1DKtfQP743DWU8_uzy_PrTArwqkV7bQ/getWebhookInfo"
   ```

7. **Test Your Bot:**
   - Go to Telegram and find your bot: `@guj_translator_bot`
   - Send `/start` to test if it's working

### Important Notes for Vercel Deployment

- The bot uses **webhook mode** on Vercel (not polling)
- The webhook endpoint is: `/webhook` or `/api/webhook`
- Make sure your `BOT_TOKEN` is set in Vercel's environment variables
- Vercel has a 10-second timeout for free tier, so very large files might timeout
- The bot will automatically scale with Vercel's serverless infrastructure

### Local Development vs Production

- **Local:** Use `bot.py` for local testing with polling mode
- **Production:** Use `api/webhook.py` for Vercel deployment with webhook mode

## License

This project is open source and available for personal use.

