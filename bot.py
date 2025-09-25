#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
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
        [InlineKeyboardButton("📊 Бухгалтерия и налоги", callback_data="accounting")],
        [InlineKeyboardButton("📋 Как проходит сделка", callback_data="process")],
        [InlineKeyboardButton("👤 Написать менеджеру", callback_data="manager")],
        [InlineKeyboardButton("🌍 Перейти на сайт K2 Crypto", url="https://k2crypto.m70.capital/")]
    ]
    return InlineKeyboardMarkup(keyboard)

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

# Обработчик нажатий на кнопки
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки меню"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    logger.info(f"Пользователь {user.id} нажал кнопку: {query.data}")
    
    if query.data == "accounting":
        response = """📊 <b>Бухгалтерия и налоги</b>

Наши специалисты помогут вам:
• Правильно оформить документы для сделки
• Разобраться с налогообложением криптовалют
• Подготовить отчетность для налоговой
• Оптимизировать налоговую нагрузку

💬 Для получения консультации напишите нашему менеджеру"""
        
    elif query.data == "process":
        response = """📋 <b>Как проходит сделка</b>

Процесс покупки USDT для бизнеса:

1️⃣ <b>Консультация</b> - обсуждение ваших потребностей
2️⃣ <b>Договор</b> - подписание официального договора
3️⃣ <b>Оплата</b> - перевод средств на наш счет
4️⃣ <b>Зачисление</b> - получение USDT на ваш кошелек
5️⃣ <b>Документы</b> - получение закрывающих документов

⚡️ Вся процедура занимает от 30 минут до 2 часов"""
        
    elif query.data == "manager":
        response = """👤 <b>Написать менеджеру</b>

Наши менеджеры готовы ответить на все ваши вопросы:

📞 <b>Telegram:</b> @k2crypto_manager
📧 <b>Email:</b> info@k2crypto.m70.capital
☎️ <b>Телефон:</b> +7 (XXX) XXX-XX-XX

🕐 <b>Работаем:</b> 24/7
⚡️ <b>Ответим в течение:</b> 5 минут"""
        
    else:
        response = "❌ Неизвестная команда"
    
    await query.edit_message_text(
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
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Запускаем бота
    logger.info("Запуск бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
