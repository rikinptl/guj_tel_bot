import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator
import docx
from PyPDF2 import PdfReader
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize translator
translator = Translator()

# Get bot token from environment variable
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is not set!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_message = (
        "Welcome to the Gujarati Translation Bot! 🇮🇳\n\n"
        "I can translate text and files to Gujarati.\n\n"
        "Just send me:\n"
        "• Any text message - I'll translate it to Gujarati\n"
        "• A text file (.txt) - I'll translate its content\n"
        "• A Word document (.docx) - I'll translate its content\n"
        "• A PDF file (.pdf) - I'll translate its content\n\n"
        "Use /help for more information."
    )
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📚 How to use this bot:\n\n"
        "1. Send any text message and I'll translate it to Gujarati\n"
        "2. Send a file (.txt, .docx, or .pdf) and I'll extract and translate its content\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n\n"
        "Note: Large files may take some time to process."
    )
    await update.message.reply_text(help_text)


def extract_text_from_file(file_content: bytes, file_name: str) -> str:
    """Extract text from different file types."""
    file_extension = os.path.splitext(file_name)[1].lower()
    
    try:
        if file_extension == '.txt':
            # Plain text file
            return file_content.decode('utf-8')
        
        elif file_extension == '.docx':
            # Word document
            doc = docx.Document(io.BytesIO(file_content))
            text_parts = [paragraph.text for paragraph in doc.paragraphs]
            return '\n'.join(text_parts)
        
        elif file_extension == '.pdf':
            # PDF file
            pdf_file = io.BytesIO(file_content)
            reader = PdfReader(pdf_file)
            text_parts = []
            for page in reader.pages:
                text_parts.append(page.extract_text())
            return '\n'.join(text_parts)
        
        else:
            return None
    
    except Exception as e:
        logger.error(f"Error extracting text from file: {e}")
        return None


def translate_to_gujarati(text: str) -> str:
    """Translate text to Gujarati."""
    try:
        # Detect language and translate to Gujarati
        result = translator.translate(text, dest='gu')
        return result.text
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return f"Translation error: {str(e)}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    user_text = update.message.text
    
    if not user_text:
        return
    
    # Show typing indicator
    await update.message.chat.send_action(action="typing")
    
    # Translate to Gujarati
    translated_text = translate_to_gujarati(user_text)
    
    # Send translated text
    await update.message.reply_text(
        f"📝 Translated to Gujarati:\n\n{translated_text}",
        reply_to_message_id=update.message.message_id
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle file/document messages."""
    document = update.message.document
    
    if not document:
        return
    
    file_name = document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()
    
    # Check if file type is supported
    supported_extensions = ['.txt', '.docx', '.pdf']
    if file_extension not in supported_extensions:
        await update.message.reply_text(
            f"❌ Unsupported file type. Please send a .txt, .docx, or .pdf file."
        )
        return
    
    # Show downloading indicator
    await update.message.chat.send_action(action="typing")
    
    try:
        # Download file
        file = await context.bot.get_file(document.file_id)
        file_content = await file.download_as_bytearray()
        
        # Extract text from file
        extracted_text = extract_text_from_file(file_content, file_name)
        
        if not extracted_text or not extracted_text.strip():
            await update.message.reply_text(
                "❌ Could not extract text from the file. Please make sure the file contains readable text."
            )
            return
        
        # Check if text is too long (Telegram message limit is 4096 characters)
        if len(extracted_text) > 4000:
            # Split into chunks
            chunk_size = 4000
            chunks = [extracted_text[i:i+chunk_size] for i in range(0, len(extracted_text), chunk_size)]
            
            await update.message.reply_text(
                f"📄 Extracted text from {file_name} ({len(extracted_text)} characters). "
                f"Translating in {len(chunks)} parts..."
            )
            
            for i, chunk in enumerate(chunks, 1):
                translated_chunk = translate_to_gujarati(chunk)
                await update.message.reply_text(
                    f"📝 Part {i}/{len(chunks)} - Translated to Gujarati:\n\n{translated_chunk}"
                )
        else:
            # Translate entire text
            translated_text = translate_to_gujarati(extracted_text)
            
            await update.message.reply_text(
                f"📄 File: {file_name}\n"
                f"📝 Translated to Gujarati:\n\n{translated_text}",
                reply_to_message_id=update.message.message_id
            )
    
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        await update.message.reply_text(
            f"❌ Error processing file: {str(e)}"
        )


def main() -> None:
    """Start the bot."""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

