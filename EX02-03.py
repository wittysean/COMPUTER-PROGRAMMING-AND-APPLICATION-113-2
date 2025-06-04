# Install feedparser
!pip install feedparser -q

# Import feedparser and parse RSS feed
import feedparser
feed_url = "https://tw.news.yahoo.com/rss"
feed_data = feedparser.parse(feed_url)

# 引入相關模組
from google.colab import auth
from google.auth import default
import gspread

auth.authenticate_user()  # 進行授權
creds, _ = default()      # 使用 default 方法獲取驗證信息
gc = gspread.authorize(creds)  # 使用 creds 變數授權 gspread 模組

# Open Google Sheet and write RSS feed data
url = 'https://docs.google.com/spreadsheets/d/157iBMp_IXG2wvojAMvuKWNPsF4mgFJ8zl_cDoJ_EG64E/edit?gid=0#gid=0'
workbook = gc.open_by_url(url)

sheet = workbook.get_worksheet(0)

sheet.clear()
sheet.append_row(['title', 'summary', 'link'])

for entry in feed_data.entries:
    sheet.append_row([entry.title, entry.summary, entry.link])