import os
import time
import asyncio
import random
import json
from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, filters
from telegram.ext import ConversationHandler
# Game Tài Xỉu 🎲
async def tai_xiu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['tài', 'xỉu']:
        await update.message.reply_text("Vui lòng chọn 'Tài' hoặc 'Xỉu'! Ví dụ: /taixiu tài hoặc /taixiu xỉu.")
        return

    user_choice = context.args[0].lower()
    dice_1 = await update.message.reply_dice(emoji="🎲")
    dice_2 = await update.message.reply_dice(emoji="🎲")
    dice_3 = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(3)

    total = dice_1.dice.value + dice_2.dice.value + dice_3.dice.value
    result = "tài" if total >= 11 else "xỉu"
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())
    win_text = "🎉 CHIẾN THẮNG!" if user_choice == result else "😞 THUA!"

    await update.message.reply_text(
        f"GAME TÀI XỈU 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ BẠN CHỌN: {user_choice.upper()}\n"
        f"┣➤ TỔNG XÚC XẮC: {total} ({dice_1.dice.value} + {dice_2.dice.value} + {dice_3.dice.value})\n"
        f"┣➤ KẾT QUẢ: {result.upper()}\n"
        f"┣➤ {win_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Chẵn Lẻ 🎲
async def chan_le(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['chẵn', 'lẻ']:
        await update.message.reply_text("Vui lòng chọn 'Chẵn' hoặc 'Lẻ'! Ví dụ: /chanle chẵn hoặc /chanle lẻ.")
        return

    user_choice = context.args[0].lower()
    dice_message = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(3)
    dice_value = dice_message.dice.value
    result = "chẵn" if dice_value % 2 == 0 else "lẻ"
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())
    win_text = "🎉 CHIẾN THẮNG!" if user_choice == result else "😞 THUA!"

    await update.message.reply_text(
        f"GAME CHẴN LẺ 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ BẠN CHỌN: {user_choice.upper()}\n"
        f"┣➤ KẾT QUẢ XÚC XẮC: {dice_value} ({result.upper()})\n"
        f"┣➤ {win_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Bóng Đá ⚽️
async def bong_da(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_message = await update.message.reply_dice(emoji="⚽️")
    await asyncio.sleep(3)

    score = dice_message.dice.value
    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Logic xử lý kết quả
    if score in [2, 3]:  # Trúng xà ngang hoặc cột dọc
        result_text = random.choice([
            "⚽️ ĐÁ TRÚNG XÀ NGANG! 😱",  # Trúng xà ngang
            "⚽️ ĐÁ TRÚNG CỘT DỌC! 😱"   # Trúng cột dọc
        ])
    elif score == 1:  # Sút yếu k vào
        result_text = "⚽️ CÚ SÚT QUÁ YẾU! 😞"
    elif score in [4, 5]:  # Đá lọt lưới
        result_text = "⚽️ ĐÁ TRÚNG GÔN! 🥳"
    else:  # Đá trượt
        result_text = "⚽️ TRƯỢT GÔN 😢"

    # Gửi kết quả
    await update.message.reply_text(
        f"GAME BÓNG ĐÁ ⚽️\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )



# Game Bóng Rổ 🏀
async def bong_ro(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_message = await update.message.reply_dice(emoji="🏀")
    await asyncio.sleep(3)

    score = dice_message.dice.value
    if score == 6:
        result_text = "🏀 Cú ném hoàn hảo! 🏆"
    elif score >= 4:
        result_text = "🏀 Ném bóng vào rổ! 🎉"
    else:
        result_text = "🏀 Ném trật rồi 😢"

    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    await update.message.reply_text(
        f"GAME BÓNG RỔ 🏀\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Phi Tiêu 🎯
async def phi_tieu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_message = await update.message.reply_dice(emoji="🎯")
    await asyncio.sleep(3)

    score = dice_message.dice.value
    if score == 6:
        result_text = "🎯 Trúng hồng tâm! 🎉"
    elif score >= 4:
        result_text = f"🎯 Gần hồng tâm! Điểm: {score}"
    else:
        result_text = f"🎯 Trượt, điểm: {score} 😢"

    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    await update.message.reply_text(
        f"GAME PHI TIÊU 🎯\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Bowling 🎳
async def bowling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_message = await update.message.reply_dice(emoji="🎳")
    await asyncio.sleep(3)

    score = dice_message.dice.value
    if score == 6:
        result_text = "🎳 Đổ hết các bowling! 🏆"
    elif score in [4, 5]:
        result_text = f"🎳 Đổ {score} bowling! 🎉"
    else:
        result_text = f"🎳 Đổ {score} bowling. Cố gắng thêm! 😢"

    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    await update.message.reply_text(
        f"GAME BOWLING 🎳\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Quay Hũ 🎰
async def quay_hu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dice_message = await update.message.reply_dice(emoji="🎰")
    await asyncio.sleep(2)

    slot_result = dice_message.dice.value
    if slot_result == 64:
        result_text = "🎉 TRÚNG GIẢI LỚN (Jackpot)! 🏆"
    elif slot_result in [1, 22, 43]:
        result_text = "🎉 TRÚNG GIẢI THREE OF A KIND!"
    else:
        result_text = "😢 KHÔNG TRÚNG. THỬ LẠI NHA!"

    player_name = update.message.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    await update.message.reply_text(
        f"GAME QUAY HŨ 🎰\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: {player_name}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Danh sách con vật và emoji
emojis = {
    'bầu': '🍐',
    'cua': '🦀',
    'tôm': '🦐',
    'cá': '🐟',
    'nai': '🦌',
    'gà': '🐓'
}

# Game Bầu Cua Tôm Cá 🦀
async def baucua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra đầu vào
    if not context.args or context.args[0].lower() not in emojis:
        await update.message.reply_text(
            "Vui lòng chọn một trong các mục: bầu, cua, tôm, cá, nai, gà.\n"
            "Ví dụ: /baucua gà"
        )
        return

    user_choice = context.args[0].lower()  # Lựa chọn của người chơi
    results = random.choices(list(emojis.keys()), k=3)  # Random 3 con vật
    results_with_icons = [emojis[res] for res in results]  # Kết quả với emoji
    player_name = update.message.from_user.username  # Tên người chơi
    game_time = time.strftime("%H:%M:%S", time.localtime())  # Thời gian hiện tại

    # Kiểm tra kết quả
    hits = results.count(user_choice)  # Số lần trúng
    if hits > 0:
        win_text = f"🎉 CHÚC MỪNG! Bạn đã trúng {hits} lần! 🏆"
    else:
        win_text = "😞 RẤT TIẾC! Bạn không trúng lần nào. Thử lại nhé!"

    # Gửi kết quả cho người chơi
    await update.message.reply_text(
        f"🍐 GAME BẦU CUA TÔM CÁ 🦀\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ NGƯỜI CHƠI: @{player_name}\n"
        f"┣➤ BẠN CHỌN: {emojis[user_choice]} ({user_choice.upper()})\n"
        f"┣➤ KẾT QUẢ: {' '.join(results_with_icons)}\n"
        f"┣➤ {win_text}\n"
        f"┣➤ THỜI GIAN: {game_time}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Game Oẳn Tù Xì
# Định nghĩa emoji cho các lựa chọn với từ có dấu
emoji_map = {
    'keo': '✌ Kéo',  # Kéo
    'bua': '👊 Búa',  # Búa
    'bao': '🤚 Bao'    # Bao
}

# Hàm xác định kết quả giữa người chơi và bot
def determine_winner(player_choice, bot_choice):
    # Lấy emoji tương ứng cho lựa chọn của người chơi và bot
    player_emoji = emoji_map.get(player_choice, '')
    bot_emoji = emoji_map.get(bot_choice, '')

    # Kiểm tra nếu cả 2 chọn giống nhau thì chơi lại
    if player_choice == bot_choice:
        return f"Hòa! Bạn và bot đều chọn {player_emoji}. Chơi lại!"
    
    # Quy tắc mới
    if (player_choice == 'bua' and bot_choice == 'keo') or \
       (player_choice == 'keo' and bot_choice == 'bao') or \
       (player_choice == 'bao' and bot_choice == 'bua'):
        return f"Bạn thắng! Bạn {player_emoji} bot {bot_emoji}"

    else:
        return f"Bạn thua! Bạn {player_emoji} bot {bot_emoji}"

# Cập nhật lại bàn phím sau khi người chơi đã chọn
def disable_choices_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Kéo ✌", callback_data="none"),
         InlineKeyboardButton("Búa 👊", callback_data="none"),
         InlineKeyboardButton("Bao 🤚", callback_data="none")]
    ])

# Hàm xử lý lệnh chơi oẳn tù xì với bot
async def start_oantuxi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Kiểm tra nếu người chơi đang tham gia trò chơi dò mìn
    if 'minesweeper' in context.user_data and context.user_data['minesweeper'].get('game_over', False):
        await update.message.reply_text("Bạn đang chơi trò Dò Mìn. Vui lòng hoàn thành trò chơi đó trước!")
        return

    # Kiểm tra xem người chơi đã bắt đầu game oẳn tù xì chưa
    if 'opponent' in context.user_data:
        await update.message.reply_text("Bạn đã bắt đầu chơi trò Oẳn Tù Xì rồi. Vui lòng hoàn thành trò chơi này trước!")
        return

    user_choice_keyboard = [
        [InlineKeyboardButton("Kéo ✌", callback_data="keo"),
         InlineKeyboardButton("Búa 👊", callback_data="bua"),
         InlineKeyboardButton("Bao 🤚", callback_data="bao")]
    ]

    reply_markup = InlineKeyboardMarkup(user_choice_keyboard)

    # Lưu trạng thái "chơi với bot"
    context.user_data['opponent'] = 'bot'

    await update.message.reply_text(
        text="Chọn một trong ba lựa chọn: Kéo ✌, Búa 👊, hoặc Bao 🤚.",
        reply_markup=reply_markup
    )

# Hàm xử lý lựa chọn của người chơi khi chơi với bot
async def process_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.callback_query.data
    player_name = update.callback_query.from_user.username
    game_time = time.strftime("%H:%M:%S", time.localtime())

    # Kiểm tra xem người chơi đã chọn chưa, nếu đã chọn thì không cho phép chọn lại
    if 'opponent' not in context.user_data:
        await update.callback_query.answer("Bạn chưa bắt đầu trò chơi!")
        return
    
    # Kiểm tra trạng thái trò chơi
    if context.user_data.get('opponent') == 'bot':
        # Bot chọn ngẫu nhiên
        bot_choice = random.choice(['keo', 'bua', 'bao'])  
        result = determine_winner(user_choice, bot_choice)
        
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            f"GAME OẢN TÙ XÌ\n"
            "┏━━━━━━━━━━━━━━━┓\n"
            f"┣➤ NGƯỜI CHƠI: {player_name}\n"
            f"┣➤ BẠN CHỌN: {emoji_map.get(user_choice, '')}\n"
            f"┣➤ BOT CHỌN: {emoji_map.get(bot_choice, '')}\n"
            f"┣➤ KẾT QUẢ: {result}\n"
            f"┣➤ THỜI GIAN: {game_time}\n"
            "┗━━━━━━━━━━━━━━━┛"
        )
        # Vô hiệu hóa các lựa chọn cho người chơi khác
        await update.callback_query.message.edit_reply_markup(reply_markup=disable_choices_keyboard())

        # Xóa đối thủ khỏi dữ liệu của người chơi
        del context.user_data['opponent']


#Game Blackjack
# Hàm chuyển giá trị bài sang emoji
CARD_EMOJIS = {
    1: "A🇦",
    2: "②",
    3: "③",
    4: "④",
    5: "⑤",
    6: "⑥",
    7: "⑦",
    8: "⑧",
    9: "⑨",
    10: "⑩",
    11: "🇯",
    12: "🇶",
    13: "🇰"
}

def card_to_emoji(card):
    return CARD_EMOJIS[card]

# Hàm tính tổng điểm bài
def calculate_score(cards):
    score = 0
    ace_count = 0

    for card in cards:
        if card > 10:  # J, Q, K
            score += 10
        elif card == 1:  # A
            ace_count += 1
            score += 11
        else:
            score += card

    while score > 21 and ace_count > 0:
        score -= 10
        ace_count -= 1

    return score

# Lệnh bắt đầu trò chơi
async def blackjack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Kiểm tra và khởi tạo trạng thái người chơi
    context.user_data[user_id] = {
        "player_cards": [],
        "dealer_cards": [],
        "deck": [],
        "game_over": False
    }

    # Tạo bộ bài và xáo trộn
    deck = [i for i in range(1, 14)] * 4
    random.shuffle(deck)

    # Khởi tạo bài cho người chơi và nhà cái
    context.user_data[user_id]["player_cards"] = [deck.pop(), deck.pop()]
    context.user_data[user_id]["dealer_cards"] = [deck.pop(), deck.pop()]
    context.user_data[user_id]["deck"] = deck
    context.user_data[user_id]["game_over"] = False

    player_cards = context.user_data[user_id]["player_cards"]
    dealer_cards = context.user_data[user_id]["dealer_cards"]

    await update.message.reply_text(
        f"BLACKJACK 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ BÀI CỦA BẠN: {', '.join(card_to_emoji(card) for card in player_cards)}\n"
        f"┣➤ BÀI NHÀ CÁI: {card_to_emoji(dealer_cards[0])}, ❓\n"
        "┗━━━━━━━━━━━━━━━┛\n"
        "Lệnh: /hit để rút thêm bài, /stand để dừng."
    )

# Lệnh rút bài
async def hit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Kiểm tra trạng thái trò chơi
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await update.message.reply_text("🎮 Trò chơi đã kết thúc. Vui lòng bắt đầu lại bằng lệnh /blackjack.")
        return

    deck = context.user_data[user_id]["deck"]
    player_cards = context.user_data[user_id]["player_cards"]

    # Rút bài mới
    player_cards.append(deck.pop())

    # Tính điểm
    player_score = calculate_score(player_cards)

    if player_score > 21:
        context.user_data[user_id]["game_over"] = True
        await update.message.reply_text(
            f"BẠN ĐÃ RÚT: {card_to_emoji(player_cards[-1])}\n"
            "🔥 QUÁ 21! BẠN ĐÃ THUA. 😞\n"
            f"BÀI CỦA BẠN: {', '.join(card_to_emoji(card) for card in player_cards)}\n"
            f"TỔNG ĐIỂM: {player_score}"
        )
        return

    await update.message.reply_text(
        f"BẠN ĐÃ RÚT: {card_to_emoji(player_cards[-1])}\n"
        f"BÀI CỦA BẠN: {', '.join(card_to_emoji(card) for card in player_cards)}\n"
        f"TỔNG ĐIỂM: {player_score}\n"
        "Lệnh: /hit để rút thêm bài, /stand để dừng."
    )

# Lệnh dừng bài
async def stand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Kiểm tra trạng thái trò chơi
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await update.message.reply_text("🎮 Trò chơi đã kết thúc. Vui lòng bắt đầu lại bằng lệnh /blackjack.")
        return

    context.user_data[user_id]["game_over"] = True
    deck = context.user_data[user_id]["deck"]
    dealer_cards = context.user_data[user_id]["dealer_cards"]
    player_cards = context.user_data[user_id]["player_cards"]

    player_score = calculate_score(player_cards)

    # Nhà cái rút bài
    while calculate_score(dealer_cards) < 17:
        dealer_cards.append(deck.pop())

    dealer_score = calculate_score(dealer_cards)

    # Xác định kết quả
    if dealer_score > 21 or player_score > dealer_score:
        result_text = "🎉 BẠN THẮNG!"
    elif player_score < dealer_score:
        result_text = "😞 BẠN THUA!"
    else:
        result_text = "🤝 HÒA!"

    await update.message.reply_text(
        f"GAME KẾT THÚC 🎲\n"
        "┏━━━━━━━━━━━━━━━┓\n"
        f"┣➤ BÀI CỦA BẠN: {', '.join(card_to_emoji(card) for card in player_cards)}\n"
        f"┣➤ TỔNG ĐIỂM: {player_score}\n"
        f"┣➤ BÀI NHÀ CÁI: {', '.join(card_to_emoji(card) for card in dealer_cards)}\n"
        f"┣➤ TỔNG ĐIỂM NHÀ CÁI: {dealer_score}\n"
        f"┣➤ KẾT QUẢ: {result_text}\n"
        "┗━━━━━━━━━━━━━━━┛"
    )

# Hàm tính điểm bài Baccarat
def calculate_points():
    banker_cards = [random.randint(1, 10) for _ in range(2)]
    player_cards = [random.randint(1, 10) for _ in range(2)]

    banker_score = sum(banker_cards) % 10
    player_score = sum(player_cards) % 10

    return banker_cards, player_cards, banker_score, player_score

# Lệnh /bacarat
async def start_bacarat(update, context):
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Nhà Cái", callback_data="banker")],
        [InlineKeyboardButton("Nhà Con", callback_data="player")]
    ])
    
    await update.message.reply_text(
        "🎲 Chọn cược của bạn:\n👉 Nhấn nút bên dưới để chọn Nhà Cái hoặc Nhà Con.",
        reply_markup=markup
    )

# Xử lý callback
async def handle_bet(update, context):
    query = update.callback_query
    user_choice = query.data

    banker_cards, player_cards, banker_score, player_score = calculate_points()

    if banker_score > player_score:
        winner = "Nhà Cái thắng 🎉"
    elif player_score > banker_score:
        winner = "Nhà Con thắng 🎉"
    else:
        winner = "Hòa 🤝"

    await query.edit_message_text(
        text=(f"🎲 Kết quả Baccarat:\n\n"
              f"💼 Nhà Cái: {banker_cards} ➤ Điểm: {banker_score}\n"
              f"👤 Nhà Con: {player_cards} ➤ Điểm: {player_score}\n\n"
              f"🏆 {winner}")
    )
# game dò mìn
# Kích thước bảng Dò Mìn
SIZE = 5
NUM_MINES = 5  # Số lượng mìn
LEADERBOARD_FILE = "bxh_domin.json"  # Tệp lưu bảng xếp hạng

# Dữ liệu bảng xếp hạng cho Dò Mìn
leaderboard_domin = {}


# Tải bảng xếp hạng từ tệp
def load_leaderboard():
    global leaderboard_domin
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
            leaderboard_domin = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard_domin = {}


# Lưu bảng xếp hạng vào tệp
def save_leaderboard():
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(leaderboard_domin, file, ensure_ascii=False, indent=4)


# Tạo bảng Dò Mìn
def generate_minesweeper_board():
    board = [["⬜" for _ in range(SIZE)] for _ in range(SIZE)]
    mines = set()

    while len(mines) < NUM_MINES:
        mine = (random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))
        mines.add(mine)

    for mine in mines:
        board[mine[0]][mine[1]] = "💣"

    return board


def count_adjacent_mines(board, row, col):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = row + dr, col + dc
            if 0 <= r < SIZE and 0 <= c < SIZE and board[r][c] == "💣":
                count += 1
    return count


def reveal_board(board):
    revealed = [["" for _ in range(SIZE)] for _ in range(SIZE)]

    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == "💣":
                revealed[row][col] = "💣"
            else:
                revealed[row][col] = str(count_adjacent_mines(board, row, col)) or "⬜"

    return revealed


# Lệnh bắt đầu trò chơi Dò Mìn
async def start_minesweeper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    # Khởi tạo bảng Dò Mìn nếu chưa có trò chơi
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        board = generate_minesweeper_board()
        context.user_data[user_id] = {
            "board": board,
            "revealed": [[False for _ in range(SIZE)] for _ in range(SIZE)],
            "game_over": False,
            "user_name": user_name
        }

        # Tạo bàn phím tương tác
        keyboard = [[InlineKeyboardButton("⬜", callback_data=f"{row},{col}") for col in range(SIZE)] for row in range(SIZE)]
        markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("🎮 DÒ MÌN 🎮\nBot được tài trợ bởi @Somethingtosay109\n👉 Nhấn vào ô để chơi:", reply_markup=markup)
    else:
        await update.message.reply_text("🎮 Trò chơi đã được bắt đầu! Hãy tiếp tục chơi.")


# Xử lý khi người chơi chọn một ô
async def handle_minesweeper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    # Trả lời ngay lập tức để tránh hết hạn query
    await query.answer()

    # Kiểm tra trạng thái trò chơi
    if user_id not in context.user_data or context.user_data[user_id]["game_over"]:
        await query.answer("🎮 Trò chơi đã kết thúc. Vui lòng bắt đầu lại bằng lệnh /domin.\nBot được tài trợ bởi @Somethingtosay109")
        return

    board = context.user_data[user_id]["board"]
    revealed = context.user_data[user_id]["revealed"]

    row, col = map(int, query.data.split(","))

    if revealed[row][col]:
        await query.answer("⛔ Ô này đã được chọn trước đó!")
        return

    revealed[row][col] = True

    # Nếu chọn phải mìn
    if board[row][col] == "💣":
        context.user_data[user_id]["game_over"] = True
        revealed_board = reveal_board(board)
        await query.edit_message_text(
            text="💥 BẠN ĐÃ CHỌN PHẢI MÌN! TRÒ CHƠI KẾT THÚC 💥\n" +
                 "\n".join(" ".join(row) for row in revealed_board) + "\n\n/bxhdomin để xem bảng xếp hạng.\nBot được tài trợ bởi @Somethingtosay109"
        )
        return

    # Kiểm tra điều kiện thắng
    remaining_safe_cells = sum(
        1 for r in range(SIZE) for c in range(SIZE) if board[r][c] != "💣" and not revealed[r][c]
    )

    if remaining_safe_cells == 0:
        context.user_data[user_id]["game_over"] = True

        # Cập nhật bảng xếp hạng
        load_leaderboard()
        if str(user_id) in leaderboard_domin:
            leaderboard_domin[str(user_id)]["win_count"] += 1
        else:
            leaderboard_domin[str(user_id)] = {"user_name": context.user_data[user_id]["user_name"], "win_count": 1}
        save_leaderboard()

        await query.edit_message_text(
            text="🎉 CHÚC MỪNG! BẠN ĐÃ THẮNG! 🎉\n\n/bxhdomin để xem bảng xếp hạng.\n/domin để chơi lại\nBot được tài trợ bởi @Somethingtosay109"
        )
        return

    # Cập nhật giao diện bàn cờ
    board_display = [["⬜" if not revealed[r][c] else (board[r][c] if board[r][c] == "💣" else str(count_adjacent_mines(board, r, c))) for c in range(SIZE)] for r in range(SIZE)]
    keyboard = [[InlineKeyboardButton(board_display[r][c], callback_data=f"{r},{c}") if not revealed[r][c] else InlineKeyboardButton(board_display[r][c], callback_data="none") for c in range(SIZE)] for r in range(SIZE)]
    markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="🎮 DÒ MÌN 🎮\n👉 Tiếp tục chơi:", reply_markup=markup
    )


# Lệnh hiển thị bảng xếp hạng Dò Mìn
async def show_leaderboard_domin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    load_leaderboard()

    if not leaderboard_domin:
        await update.message.reply_text("🏆 BẢNG XẾP HẠNG DÒ MÌN 🏆\nHiện chưa có người chơi nào!")
        return

    leaderboard_text = "🏆 BẢNG XẾP HẠNG DÒ MÌN 🏆\n"
    sorted_leaderboard = sorted(leaderboard_domin.values(), key=lambda x: x["win_count"], reverse=True)
    for i, entry in enumerate(sorted_leaderboard[:5], start=1):  # Hiển thị tối đa 5 người chơi
        leaderboard_text += f"{i}. {entry['user_name']} - Số lần thắng: {entry['win_count']}\n"

    await update.message.reply_text(leaderboard_text)


# Hàm gửi ảnh QR và lời cảm ơn trong 1 tin nhắn
async def ung_ho(update: Update, context: CallbackContext):
    # Link đến ảnh QR
    qr_image_url = "https://i.ibb.co/k8Mznt7/image.png"  # Thay bằng link ảnh QR của bạn

    # Lời cảm ơn với icon và định dạng đẹp
    message = (
        "🌟 Cảm ơn bạn rất nhiều! 🌟\n\n"
        "Bọn mình rất trân trọng sự ủng hộ của bạn! 💖\n"
        "Mỗi đóng góp của bạn đều giúp bot trở nên mạnh mẽ hơn,\nmang lại nhiều tính năng hay ho hơn cho mọi người! 🎉\n\n"
        "Nếu bạn muốn hỗ trợ Bọn mình, bạn có thể quét mã QR dưới đây 📱💡\n"
        "Một lần nữa, xin chân thành cảm ơn! 🙏\n\n"
        "Chúc bạn có một ngày tuyệt vời! 🌞"
    )

    # Gửi ảnh với lời cảm ơn
    await update.message.reply_photo(photo=qr_image_url, caption=message)



# lệnh /game
# Dữ liệu mô tả tất cả các trò chơi
GAME_DETAILS = {
    "taixiu": {
        "name": "Tài Xỉu 🎲",
        "description": "🔸 Một trò chơi dựa vào kết quả tung 3 xúc xắc.\n🔸 Dự đoán 'Tài' (11-17) hoặc 'Xỉu' (3-10).",
        "command": "/taixiu [tài/xỉu]"
    },
    "chanle": {
        "name": "Chẵn Lẻ 🎲",
        "description": "🔸 Dự đoán tổng điểm của xúc xắc là chẵn hay lẻ.\n🔸 Chọn 'chẵn' hoặc 'lẻ'.",
        "command": "/chanle [chẵn/lẻ]"
    },
    "bongda": {
        "name": "Bóng Đá ⚽️",
        "description": "🔸 Đặt cược vào đôi chân của bạn vào trò chơi bóng đá.",
        "command": "/bongda"
    },
    "bongro": {
        "name": "Bóng Rổ 🏀",
        "description": "🔸 Đặt cược vào kết quả vào trái bóng bóng rổ trong tay bạn.",
        "command": "/bongro"
    },
    "phitieu": {
        "name": "Phi Tiêu 🎯",
        "description": "🔸 Dự đoán kết quả khi ném phi tiêu.\n🔸 May mắn sẽ quyết định thắng thua!",
        "command": "/phitieu"
    },
    "bowling": {
        "name": "Bowling 🎳",
        "description": "🔸 Thử tài đoán số điểm khi chơi bowling.\n🔸 Trò chơi dành cho những ai yêu thích thể thao.",
        "command": "/bowling"
    },
    "quayhu": {
        "name": "Quay Hũ 🎰",
        "description": "🔸 Chơi máy quay hũ với tỷ lệ thưởng cao.\n🔸 Hãy thử vận may của bạn!",
        "command": "/quayhu"
    },
    "baucua": {
        "name": "Bầu Cua 🦀",
        "description": "🔸 Đặt cược vào các biểu tượng: Bầu, Cua, Tôm, Cá, Nai, Gà.\n🔸 Trò chơi dân gian đầy thú vị!",
        "command": "/baucua [bầu/cua/tôm/cá/nai/gà]"
    },
    "oantuxi": {
        "name": "Oẳn Tù Tì ✌️",
        "description": "🔸 Chơi Kéo, Búa, Bao với bot hoặc với.\n🔸 Dự đoán lựa chọn của đối thủ để chiến thắng.",
        "command": "/oantuxi"
    },
    "blackjack": {
        "name": "Blackjack 🃏",
        "description": "🔸 Trò chơi bài hấp dẫn, bạn cần đạt tổng điểm gần 21 nhất mà không vượt quá. Các lá bài 2-10 có giá trị tương ứng, J, Q, K có giá trị 10, và A có thể tính là 1 hoặc 11.",
        "command": "/blackjack"
    },
    "bacarat": {
        "name": "Baccarat 🎴",
        "description": "🔸 Trò chơi bài giữa hai bên: Banker và Player. Bạn đặt cược vào bên nào sẽ có tổng điểm gần 9 nhất.\n🔸 Các lá bài có giá trị từ 2 đến 9, A có giá trị 1, 10 và các lá bài hình (J, Q, K) có giá trị 0.",
        "command": "/bacarat"
    },
    "domin": {
        "name": "Dò Mìn 💣",
        "description": "🔸 Mở các ô trên bảng mà không trúng phải mìn. Mỗi ô hiển thị một con số, cho biết số mìn xung quanh.\n🔸 Tránh mở ô có mìn và chiến thắng bằng cách mở tất cả các ô an toàn.",
        "command": "/domin"
    },
    "ungho": {
        "name": "Ủng Hộ",
            "description": (
        "🌟 Cảm ơn bạn rất nhiều! 🌟\n\n"
        "Bọn mình rất trân trọng sự ủng hộ của bạn! 💖\n"
        "Mỗi đóng góp của bạn đều giúp bot trở nên mạnh mẽ hơn,\nmang lại nhiều tính năng hay ho hơn cho mọi người! 🎉\n\n"
        "Nếu bạn muốn hỗ trợ Bọn mình, bạn có thể quét mã QR dưới đây 📱💡\n"
        "Một lần nữa, xin chân thành cảm ơn! 🙏\n\n"
        "Chúc bạn có một ngày tuyệt vời! 🌞"
    ),
        "command": "/ungho"
    }
}

# Tạo bàn phím các nút (xếp hàng ngang)
def create_game_keyboard():
    keyboard = []
    row = []
    for index, (game_key, game_data) in enumerate(GAME_DETAILS.items(), 1):
        row.append(InlineKeyboardButton(game_data["name"], callback_data=f"game_{game_key}"))
        if index % 3 == 0:  # 3 nút mỗi hàng
            keyboard.append(row)
            row = []
    if row:  # Thêm hàng còn lại nếu còn nút
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# Hàm hiển thị menu nút các trò chơi
async def danh_sach_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:  # Xử lý quay lại menu từ callback query
        await update.callback_query.edit_message_text(
            "🎮 DANH SÁCH TRÒ CHƠI 🎮\n👉 Nhấn vào một trò chơi để xem chi tiết:",
            reply_markup=create_game_keyboard()
        )
    else:  # Xử lý lệnh /game
        await update.message.reply_text(
            "🎮 DANH SÁCH TRÒ CHƠI 🎮\n👉 Nhấn vào một trò chơi để xem chi tiết:",
            reply_markup=create_game_keyboard()
        )

# Hàm hiển thị thông tin chi tiết từng trò chơi
async def chi_tiet_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    game_key = query.data.split("_")[1]
    if game_key in GAME_DETAILS:
        game = GAME_DETAILS[game_key]
        await query.edit_message_text(
            text=(f"🎲 {game['name']}\n\n{game['description']}\n\n👉 Lệnh để chơi: {game['command']}"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Quay lại danh sách", callback_data="back_to_menu")]
            ])
        )
    else:
        await query.edit_message_text("⚠️ Trò chơi không tồn tại!")

# Hàm quay lại menu
async def quay_lai_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await danh_sach_game(update, context)

# Trạng thái của game đoán từ
WORD_GUESS = 1

def hide_letters(word):
    return "".join([char if random.random() > 0.5 else "_" for char in word])

def update_wordgame_leaderboard_data(user_data):
    leaderboard = user_data.get("leaderboard", {})
    user_id = user_data["user_id"]
    score = user_data.get("wordgame_score", 0)
    
    if user_id in leaderboard:
        leaderboard[user_id]["score"] = max(leaderboard[user_id]["score"], score)
    else:
        leaderboard[user_id] = {"user_name": user_data["user_name"], "score": score}
    
    with open("bxhwordgame.txt", "w", encoding="utf-8") as f:
        for user_id, data in leaderboard.items():
            f.write(f"{data['user_name']} - {data['score']}\n")

def load_words_from_file():
    try:
        with open("worldlist.txt", "r", encoding="utf-8") as f:
            words = f.readlines()
        return [word.strip() for word in words if word.strip()]
    except FileNotFoundError:
        print("File worldlist.txt không tồn tại.")
        return []

async def timeout_word(context):
    user_data = context.job.data["user_data"].copy()
    chat_id = context.job.data["chat_id"]
    
    await context.bot.send_message(
        chat_id, 
        f"⏰ Bạn đã hết thời gian! Từ đúng là: <b>{user_data['current_word']}</b>\n🏁 Game kết thúc.",
        parse_mode="HTML"
    )
    update_wordgame_leaderboard_data(user_data)
    context.job.data["user_data"].clear()
    return ConversationHandler.END

async def start_wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    context.user_data.clear()
    context.user_data["user_id"] = user.id
    context.user_data["user_name"] = user.username
    context.user_data["wordgame_score"] = 0
    
    words = load_words_from_file()
    if not words:
        await update.message.reply_text("❌ Không tìm thấy từ nào trong worldlist.txt.")
        return ConversationHandler.END

    context.user_data["words"] = words
    word = random.choice(words)
    context.user_data["current_word"] = word
    masked_word = hide_letters(word)

    await update.message.reply_text(f"🔎 Đoán từ: <b>{masked_word}</b>", parse_mode="HTML")

    job = context.job_queue.run_once(timeout_word, 15, data={"chat_id": update.effective_chat.id, "user_data": context.user_data.copy()})
    context.user_data["timeout_job"] = job

    return WORD_GUESS

async def word_guess(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    if user.id != context.user_data.get("user_id"):
        await update.message.reply_text("❌ Bạn không phải là người chơi!")
        return WORD_GUESS

    job = context.user_data.pop("timeout_job", None)
    if job:
        job.schedule_removal()

    user_answer = update.message.text.strip()
    if user_answer.lower() == "thoát":
        score = context.user_data.get("wordgame_score", 0)
        await update.message.reply_text(f"🚪 Bạn đã thoát game. Tổng điểm: {score}")
        update_wordgame_leaderboard_data(context.user_data)
        context.user_data.clear()
        return ConversationHandler.END

    current_word = context.user_data.get("current_word")
    if user_answer.lower().strip() == current_word.lower().strip():
        context.user_data["wordgame_score"] += 1
        new_score = context.user_data["wordgame_score"]
        await update.message.reply_text(f"🎉 Chính xác! Điểm hiện tại: {new_score}")
    else:
        await update.message.reply_text(
            f"❌ Sai! Từ đúng là: <b>{current_word}</b>\n🏁 Game kết thúc. Tổng điểm: {context.user_data.get('wordgame_score', 0)}",
            parse_mode="HTML"
        )
        update_wordgame_leaderboard_data(context.user_data)
        context.user_data.clear()
        return ConversationHandler.END
    
    word = random.choice(context.user_data["words"])
    context.user_data["current_word"] = word
    masked_word = hide_letters(word)

    await update.message.reply_text(f"🔎 Đoán từ mới: <b>{masked_word}</b>", parse_mode="HTML")
    job = context.job_queue.run_once(timeout_word, 15, data={"chat_id": update.effective_chat.id, "user_data": context.user_data.copy()})
    context.user_data["timeout_job"] = job

    return WORD_GUESS

async def show_leaderboard_wordgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open("bxhwordgame.txt", "r", encoding="utf-8") as f:
        leaderboard_text = "🏆 BẢNG XẾP HẠNG ĐOÁN TỪ 🏆\n" + f.read()
        await update.message.reply_text(leaderboard_text)


# Cài đặt bot
def main():
    app = Application.builder().token("7869286177:AAE7ZuhrH-cKa9WMrwL-wUincvG6SqJG0Rc").build()
    app.add_handler(CommandHandler("taixiu", tai_xiu))
    app.add_handler(CommandHandler("chanle", chan_le))
    app.add_handler(CommandHandler("baucua", baucua))
    app.add_handler(CommandHandler("bongda", bong_da))
    app.add_handler(CommandHandler("bongro", bong_ro))
    app.add_handler(CommandHandler("phitieu", phi_tieu))
    app.add_handler(CommandHandler("bowling", bowling))
    app.add_handler(CommandHandler("quayhu", quay_hu))
    app.add_handler(CommandHandler("oantuxi", start_oantuxi))
    app.add_handler(CommandHandler("game", danh_sach_game))
    app.add_handler(CallbackQueryHandler(chi_tiet_game, pattern=r"^game_"))
    app.add_handler(CallbackQueryHandler(quay_lai_menu, pattern="^back_to_menu$"))
    app.add_handler(CommandHandler("blackjack", blackjack))
    app.add_handler(CommandHandler("hit", hit))
    app.add_handler(CommandHandler("stand", stand))
    # Thêm handler cho game Baccarat
    app.add_handler(CommandHandler("bacarat", start_bacarat))
    app.add_handler(CallbackQueryHandler(handle_bet, pattern='^(banker|player)$'))
    app.add_handler(CommandHandler("domin", start_minesweeper))  # Lệnh bắt đầu trò Dò Mìn
    app.add_handler(CommandHandler("bxhdomin", show_leaderboard_domin))  # Lệnh hiển thị bảng xếp hạng Dò Mìn
    app.add_handler(CallbackQueryHandler(handle_minesweeper, pattern=r'^\d+,\d+$'))
    app.add_handler(CommandHandler("ungho", ung_ho))
    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("doantu", start_wordgame)],
    states={WORD_GUESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, word_guess)]},
    fallbacks=[CommandHandler("bxhdoantu", show_leaderboard_wordgame)],
)
    
    app.add_handler(CallbackQueryHandler(process_choice))  # Xử lý lựa chọn của người chơi
    app.run_polling()

if __name__ == "__main__":
    main()
