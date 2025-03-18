import requests
url = "https://data.kcg.gov.tw/dataset/2629db6d-98ec-4b24-8ab1-5dc34d998460/resource/662f822c-632b-4cb3-80f6-b5ac053d210b/download/11311.json"
response = requests.get(url)
stats = response.json()

import gradio as gr

def stat_info(id):
  info = ""
  for row in stats[1:]:
    if row[1] == id:
      info = f'車站編號：{row[1]}\n中文名稱：{row[2]}\n英文名稱：{row[3]}'
      html = get_html(row[4], row[5])
  return info, html

def get_html(latitude, longitude):
  lat = float(latitude)
  lon = float(longitude)
  html = f'''
  <div style="width: 100%; height: 600px;">
    <iframe
      width="100%"
      height="100%"
      frameborder="0"
      scrolling="no"
      marginheight="0"
      marginwidth="0"
      src="https://maps.google.com/maps?q={lat},{lon}&z=15&output=embed">
    </iframe>
  </div>
  '''
  return html

menu = []
for row in stats[1:]:
  menu.append(row[1])

gr.Interface(
    fn = stat_info,
    inputs = gr.Dropdown(choices = menu, label = "車站編號："),
    outputs = [ gr.Textbox(label = "車站資訊："), gr.HTML(label = "車站地圖") ]
).launch()