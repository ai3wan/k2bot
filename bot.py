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
        response = """⚖️ <b>Работаем строго в рамках законодательства РФ</b>

💼 <b>Все расчёты оформляются официально</b> — с договором и учётом цифровых активов

📄 <b>Предоставляем комплект документов:</b> договор, заявка, счёт, акт

📊 <b>Помогаем с бухгалтерским учётом операций</b>

📑 <b>При необходимости</b> — готовим legal opinion для налоговой и контролирующих органов"""
        
    elif message_text == "📋 Как проходит сделка":
        response = """📋 <b>Как проходит сделка:</b>

🛂 <b>1. Верификация</b>
Проходите KYC — быстрая проверка клиента

📝 <b>2. Договор</b>
Заключаем рамочный договор на проведение цифровых расчётов

📨 <b>3. Заявка</b>
Вы оставляете заявку — фиксируем объём и параметры сделки

💳 <b>4. Оплата</b>
Средства перечисляются по безналу с расчётного счёта вашей компании

🚀 <b>5. Исполнение</b>
Проводим расчёт в согласованные сроки и объёме

📄 <b>6. Документы</b>
Предоставляем комплект закрывающих документов: договор, счёт, акт"""
        
    elif message_text == "👤 Написать менеджеру":
        response = """👤 <b>Написать менеджеру</b>

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

<b>На сайте вы найдете:</b>
• Подробную информацию об услугах
• Калькулятор курсов
• Форму для заявки
• Контактную информацию

💬 <b>Или просто напишите нашему менеджеру</b> для быстрой консультации!"""
        
    else:
        response = """❓ <b>Не понимаю ваше сообщение.</b>

Пожалуйста, используйте кнопки меню ниже или команды:
<b>/start</b> - Главное меню
<b>/help</b> - Справка"""
    
    await update.message.reply_text(
        text=response,
        parse_mode='HTML',
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет справочную информацию"""
    help_text = """🤖 <b>Команды бота:</b>

<b>/start</b> - Главное меню
<b>/help</b> - Эта справка

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
