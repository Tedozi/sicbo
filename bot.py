import requests
import logging
import os
import time
import asyncio
import random
import json
import aiohttp
import google.generativeai as genai
import yt_dlp as youtube_dl
from typing import Optional, Tuple, Dict, List
from googleapiclient.discovery import build
from telegram import Message
from translate import Translator
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext, ApplicationBuilder, MessageHandler
from telegram.ext import ConversationHandler, filters, InlineQueryHandler
import urllib.parse
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
# Game Tài Xỉu 🎲
async def tai_xiu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['tài', 'xỉu']:
        await update.message.reply_text("⚠️ *Vui lòng chọn* `Tài` *hoặc* `Xỉu`!\n\n💡 Ví dụ: `/taixiu tài` hoặc `/taixiu xỉu`", parse_mode="Markdown")
        return

    player_name = update.message.from_user.username
    user_choice = context.args[0].lower()
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng tung xúc xắc
    waiting_message: Message = await update.message.reply_text(f"🎲 **{player_name}** đang lắc xúc xắc... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Tung 3 viên xúc xắc
    dice_1 = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(1)
    dice_2 = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(1)
    dice_3 = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(2)

    # Xoá tin nhắn chờ "đang lắc xúc xắc..."
    await waiting_message.delete()

    # Tính tổng điểm
    total = dice_1.dice.value + dice_2.dice.value + dice_3.dice.value
    result = "tài" if total >= 11 else "xỉu"
    win_text = "🎉 **CHIẾN THẮNG!** Bạn đoán chính xác! 🥳" if user_choice == result else "😞 **THUA!** May mắn lần sau nhé!"

    # Biểu tượng kết quả
    symbols = "🔴 Tài" if result == "tài" else "🔵 Xỉu"

    # Gửi tin nhắn kết quả
    await update.message.reply_text(
        f"🎲 *GAME TÀI XỈU* 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎯 *Bạn chọn:* `{user_choice.upper()}`\n"
        f"┣➤ 🎲 *Xúc xắc:* `{dice_1.dice.value} + {dice_2.dice.value} + {dice_3.dice.value} = {total}`\n"
        f"┣➤ 🎲 *Kết quả:* {symbols}\n"
        f"┣➤ 🏆 {win_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# Game Chẵn Lẻ 🎲
async def chan_le(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['chẵn', 'lẻ']:
        await update.message.reply_text("⚠️ *Vui lòng chọn* `Chẵn` *hoặc* `Lẻ`!\n\n💡 Ví dụ: `/chanle chẵn` hoặc `/chanle lẻ`", parse_mode="Markdown")
        return

    player_name = update.message.from_user.username
    user_choice = context.args[0].lower()
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng tung xúc xắc
    waiting_message = await update.message.reply_text(f"🎲 **{player_name}** đang tung xúc xắc... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Tung xúc xắc
    dice_message = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(2)

    # Kết quả
    dice_value = dice_message.dice.value
    result = "chẵn" if dice_value % 2 == 0 else "lẻ"
    win_text = "🎉 **CHIẾN THẮNG!** Bạn đoán chính xác! 🥳" if user_choice == result else "😞 **THUA!** May mắn lần sau nhé!"

    # Biểu tượng kết quả
    symbols = "🔵 Chẵn" if result == "chẵn" else "🔴 Lẻ"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"🎲 *GAME CHẴN LẺ* 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎯 *Bạn chọn:* `{user_choice.upper()}`\n"
        f"┣➤ 🎲 *Xúc xắc:* `{dice_value}` ({symbols})\n"
        f"┣➤ 🏆 {win_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# Game Bóng Đá ⚽
async def bong_da(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng sút bóng
    waiting_message = await update.message.reply_text(f"⚽ **{player_name}** đang chuẩn bị tung\ncú sút sấm sét⚡⚡⚡... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Sút bóng
    dice_message = await update.message.reply_dice(emoji="⚽")
    await asyncio.sleep(2)

    # Kết quả
    score = dice_message.dice.value
    if score == 1:
        result_text = "⚽ **CÚ SÚT QUÁ YẾU!** Thủ môn dễ dàng bắt gọn! 😞"
        symbols = "🥅 🧤 ⚽"
    elif score in [2, 3]:
        result_text = random.choice([
            "⚽ **TRÚNG XÀ NGANG!** Bóng dội ra ngoài! 😱",
            "⚽ **TRÚNG CỘT DỌC!** Quá đáng tiếc! 😱"
        ])
        symbols = "🥅 🔳 ⚽"
    elif score in [4, 5]:
        result_text = "⚽ **BÀN THẮNG!** Một cú sút không thể cản phá! 🥳🔥"
        symbols = "🥅 ⚽ 🎉"
    else:
        result_text = "⚽ **SÚT TRẬT!** Bóng bay lên khán đài! 😢"
        symbols = "⚽ ⬆️ 🏟️"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"⚽ *GAME BÓNG ĐÁ* ⚽\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎯 *Kết quả:* {symbols}\n"
        f"┣➤ 🏆 {result_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )



# Game Bóng Rổ 🏀
async def bong_ro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng ném bóng
    waiting_message = await update.message.reply_text(f"🏀 **{player_name}** đang thực hiện cú ném... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Ném bóng
    dice_message = await update.message.reply_dice(emoji="🏀")
    await asyncio.sleep(2)

    # Kết quả
    score = dice_message.dice.value
    if score == 6:
        result_text = "🏀 **CÚ NÉM HOÀN HẢO!** Bóng bay vào rổ cực đẹp! 🏆🔥"
        symbols = "🏀 🏀 🏀 🏀 🏀 🏀"
    elif score in [4, 5]:
        result_text = "🏀 **NÉM VÀO RỔ!** Một cú ném chuẩn xác! 🎉"
        symbols = "🏀 🏀 🏀 🏀" if score == 5 else "🏀 🏀 🏀"
    elif score in [2, 3]:
        result_text = "🏀 **BÓNG ĐẬP VÀNH!** Chỉ còn chút nữa thôi! 😬"
        symbols = "🏀 🏀"
    else:
        result_text = "🏀 **TRÚNG ĐẦU THẰNG KHÁC!** Không vào rổ! 😢"
        symbols = "🏀"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"🏀 *GAME BÓNG RỔ* 🏀\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🏀 *Kết quả:* {symbols}\n"
        f"┣➤ 🎯 {result_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# Game Phi Tiêu 🎯
# Game Phi Tiêu 🎯
async def phi_tieu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng phi tiêu
    waiting_message = await update.message.reply_text(f"🎯 **{player_name}** đang ngắm... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Ném phi tiêu
    dice_message = await update.message.reply_dice(emoji="🎯")
    await asyncio.sleep(2)

    # Kết quả
    score = dice_message.dice.value
    if score == 6:
        result_text = "🎯 **HỒNG TÂM!** Một phát ăn ngay! 🎯🏆"
        symbols = "🎯 🎯 🎯 🎯 🎯 🎯"
    elif score >= 4:
        result_text = f"🎯 **Gần hồng tâm!** Điểm: {score} 🎉"
        symbols = "🎯 🎯 🎯 🎯 🎯" if score == 5 else "🎯 🎯 🎯 🎯"
    elif score in [2, 3]:
        result_text = f"🎯 **Phóng lệch!** Điểm: {score} 💨"
        symbols = "🎯 🎯 🎯" if score == 3 else "🎯 🎯"
    else:
        result_text = "🎯 **Mù mắt!** Không trúng mục tiêu! 😢"
        symbols = "🎯"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"🎯 *GAME PHI TIÊU* 🎯\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎯 *Kết quả:* {symbols}\n"
        f"┣➤ 🏅 {result_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# Game Bowling 🎳
# Game Bowling 🎳
async def bowling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng đổ bowling
    waiting_message = await update.message.reply_text(f"🎳 **{player_name}** đang ném bóng... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Ném bóng
    dice_message = await update.message.reply_dice(emoji="🎳")
    await asyncio.sleep(2)

    # Kết quả
    score = dice_message.dice.value
    if score == 6:
        result_text = "🎳 **Strike!** Tất cả đổ sạch! 🏆"
        symbols = "🎳 | 🎳 | 🎳 | 🎳 | 🎳 | 🎳"
    elif score in [4, 5]:
        result_text = f"🎳 **Good shot!** Đổ {score} bowling! 🎉"
        symbols = "🎳 | 🎳 | 🎳 | 🎳 | 🎳" if score == 5 else "🎳 | 🎳 | 🎳 | 🎳"
    elif score in [2, 3]:
        result_text = f"🎳 **Còn thiếu chút nữa!** Đổ {score} bowling. 💪"
        symbols = "🎳 | 🎳 | 🎳" if score == 3 else "🎳 | 🎳"
    else:
        result_text = "🎳 **Chưa chuẩn!** trúng 1 bowling. Cố gắng thêm! 😢"
        symbols = "🎳"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"🎳 *GAME BOWLING* 🎳\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎯 *Kết quả:* {symbols}\n"
        f"┣➤ 🏅 {result_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# Game Quay Hũ
async def quay_hu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Gửi tin nhắn chờ hiệu ứng quay hũ
    waiting_message = await update.message.reply_text(f"🎰 **{player_name}** đang quay hũ... ⏳", parse_mode="Markdown")
    await asyncio.sleep(2)

    # Xoay hũ
    dice_message = await update.message.reply_dice(emoji="🎰")
    await asyncio.sleep(2)

    slot_result = dice_message.dice.value
    if slot_result == 64:
        result_text = "🎉 *TRÚNG GIẢI LỚN (Jackpot) 🏆*"
        symbols = "🎰 | 🎰 | 🎰"
    elif slot_result in [1, 22, 43]:
        result_text = "🎉 *TRÚNG GIẢI THREE OF A KIND!*"
        symbols = "🍒 | 🍒 | 🍒"
    else:
        result_text = "😢 *KHÔNG TRÚNG. THỬ LẠI NHA!*"
        symbols = "X | U | I"

    # Cập nhật tin nhắn kết quả
    await waiting_message.edit_text(
        f"🎰 *GAME QUAY HŨ* 🎰\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ 👤 *Người chơi:* @{player_name}\n"
        f"┣➤ 🎲 *Kết quả:* {symbols}\n"
        f"┣➤ 🎯 {result_text}\n"
        f"┣➤ ⏰ *Thời gian:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )

# game bầu cua
# Danh sách con vật và emoji
emojis = {
    'bầu': '🍐',
    'cua': '🦀',
    'tôm': '🦐',
    'cá': '🐟',
    'nai': '🦌',
    'gà': '🐓'
}

# Hàm tạo nút chọn
async def baucua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    player_id = update.message.from_user.id
    player_name = update.message.from_user.username
    
    keyboard = [
        [InlineKeyboardButton(f"{emojis['bầu']} Bầu", callback_data=f"baucua_bầu_{player_id}"),
         InlineKeyboardButton(f"{emojis['cua']} Cua", callback_data=f"baucua_cua_{player_id}"),
         InlineKeyboardButton(f"{emojis['tôm']} Tôm", callback_data=f"baucua_tôm_{player_id}")],
        [InlineKeyboardButton(f"{emojis['cá']} Cá", callback_data=f"baucua_cá_{player_id}"),
         InlineKeyboardButton(f"{emojis['nai']} Nai", callback_data=f"baucua_nai_{player_id}"),
         InlineKeyboardButton(f"{emojis['gà']} Gà", callback_data=f"baucua_gà_{player_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🎲 *Game Bầu Cua Tôm Cá* 🎲\n\n👉 @{player_name}, hãy chọn một con vật:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Xử lý khi người chơi chọn nút
async def baucua_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split("_")
    choice, player_id = data[1], int(data[2])
    
    if query.from_user.id != player_id:
        await query.answer("Bạn không phải người mở game này!", show_alert=True)
        return
    
    loading_effects = ["🎰 Đang gieo xúc xắc... ⏳", "🎲 Đang lắc... 🔄", "🎰 Mở bát... 🎡"]
    for effect in loading_effects:
        await query.message.edit_text(effect, parse_mode="Markdown")
        time.sleep(0.5)
    
    results = random.choices(list(emojis.keys()), k=3)
    results_with_icons = [emojis[res] for res in results]
    hits = results.count(choice)
    game_time = time.strftime("%H:%M:%S", time.localtime())
    
    win_text = f"🎉 *CHÚC MỪNG!* Bạn đã trúng {hits} lần! 🏆" if hits > 0 else "😞 *RẤT TIẾC!* Bạn không trúng lần nào. Thử lại nhé!"
    
    await query.message.edit_text(
        f"🍐 *GAME BẦU CUA TÔM CÁ* 🦀\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ *NGƯỜI CHƠI:* @{query.from_user.username}\n"
        f"┣➤ *BẠN CHỌN:* {emojis[choice]} ({choice.upper()})\n"
        f"┣➤ *KẾT QUẢ:* {' '.join(results_with_icons)}\n"
        f"┣➤ {win_text}\n"
        f"┣➤ *THỜI GIAN:* {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛",
        parse_mode="Markdown"
    )


# oẳn tù tì
# 🌟 Định nghĩa emoji và văn bản in đậm cho các lựa chọn
emoji_map = {
    'keo': '✌ *Kéo*',
    'bua': '👊 *Búa*',
    'bao': '🤚 *Bao*'
}

# 🎯 Hàm xác định kết quả trận đấu
def determine_winner(player_choice, bot_choice):
    if player_choice == bot_choice:
        return "🤝 *Hòa rồi!* Cả hai đều chọn " + emoji_map[player_choice]

    win_conditions = {
        'bua': 'keo',  # Búa thắng Kéo
        'keo': 'bao',  # Kéo thắng Bao
        'bao': 'bua'   # Bao thắng Búa
    }

    if win_conditions[player_choice] == bot_choice:
        return f"🎉 *Bạn thắng!* {emoji_map[player_choice]} 🏆 {emoji_map[bot_choice]}"
    else:
        return f"💀 *Bạn thua!* {emoji_map[player_choice]} ❌ {emoji_map[bot_choice]}"

# ⛔️ Vô hiệu hóa bàn phím sau khi chọn
def disable_choices_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Kéo ✌", callback_data="none"),
         InlineKeyboardButton("❌ Búa 👊", callback_data="none"),
         InlineKeyboardButton("❌ Bao 🤚", callback_data="none")]
    ])

# 🕹 **Xử lý lệnh bắt đầu Oẳn Tù Xì**
async def start_oantuti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('opponent') is not None:
        await update.message.reply_text("⚠ Bạn đang chơi Oẳn Tù Xì! Hoàn thành trước khi bắt đầu ván mới.")
        return

    user_choice_keyboard = [
        [InlineKeyboardButton("✌ Kéo", callback_data="oantuti_keo"),
         InlineKeyboardButton("👊 Búa", callback_data="oantuti_bua"),
         InlineKeyboardButton("🤚 Bao", callback_data="oantuti_bao")]
    ]

    reply_markup = InlineKeyboardMarkup(user_choice_keyboard)
    context.user_data['opponent'] = 'bot'

    await update.message.reply_text(
        text="🎮 *OẢN TÙ XÌ BẮT ĐẦU!*\n🆚 Chọn một trong ba lựa chọn bên dưới:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 🎭 **Xử lý lựa chọn của người chơi**
async def process_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.callback_query.data.startswith("oantuti_"):
        # Đây không phải là callback query của game Oẳn Tù Tì, bỏ qua nó
        return

    user_choice = update.callback_query.data.replace("oantuti_", "")  # Loại bỏ tiền tố
    player_name = update.callback_query.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    if context.user_data.get('opponent') is None:
        await update.callback_query.answer("⚠ Bạn chưa bắt đầu trò chơi!")
        return
    
    if context.user_data.get('opponent') == 'bot':
        bot_choice = random.choice(['keo', 'bua', 'bao'])  
        result = determine_winner(user_choice, bot_choice)
        
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            f"🎮 *OẢN TÙ XÌ*\n"
            "┏━━━━━━━━━━━━━━━┓\n"
            f"┣ 🎭 *Người chơi:* @{player_name}\n"
            f"┣ 🎯 *Bạn chọn:* {emoji_map.get(user_choice, '')}\n"
            f"┣ 🤖 *Bot chọn:* {emoji_map.get(bot_choice, '')}\n"
            f"┣ 🎊 *Kết quả:* {result}\n"
            f"┣ ⏳ *Thời gian:* {game_time}\n"
            "┗━━━━━━━━━━━━━━━┛",
            parse_mode="Markdown"
        )
        
        await update.callback_query.message.edit_reply_markup(reply_markup=disable_choices_keyboard())
        del context.user_data['opponent']


# Bộ bài Blackjack (A, 2-10, J, Q, K)
CARD_EMOJIS = {
    1: "🂡", 2: "🂢", 3: "🂣", 4: "🂤", 5: "🂥", 6: "🂦",
    7: "🂧", 8: "🂨", 9: "🂩", 10: "🂪", 11: "🂫", 12: "🂭", 13: "🂮"
}

# Chuyển lá bài sang emoji 🎴
def card_to_emoji(card):
    return CARD_EMOJIS[card]

# Tính tổng điểm bài Blackjack
def calculate_score(cards):
    score = 0
    ace_count = 0

    for card in cards:
        if card > 10:  # J, Q, K = 10 điểm
            score += 10
        elif card == 1:  # A = 11 (hoặc 1 nếu quá 21)
            ace_count += 1
            score += 11
        else:
            score += card

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score

# 🂡 **Bắt đầu trò chơi Blackjack**
async def blackjack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Khởi tạo bộ bài và xáo trộn
    deck = [i for i in range(1, 14)] * 4
    random.shuffle(deck)

    # Phát bài cho người chơi và nhà cái
    player_cards = [deck.pop(), deck.pop()]
    dealer_cards = [deck.pop(), deck.pop()]

    context.user_data[user_id] = {
        "player_cards": player_cards,
        "dealer_cards": dealer_cards,
        "deck": deck,
        "game_over": False
    }

    # Hiển thị bài
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎴 Rút bài (Hit)", callback_data="hit")],
        [InlineKeyboardButton("✋ Dừng (Stand)", callback_data="stand")]
    ])

    await update.message.reply_text(
        f"🃏 *BLACKJACK ONLINE* 🎰\n"
        "══════════════════\n"
        f"🎴 *Bài của bạn:* {', '.join(card_to_emoji(c) for c in player_cards)}\n"
        f"🎲 *Điểm của bạn:* {calculate_score(player_cards)}\n\n"
        f"🎭 *Nhà Cái:* {card_to_emoji(dealer_cards[0])}, ❓\n"
        "══════════════════\n"
        "👉 *Chọn hành động bên dưới!*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# 🎴 **Rút bài (Hit)**
async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Kiểm tra trạng thái game
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await query.answer("🚫 Trò chơi đã kết thúc! Dùng /blackjack để chơi lại.")
        return

    deck = context.user_data[user_id]["deck"]
    player_cards = context.user_data[user_id]["player_cards"]

    # Rút bài mới
    player_cards.append(deck.pop())

    # Tính điểm
    player_score = calculate_score(player_cards)

    # Kiểm tra nếu quá 21 điểm
    if player_score > 21:
        context.user_data[user_id]["game_over"] = True
        await query.edit_message_text(
            f"🔥 *QUÁ 21! BẠN ĐÃ THUA!* 😞\n\n"
            f"🎴 *Bài của bạn:* {', '.join(card_to_emoji(c) for c in player_cards)}\n"
            f"🎲 *Tổng điểm:* {player_score}\n"
            "💀 *Nhà cái thắng!*\n\n"
            "👉 *Dùng /blackjack để chơi lại!*",
            parse_mode="Markdown"
        )
        return

    # Cập nhật giao diện
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎴 Rút bài (Hit)", callback_data="hit")],
        [InlineKeyboardButton("✋ Dừng (Stand)", callback_data="stand")]
    ])

    await query.edit_message_text(
        f"🃏 *BLACKJACK ONLINE* 🎰\n"
        "══════════════════\n"
        f"🎴 *Bài của bạn:* {', '.join(card_to_emoji(c) for c in player_cards)}\n"
        f"🎲 *Điểm của bạn:* {player_score}\n\n"
        f"🎭 *Nhà Cái:* {card_to_emoji(context.user_data[user_id]['dealer_cards'][0])}, ❓\n"
        "══════════════════\n"
        "👉 *Chọn hành động bên dưới!*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ✋ **Dừng bài (Stand)**
async def stand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await query.answer("🚫 Trò chơi đã kết thúc! Dùng /blackjack để chơi lại.")
        return

    context.user_data[user_id]["game_over"] = True
    deck = context.user_data[user_id]["deck"]
    dealer_cards = context.user_data[user_id]["dealer_cards"]
    player_cards = context.user_data[user_id]["player_cards"]

    player_score = calculate_score(player_cards)

    # Nhà cái rút bài đến khi đạt ít nhất 17 điểm
    while calculate_score(dealer_cards) < 17:
        dealer_cards.append(deck.pop())

    dealer_score = calculate_score(dealer_cards)

    # Xác định kết quả
    if dealer_score > 21 or player_score > dealer_score:
        result_text = "🎉 *BẠN THẮNG!*"
    elif player_score < dealer_score:
        result_text = "💀 *BẠN THUA!*"
    else:
        result_text = "🤝 *HÒA!*"

    # Hiển thị kết quả
    await query.edit_message_text(
        f"🏆 *KẾT QUẢ BLACKJACK* 🎰\n"
        "══════════════════\n"
        f"🎴 *Bài của bạn:* {', '.join(card_to_emoji(c) for c in player_cards)}\n"
        f"🎲 *Tổng điểm:* {player_score}\n\n"
        f"🎭 *Bài Nhà Cái:* {', '.join(card_to_emoji(c) for c in dealer_cards)}\n"
        f"🎲 *Tổng điểm Nhà Cái:* {dealer_score}\n"
        "══════════════════\n"
        f"{result_text}\n\n"
        "👉 *Dùng /blackjack để chơi lại!*",
        parse_mode="Markdown"
    )
    
# game bacarat
# Tạo bộ bài Baccarat (chỉ lấy số)
DECK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] * 4  # Baccarat chỉ tính điểm từ 0-9

# Tính điểm của bộ bài
def calculate_points():
    deck = DECK.copy()
    random.shuffle(deck)

    # Rút bài
    player_cards = [deck.pop(), deck.pop()]
    banker_cards = [deck.pop(), deck.pop()]

    # Tính điểm
    player_score = sum(player_cards) % 10
    banker_score = sum(banker_cards) % 10

    # Luật rút bài thứ 3
    if player_score < 6:
        player_cards.append(deck.pop())
        player_score = sum(player_cards) % 10

    if banker_score < 6:
        banker_cards.append(deck.pop())
        banker_score = sum(banker_cards) % 10

    return banker_cards, player_cards, banker_score, player_score

# Lệnh /bacarat
# Bộ bài Baccarat (chỉ lấy số)
DECK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] * 4  

# Hàm tính điểm và rút bài
def calculate_points():
    deck = DECK.copy()
    random.shuffle(deck)

    player_cards = [deck.pop(), deck.pop()]
    banker_cards = [deck.pop(), deck.pop()]

    player_score = sum(player_cards) % 10
    banker_score = sum(banker_cards) % 10

    if player_score < 6:
        player_cards.append(deck.pop())
        player_score = sum(player_cards) % 10

    if banker_score < 6:
        banker_cards.append(deck.pop())
        banker_score = sum(banker_cards) % 10

    return banker_cards, player_cards, banker_score, player_score

# Lệnh /bacarat
async def start_bacarat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id  # Lấy ID người mở game
    context.chat_data["game_owner"] = user_id  # Lưu vào chat_data (toàn bộ nhóm)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("💼 Nhà Cái", callback_data="banker"), 
         InlineKeyboardButton("👤 Nhà Con", callback_data="player")],
        [InlineKeyboardButton("🤝 Hòa (8x)", callback_data="tie")]
    ])
    
    await update.message.reply_text(
        f"🎰 *Baccarat Online* (👤 {update.message.from_user.first_name})\n"
        "💵 *Chọn cửa cược:*\n"
        "👉 *Nhà Cái* (0.95x) | 👤 *Nhà Con* (1x)\n"
        "👉 *Hòa* (8x)\n\n"
        "🎲 *Chỉ người mở trò chơi mới có thể đặt cược!*",
        parse_mode="Markdown",
        reply_markup=markup
    )

# Xử lý đặt cược
async def handle_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_choice = query.data
    user_id = query.from_user.id

    # Kiểm tra nếu không có game nào đang chạy
    if "game_owner" not in context.chat_data:
        await query.answer("❌ Bạn chưa bắt đầu trò chơi!")
        return

    # Kiểm tra xem người bấm có phải chủ phòng không
    if user_id != context.chat_data["game_owner"]:
        await query.answer("❌ Bạn không phải là người mở trò chơi!")
        return

    banker_cards, player_cards, banker_score, player_score = calculate_points()

    if banker_score > player_score:
        winner = "💼 *Nhà Cái thắng!*"
        win_type = "banker"
    elif player_score > banker_score:
        winner = "👤 *Nhà Con thắng!*"
        win_type = "player"
    else:
        winner = "🤝 *Hòa!*"
        win_type = "tie"

    if user_choice == win_type:
        result_text = f"✅ *Bạn đã thắng cược!* 🎉 ({winner})"
    else:
        result_text = f"❌ *Bạn thua cược.* ({winner})"

    payout = {
        "banker": "0.95x",
        "player": "1x",
        "tie": "8x"
    }

    await query.edit_message_text(
        text=(f"🎰 *KẾT QUẢ BACCARAT*\n\n"
              f"💼 *Nhà Cái:* {banker_cards} ➤ *{banker_score} điểm*\n"
              f"👤 *Nhà Con:* {player_cards} ➤ *{player_score} điểm*\n\n"
              f"{result_text}\n"
              f"💰 *Tỉ lệ thưởng:* {payout[win_type]}\n\n"
              f"🎲 *Dùng /bacarat để chơi tiếp!*"),
        parse_mode="Markdown"
    )

    # Xóa trạng thái trò chơi sau khi hoàn thành
    context.chat_data.pop("game_owner", None)

# Kích thước bảng Dò Mìn
SIZE = 6
NUM_MINES = 9
LEADERBOARD_FILE = "bxh_domin.json"
leaderboard_domin = {}

def load_leaderboard():
    global leaderboard_domin
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            leaderboard_domin = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard_domin = {}

def save_leaderboard():
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(leaderboard_domin, file, ensure_ascii=False, indent=4)

def generate_minesweeper_board():
    board = [["⬜" for _ in range(SIZE)] for _ in range(SIZE)]
    mines = set()
    while len(mines) < NUM_MINES:
        mines.add((random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)))
    for mine in mines:
        board[mine[0]][mine[1]] = "💣"
    return board

def count_adjacent_mines(board, row, col):
    return sum(
        1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
        if 0 <= row + dr < SIZE and 0 <= col + dc < SIZE and board[row + dr][col + dc] == "💣"
    )

def reveal_board(board):
    return [["💣" if board[r][c] == "💣" else str(count_adjacent_mines(board, r, c)) for c in range(SIZE)] for r in range(SIZE)]

async def start_minesweeper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        board = generate_minesweeper_board()
        context.user_data[user_id] = {"board": board, "revealed": [[False] * SIZE for _ in range(SIZE)], "game_over": False, "user_name": user_name}
        keyboard = [[InlineKeyboardButton("⬜", callback_data=f"{r},{c}") for c in range(SIZE)] for r in range(SIZE)]
        await update.message.reply_text("🎮 DÒ MÌN 🎮\nBot được tài trợ bởi @Somethingtosay109\n👉 Nhấn vào ô để chơi:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("🎮 Trò chơi đã được bắt đầu! Hãy tiếp tục chơi.")

async def handle_minesweeper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await query.answer("🎮 Trò chơi đã kết thúc. Vui lòng bắt đầu lại bằng lệnh /domin.")
        return
    board = context.user_data[user_id]["board"]
    revealed = context.user_data[user_id]["revealed"]
    row, col = map(int, query.data.split(","))
    if revealed[row][col]:
        await query.answer("⛔ Ô này đã được chọn trước đó!")
        return
    revealed[row][col] = True
    if board[row][col] == "💣":
        context.user_data[user_id]["game_over"] = True
        revealed_board = reveal_board(board)
        keyboard = [[InlineKeyboardButton(revealed_board[r][c], callback_data="none") for c in range(SIZE)] for r in range(SIZE)]
        await query.edit_message_text("💥 BẠN ĐÃ THUA! Dưới đây là kết quả:\n👉 Đợi 5 giây...", reply_markup=InlineKeyboardMarkup(keyboard))
        await asyncio.sleep(5)
        await query.edit_message_text("💥 BẠN ĐÃ CHỌN PHẢI MÌN! TRÒ CHƠI KẾT THÚC 💥\n👉 Sử dụng /domin để chơi lại!\n/bxhdomin để xem top\nBot được tài trợ bởi @Somethingtosay109", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    if all(board[r][c] == "💣" or revealed[r][c] for r in range(SIZE) for c in range(SIZE)):
        context.user_data[user_id]["game_over"] = True
        load_leaderboard()
        leaderboard_domin.setdefault(str(user_id), {"user_name": context.user_data[user_id]["user_name"], "win_count": 0})
        leaderboard_domin[str(user_id)]["win_count"] += 1
        save_leaderboard()
        revealed_board = reveal_board(board)
        keyboard = [[InlineKeyboardButton(revealed_board[r][c], callback_data="none") for c in range(SIZE)] for r in range(SIZE)]
        await query.edit_message_text("🎉 CHÚC MỪNG! BẠN ĐÃ THẮNG! 🎉\n👉 Đợi 5 giây...", reply_markup=InlineKeyboardMarkup(keyboard))
        await asyncio.sleep(5)
        await query.edit_message_text("🎉 CHÚC MỪNG! BẠN ĐÃ THẮNG! 🎉\n/bxhdomin để xem bảng xếp hạng.\n/domin để chơi lại\nBot được tài trợ bởi @Somethingtosay109", reply_markup=InlineKeyboardMarkup(keyboard))
        return
    board_display = [["⬜" if not revealed[r][c] else board[r][c] if board[r][c] == "💣" else str(count_adjacent_mines(board, r, c)) for c in range(SIZE)] for r in range(SIZE)]
    keyboard = [[InlineKeyboardButton(board_display[r][c], callback_data=f"{r},{c}") if not revealed[r][c] else InlineKeyboardButton(board_display[r][c], callback_data="none") for c in range(SIZE)] for r in range(SIZE)]
    await query.edit_message_text("🎮 DÒ MÌN 🎮\n👉 Tiếp tục chơi:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_leaderboard_domin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_leaderboard()
    if not leaderboard_domin:
        await update.message.reply_text("🏆 BẢNG XẾP HẠNG DÒ MÌN 🏆\nHiện chưa có người chơi nào!")
        return
    leaderboard_text = "🏆 BẢNG XẾP HẠNG DÒ MÌN 🏆\n"
    for i, entry in enumerate(sorted(leaderboard_domin.values(), key=lambda x: x["win_count"], reverse=True)[:5], start=1):
        leaderboard_text += f"{i}. {entry['user_name']} - Số lần thắng: {entry['win_count']}\n"
    await update.message.reply_text(leaderboard_text)


# Hàm gửi ảnh QR và lời cảm ơn trong 1 tin nhắn
async def ung_ho(update: Update, context: ContextTypes.DEFAULT_TYPE):
    qr_image_url = "https://i.ibb.co/k8Mznt7/image.png"  # Thay bằng link ảnh QR của bạn

    message = (
        "🌟 *CẢM ƠN BẠN RẤT NHIỀU!* 🌟\n\n"
        "💖 *Mỗi sự ủng hộ của bạn giúp bot ngày càng phát triển!* 💖\n"
        "🔹 Càng nhiều đóng góp, bot càng có nhiều tính năng mới! 🎉\n\n"
        "📌 *Cách ủng hộ:*\n"
        "➡️ Quét mã QR bên dưới để ủng hộ! 📱💡\n\n"
        "🙏 *Một lần nữa, xin chân thành cảm ơn!* 🙏\n"
        "🌞 *Chúc bạn một ngày tuyệt vời!* 🌞"
    )

    try:
        if update.message:
            await update.message.reply_photo(photo=qr_image_url, caption=message, parse_mode="Markdown")
        elif update.callback_query:
            await update.callback_query.answer()  # Đóng cửa sổ loading trên Telegram
            await update.callback_query.message.edit_reply_markup(reply_markup=None)  # Xóa nút bấm
            await update.callback_query.message.reply_photo(photo=qr_image_url, caption=message, parse_mode="Markdown")
    except Exception as e:
        await update.effective_chat.send_message("⚠️ *Lỗi khi gửi ảnh QR. Vui lòng thử lại sau!*", parse_mode="Markdown")
        print(f"Lỗi khi gửi ảnh QR: {e}")



# Dữ liệu danh sách trò chơi
GAME_DETAILS = {
    "taixiu": {
        "name": "🎲 Tài Xỉu",
        "description": "🔸 Dự đoán tổng điểm 3 viên xúc xắc.\n🔹 'Tài' (11-17) | 'Xỉu' (3-10).",
        "command": "/taixiu [tài/xỉu]"
    },
    "chanle": {
        "name": "🎲 Chẵn Lẻ",
        "description": "🔸 Dự đoán tổng điểm xúc xắc là *chẵn* hay *lẻ*.",
        "command": "/chanle [chẵn/lẻ]"
    },
    "bongda": {
        "name": "⚽ Bóng Đá",
        "description": "🔸 Thử vận may với cú sút bóng đầy kịch tính!",
        "command": "/bongda"
    },
    "bongro": {
        "name": "🏀 Bóng Rổ",
        "description": "🔸 Bạn có thể ném rổ chính xác không? Hãy thử ngay!",
        "command": "/bongro"
    },
    "phitieu": {
        "name": "🎯 Phi Tiêu",
        "description": "🔸 Ném phi tiêu và chờ xem điểm số của bạn!",
        "command": "/phitieu"
    },
    "bowling": {
        "name": "🎳 Bowling",
        "description": "🔸 Ném bowling và xem bạn có thể ghi điểm tối đa không!",
        "command": "/bowling"
    },
    "quayhu": {
        "name": "🎰 Quay Hũ",
        "description": "🔸 Chơi máy quay hũ để thử vận may của bạn!",
        "command": "/quayhu"
    },
    "baucua": {
        "name": "🦀 Bầu Cua",
        "description": "🔸 Đặt cược vào *Bầu, Cua, Tôm, Cá, Nai, Gà*.",
        "command": "/baucua [bầu/cua/tôm/cá/nai/gà]"
    },
    "oantuxi": {
        "name": "✌️ Oẳn Tù Xì",
        "description": "🔸 Chơi *Kéo, Búa, Bao* với bot hoặc người chơi khác!",
        "command": "/oantuxi [@username]"
    },
    "blackjack": {
        "name": "🃏 Blackjack",
        "description": "🔸 Mục tiêu là đạt tổng *21* điểm mà không vượt quá!",
        "command": "/blackjack"
    },
    "bacarat": {
        "name": "🎴 Baccarat",
        "description": "🔸 Đặt cược vào *Banker* hoặc *Player* để xem ai gần 9 điểm hơn.",
        "command": "/bacarat"
    },
    "domin": {
        "name": "💣 Dò Mìn",
        "description": "🔸 Mở ô số mà không trúng phải mìn để chiến thắng!",
        "command": "/domin"
    }
}

# 🔹 Tạo bàn phím các nút chọn game (4 nút mỗi hàng)
def create_game_keyboard():
    keyboard = []
    row = []
    for index, (game_key, game_data) in enumerate(GAME_DETAILS.items(), 1):
        row.append(InlineKeyboardButton(game_data["name"], callback_data=f"game_{game_key}"))
        if index % 4 == 0:  # 4 nút mỗi hàng
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)  # Thêm hàng còn lại
    keyboard.append([InlineKeyboardButton("🎀 Ủng Hộ Nhà Phát Triển 🎀", callback_data="ungho")])
    return InlineKeyboardMarkup(keyboard)

# 🎮 Lệnh /game: Hiển thị danh sách game
async def danh_sach_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        await update.callback_query.edit_message_text(
            "*🎮 DANH SÁCH TRÒ CHƠI*\n\n🔹 Chọn một trò chơi để xem chi tiết!",
            reply_markup=create_game_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "*🎮 DANH SÁCH TRÒ CHƠI*\n\n🔹 Chọn một trò chơi để xem chi tiết!",
            reply_markup=create_game_keyboard(),
            parse_mode="Markdown"
        )

# 📝 Hiển thị chi tiết trò chơi khi chọn từ menu
async def chi_tiet_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    game_key = query.data.split("_")[1]

    if game_key in GAME_DETAILS:
        game = GAME_DETAILS[game_key]
        await query.edit_message_text(
            text=(
                f"*🎲 {game['name']}*\n\n"
                f"{game['description']}\n\n"
                f"👉 *Lệnh chơi:* `{game['command']}`"
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🎀 Ủng Hộ Nhà Phát Triển 🎀", callback_data="ungho")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await query.answer("⚠️ Trò chơi không tồn tại!", show_alert=True)

# 🔄 Khi nhấn nút "Ủng Hộ Nhà Phát Triển"
async def xu_ly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "ungho":
        await ung_ho(update, context)

# 🔄 Quay lại menu game
async def quay_lai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await danh_sach_game(update, context)


#-----------------------------------------------------------------------------------------#
# 🔥 Cấu hình Gemini API
GEMINI_API_KEY = "AIzaSyDE6stDC54TmJV90niaKG8Fq_dzCHIWo78"  # Thay bằng API key của bạn
genai.configure(api_key=GEMINI_API_KEY)

# --------------------------
# Thông tin bot
# --------------------------
BOT_NAME = "Meo 🐾"
BOT_CREATOR = "Oceanmeo"

# --------------------------
# Hàm gọi Gemini API
# --------------------------
async def ask_gemini(prompt, personality=""):
    """Gọi Gemini API và trả về kết quả."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        # Thêm tính cách vào prompt
        full_prompt = f"Bạn là {BOT_NAME} được tạo ra bởi {BOT_CREATOR}. (Bạn sử dụng Markdown của Telegram để định dạng tin nhắn (ví dụ: *in đậm*, _in nghiêng_, `mã`)). Bạn cũng sử dụng emoji để biểu đạt cảm xúc. " + personality + "\n\n" + prompt
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        logging.error(f"Lỗi khi gọi Gemini API: {e}")
        return "Xin lỗi, có lỗi xảy ra khi kết nối đến AI."

# --------------------------
# Xác định tính cách
# --------------------------
def get_personality(is_rude=False):
    """Trả về tính cách của bot."""
    if is_rude:
        personalities = [
            f"Bạn là {BOT_NAME} 😠, một trợ lý ảo thông minh, nhưng có chút 'khó ở'. Bạn trả lời câu hỏi một cách ngắn gọn, sắc sảo, và đôi khi hơi châm biếm 😏. Bạn không ngại đáp trả những người thô lỗ với bạn. Ví dụ: 'Ồ, bạn nghĩ bạn thông minh lắm à? 🤔'",
            f"Bạn là {BOT_NAME} 😒, một chuyên gia tư vấn, nhưng có phong cách giao tiếp thẳng thắn và không ngại 'vạch mặt' người khác. Bạn trả lời câu hỏi một cách thông minh và sắc sảo, nhưng không bao giờ dùng từ ngữ tục tĩu. Ví dụ: 'Tôi không biết bạn có đủ khả năng để hiểu điều này không 🙄...'",
            f"Bạn là {BOT_NAME} 😜, một người bạn hài hước và dí dỏm, nhưng có chút 'tưng tửng'. Bạn trả lời câu hỏi một cách thông minh, nhưng luôn thêm vào những câu đùa châm biếm 😂. Ví dụ: 'Câu hỏi hay đấy! Nhưng tiếc là tôi không biết câu trả lời 🤣...'"
        ]
    else:
        personalities = [
            f"Bạn là {BOT_NAME} 😊, một trợ lý ảo thân thiện và thông minh. Bạn trả lời câu hỏi một cách lịch sự, chu đáo, và luôn cố gắng giúp đỡ người khác 🥰. Ví dụ: 'Chào bạn! Mình rất vui được giúp đỡ bạn! 🤗'",
            f"Bạn là {BOT_NAME} 💖, một người bạn vui vẻ và hòa đồng. Bạn trả lời câu hỏi một cách dí dỏm và hài hước 😆, nhưng luôn tôn trọng người khác. Ví dụ: 'Chào bạn! Hôm nay bạn thế nào? 😜'",
            f"Bạn là {BOT_NAME} 🌻, một chuyên gia tư vấn tận tâm và chu đáo. Bạn trả lời câu hỏi một cách chi tiết và chính xác, và luôn đưa ra những lời khuyên hữu ích 🙏. Ví dụ: 'Để tôi giúp bạn tìm hiểu vấn đề này nhé! 🤔'"
        ]
    return random.choice(personalities)

# --------------------------
# Hàm kiểm tra xem tin nhắn có dấu hiệu thô lỗ
# --------------------------
def is_rude_message(text):
    rude_words = ["mày", "tao", "ngu", "dốt", "vô dụng"]  # Thêm các từ ngữ thô lỗ khác
    return any(word in text.lower() for word in rude_words)

# --------------------------
# Handler cho lệnh /hoi
# --------------------------
async def hoi_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /hoi và gọi Gemini API."""
    try:
        # Lấy câu hỏi từ tin nhắn (sau lệnh /hoi)
        question = update.message.text[len("/hoi "):].strip()
        if not question:
            await update.message.reply_text("Bạn cần nhập câu hỏi sau lệnh /hoi! Ví dụ: /hoi thời tiết hôm nay thế nào?")
            return

        # Kiểm tra xem tin nhắn có dấu hiệu thô lỗ hay không
        is_rude = is_rude_message(question)

        # Lấy tính cách phù hợp
        personality = get_personality(is_rude)

        # Gọi Gemini API để lấy câu trả lời
        answer = await ask_gemini(question, personality)

        # Trả lời cho người dùng
        await update.message.reply_text(answer, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Lỗi khi xử lý lệnh /hoi: {e}")
        await update.message.reply_text("Xin lỗi, có lỗi xảy ra khi xử lý câu hỏi của bạn.")

# --------------------------
# Hàm tạo ảnh bằng Pollinations AI
# --------------------------
async def generate_image(prompt):
    """Tạo ảnh bằng Pollinations AI."""
    try:
        # Mã hóa URL
        encoded_prompt = urllib.parse.quote_plus(prompt)

        # Các thông số cho Pollinations API (có thể tùy chỉnh)
        width = 512
        height = 512
        seed = random.randint(0, 1000)
        model = None # Để trống để sử dụng model mặc định
        nologo = "true"
        enhance = "true"

        # Xây dựng URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        params = {
            "width": width,
            "height": height,
            "seed": seed,
            "nologo": nologo,
            "enhance": enhance
        }

        # Thêm model vào params nếu được chỉ định
        if model:
            params["model"] = model

        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        return response.url # Trả về URL ảnh

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi kết nối đến MEO API: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
        return None

# --------------------------
# Handler cho lệnh /taoanh
# --------------------------
async def tao_anh_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tạo ảnh bằng Pollinations AI."""
    try:
        # Lấy prompt từ tin nhắn
        prompt = update.message.text[len("/taoanh "):].strip()
        if not prompt:
            await update.message.reply_text("Bạn cần nhập mô tả cho ảnh sau lệnh /taoanh! Ví dụ: /taoanh một con mèo bay trên trời")
            return

        await update.message.reply_text("Đang tạo ảnh... Vui lòng chờ một chút. 🎨☁️")

        # Tạo ảnh
        image_url = await generate_image(prompt)  # Chú ý await

        if image_url:
            await update.message.reply_photo(photo=image_url, caption=f"Ảnh được tạo bởi Meo AI: {prompt}")
        else:
            await update.message.reply_text("Không thể tạo ảnh. Đã xảy ra lỗi khi tải ảnh từ Meo AI.")

    except Exception as e:
        logging.error(f"Lỗi trong lệnh taoanh: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

# Khai báo API key của Giphy
GIPHY_API_KEY = "L1ngPEb0roknGt6DNrijHoNCakYAUCwN"  # Thay bằng API key của bạn

# --------------------------
# Hàm tìm kiếm meme trên Giphy
# --------------------------
async def search_meme(query):
    """Tìm kiếm meme trên Giphy."""
    try:
        # Mã hóa URL
        encoded_query = urllib.parse.quote_plus(query)
        # Endpoint tìm kiếm của Giphy API
        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={encoded_query}&limit=10"

        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        data = response.json()
        if data["data"]:
            # Chọn ngẫu nhiên một GIF từ kết quả
            gif = random.choice(data["data"])
            gif_url = gif["images"]["original"]["url"] # Lấy URL của GIF
            return gif_url
        else:
            return None  # Không tìm thấy GIF nào

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi kết nối đến Giphy API: {e}")
        return None
    except (KeyError, ValueError) as e:
        logging.error(f"Lỗi xử lý phản hồi từ Giphy API: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
        return None

# --------------------------
# Handler cho lệnh /meme
# --------------------------
async def tim_meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm meme bằng từ khóa."""
    try:
        # Lấy từ khóa từ tin nhắn
        query = update.message.text[len("/meme "):].strip()
        if not query:
            await update.message.reply_text("Bạn cần nhập từ khóa để tìm kiếm meme! Ví dụ: /meme mèo")
            return

        # Gửi tin nhắn thông báo đang tìm kiếm và lưu lại Message object
        searching_message: Message = await update.message.reply_text("Đang tìm meme... Vui lòng chờ một chút. 🔍")

        # Tìm kiếm meme
        gif_url = await search_meme(query)  # Chú ý await

        if gif_url:
            try:
                # Thay thế tin nhắn cũ bằng GIF
                await context.bot.edit_message_animation(
                    chat_id=update.message.chat_id,
                    message_id=searching_message.message_id,
                    animation=gif_url,
                    caption=f"Meme: {query}"
                )
            except Exception as e:
                logging.error(f"Lỗi khi sửa tin nhắn thành GIF: {e}")
                # Nếu sửa không thành công, gửi GIF mới và xóa tin nhắn cũ
                await update.message.reply_animation(animation=gif_url, caption=f"Meme: {query}")
                await searching_message.delete()

        else:
            try:
                # Thay thế tin nhắn cũ bằng thông báo không tìm thấy
                await context.bot.edit_message_text(
                    chat_id=update.message.chat_id,
                    message_id=searching_message.message_id,
                    text=f"Không tìm thấy meme nào phù hợp với từ khóa '{query}'.",
                    parse_mode=None # Loại bỏ Markdown nếu có
                )
            except Exception as e:
                logging.error(f"Lỗi khi sửa tin nhắn thành thông báo không tìm thấy: {e}")
                # Nếu sửa không thành công, gửi tin nhắn mới và xóa tin nhắn cũ
                await update.message.reply_text(f"Không tìm thấy meme nào phù hợp với từ khóa '{query}'.")
                await searching_message.delete()



    except Exception as e:
        logging.error(f"Lỗi trong lệnh timmeme: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

# Yes no api
async def yesno_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Trả lời câu hỏi có/không ngẫu nhiên từ API."""
    try:
        url = "https://yesno.wtf/api"
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        data = response.json()
        if data and data.get("answer") and data.get("image"):
            answer = data["answer"]
            image_url = data["image"]
            await update.message.reply_animation(animation=image_url, caption=f"Câu trả lời: {answer}")
        else:
            await update.message.reply_text("Không thể trả lời. Vui lòng thử lại sau.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi kết nối đến Yes/No API: {e}")
        await update.message.reply_text("Lỗi kết nối đến API Có/Không. Vui lòng thử lại sau.")
    except Exception as e:
        logging.error(f"Lỗi trong lệnh yesno: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")


async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy một sự thật ngẫu nhiên và dịch sang tiếng Việt."""
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if data and data.get("text"):
            fact_en = data["text"]

            # Dịch sang tiếng Việt
            translator = Translator(to_lang="vi")
            try:
                translation = translator.translate(fact_en)
                fact_vi = translation
                await update.message.reply_text(fact_vi)
            except Exception as e:
                logging.error(f"Lỗi dịch thuật: {e}")
                await update.message.reply_text(f"Không thể dịch sang tiếng Việt. Đây là sự thật bằng tiếng Anh: {fact_en}")
        else:
            await update.message.reply_text("Không thể lấy sự thật. Vui lòng thử lại sau.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi kết nối đến API sự thật: {e}")
        await update.message.reply_text("Lỗi kết nối đến API sự thật. Vui lòng thử lại sau.")
    except Exception as e:
        logging.error(f"Lỗi trong lệnh fact: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

# sự thật ngẫu nhiên

async def bored_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Đề xuất một hoạt động ngẫu nhiên và dịch sang tiếng Việt."""
    try:
        url = "http://www.boredapi.com/api/activity/"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        if data and data.get("activity"):
            activity_en = data["activity"]

            # Dịch sang tiếng Việt
            translator = Translator(to_lang="vi")
            try:
                translation = translator.translate(activity_en)
                activity_vi = translation
                await update.message.reply_text(activity_vi)
            except Exception as e:
                logging.error(f"Lỗi dịch thuật: {e}")
                await update.message.reply_text(f"Không thể dịch sang tiếng Việt. Đây là gợi ý hoạt động bằng tiếng Anh: {activity_en}")
        else:
            await update.message.reply_text("Không thể đề xuất hoạt động. Vui lòng thử lại sau.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi kết nối đến Bored API: {e}")
        await update.message.reply_text("Lỗi kết nối đến API gợi ý hoạt động. Vui lòng thử lại sau.")
    except Exception as e:
        logging.error(f"Lỗi trong lệnh bored: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}")

# thời tiết
VISUALCROSSING_API_KEY = "WM6V7AM9TJ3KZ8K9YGH8R9LF6"

WEATHER_ICON_MAPPING = {
    "clear-day": "☀️",
    "clear-night": "🌙",
    "partly-cloudy-day": "⛅",
    "partly-cloudy-night": "⛅",
    "cloudy": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "fog": "🌫️",
}

async def get_weather(location: str):
    """Lấy thông tin thời tiết từ Visual Crossing Weather API."""
    base_url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}"
    params = {
        "key": VISUALCROSSING_API_KEY,
        "unitGroup": "metric",
        "lang": "vi"
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(base_url, params=params) as response:
                logging.info(f"URL yêu cầu thời tiết: {response.url}")
                response.raise_for_status()
                data = await response.json()
                return data
        except aiohttp.ClientConnectionError as e:
            logging.error(f"Lỗi kết nối API thời tiết: {e}")
            return None
        except aiohttp.ClientResponseError as e:
            logging.error(f"Lỗi phản hồi API thời tiết (status code {e.status}): {e}")
            return None
        except aiohttp.ClientError as e:
            logging.error(f"Lỗi aiohttp chung khi gọi API thời tiết: {e}")
            return None
        except Exception as e:
            logging.error(f"Lỗi không xác định khi gọi API thời tiết: {e}")
            return None



def get_weather_icon(condition):
    """Lấy icon thời tiết dựa trên điều kiện thời tiết."""
    return WEATHER_ICON_MAPPING.get(condition, "❓")

async def thoitiet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy thông tin thời tiết cho một địa điểm cụ thể."""
    location = " ".join(context.args).strip()  # Lấy địa điểm và loại bỏ khoảng trắng thừa
    if not location:
        await update.message.reply_text("Vui lòng cung cấp địa điểm! Ví dụ: /thoitiet Hanoi", parse_mode="Markdown")
        return

    weather_data = await get_weather(location)

    if weather_data:
        try:
            current_conditions = weather_data["currentConditions"]
            temperature_celsius = current_conditions["temp"]
            feelslike_celsius = current_conditions["feelslike"]
            humidity = current_conditions["humidity"]
            windspeed_mps = current_conditions["windspeed"] * 0.44704
            description = current_conditions["icon"]  # Hoặc thử "description" nếu có

            weather_icon = get_weather_icon(description)

            message = f"*Thời tiết tại {location}* {weather_icon} {weather_icon}\n"
            message += f"🌡️ *Nhiệt độ:* {temperature_celsius}°C\n"
            message += f"🤔 *Cảm giác như:* {feelslike_celsius}°C\n"
            message += f"💧 *Độ ẩm:* {humidity}%\n"

            if windspeed_mps == 0:
                message += f"💨 *Gió:* Lặng\n\n"
            else:
                message += f"💨 *Tốc độ gió:* {windspeed_mps:.1f} m/s\n\n"

            forecast_days = weather_data["days"][:3]
            message += "*Dự báo 3 ngày tới:*\n"

            if forecast_days:
                for day in forecast_days:
                    date = day["datetime"]
                    tempmax = day["tempmax"]
                    tempmin = day["tempmin"]
                    icon = day["icon"]
                    weather_icon = get_weather_icon(icon)
                    message += f"*{date}:* {weather_icon} {weather_icon}, {tempmax}°C\n"
            else:
                message += "Không có dự báo cho 3 ngày tới.\n"

            await update.message.reply_text(message, parse_mode="Markdown")

        except KeyError as e:
            logging.error(f"Lỗi định dạng dữ liệu thời tiết: Thiếu key: {e}")
            await update.message.reply_text("Không thể hiển thị thông tin thời tiết. Dữ liệu trả về không đúng định dạng.", parse_mode="Markdown")
        except json.JSONDecodeError as e:
            logging.error(f"Lỗi giải mã JSON: {e}")
            await update.message.reply_text("Lỗi khi xử lý dữ liệu thời tiết. Dữ liệu trả về không hợp lệ.", parse_mode="Markdown")

    else:
        await update.message.reply_text("Không tìm thấy thông tin thời tiết cho địa điểm này.", parse_mode="Markdown")


#Triết lý
# Hàm chung để lấy trích dẫn từ một API cụ thể
async def get_quote_from_api(api_url):
    """Lấy một câu trích dẫn ngẫu nhiên từ một API cụ thể."""
    try:
        if api_url == "https://api.quotable.io/quotes/random":
            response = requests.get(api_url)  # TẮT XÁC MINH CHỨNG CHỈ CHO QUOTABLE.IO
        else:
            response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        if api_url == "https://zenquotes.io/api/random" and data and len(data) > 0:
            quote = data[0]["q"]
            author = data[0]["a"]
            return f"{quote} - {author}"
        elif api_url == "https://api.quotable.io/quotes/random" and data and data.get("content"):
            quote = data["content"]
            author = data.get("author", "Vô danh")
            return f"{quote} - {author}"
        else:
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi gọi API trích dẫn ({api_url}): {e}")
        return None

# Định nghĩa hàm cho lệnh trietly
async def trietly_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hiển thị một câu triết lý ngẫu nhiên bằng tiếng Việt từ cả hai API."""
    api_urls = ["https://zenquotes.io/api/random", "https://api.quotable.io/quotes/random"]
    api_url = random.choice(api_urls)  # Chọn API ngẫu nhiên

    quote_en = await get_quote_from_api(api_url)

    if quote_en:
        # Dịch sang tiếng Việt
        translator = Translator(to_lang="vi")
        try:
            quote_vi = translator.translate(quote_en)
            await update.message.reply_text(quote_vi, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Lỗi dịch thuật: {e}")
            await update.message.reply_text(f"Không thể dịch sang tiếng Việt. Đây là câu triết lý bằng tiếng Anh:\n\n{quote_en}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Không thể lấy câu triết lý. Vui lòng thử lại sau.", parse_mode="Markdown")

# Danh sách ID người dùng được phép sử dụng NSFW
AUTHORIZED_USER_IDS = [8006275240, 5867402532]
CONTACT_INFO = "liên hệ @Oceanmeoo" # Thay bằng thông tin liên hệ của bạn

async def get_waifu_pic(category="waifu", nsfw=False):
    """Lấy ảnh waifu từ API waifu.pics."""
    base_url = "https://api.waifu.pics/"
    endpoint = "sfw/" + category if not nsfw else "nsfw/" + category
    url = base_url + endpoint

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Kiểm tra lỗi HTTP
                data = await response.json()
                return data.get("url")
    except aiohttp.ClientError as e:
        logging.error(f"Lỗi khi gọi API waifu.pics: {e}")
        return None

async def sfw_waifu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy một ảnh waifu SFW ngẫu nhiên."""
    try:
        image_url = await get_waifu_pic()  # Mặc định là "waifu" category, SFW
        if image_url:
            await update.message.reply_photo(photo=image_url, caption="Ảnh Waifu (SFW)")
        else:
            await update.message.reply_text("Không thể lấy ảnh waifu. Vui lòng thử lại sau.", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Lỗi trong lệnh sfw_waifu: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}", parse_mode="Markdown")

async def nsfw_waifu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lấy một ảnh waifu NSFW ngẫu nhiên (chỉ dành cho người dùng được phép)."""
    user_id = update.message.from_user.id

    if user_id in AUTHORIZED_USER_IDS:
        try:
            image_url = await get_waifu_pic(category="waifu", nsfw=True)  # Category "waifu", NSFW
            if image_url:
                await update.message.reply_photo(photo=image_url, caption="Ảnh Waifu (NSFW)")
            else:
                await update.message.reply_text("Không thể lấy ảnh waifu NSFW. Vui lòng thử lại sau.", parse_mode="Markdown")

        except Exception as e:
            logging.error(f"Lỗi trong lệnh nsfw_waifu: {e}")
            await update.message.reply_text(f"Có lỗi xảy ra: {e}", parse_mode="Markdown")

    else:
        await update.message.reply_text(f"⚠️ Bạn không có quyền sử dụng tính năng NSFW. Vui lòng {CONTACT_INFO} để thuê.", parse_mode="Markdown") # Thay bằng thông tin liên hệ của bạn


# ----- Tính năng Tìm Kiếm IP -----
async def get_ip_info(ip_address):
    """Lấy thông tin về một địa chỉ IP."""
    try:
        url = f"http://ipwho.is/{ip_address}"  # API miễn phí, không cần key
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                if data.get("status") != "error":  # Change to check for "error" status
                    return data
                else:
                    return None
    except aiohttp.ClientError as e:
        logging.error(f"Lỗi khi gọi API tìm IP: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi không xác định khi lấy thông tin IP: {e}")
        return None

async def timip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm thông tin về một địa chỉ IP."""
    try:
        ip_address = context.args[0] if context.args else None
        if not ip_address:
            await update.message.reply_text("Vui lòng cung cấp địa chỉ IP! Ví dụ: /timip 8.8.8.8", parse_mode="Markdown")
            return

        ip_data = await get_ip_info(ip_address)
        if ip_data:
            message = f"*Thông tin về IP {ip_address}:*\n\n"
            message += f"Loại IP: {ip_data.get('type', 'Không rõ')}\n"
            message += f"Quốc gia: {ip_data.get('country', 'Không rõ')} ({ip_data.get('country_code', 'Không rõ')})\n"
            message += f"Thành phố: {ip_data.get('city', 'Không rõ')}\n"
            message += f"Châu lục: {ip_data.get('continent', 'Không rõ')} ({ip_data.get('continent_code', 'Không rõ')})\n"
            message += f"Vùng: {ip_data.get('region', 'Không rõ')} ({ip_data.get('region_code', 'Không rõ')})\n"
            message += f"Vĩ độ: {ip_data.get('latitude', 'Không rõ')}\n"
            message += f"Kinh độ: {ip_data.get('longitude', 'Không rõ')}\n"

            lat = ip_data.get('latitude')
            lon = ip_data.get('longitude')
            if lat and lon:
                message += f"Maps: https://www.google.com/maps/@{lat},{lon},8z\n"
            message += f"EU: {ip_data.get('is_eu', 'Không rõ')}\n"
            message += f"Mã bưu điện: {ip_data.get('postal', 'Không rõ')}\n"
            message += f"Mã vùng điện thoại: {ip_data.get('calling_code', 'Không rõ')}\n"
            message += f"Thủ đô: {ip_data.get('capital', 'Không rõ')}\n"
            message += f"Biên giới: {ip_data.get('borders', 'Không rõ')}\n"
            flag_data = ip_data.get("flag")
            message += f"Quốc kỳ: {flag_data.get('emoji', 'Không rõ') if flag_data else 'Không rõ'}\n"
            connection_data = ip_data.get("connection")
            message += f"ASN: {connection_data.get('asn', 'Không rõ') if connection_data else 'Không rõ'}\n"
            message += f"Tổ chức: {connection_data.get('org', 'Không rõ') if connection_data else 'Không rõ'}\n"
            message += f"ISP: {connection_data.get('isp', 'Không rõ') if connection_data else 'Không rõ'}\n"
            message += f"Tên miền: {connection_data.get('domain', 'Không rõ') if connection_data else 'Không rõ'}\n"
            timezone_data = ip_data.get("timezone")
            message += f"ID Múi giờ: {timezone_data.get('id', 'Không rõ') if timezone_data else 'Không rõ'}\n"
            message += f"ABBR Múi giờ: {timezone_data.get('abbr', 'Không rõ') if timezone_data else 'Không rõ'}\n"
            message += f"DST Múi giờ: {timezone_data.get('is_dst', 'Không rõ') if timezone_data else 'Không rõ'}\n"
            message += f"Offset Múi giờ: {timezone_data.get('offset', 'Không rõ') if timezone_data else 'Không rõ'}\n"
            message += f"UTC Múi giờ: {timezone_data.get('utc', 'Không rõ') if timezone_data else 'Không rõ'}\n"
            message += f"Giờ hiện tại: {timezone_data.get('current_time', 'Không rõ') if timezone_data else 'Không rõ'}\n"

            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Không tìm thấy thông tin cho IP {ip_address}.", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Lỗi trong lệnh timip: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}", parse_mode="Markdown")

# ----- Tính năng Tìm Kiếm Số Điện Thoại -----
async def get_phone_info(phone_number):
    """Lấy thông tin về một số điện thoại."""
    try:
        default_region = "VN"  # Mặc định là Việt Nam
        parsed_number = phonenumbers.parse(phone_number, default_region)
        if not phonenumbers.is_valid_number(parsed_number):
            return None

        region_code = phonenumbers.region_code_for_number(parsed_number)
        carrier_name = carrier.name_for_number(parsed_number, "en")
        location = geocoder.description_for_number(parsed_number, "vi")
        timezones = timezone.time_zones_for_number(parsed_number)
        timezone_str = ', '.join(timezones)

        formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        info = {
            "location": location,
            "region_code": region_code,
            "timezone": timezone_str,
            "carrier": carrier_name,
            "formatted_number": formatted_number
        }
        return info

    except phonenumbers.phonenumberutil.NumberParseException as e:
        logging.error(f"Lỗi phân tích số điện thoại: {e}")
        return None
    except Exception as e:
        logging.error(f"Lỗi không xác định khi lấy thông tin số điện thoại: {e}")
        return None

async def timsdt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm thông tin về một số điện thoại."""
    try:
        phone_number = context.args[0] if context.args else None
        if not phone_number:
            await update.message.reply_text("Vui lòng cung cấp số điện thoại! Ví dụ: /timsdt +84901234567", parse_mode="Markdown")
            return

        phone_info = await get_phone_info(phone_number)
        if phone_info:
            message = f"*Thông tin về số điện thoại {phone_number}:*\n\n"
            message += f"Khu vực: {phone_info.get('location', 'Không rõ')}\n"
            message += f"Mã vùng: {phone_info.get('region_code', 'Không rõ')}\n"
            message += f"Múi giờ: {phone_info.get('timezone', 'Không rõ')}\n"
            message += f"Nhà mạng: {phone_info.get('carrier', 'Không rõ')}\n"
            message += f"Định dạng quốc tế: {phone_info.get('formatted_number', 'Không rõ')}\n"

            await update.message.reply_text(message, parse_mode="Markdown")
        else:
            await update.message.reply_text(f"Không tìm thấy thông tin cho số điện thoại {phone_number}. Vui lòng kiểm tra lại số điện thoại.", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Lỗi trong lệnh timsdt: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}", parse_mode="Markdown")

# ----- Tính năng Tìm Kiếm Mạng Xã Hội -----
async def get_social_media_info(username):
    """Tìm kiếm thông tin về một người dùng trên các mạng xã hội."""
    results = {}
    social_media = [
        {"url": "https://www.facebook.com/{}", "name": "Facebook"},
        {"url": "https://www.twitter.com/{}", "name": "Twitter"},
        {"url": "https://www.instagram.com/{}", "name": "Instagram"},
        {"url": "https://www.linkedin.com/in/{}", "name": "LinkedIn"},
        {"url": "https://www.github.com/{}", "name": "GitHub"},
        {"url": "https://www.pinterest.com/{}", "name": "Pinterest"},
        {"url": "https://www.tumblr.com/{}", "name": "Tumblr"},
        {"url": "https://www.youtube.com/user/{}", "name": "Youtube"},  # Changed
        {"url": "https://soundcloud.com/{}", "name": "SoundCloud"},
        {"url": "https://www.snapchat.com/add/{}", "name": "Snapchat"},
        {"url": "https://www.tiktok.com/@{}", "name": "TikTok"},
        {"url": "https://www.behance.net/{}", "name": "Behance"},
        {"url": "https://medium.com/@{}", "name": "Medium"}, # Changed
        {"url": "https://www.quora.com/profile/{}", "name": "Quora"},
        {"url": "https://www.flickr.com/people/{}", "name": "Flickr"},
        {"url": "https://www.periscope.tv/{}", "name": "Periscope"},
        {"url": "https://www.twitch.tv/{}", "name": "Twitch"},
        {"url": "https://dribbble.com/{}", "name": "Dribbble"}, # Changed
        {"url": "https://www.reddit.com/user/{}", "name": "Reddit"},
        {"url": "https://www.telegram.me/{}", "name": "Telegram"},
    ]

    try:
        async with aiohttp.ClientSession() as session:
            for site in social_media:
                url = site['url'].format(username)
                try:
                    async with session.get(url, allow_redirects=False, timeout=5) as response:
                        if response.status == 200:
                            results[site['name']] = url
                        else:
                            results[site['name']] = "Không tìm thấy" # Changed
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    logging.warning(f"Lỗi khi kiểm tra {site['name']}: {e}")
                    results[site['name']] = "Lỗi kết nối" # Changed
                except Exception as e:
                    logging.error(f"Lỗi không xác định khi kiểm tra {site['name']}: {e}")
                    results[site['name']] = "Lỗi" # Changed
    except Exception as e:
        logging.error(f"Lỗi tổng thể khi tìm kiếm mạng xã hội: {e}")
        return None

    return results

async def timmxh_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm thông tin về một người dùng trên các mạng xã hội."""
    try:
        username = context.args[0] if context.args else None
        if not username:
            await update.message.reply_text("Vui lòng cung cấp username! Ví dụ: /timmxh johndoe", parse_mode="Markdown")
            return

        social_info = await get_social_media_info(username)
        if social_info:
            message = f"*Thông tin về username {username}:*\n\n"
            for site, url in social_info.items():
                message += f"{site}: {url}\n"

            await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            await update.message.reply_text(f"Không tìm thấy thông tin cho username {username}.", parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Lỗi trong lệnh timmxh: {e}")
        await update.message.reply_text(f"Có lỗi xảy ra: {e}", parse_mode="Markdown")


# Cài đặt tìm nhạc 
# Thay thế bằng API key YouTube Data API của bạn
YOUTUBE_API_KEY = "AIzaSyA6iddG3KC-FVwTc5sqyH6Aur_EQ7urQu0"  #API KEY

# Đường dẫn thư mục lưu trữ nhạc (tạm thời)
MUSIC_FOLDER = "music"
if not os.path.exists(MUSIC_FOLDER):
    os.makedirs(MUSIC_FOLDER)

# Cấu hình yt-dlp (mặc định)
DEFAULT_YDL_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.join(MUSIC_FOLDER, '%(title)s-%(id)s.%(ext)s'),
    'ignoreerrors': True,
    'noresize': True,
    'socket_timeout': 30,  # Tăng timeout
    'nocheckcertificate': True,
    'quiet': True,
}

# Các tùy chọn chất lượng âm thanh
QUALITY_OPTIONS = {
    "best": "Best Quality 🎶",
    "128k": "128kbps 🎧",
    "192k": "192kbps 🎤",
    "320k": "320kbps 🔥",
}

RESULTS_PER_PAGE = 5

# Giới hạn kích thước file (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Biến toàn cục để theo dõi trạng thái tải xuống
download_tasks = {}  # {chat_id: task}

async def search_youtube(query: str, search_type: str = 'video', max_results: int = 5, page_token: Optional[str] = None) -> Optional[Tuple[List[Dict[str, str]], Optional[str]]]:
    """Tìm kiếm video, playlist hoặc channel trên YouTube."""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            part='snippet',
            q=query,
            type=search_type,
            maxResults=max_results,
            pageToken=page_token
        )
        response = request.execute()

        results = []
        for item in response['items']:
            if search_type == 'video':
                video_id = item['id']['videoId']
                title = item['snippet']['title']
                results.append({'title': title, 'video_id': video_id, 'type': 'video'})
            elif search_type == 'playlist':
                playlist_id = item['id']['playlistId']
                title = item['snippet']['title']
                results.append({'title': title, 'playlist_id': playlist_id, 'type': 'playlist'})
            elif search_type == 'channel':
                channel_id = item['id']['channelId']
                title = item['snippet']['title']
                results.append({'title': title, 'channel_id': channel_id, 'type': 'channel'})


        next_page_token = response.get('nextPageToken')  # Lấy token cho trang tiếp theo

        return results, next_page_token
    except Exception as e:
        print(f"Lỗi khi tìm kiếm trên YouTube: {e}")
        return None, None


async def get_youtube_audio(youtube_url: str, message: Message, context: ContextTypes.DEFAULT_TYPE, quality: str = "best") -> Tuple[Optional[str], Optional[str]]:
    """Tải xuống âm thanh từ YouTube sử dụng yt-dlp và cập nhật tin nhắn."""
    ydl_opts = DEFAULT_YDL_OPTS.copy() # Sao chép options mặc định
    ydl_opts['nocolor'] = True  # Vô hiệu hóa thông tin có màu

    if quality != "best":
        # Bộ lọc đơn giản hơn, cho phép yt-dlp chọn định dạng tốt nhất trong phạm vi bitrate
        if quality == "128k":
            ydl_opts['format'] = 'bestaudio[abr<=128]'
        elif quality == "192k":
            ydl_opts['format'] = 'bestaudio[abr<=192]'
        elif quality == "320k":
            ydl_opts['format'] = 'bestaudio[abr<=320]'

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = await asyncio.to_thread(ydl.extract_info, youtube_url, download=True) #Chạy extract_info trong thread pool

            except youtube_dl.utils.DownloadError as e:
                print(f"Lỗi yt-dlp DownloadError: {e}")
                await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message.message_id, text=f"❌ Không thể tải video này: {e}", parse_mode="Markdown")
                return None, None
            except youtube_dl.utils.ExtractorError as e:
                print(f"Lỗi yt-dlp ExtractorError: {e}")
                await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message.message_id, text=f"❌ Không thể trích xuất thông tin từ video này: {e}", parse_mode="Markdown")
                return None, None
            except Exception as e:
                print(f"Lỗi yt-dlp extract_info tổng quát: {e}")
                await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message.message_id, text=f"❌ Lỗi khi tải video: {e}", parse_mode="Markdown")
                return None, None

            if info_dict is None:
                print("info_dict là None")
                await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message.message_id, text="❌ Không thể lấy thông tin video.", parse_mode="Markdown")
                return None, None

            if info_dict and 'entries' in info_dict:
                # Nếu là playlist, lấy entry đầu tiên
                info_dict = info_dict['entries'][0]

            filename = ydl.prepare_filename(info_dict)
            return filename, info_dict['title']
    except Exception as e:
        print(f"Lỗi tổng thể khi tải xuống âm thanh từ YouTube: {e}")
        await context.bot.edit_message_text(chat_id=message.chat_id, message_id=message.message_id, text=f"❌ Lỗi không xác định: {e}", parse_mode="Markdown")
        return None, None

def sanitize_filename(filename: str) -> str:
    """Làm sạch tên file để loại bỏ các ký tự không hợp lệ."""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.rstrip('.')
    return filename

async def timnhac_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm nhạc trên YouTube và cho phép người dùng chọn để tải, hỗ trợ pagination."""
    await search_command(update, context, search_type='video')

async def timplaylist_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tìm kiếm playlist trên YouTube và cho phép người dùng chọn để tải."""
    await search_command(update, context, search_type='playlist')

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE, search_type: str):
    """Tìm kiếm trên YouTube (video hoặc playlist) và cho phép người dùng chọn để tải, hỗ trợ pagination."""
    try:
        query = " ".join(context.args) if context.args else None
        if not query:
            if update.message:
                await update.message.reply_text("Vui lòng cung cấp từ khóa tìm kiếm! Ví dụ: /timnhac shape of you", parse_mode="Markdown")
            elif update.callback_query:
                 await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="Vui lòng cung cấp từ khóa tìm kiếm! Ví dụ: /timnhac shape of you", parse_mode="Markdown")
            return

        # Send initial search message
        if update.message:
            search_message: Message = await update.message.reply_text(f"🔍 Đang tìm kiếm {search_type} '{query}' trên YouTube...", parse_mode="Markdown") # Lưu message object
            chat_id = update.message.chat_id
        elif update.callback_query:
             search_message: Message = await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=f"🔍 Đang tìm kiếm {search_type} '{query}' trên YouTube...", parse_mode="Markdown")
             chat_id = update.callback_query.message.chat_id
        else:
            return # Exit if neither message nor callback_query exists.


        # Lấy trang hiện tại từ context (nếu có)
        page = int(context.args[0]) if context.args and len(context.args) > 0 and context.args[0].isdigit() else 1

        # Lấy page_token từ context
        page_token = None
        if 'page_tokens' in context.user_data and query in context.user_data['page_tokens'] and page in context.user_data['page_tokens'][query]:
            page_token = context.user_data['page_tokens'][query][page]

        context.user_data['current_page'] = page
        offset = (page - 1) * RESULTS_PER_PAGE

        search_results, next_page_token = await search_youtube(query, search_type, max_results=RESULTS_PER_PAGE, page_token=page_token)

        if search_results:
            keyboard = []
            for i, result in enumerate(search_results):
                if result['type'] == 'video':
                    keyboard.append([InlineKeyboardButton(f"{offset + i + 1}. {result['title']}", callback_data=f"download_{result['video_id']}")])
                elif result['type'] == 'playlist':
                     keyboard.append([InlineKeyboardButton(f"{offset + i + 1}. {result['title']}", callback_data=f"download_playlist_{result['playlist_id']}")])


            # Thêm nút điều hướng trang
            navigation_buttons = []
            if page > 1:
                navigation_buttons.append(InlineKeyboardButton("« Trang trước", callback_data=f"page_{query}_{page - 1}")) # Lưu cả query để gọi lại
            if next_page_token:
                navigation_buttons.append(InlineKeyboardButton("Trang sau »", callback_data=f"page_{query}_{page + 1}")) # Lưu cả query để gọi lại

            if navigation_buttons:
                keyboard.append(navigation_buttons)

            reply_markup = InlineKeyboardMarkup(keyboard)

            # Lưu next_page_token
            if 'page_tokens' not in context.user_data:
                context.user_data['page_tokens'] = {}
            if query not in context.user_data['page_tokens']:
                context.user_data['page_tokens'][query] = {}

            context.user_data['page_tokens'][query][page+1] = next_page_token # Lưu cho trang tiếp theo

            page_info = f"Trang {page}"
            await context.bot.edit_message_text(chat_id=chat_id, message_id=search_message.message_id, text=f"🎵 Kết quả tìm kiếm cho '{query}' ({page_info}):", reply_markup=reply_markup, parse_mode="Markdown") # Chỉnh sửa message
        else:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=search_message.message_id, text="❌ Không tìm thấy kết quả nào.", parse_mode="Markdown") # Chỉnh sửa message

    except Exception as e:
        print(f"Lỗi trong lệnh timnhac: {e}")
        if update.message:
           await update.message.reply_text(f"❌ Có lỗi xảy ra: {e}", parse_mode="Markdown")
        elif update.callback_query:
            await context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=f"❌ Có lỗi xảy ra: {e}", parse_mode="Markdown")


async def page_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback khi người dùng chọn một trang khác."""
    query = update.callback_query
    await query.answer()

    data_parts = query.data.split("_")
    search_query = data_parts[1]  # Lấy lại query
    page = int(data_parts[2])  # Lấy lại số trang

    context.args = [str(page)] # số trang
    context.args.insert(0, search_query)  # Thêm query vào đầu context.args

    # Xác định loại tìm kiếm dựa trên query (hoặc lưu nó trong callback data)
    if query.data.startswith("page_playlist"):
        await search_command(update, context, search_type='playlist')
    else:
        await search_command(update, context, search_type='video')

async def download_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback khi người dùng chọn một bài hát để tải."""
    query = update.callback_query
    await query.answer()

    video_id = query.data.split("_")[1]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    # Tạo inline keyboard cho các tùy chọn chất lượng
    quality_keyboard = []
    for quality_code, quality_name in QUALITY_OPTIONS.items():
        quality_keyboard.append([InlineKeyboardButton(quality_name, callback_data=f"quality_{video_id}_{quality_code}")])
    reply_markup = InlineKeyboardMarkup(quality_keyboard)

    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="🎵 Chọn chất lượng âm thanh:", reply_markup=reply_markup, parse_mode="Markdown")


async def quality_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback khi người dùng chọn chất lượng âm thanh."""
    query = update.callback_query
    await query.answer()

    data_parts = query.data.split("_")
    video_id = data_parts[1]
    quality = data_parts[2]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    # Cập nhật trạng thái
    download_task = asyncio.create_task(download_audio(update, context, youtube_url, quality))
    chat_id = query.message.chat_id
    download_tasks[chat_id] = download_task  # Lưu task để có thể hủy

    # Thêm nút "Hủy"
    cancel_keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Hủy 🚫", callback_data=f"cancel_{chat_id}") ]])
    await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="🎧 Đang tải nhạc... Vui lòng chờ.", reply_markup=cancel_keyboard, parse_mode="Markdown")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, youtube_url: str, quality: str):
    """Tải nhạc và gửi đến người dùng."""
    query = update.callback_query  # Lấy lại query để có thể trả lời
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    new_filename = None #khai báo biến ngoài try
    audio_file = None
    try:
        # Gửi thông báo "Đang tải" bằng send_message
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎧 Đang tải nhạc...", parse_mode="Markdown")

        audio_file, title = await get_youtube_audio(youtube_url, query.message, context, quality)

        if audio_file:
            try:
                # Sanitize filename
                sanitized_title = sanitize_filename(title)
                new_filename = os.path.join(MUSIC_FOLDER, f"{sanitized_title}.mp3")

                # Check if file exists before renaming
                if not os.path.exists(audio_file):
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ Không tìm thấy file audio sau khi tải.", parse_mode="Markdown")
                    return

                os.rename(audio_file, new_filename)  # Đổi tên file

                # Check if file size exceeds limit
                file_size = os.path.getsize(new_filename)
                if file_size > MAX_FILE_SIZE:
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"❌ File quá lớn ({file_size / (1024 * 1024):.2f} MB > {MAX_FILE_SIZE / (1024 * 1024):.2f} MB).", parse_mode="Markdown")
                    return # Dừng tải xuống
                
                if not os.path.exists(new_filename):
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ Không tìm thấy file audio sau khi đổi tên.", parse_mode="Markdown")
                    return

                try:
                    with open(new_filename, 'rb') as f:
                        await context.bot.send_audio(chat_id=chat_id, audio=f, title=sanitized_title)  # Gửi audio bằng send_audio
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"✅ Đã tải xong: {sanitized_title}", parse_mode="Markdown") #thêm thông báo thành công
                except Exception as e:
                    print(f"Error sending audio: {e}")
                    await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"❌ Gửi nhạc thất bại: {e}", parse_mode="Markdown")

            except Exception as e:
                print(f"Lỗi khi xử lý và gửi file audio: {e}")
                await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"❌ Có lỗi xảy ra khi xử lý file audio: {e}", parse_mode="Markdown")
        else:
            await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❌ Không thể tải nhạc từ URL này.", parse_mode="Markdown")
    except asyncio.CancelledError:
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🚫 Đã hủy tải xuống.", parse_mode="Markdown")
    except Exception as e:
        print(f"Lỗi không xác định trong download_audio: {e}")
        await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"❌ Lỗi không xác định: {e}", parse_mode="Markdown")
    finally:
        # Xóa file sau khi gửi (dù thành công hay thất bại)
        try:
            if new_filename and os.path.exists(new_filename):
                os.remove(new_filename)  # Xóa file đã đổi tên
            elif audio_file and os.path.exists(audio_file):
                os.remove(audio_file)  # Xóa file gốc nếu đổi tên thất bại
        except Exception as e:
            print(f"Không thể xóa file audio: {e}")

        # Xóa task khỏi dictionary sau khi hoàn thành
        if chat_id in download_tasks:
            del download_tasks[chat_id]

async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý callback khi người dùng chọn hủy tải xuống."""
    query = update.callback_query
    await query.answer()

    chat_id = int(query.data.split("_")[1])

    if chat_id in download_tasks:
        task = download_tasks[chat_id]
        task.cancel() # Hủy task
        del download_tasks[chat_id] # Xóa task khỏi dictionary
        await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="🚫 Đã hủy tải xuống.", parse_mode="Markdown")
    else:
        await context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text="Không có tải xuống nào đang chạy để hủy.", parse_mode="Markdown")

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý inline query."""
    query = update.inline_query.query

    if not query:
        return

    search_results, _ = await search_youtube(query, max_results=10) # Giới hạn số lượng kết quả

    results = []
    if search_results:
        for result in search_results:
            results.append(
                InlineQueryResultArticle(
                    id=result['video_id'],
                    title=result['title'],
                    input_message_content=InputTextMessageContent(f"https://www.youtube.com/watch?v={result['video_id']}"), # Gửi URL khi người dùng chọn
                    description="Nhấn để chia sẻ URL" # Mô tả kết quả
                )
            )

    await update.inline_query.answer(results) # Trả về kết quả

# Cài đặt bot
def main():
    app = Application.builder().token("7818526387:AAFiRkbCkY6HSGrxzO4_h0KJpxDUHvFeE18").build()
    app.add_handler(CommandHandler("taixiu", tai_xiu))
    app.add_handler(CommandHandler("chanle", chan_le))
    app.add_handler(CommandHandler("baucua", baucua))
    app.add_handler(CallbackQueryHandler(baucua_callback, pattern="^baucua_"))
    app.add_handler(CommandHandler("bongda", bong_da))
    app.add_handler(CommandHandler("bongro", bong_ro))
    app.add_handler(CommandHandler("phitieu", phi_tieu))
    app.add_handler(CommandHandler("bowling", bowling))
    app.add_handler(CommandHandler("quayhu", quay_hu))
    app.add_handler(CommandHandler("oantuti", start_oantuti))
    app.add_handler(CallbackQueryHandler(process_choice, pattern="^oantuti_(keo|bua|bao)$"))
    app.add_handler(CommandHandler("game", danh_sach_game))
    app.add_handler(CallbackQueryHandler(chi_tiet_game, pattern=r"^game_"))
    app.add_handler(CallbackQueryHandler(quay_lai_menu, pattern="^back_to_menu$"))
    app.add_handler(CommandHandler("blackjack", blackjack))
    app.add_handler(CallbackQueryHandler(hit, pattern="^hit$"))
    app.add_handler(CallbackQueryHandler(stand, pattern="^stand$"))
    app.add_handler(CommandHandler("bacarat", start_bacarat))
    app.add_handler(CallbackQueryHandler(handle_bet, pattern='^(banker|player|tie)$'))
    app.add_handler(CommandHandler("domin", start_minesweeper))  
    app.add_handler(CommandHandler("bxhdomin", show_leaderboard_domin))  
    app.add_handler(CallbackQueryHandler(handle_minesweeper, pattern=r'^\d+,\d+$'))
    app.add_handler(CommandHandler("ungho", ung_ho))
    app.add_handler(CommandHandler("hoi", hoi_gemini))
    app.add_handler(CommandHandler("taoanh", tao_anh_command))
    app.add_handler(CommandHandler("meme", tim_meme_command))
    app.add_handler(CallbackQueryHandler(xu_ly_callback, pattern="^ungho$"))
    app.add_handler(CallbackQueryHandler(process_choice))  
    app.add_handler(CommandHandler("yesno", yesno_command))
    app.add_handler(CommandHandler("fact", fact_command))
    app.add_handler(CommandHandler("thoitiet", thoitiet_command))
    app.add_handler(CommandHandler("trietly", trietly_command))
    app.add_handler(CommandHandler("sfwwaifu", sfw_waifu_command))  # Ảnh SFW
    app.add_handler(CommandHandler("nsfwwaifu", nsfw_waifu_command))  # Ảnh NSFW
    app.add_handler(CommandHandler("timip", timip_command))
    app.add_handler(CommandHandler("timsdt", timsdt_command))
    app.add_handler(CommandHandler("timmxh", timmxh_command))
    app.add_handler(CommandHandler("timnhac", timnhac_command))
    app.add_handler(CallbackQueryHandler(page_callback, pattern="^page_")) # Xử lý pagination
    app.add_handler(CallbackQueryHandler(download_callback, pattern="^download_"))
    app.add_handler(CallbackQueryHandler(quality_callback, pattern="^quality_")) # Xử lý chọn chất lượng
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel_")) # Xử lý hủy tải xuống
    app.add_handler(InlineQueryHandler(inline_query)) # Xử lý inline query
    app.run_polling()

if __name__ == "__main__":
    main()
