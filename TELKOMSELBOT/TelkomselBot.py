import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from tabulate import tabulate
from telegram import Update


# Konfigurasi Google Spreadsheet
spreadsheet_key = '1Jfu7VJqOq4ELZMeVRgdC7TN2OgDRBHXSukuZleVcRHE'
credentials = ServiceAccountCredentials.from_json_keyfile_name('telkomselbot-399c84132ae2.json', ['https://www.googleapis.com/auth/spreadsheets'])
client = gspread.authorize(credentials)
sheet = client.open_by_key(spreadsheet_key).sheet1
sheet2 = client.open_by_key(spreadsheet_key).get_worksheet(1)

telegram_token = '6378921668:AAGTC5joAk6Wm6YlrpzD9jKk-Sdmdnm-a3M'
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher

# Fungsi untuk menampilkan seluruh row berdasarkan column yang dimasukkan
def display_row_by_column(update: Update, context):
    column_value = update.message.text.strip()  # Mendapatkan nilai yang dikirimkan oleh pengguna
    column_values = sheet2.col_values(2) 

    if column_value in column_values:
        row_num = column_values.index(column_value) + 1
        row = sheet2.row_values(row_num)
        
        # Mengambil header (baris pertama) dari spreadsheet
        header = sheet2.row_values(1)
        
        # Menggabungkan header dan data baris yang ditemukan
        table_data = list(zip(header, row))  # Menggabungkan header dengan data row secara vertikal
        
        # Membuat pesan dengan format yang diinginkan
        message = "\n".join([f"{header_item}: {row_item}" for header_item, row_item in table_data])
        
        update.message.reply_text(message)
    else:
        update.message.reply_text("Data tidak ditemukan.")

# Menghubungkan handler pesan ke fungsi display_row_by_column
message_handler = MessageHandler(Filters.text & ~Filters.command, display_row_by_column)
dispatcher.add_handler(message_handler)

# Memulai bot Telegram
updater.start_polling()

# Jaga agar bot berjalan terus
updater.idle()

