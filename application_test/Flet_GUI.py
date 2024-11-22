# %%

import requests
import flet as ft
from flet import Image
from io import BytesIO
import base64

proxies_dic = {"http": "http://g3.konicaminolta.jp:8080",
                "https": "http://g3.konicaminolta.jp:8080",}


def main(page: ft.Page):
    page.title = "画像取得TEST_APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url = ft.TextField(label = "画像URLを入力", width=400)

    image_display = ft.Image(R"C:\Users\t68351\AppData\Local\Programs\Python\Python312\Lib\site-packages\flet\web\favicon.png")
    status_text = ft.Text("画像URLを入力して、表示ボタンを押してください")
    
    
    def fetch_image(e):
        nonlocal image_display
        try:
            response = requests.get(url.value, proxies=proxies_dic)
            response.raise_for_status()
            image_data = BytesIO(response.content)
            image_base64 = base64.b64encode(image_data.getvalue()).decode("utf-8")
            
            image_display.src_base64 = image_base64
            status_text.value = "画像が正常に読み込まれました！"

        except Exception as ex:
            status_text.value = f"エラーが発生しました：{ex}"

        page.update()

    fetch_button = ft.ElevatedButton("表示", on_click=fetch_image)

    page.add(
        ft.Column([
            url,
            fetch_button,
            status_text,
            image_display,
        ],
        alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    )

ft.app(main)




