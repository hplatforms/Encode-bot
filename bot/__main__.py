from pyrogram import filters
from bot import app, data, sudo_users
from bot.helper.utils import add_task

video_mimetype = [
  "video/x-flv",
  "video/mp4",
  "application/x-mpegURL",
  "video/MP2T",
  "video/3gpp",
  "video/quicktime",
  "video/x-msvideo",
  "video/x-ms-wmv",
  "video/x-matroska",
  "video/webm",
  "video/x-m4v",
  "video/quicktime",
  "video/mpeg"
  ]

@app.on_message(filters.user(sudo_users) & filters.incoming & filters.command(['start', 'help']))
def help_message(app, message):
        message.reply_text(f"Merhaba {0}\nTelegram dosyalarını x265'te kodlayabilirim aynı zamanda HEVC olarak boyut düşürebilirim, bana bir video göndermeniz yeterli.", quote=True)
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Destek", url="https://t.me/trbotlistesi"
                        )
                    ]
                ]
            ),
            reply_to_message_id=message.message_id
        ) 
    
@app.on_message(filters.user(sudo_users) & filters.incoming & (filters.video | filters.document))
def encode_video(app, message):
    if message.document:
      if not message.document.mime_type in video_mimetype:
        message.reply_text("```Geçersiz Video!\nGeçerli bir video dosyası olduğundan emin olun.```", quote=True)
        return
    message.reply_text("```✔️ Sıraya Eklendi...\nSıra: {len(data)}\n\nSabırlı olun...\n\n#kuyruk```", quote=True)
    data.append(message)
    if len(data) == 1:
      add_task(message)

app.run()
