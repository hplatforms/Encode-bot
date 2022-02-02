import os
from bot import data, download_dir
from pyrogram.types import Message
from .ffmpeg_utils import encode, get_thumbnail, get_duration, get_width_height

def on_task_complete():
    del data[0]
    if len(data) > 0:
      add_task(data[0])

def add_task(message: Message):
    try:
      msg = message.reply_text("`🟡 Video İşleme Alındı... 🟡\n\n⚙️ Motor: Pyrogram\n\n#indirme`", quote=True)
      filepath = message.download(file_name=download_dir)
      msg.edit("`🟣 Video Kodlanıyor... 🟣\n\n⚙️ Motor: FFMPEG\n\n#kodlama`")
      new_file = encode(filepath)
      if new_file:
        msg.edit("`🟢 Video Kodlandı, Veriler Alınıyor... 🟢`")
        duration = get_duration(new_file)
        thumb = get_thumbnail(new_file, download_dir, duration / 4)
        width, height = get_width_height(new_file)
        msg.edit("`🔵 Video Yükleniyor... 🔵`")
        message.reply_video(new_file, quote=True, supports_streaming=True, thumb=thumb, duration=duration, width=width, height=height)
        os.remove(new_file)
        os.remove(thumb)
        msg.edit("`✔️ İşlem Bitti.\nVideo x265 formatında kodlandı.`")
      else:
        msg.edit("`⚪️ Dosyanız kodlanırken bir şeyler ters gitti.  HEVC biçiminde olmadığından emin olun. ⚪️`")
        os.remove(filepath)
    except Exception as e:
      msg.edit(f"```{e}```")
    on_task_complete()
