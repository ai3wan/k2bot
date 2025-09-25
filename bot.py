#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Основное сообщение бота
WELCOME_MESSAGE = """💼 USDT для бизнеса по договору
Покупка криптовалюты для ООО, ИП, фрилансеров — быстро и официально:

💵 Сделки от ₽500к
💰 Выгодный курс
📉 Комиссия от 0.5%
⚡️ Быстрое зачисление
📄 Закрывающие документы
📊 Консультация по бухучету
🛠 Поддержка 24/7

💬 Бесплатная консультация по вашему кейсу
📎 Легально. Безопасно. Без налога на нервную систему.

🌍 https://k2crypto.m70.capital/"""

# Создание клавиатуры с кнопками
def get_main_keyboard():
    keyboard = [
        ["📊 Бухгалтерия и налоги", "📋 Как проходит сделка"],
        ["👤 Написать менеджеру", "🌍 Перейти на сайт K2 Crypto"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение с меню кнопок"""
    user = update.effective_user
    logger.info(f"Пользователь {user.id} ({user.first_name}) запустил бота")
    
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=get_main_keyboard(),
        parse_mode='HTML'
    )

# Обработчик текстовых сообщений (нажатий на кнопки)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текстовые сообщения и нажатия на кнопки меню"""
    user = update.effective_user
    message_text = update.message.text
    
    logger.info(f"Пользователь {user.id} отправил сообщение: {message_text}")
    
    if message_text == "📊 Бухгалтерия и налоги":
        response = """⚖️ Работаем строго в рамках законодательства РФ
💼 Все расчёты оформляются официально — с договором и учётом цифровых активов
📄 Предоставляем комплект документов: договор, заявка, счёт, акт
📊 Помогаем с бухгалтерским учётом операций
📑 При необходимости — готовим legal opinion для налоговой и контролирующих органов"""
        
    elif message_text == "📋 Как проходит сделка":
        response = """📋 Как проходит сделка:

🛂 1. Верификация
Проходите KYC — быстрая проверка клиента

📝 2. Договор
Заключаем рамочный договор на проведение цифровых расчётов

📨 3. Заявка
Вы оставляете заявку — фиксируем объём и параметры сделки

💳 4. Оплата
Средства перечисляются по безналу с расчётного счёта вашей компании

🚀 5. Исполнение
Проводим расчёт в согласованные сроки и объёме

📄 6. Документы
Предоставляем комплект закрывающих документов: договор, счёт, акт"""
        
    elif message_text == "👤 Написать менеджеру":
        response = """👤 Написать менеджеру

Наши менеджеры готовы ответить на все ваши вопросы и помочь с оформлением сделки."""
        
        # Создаем inline кнопку для перехода к менеджеру
        keyboard = [[InlineKeyboardButton("💬 Написать менеджеру", url="https://t.me/k2cryptopro")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=response,
            reply_markup=reply_markup
        )
        return
        
    elif message_text == "🌍 Перейти на сайт K2 Crypto":
        response = """🌍 <b>Перейти на сайт K2 Crypto</b>

🔗 <b>Наш сайт:</b> https://k2crypto.m70.capital/

На сайте вы найдете:
• Подробную информацию об услугах
• Калькулятор курсов
• Форму для заявки
• Контактную информацию

💬 Или просто напишите нашему менеджеру для быстрой консультации!"""
        
    else:
        response = """❓ Не понимаю ваше сообщение.

Пожалуйста, используйте кнопки меню ниже или команды:
/start - Главное меню
/help - Справка"""
    
    await update.message.reply_text(
        text=response,
        parse_mode='HTML',
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет справочную информацию"""
    help_text = """🤖 <b>Команды бота:</b>

/start - Главное меню
/help - Эта справка

<b>Основные функции:</b>
• Информация о покупке USDT для бизнеса
• Консультации по бухгалтерии и налогам
• Связь с менеджерами
• Переход на сайт K2 Crypto

🌍 <b>Сайт:</b> https://k2crypto.m70.capital/"""
    
    await update.message.reply_text(help_text, parse_mode='HTML')

def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    logger.info("Запуск бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
