import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import yt_dlp
import os

def download_playlist():
    playlist_url = entry_url.get()
    output_folder = entry_output.get()
    quality = quality_var.get()
    download_format = format_var.get()

    if not playlist_url:
        messagebox.showerror("خطأ", "الرجاء إدخال رابط Playlist!")
        return

    if not output_folder:
        messagebox.showerror("خطأ", "الرجاء تحديد مسار الحفظ!")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    if download_format == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_folder}/%(playlist_index)s - %(title)s.%(ext)s',
            'ignoreerrors': True,
            'yesplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'format': f'bestvideo[height<={quality}]+bestaudio/best',
            'outtmpl': f'{output_folder}/%(playlist_index)s - %(title)s.%(ext)s',
            'ignoreerrors': True,
            'yesplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }, {
                'key': 'FFmpegMetadata',
            }],
        }

    try:
        progress_bar.start()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
        progress_bar.stop()
        messagebox.showinfo("تم", "تم التحميل بنجاح!")
        open_folder_button.config(state=tk.NORMAL)
    except Exception as e:
        progress_bar.stop()
        messagebox.showerror("خطأ", f"حدث خطأ: {e}")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_output.delete(0, tk.END)
        entry_output.insert(0, folder_selected)

def open_folder():
    output_folder = entry_output.get()
    if os.path.exists(output_folder):
        os.startfile(output_folder)

# إنشاء واجهة المستخدم
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("700x600")
root.configure(bg="#263238")

# إطار للإدخالات مع تأثير الظل
frame = tk.Frame(root, bg="#263238", bd=15, relief="solid", borderwidth=3)
frame.pack(padx=30, pady=30, fill='both', expand=True)

# عنوان التطبيق
title_label = tk.Label(frame, text="YouTube Playlist Downloader", font=("Roboto", 22, "bold"), bg="#263238", fg="#FF4081")
title_label.grid(row=0, column=0, columnspan=3, pady=20)

# رابط Playlist
tk.Label(frame, text="رابط Playlist:", bg="#263238", fg="#FFFFFF", font=("Roboto", 12)).grid(row=1, column=0, sticky="w", pady=15)
entry_url = tk.Entry(frame, width=40, font=("Roboto", 12), relief="flat", bd=2, fg="#263238")
entry_url.grid(row=1, column=1, padx=5, pady=15)

# مسار الحفظ
tk.Label(frame, text="مسار الحفظ:", bg="#263238", fg="#FFFFFF", font=("Roboto", 12)).grid(row=2, column=0, sticky="w", pady=15)
entry_output = tk.Entry(frame, width=40, font=("Roboto", 12), relief="flat", bd=2, fg="#263238")
entry_output.grid(row=2, column=1, padx=5, pady=15)
tk.Button(frame, text="استعراض", command=browse_folder, bg="#4CAF50", fg="white", font=("Roboto", 10), relief="flat", activebackground="#388E3C").grid(row=2, column=2, padx=5, pady=15)

# جودة الفيديو
tk.Label(frame, text="جودة الفيديو:", bg="#263238", fg="#FFFFFF", font=("Roboto", 12)).grid(row=3, column=0, sticky="w", pady=15)
quality_var = tk.StringVar(value="720")
quality_options = ["360", "480", "720", "1080"]
quality_menu = ttk.Combobox(frame, textvariable=quality_var, values=quality_options, width=10, font=("Roboto", 12), state="readonly")
quality_menu.grid(row=3, column=1, padx=5, pady=15)

# تنسيق التحميل
tk.Label(frame, text="تنسيق التحميل:", bg="#263238", fg="#FFFFFF", font=("Roboto", 12)).grid(row=4, column=0, sticky="w", pady=15)
format_var = tk.StringVar(value="mp4")
format_options = ["mp4", "mp3"]
format_menu = ttk.Combobox(frame, textvariable=format_var, values=format_options, width=10, font=("Roboto", 12), state="readonly")
format_menu.grid(row=4, column=1, padx=5, pady=15)

# شريط التقدم
progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="indeterminate")
progress_bar.grid(row=5, column=0, columnspan=3, pady=20)

# زر التحميل
tk.Button(frame, text="تحميل", command=download_playlist, bg="#008CBA", fg="white", font=("Roboto", 14), relief="flat", activebackground="#005f73").grid(row=6, column=1, pady=20)

# زر فتح المجلد
open_folder_button = tk.Button(frame, text="فتح مجلد الحفظ", command=open_folder, state=tk.DISABLED, bg="#F44336", fg="white", font=("Roboto", 14), relief="flat", activebackground="#C62828")
open_folder_button.grid(row=7, column=1, pady=15)

root.mainloop()
