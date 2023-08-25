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

def display_row_by_column(update: Update, context):
    column_value = update.message.text.strip()
    column_values = sheet2.col_values(2)

    if column_value in column_values:
        row_num = column_values.index(column_value) + 1
        row = sheet2.row_values(row_num)
        header = sheet2.row_values(1)
        
        # Menyusun data header dan baris sebagai tabel vertikal
        table_data = [[header[i], row[i]] for i in range(len(header))]
        
        # Menambahkan baris pembatas sebelum row ke-8 (index 7)
        index_of_separator = 7  # Index column sebelum pembatas
        separator = ['-' * len(cell) for cell in table_data[0]]  # Baris pembatas
        
        # Memasukkan baris pembatas sebelum row ke-8
        table_data.insert(index_of_separator, separator)
        
        # Menggunakan tabulate untuk format tabel
        table = tabulate(table_data, tablefmt="plain")
        
        update.message.reply_text("Data ditemukan:\n```\n" + table + "\n```", parse_mode="Markdown")
    else:
        update.message.reply_text("Data tidak ditemukan.")

# Menghubungkan handler pesan ke fungsi display_row_by_column
message_handler = MessageHandler(Filters.text & ~Filters.command, display_row_by_column)
dispatcher.add_handler(message_handler)

# Memulai bot Telegram
updater.start_polling()

# Jaga agar bot berjalan terus
updater.idle()





