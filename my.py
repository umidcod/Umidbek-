import telebot
import yt_dlp
import os
import time

# Telegram bot API tokeningizni kiriting
telegram_token = '5742670758:AAGHsmYUhW3M4SuKVUL8fuTWrVnrelfH1S4'  # Tokeningizni shu yerga kiriting
bot = telebot.TeleBot(telegram_token)


# Video yoki musiqa yuklab olish funksiyasi
def download_media(query, chat_id, media_type='video'):
    # Fayl nomiga vaqt tamg'asi qo'shish
    filename = f"downloaded_{media_type}_{int(time.time())}.mp4" if media_type == 'video' else f"downloaded_{media_type}_{int(time.time())}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio' if media_type == 'music' else 'best',
        'outtmpl': filename,
        'default_search': 'ytsearch' if media_type == 'music' else None,
    }

    # Yuklab olish boshlangani haqida foydalanuvchiga xabar yuborish
    bot.send_message(chat_id, "Yuklab olish boshlandi...")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([query])

    # Yuklab olish yakunlangani haqida foydalanuvchiga xabar yuborish
    bot.send_message(chat_id, "Yuklab olish tugadi, endi faylni yuboryapman...")

    return filename  # Fayl nomini qaytarish


# Botga kelgan URL ni qayta ishlash
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    chat_id = message.chat.id

    # Musiqa qidirish
    if user_input.startswith("music "):
        search_query = user_input[6:]  # "music " so'zidan keyin kelgan qidiruv so'zini oling
        try:
            bot.send_message(chat_id, "Musiqani yuklab olish uchun qabul qilindi. Iltimos, kuting...")
            music_path = download_media(search_query, chat_id, 'music')

            with open(music_path, 'rb') as music:
                bot.send_audio(chat_id, music)

            bot.send_message(chat_id, "Musiqa muvaffaqiyatli yuborildi!")
            os.remove(music_path)

        except Exception as e:
            bot.send_message(chat_id, f"Xato yuz berdi: {str(e)}")

    elif 'tiktok.com' in user_input or 'instagram.com' in user_input or 'youtube.com' in user_input:
        try:
            bot.send_message(chat_id, "Videoni yuklab olish uchun qabul qilindi. Iltimos, kuting...")

            video_path = download_media(user_input, chat_id, 'video')

            with open(video_path, 'rb') as video:
                bot.send_video(chat_id, video)

            bot.send_message(chat_id, "Video muvaffaqiyatli yuborildi!")
            os.remove(video_path)

        except Exception as e:
            bot.send_message(chat_id, f"Xato yuz berdi: {str(e)}")

    else:
        bot.send_message(chat_id, "Iltimos, 'music <qidiruv so'zi>' yoki TikTok, Instagram, yoki YouTube video URLini yuboring.")


# Botni ishga tushirish
bot.polling()
