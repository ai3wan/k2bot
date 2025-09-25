#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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
        response = """📊 <b>Бухгалтерия и налоги</b>

Наши специалисты помогут вам:
• Правильно оформить документы для сделки
• Разобраться с налогообложением криптовалют
• Подготовить отчетность для налоговой
• Оптимизировать налоговую нагрузку

💬 Для получения консультации напишите нашему менеджеру"""
        
    elif message_text == "📋 Как проходит сделка":
        response = """📋 <b>Как проходит сделка</b>

Процесс покупки USDT для бизнеса:

1️⃣ <b>Консультация</b> - обсуждение ваших потребностей
2️⃣ <b>Договор</b> - подписание официального договора
3️⃣ <b>Оплата</b> - перевод средств на наш счет
4️⃣ <b>Зачисление</b> - получение USDT на ваш кошелек
5️⃣ <b>Документы</b> - получение закрывающих документов

⚡️ Вся процедура занимает от 30 минут до 2 часов"""
        
    elif message_text == "👤 Написать менеджеру":
        response = """👤 <b>Написать менеджеру</b>

Наши менеджеры готовы ответить на все ваши вопросы:

📞 <b>Telegram:</b> @k2crypto_manager
📧 <b>Email:</b> info@k2crypto.m70.capital
☎️ <b>Телефон:</b> +7 (XXX) XXX-XX-XX

🕐 <b>Работаем:</b> 24/7
⚡️ <b>Ответим в течение:</b> 5 минут"""
        
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
