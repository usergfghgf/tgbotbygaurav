import asyncio
import logging
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN, ROLES, BOT_OWNER_ID, CEREBRAS_API_KEY
from cerebras_client import CerebrasClient
from user_manager import UserManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class RoleBasedBot:
    def __init__(self):
        self.cerebras_client = CerebrasClient()
        self.user_manager = UserManager()
        
        # Check if API key is configured
        if not self.cerebras_client.is_api_key_valid():
            logger.error("Cerebras API key not configured properly!")
            raise ValueError("Please configure your Cerebras API key in .env file")
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            user = update.effective_user
            user_id = user.id
            
            # Set user name
            self.user_manager.set_user_name(user_id, user.first_name)
            
            welcome_message = (
                f"👋 Hello {html.escape(user.first_name)}! Welcome to your AI companion bot!\n\n"
                "I can adapt to different roles to better assist you:\n\n"
                "🎭 <b>Available Roles:</b>\n"
                "• Default Assistant - General help\n"
                "• Code Expert - Programming assistance\n"
                "• Data Analyst - Data insights\n"
                "• Male/Female Partner - Supportive companion\n"
                "• Supportive Friend - Encouraging friend\n"
                "• Therapeutic Support - Emotional guidance\n\n"
                "Use /roles to change my role, or just start chatting!\n\n"
                "For queries contact @Glitch_artist0611"
            )
            
            await update.message.reply_text(welcome_message, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            await update.message.reply_text("❌ Error starting bot. Please try again.")
    
    async def roles(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /roles command - show role selection"""
        try:
            keyboard = []
            row = []
            
            for role_key, role_info in ROLES.items():
                button = InlineKeyboardButton(
                    f"{role_info['name']}",
                    callback_data=f"role_{role_key}"
                )
                row.append(button)
                
                # Create new row every 2 buttons for better layout
                if len(row) == 2:
                    keyboard.append(row)
                    row = []
            
            # Add remaining buttons if any
            if row:
                keyboard.append(row)
            
            # Add info button
            keyboard.append([InlineKeyboardButton("ℹ️ Role Info", callback_data="role_info")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                "🎭 <b>Choose Your AI Companion Role:</b>\n\n"
                "Select a role that best fits your current needs:",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error in roles command: {e}")
            await update.message.reply_text("❌ Error displaying roles. Please try again.")
    
    async def role_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle role selection callbacks"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_id = query.from_user.id
            
            if query.data.startswith("role_"):
                role_key = query.data[5:]  # Remove "role_" prefix
                
                if role_key == "info":
                    # Show role information
                    info_text = "<b>Role Descriptions:</b>\n\n"
                    for key, role_info in ROLES.items():
                        info_text += f"<b>{html.escape(role_info['name'])}:</b>\n{html.escape(role_info['description'])}\n\n"
                    
                    await query.edit_message_text(
                        info_text,
                        parse_mode=ParseMode.HTML
                    )
                    return
                
                if role_key in ROLES:
                    # Check if this is a partner role that needs a name
                    if role_key in ["partner_male", "partner_female"]:
                        # Store the pending role change
                        context.user_data['pending_role'] = role_key
                        
                        # Ask for the partner's name
                        role_info = ROLES[role_key]
                        partner_type = "boyfriend" if role_key == "partner_male" else "girlfriend"
                        
                        await query.edit_message_text(
                            f"💕 <b>Setting up your {partner_type}...</b>\n\n"
                            f"Please send me the name you'd like to give to your {partner_type}.\n\n"
                            f"<i>Example: Alex, James, Sarah, Emma, etc.</i>\n\n"
                            f"Just type the name in the chat!",
                            parse_mode=ParseMode.HTML
                        )
                        return
                    
                    # For non-partner roles, proceed normally
                    success = self.user_manager.set_user_role(user_id, role_key)
                    if success:
                        # Clear partner name if switching away from partner roles
                        current_role = self.user_manager.get_user_role(user_id)
                        if current_role in ["partner_male", "partner_female"]:
                            self.user_manager.clear_partner_name(user_id)
                        
                        role_info = ROLES[role_key]
                        
                        # Clear conversation history when changing roles
                        self.user_manager.clear_conversation(user_id)
                        
                        await query.edit_message_text(
                            f"✅ <b>Role Changed Successfully!</b>\n\n"
                            f"You are now chatting with: <b>{html.escape(role_info['name'])}</b>\n\n"
                            f"<i>{html.escape(role_info['description'])}</i>\n\n"
                            f"Your conversation history has been cleared for the new role.\n"
                            f"Start chatting to experience the new personality!",
                            parse_mode=ParseMode.HTML
                        )
                    else:
                        await query.edit_message_text("❌ Failed to change role. Please try again.")
                else:
                    await query.edit_message_text("❌ Invalid role selected.")
                    
        except Exception as e:
            logger.error(f"Error in role_callback: {e}")
            try:
                await query.edit_message_text("❌ Error processing role selection. Please try again.")
            except:
                pass
    
    async def ping_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /ping command - check bot response time"""
        try:
            start_time = context.bot_data.get('ping_start_time', 0)
            if start_time == 0:
                # First ping, set start time
                context.bot_data['ping_start_time'] = update.message.date.timestamp()
                await update.message.reply_text("🏓 Pong! Send /ping again to see response time.")
            else:
                # Calculate response time
                end_time = update.message.date.timestamp()
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                await update.message.reply_text(f"🏓 Pong! Response time: {response_time:.2f} ms")
                # Reset for next ping
                context.bot_data['ping_start_time'] = 0
        except Exception as e:
            logger.error(f"Error in ping command: {e}")
            await update.message.reply_text("❌ Error processing ping. Please try again.")

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /models command - owner only, show available models"""
        user_id = update.effective_user.id
        
        # Check if user is owner
        if str(user_id) != BOT_OWNER_ID:
            await update.message.reply_text("❌ This command is only available to the bot owner.")
            return
        
        try:
            models = self.cerebras_client.get_available_models()
            current_model = self.cerebras_client.get_current_model()
            
            if models:
                models_text = "🤖 <b>Available Models:</b>\n\n"
                for model in models:
                    if model == current_model:
                        models_text += f"✅ <b>{html.escape(model)}</b> (Current)\n"
                    else:
                        models_text += f"📋 {html.escape(model)}\n"
                
                models_text += f"\n💡 <b>Current Model:</b> {html.escape(current_model)}"
                models_text += "\n\nUse <code>/setmodel &lt;model_name&gt;</code> to change models."
                
                await update.message.reply_text(models_text, parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text("❌ Failed to fetch available models.")
                
        except Exception as e:
            logger.error(f"Error in models command: {e}")
            await update.message.reply_text(f"❌ Error fetching models: {html.escape(str(e))}")

    async def setmodel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /setmodel command - owner only, set the AI model"""
        user_id = update.effective_user.id
        
        # Check if user is owner
        if str(user_id) != BOT_OWNER_ID:
            await update.message.reply_text("❌ This command is only available to the bot owner.")
            return
        
        # Check if model name was provided
        if not context.args:
            await update.message.reply_text("❌ Please specify a model name.\nUsage: <code>/setmodel &lt;model_name&gt;</code>", parse_mode=ParseMode.HTML)
            return
        
        model_name = context.args[0]
        
        try:
            success = self.cerebras_client.set_model(model_name)
            if success:
                await update.message.reply_text(f"✅ Model successfully set to: <b>{html.escape(model_name)}</b>", parse_mode=ParseMode.HTML)
            else:
                await update.message.reply_text(f"❌ Failed to set model to: {html.escape(model_name)}")
                
        except Exception as e:
            logger.error(f"Error in setmodel command: {e}")
            await update.message.reply_text(f"❌ Error setting model: {html.escape(str(e))}")

    async def currentmodel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /currentmodel command - show current model"""
        try:
            current_model = self.cerebras_client.get_current_model()
            await update.message.reply_text(f"🤖 <b>Current AI Model:</b> {html.escape(current_model)}", parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.error(f"Error in currentmodel command: {e}")
            await update.message.reply_text(f"❌ Error fetching current model: {html.escape(str(e))}")

    async def debug_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /debug command - show detailed user session info (owner only)"""
        user_id = update.effective_user.id
        
        # Check if user is owner
        if str(user_id) != BOT_OWNER_ID:
            await update.message.reply_text("❌ This command is only available to the bot owner.")
            return
        
        try:
            current_role = self.user_manager.get_user_role(user_id)
            role_info = ROLES.get(current_role, ROLES["default"])
            user_name = self.user_manager.get_user_name(user_id)
            conversation = self.user_manager.get_conversation(user_id)
            partner_name = self.user_manager.get_partner_name(user_id)
            
            debug_text = (
                f"🐛 <b>Debug Information:</b>\n\n"
                f"👤 <b>User ID:</b> {user_id}\n"
                f"👤 <b>User Name:</b> {html.escape(user_name or 'N/A')}\n"
                f"🎭 <b>Current Role:</b> {html.escape(current_role)}\n"
                f"📝 <b>Role Name:</b> {html.escape(role_info['name'])}\n"
                f"💬 <b>Messages in History:</b> {len(conversation)}\n"
                f"🔑 <b>Available Roles:</b> {', '.join(ROLES.keys())}\n"
            )
            
            # Add partner name if applicable
            if partner_name:
                partner_type = "Boyfriend" if current_role == "partner_male" else "Girlfriend"
                debug_text += f"💕 <b>{partner_type} Name:</b> {html.escape(partner_name)}\n"
            
            debug_text += "\n<b>Last 3 Messages:</b>\n"
            
            # Show last 3 messages
            for i, msg in enumerate(conversation[-3:], 1):
                role_emoji = "👤" if msg["role"] == "user" else "🤖"
                debug_text += f"{i}. {role_emoji} {html.escape(msg['role'])}: {html.escape(msg['content'][:50])}...\n"
            
            await update.message.reply_text(debug_text, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in debug command: {e}")
            await update.message.reply_text(f"❌ Debug error: {html.escape(str(e))}")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        try:
            user_id = update.effective_user.id
            is_owner = str(user_id) == BOT_OWNER_ID
            
            help_text = (
                "<b>Bot Commands:</b>\n\n"
                "/start - Start the bot and see welcome message\n"
                "/roles - Choose your AI companion's role\n"
                "/help - Show this help message\n"
                "/clear - Clear conversation history\n"
                "/status - Show current role and status\n"
                "/ping - Check bot response time\n"
                "/currentmodel - Show current AI model\n"
            )
            
            # Add owner-only commands
            if is_owner:
                help_text += (
                    "/models - Show available AI models (Owner only)\n"
                    "/setmodel &lt;name&gt; - Set AI model (Owner only)\n"
                    "/debug - Show detailed debug info (Owner only)\n"
                )
            
            help_text += (
                "\n💡 <b>Tips:</b>\n"
                "• Change roles anytime with /roles\n"
                "• Each role has unique personality and expertise\n"
                "• Male/Female Partner roles let you choose a name\n"
                "• Just type to start chatting!\n\n"
                "🎭 <b>Current Role:</b> Use /roles to see available options"
            )
            
            await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            await update.message.reply_text("❌ Error displaying help. Please try again.")
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clear command - clear conversation history"""
        try:
            user_id = update.effective_user.id
            self.user_manager.clear_conversation(user_id)
            
            await update.message.reply_text(
                "🗑️ <b>Conversation History Cleared!</b>\n\n"
                "Your chat history has been reset. Start fresh!",
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            logger.error(f"Error in clear command: {e}")
            await update.message.reply_text("❌ Error clearing conversation. Please try again.")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command - show current status"""
        try:
            user_id = update.effective_user.id
            current_role = self.user_manager.get_user_role(user_id)
            role_info = ROLES.get(current_role, ROLES["default"])
            user_name = self.user_manager.get_user_name(user_id)
            
            status_text = (
                f"<b>Your Bot Status:</b>\n\n"
                f"👤 <b>User:</b> {html.escape(user_name or 'N/A')}\n"
                f"🎭 <b>Current Role:</b> {html.escape(role_info['name'])}\n"
                f"📝 <b>Description:</b> {html.escape(role_info['description'])}\n\n"
            )
            
            # Add partner name if in partner role
            if current_role in ["partner_male", "partner_female"]:
                partner_name = self.user_manager.get_partner_name(user_id)
                if partner_name:
                    partner_type = "Boyfriend" if current_role == "partner_male" else "Girlfriend"
                    status_text += f"💕 <b>{partner_type}:</b> {html.escape(partner_name)}\n\n"
            
            status_text += (
                f"💬 <b>Messages in History:</b> {len(self.user_manager.get_conversation(user_id))}\n\n"
                f"Use /roles to change your AI companion's role!"
            )
            
            await update.message.reply_text(status_text, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("❌ Error displaying status. Please try again.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        try:
            # Check if user is setting up a partner role
            if 'pending_role' in context.user_data:
                await self._handle_partner_setup(update, context, user_id, user_message)
                return
            
            # Get user's current role
            current_role = self.user_manager.get_user_role(user_id)
            if current_role not in ROLES:
                # Fallback to default role if current role is invalid
                current_role = "default"
                self.user_manager.set_user_role(user_id, current_role)
                logger.warning(f"User {user_id} had invalid role, reset to default")
            
            role_info = ROLES[current_role]
            
            # Add user message to conversation
            self.user_manager.add_message(user_id, "user", user_message)
            
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Get conversation history
            conversation = self.user_manager.get_conversation(user_id)
            
            # Get the system prompt and personalize it if needed
            system_prompt = role_info['system_prompt']
            
            # Personalize partner role prompts with the user's chosen name
            if current_role in ["partner_male", "partner_female"]:
                partner_name = self.user_manager.get_partner_name(user_id)
                if partner_name:
                    # Replace {name} placeholder with actual partner name
                    system_prompt = system_prompt.replace("{name}", partner_name)
                    logger.info(f"Personalized prompt for {current_role} with name: {partner_name}")
                else:
                    logger.warning(f"No partner name found for {current_role}, using default prompt")
            else:
                logger.info(f"Using standard prompt for role: {current_role}")
            
            # Generate response using Cerebras API (synchronous call)
            response = self.cerebras_client.generate_response(
                conversation, 
                system_prompt
            )
            
            # Add bot response to conversation
            self.user_manager.add_message(user_id, "assistant", response)
            
            # Send response with proper parsing
            await update.message.reply_text(response, parse_mode=ParseMode.HTML)
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            # Provide a more helpful error message
            error_response = (
                "I'm experiencing some technical difficulties right now. "
                "Please try again in a moment, or use /clear to reset our conversation."
            )
            await update.message.reply_text(error_response, parse_mode=ParseMode.HTML)
    
    async def _handle_partner_setup(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, user_message: str):
        """Handle partner role setup when user provides a name"""
        try:
            pending_role = context.user_data['pending_role']
            partner_name = user_message.strip()
            
            # Validate the name (basic validation)
            if len(partner_name) < 2 or len(partner_name) > 20:
                await update.message.reply_text(
                    "❌ Please provide a valid name (2-20 characters).\n\n"
                    "Try again with a shorter or longer name.",
                    parse_mode=ParseMode.HTML
                )
                return
            
            # Set the role and store the partner name
            success = self.user_manager.set_user_role(user_id, pending_role)
            if success:
                # Store the partner name
                self.user_manager.set_partner_name(user_id, partner_name)
                
                # Clear conversation history
                self.user_manager.clear_conversation(user_id)
                
                # Get role info
                role_info = ROLES[pending_role]
                partner_type = "boyfriend" if pending_role == "partner_male" else "girlfriend"
                
                # Confirm the setup
                await update.message.reply_text(
                    f"💕 <b>{partner_type.title()} Setup Complete!</b>\n\n"
                    f"Your {partner_type} <b>{html.escape(partner_name)}</b> is ready to chat!\n\n"
                    f"<i>{html.escape(role_info['description'])}</i>\n\n"
                    f"💬 <b>{html.escape(partner_name)}</b> will now respond as your personalized {partner_type}.\n"
                    f"Start chatting with {html.escape(partner_name)} now! 💕",
                    parse_mode=ParseMode.HTML
                )
                
                # Clear the pending role
                del context.user_data['pending_role']
                
            else:
                await update.message.reply_text(
                    "❌ Failed to set up partner role. Please try again.",
                    parse_mode=ParseMode.HTML
                )
                del context.user_data['pending_role']
                
        except Exception as e:
            logger.error(f"Error in partner setup: {e}")
            await update.message.reply_text(
                "❌ An error occurred during setup. Please try again.",
                parse_mode=ParseMode.HTML
            )
            # Clear pending role on error
            if 'pending_role' in context.user_data:
                del context.user_data['pending_role']
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        try:
            logger.error(f"Update {update} caused error {context.error}")
            
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "An error occurred while processing your request. Please try again.",
                    parse_mode=ParseMode.HTML
                )
        except Exception as e:
            logger.error(f"Error in error handler: {e}")

def main():
    """Main function to run the bot"""
    try:
        # Check if bot token is configured
        if not BOT_TOKEN:
            print("❌ BOT_TOKEN not configured in .env file!")
            print("Please create a .env file with your BOT_TOKEN and CEREBRAS_API_KEY")
            return
        
        # Check if Cerebras API key is configured
        if not CEREBRAS_API_KEY:
            print("❌ CEREBRAS_API_KEY not configured in .env file!")
            print("Please add your CEREBRAS_API_KEY to the .env file")
            return
        
        # Check if owner ID is configured
        if not BOT_OWNER_ID:
            print("⚠️ BOT_OWNER_ID not configured - owner commands will be disabled")
        
        print("🔧 Starting bot initialization...")
        
        # Initialize bot
        bot = RoleBasedBot()
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("roles", bot.roles))
        application.add_handler(CommandHandler("help", bot.help_command))
        application.add_handler(CommandHandler("clear", bot.clear_command))
        application.add_handler(CommandHandler("status", bot.status_command))
        application.add_handler(CommandHandler("ping", bot.ping_command))
        application.add_handler(CommandHandler("models", bot.models_command))
        application.add_handler(CommandHandler("setmodel", bot.setmodel_command))
        application.add_handler(CommandHandler("currentmodel", bot.currentmodel_command))
        application.add_handler(CommandHandler("debug", bot.debug_command))
        
        # Add callback query handler for role selection
        application.add_handler(CallbackQueryHandler(bot.role_callback))
        
        # Add message handler
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
        
        # Add error handler
        application.add_error_handler(bot.error_handler)
        
        # Start the bot
        print("🤖 Bot is starting...")
        print("✅ Configuration verified successfully")
        print("📱 Bot will start polling for messages...")
        print("🚀 Bot is now deployment ready!")
        
        # Start polling with better compatibility
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"❌ Failed to start bot: {e}")
        print("Please check your configuration and try again.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure .env file exists with BOT_TOKEN and CEREBRAS_API_KEY")
        print("2. Check internet connection")
        print("3. Verify bot token is valid")
        print("4. Ensure Cerebras API key is valid")

if __name__ == "__main__":
    main()