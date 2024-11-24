import requests
import flet as ft
from flet import Image
from io import BytesIO
import base64
from PIL import Image


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

    #def copy_clip():
        
    
    ###イメージ取得、リサイズ、保存、表示切替###
    def fetch_image(e):
        nonlocal image_display
        global image_data
        try:
            response = requests.get(url.value)
            response.raise_for_status()

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




