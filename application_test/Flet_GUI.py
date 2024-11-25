import requests
import flet as ft
from flet import Image
from io import BytesIO
import base64
from PIL import Image
import pyperclip
from disco_bot import client, send_image
import asyncio

TOKEN = "MTMwOTQyNjc3NDAwOTk3NDg3NA.G4v112.06AVIquouZ-nznSejhxXE4_zGtF9N3VOugKKSI"


'''
proxies_dic = {"http": "http://g3.konicaminolta.jp:8080",
                "https": "http://g3.konicaminolta.jp:8080",}
'''

def main(page: ft.Page):
    page.title = "画像取得TEST_APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url = ft.TextField(label = "画像URLを入力", width=400)

    image_display = ft.Image("favicon.png")
    status_text = ft.Text("画像URLを入力して、表示ボタンを押してください")
    send_image_text = ft.Text("")

    ###クリップボードの内容をコピー###
    def copy_clip(e):
        try:
            clip = pyperclip.paste()
            url.value = clip
            page.update()
        except Exception as ex:
            status_text.value = f"Copy_ERROR：{ex}"
    
    ###イメージ取得、リサイズ、保存、表示切替###
    async def fetch_image(e):
        nonlocal image_display
        global image_data
        try:
            _url = url.value
            if _url[:4] == "http": 
                response = requests.get(_url)
                response.raise_for_status()
            else:
                image_in = Image.open(_url)

            if "image" not in response.headers["content-type"]:
                raise ValueError("URLが画像ではありません")

            image_data = BytesIO(response.content)
            image_in = Image.open(image_data)
            image_in.save("import.PNG")

            #取得画像をローカルに保存
            image_resize = scale_size(image_in, 2048)
            image_byte = BytesIO()
            image_resize.save(image_byte, format="PNG")
            image_resize.save('output.png')

            #画像サムネイルを作成
            image_thumbnail = scale_size(image_in, 600)
            image_thumb_byte = BytesIO()
            image_thumbnail.save(image_thumb_byte, format="PNG")

            #画像をエンコードして表示
            image_base64 = base64.b64encode(image_thumb_byte.getvalue()).decode("utf-8")
            image_display.src_base64 = image_base64
            status_text.value = f"画像が正常に読み込まれました！\nサムネイルサイズ{image_thumbnail.size}"

            await handle_send_image()

        except Exception as ex:
            status_text.value = f"エラーが発生しました：{ex}"

        page.update()
    


    ###比率をそのままリサイズ###
    def scale_size(image, hei):
        x_size = image.width
        y_size = image.height
        original_size = image.size
        try:
            if x_size > hei or y_size > hei: #指定されたサイズよりも大きい場合リサイズ
                image.thumbnail((hei, hei))
                status_text.value = f"画像リサイズ成功: {original_size} -> {image.size}"
            else:
                status_text.value = f"リサイズ不要：{original_size}"
            return image
        
        except Exception as ex:
            status_text.value = f"リサイズERROR：{ex}"
            raise
        
    copy_button = ft.ElevatedButton("Copy", on_click=copy_clip)  #クリップボードから貼り付けボタン
    fetch_button = ft.ElevatedButton("表示", on_click=fetch_image)  #画像の変換表示、URL取得ボタン

    ###GUI設定###
    page.add(
        ft.Column([
            url,
            copy_button,
            fetch_button,
            status_text,
            image_display,
            send_image_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER, spacing=20)
    )

    ###Discord_Botから呼び出し・送信###
    async def handle_send_image():
        try:
            image_path = "output.png"
            url_send = await send_image(image_path)
            pyperclip.copy(url_send)
            if url:
                send_image_text.value = "送信されました"
            else:
                send_image_text.value = "送信できませんでした" 
        except Exception as ee:
            send_image_text.value = f"送信エラー：{ee}"



async def async_main():
    asyncio.create_task(client.start(TOKEN))
    try:
        await ft.app_async(target=main)
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(async_main())
    #ft.app(main)
