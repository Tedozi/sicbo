import os
import time
import asyncio
import random
import json
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
from telegram.ext import ConversationHandler
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
async def start_oantuxi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'opponent' in context.user_data:
        await update.message.reply_text("⚠ Bạn đang chơi Oẳn Tù Xì! Hoàn thành trước khi bắt đầu ván mới.")
        return

    user_choice_keyboard = [
        [InlineKeyboardButton("✌ Kéo", callback_data="keo"),
         InlineKeyboardButton("👊 Búa", callback_data="bua"),
         InlineKeyboardButton("🤚 Bao", callback_data="bao")]
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
    user_choice = update.callback_query.data
    player_name = update.callback_query.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    if 'opponent' not in context.user_data:
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


# Cài đặt bot
def main():
    app = Application.builder().token("7869286177:AAE7ZuhrH-cKa9WMrwL-wUincvG6SqJG0Rc").build()
    app.add_handler(CommandHandler("taixiu", tai_xiu))
    app.add_handler(CommandHandler("chanle", chan_le))
    app.add_handler(CommandHandler("baucua", baucua))
    app.add_handler(CallbackQueryHandler(baucua_callback, pattern="^baucua_"))
    app.add_handler(CommandHandler("bongda", bong_da))
    app.add_handler(CommandHandler("bongro", bong_ro))
    app.add_handler(CommandHandler("phitieu", phi_tieu))
    app.add_handler(CommandHandler("bowling", bowling))
    app.add_handler(CommandHandler("quayhu", quay_hu))
    app.add_handler(CommandHandler("oantuxi", start_oantuxi))
    app.add_handler(CommandHandler("game", danh_sach_game))
    app.add_handler(CallbackQueryHandler(chi_tiet_game, pattern=r"^game_"))
    app.add_handler(CallbackQueryHandler(quay_lai_menu, pattern="^back_to_menu$"))
    # Đăng ký handler cho lệnh blackjack
    app.add_handler(CommandHandler("blackjack", blackjack))
    # Đăng ký handler cho nút bấm (Hit & Stand)
    app.add_handler(CallbackQueryHandler(hit, pattern="^hit$"))
    app.add_handler(CallbackQueryHandler(stand, pattern="^stand$"))
    # Thêm handler cho game Baccarat
    app.add_handler(CommandHandler("bacarat", start_bacarat))
    app.add_handler(CallbackQueryHandler(handle_bet, pattern='^(banker|player|tie)$'))
    app.add_handler(CommandHandler("domin", start_minesweeper))  # Lệnh bắt đầu trò Dò Mìn
    app.add_handler(CommandHandler("bxhdomin", show_leaderboard_domin))  # Lệnh hiển thị bảng xếp hạng Dò Mìn
    app.add_handler(CallbackQueryHandler(handle_minesweeper, pattern=r'^\d+,\d+$'))
    app.add_handler(CommandHandler("ungho", ung_ho))
    app.add_handler(CallbackQueryHandler(xu_ly_callback, pattern="^ungho$"))
    
    app.add_handler(CallbackQueryHandler(process_choice))  # Xử lý lựa chọn của người chơi
    app.run_polling()

if __name__ == "__main__":
    main()
