import requests
url = 'https://data.kcg.gov.tw/dataset/7059ab4b-9f3c-4cc8-8667-02221e76fc7f/resource/fc4bbc3e-b019-4c3b-8526-72b29bc0a77e/download/11311.json'
response = requests.get(url)
response.status_code  # Should return 200 if successful

stats = response.json()
stats[0]

import csv
import io

wr = []
wr.append(list(stats[0].keys()))
for i in stats:
    wr.append(list(i.values()))

output = io.StringIO()
writer = csv.writer(output)
writer.writerows(wr)

output.seek(0)
reader = csv.reader(output)
stats = list(reader)
stats

!pip install gradio -q

import gradio as gr

def stat_info(id):
    print(f"User selected ID: {id}")

    for i in stats[1:]:
        print(f"Checking row: {i}")

        if len(i) < 8:
            print("Skipping row: too few columns")
            continue

        if str(i[1]).strip() == str(id).strip():
            lat_str, lon_str = i[6], i[7]

            if not lat_str or not lon_str:
                return f"經緯度缺失: lat={lat_str}, lon={lon_str}", ""

            try:
                lat = float(lat_str)
                lon = float(lon_str)
            except (ValueError, TypeError):
                return f"經緯度格式錯誤: lat={lat_str}, lon={lon_str}", ""

            info = f"統計區({id})\n戶數:{i[2]}戶\n男:{i[3]}人\n女:{i[4]}人\n人口:{i[5]}人"
            return info, get_html(lat, lon)

    return "找不到資料", ""

def get_html(lat, lon):
    iframe = f'''
    <iframe style="width: 100%; height: 400px;"
        src="https://www.openstreetmap.org/export/embed.html?bbox={lon-0.01}%2C{lat-0.01}%2C{lon+0.01}%2C{lat+0.01}&layer=mapnik&marker={lat}%2C{lon}">
    </iframe>
    '''
    return iframe

menu = []
for i in stats[1:]:
    if len(i) >= 2:
        menu.append(i[1].strip())

iface = gr.Interface(
    fn=stat_info,
    inputs=gr.Dropdown(choices=menu, label="統計區代碼"),
    outputs=[gr.Textbox(label="統計資訊"), gr.HTML(label="地圖地點")]
)
iface.launch(debug=True)