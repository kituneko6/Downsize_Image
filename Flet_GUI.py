# %%

import requests, os
import flet as ft
from flet import Image
from io import BytesIO
import base64
from PIL import Image, ExifTags
import pyperclip
from disco_bot import client, send_image
import asyncio
import sys

def resource_path(relative_path):
    try:
        # PyInstallerのとき
        base_path = sys._MEIPASS
    except AttributeError:
        # 通常実行時
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)



with open(resource_path("../bot_token.txt"), 'r', encoding='utf-8') as file:
    TOKEN = file.read().strip()
print(TOKEN)



def main(page: ft.Page):
    page.title = "画像取得TEST_APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url = ft.TextField(label = "画像URLを入力", width=400)

    image_display = ft.Image("favicon.png")
    status_text = ft.Text("画像URLを入力して、表示ボタンを押してください")
    send_image_text = ft.Text("")




    ###ボタン：クリップボードの内容をコピー###
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

                image_data = BytesIO(response.content)
                image_in = Image.open(image_data)
                image_in.save("import.PNG")

            else:
                image_in = Image.open(_url[1:len(_url)-1])



            #取得画像をリサイズし、ローカルに保存
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
            print(f"画像が正常に読み込まれました！\nサムネイルサイズ{image_thumbnail.size}")

            await handle_send_image()

        except Exception as ex:
            status_text.value = f"エラーが発生しました：{ex}"
            print(f"エラーが発生しました：{ex}")

        page.update()
    




    ###画像のExif情報を修正###
    def fix_Exif(image):
        try:
            exif = image._getexif()
            if exif is not None:
                ori_key = next(key for key, val in ExifTags.TAGS.items() if val == 'Orientation')
                ori = exif.get(ori_key)

            if ori == 2:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif ori == 3:
                image = image.rotate(180, expand = True)
            elif ori == 4:
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
            elif ori == 5:
                image = image.transpose(Image.FLIP_TOP_BOTTOM).rotate(-90, expand = True)
            elif ori == 6:
                image = image.rotate(-90, expand = True)
            elif ori == 7:
                image = image.transpose(Image.FLIP_LEFT_RIGHT).rotate(-90, expand = True)
            elif ori == 8:
                image = image.rotate(90, expand = True)
        
        except Exception as e:
            status_text.value = f"エラーが発生しました：{e}"
            print(f"エラーが発生しました：{e}")
        return image




    ###比率をそのままリサイズ###
    def scale_size(image, hei):
        image = fix_Exif(image)
        x_size = image.width
        y_size = image.height
        original_size = image.size
        
        try:
            if x_size > hei or y_size > hei: #指定されたサイズよりも大きい場合リサイズ
                image.thumbnail((hei, hei))
                status_text.value = f"画像リサイズ成功: {original_size} -> {image.size}"
                print(f"画像リサイズ成功: {original_size} -> {image.size}")
            else:
                status_text.value = f"リサイズ不要：{original_size}"
                print(f"リサイズ不要：{original_size}")
            return image
        
        except Exception as ex:
            status_text.value = f"リサイズERROR：{ex}"
            print(f"リサイズERROR：{ex}")
            raise
        
    copy_button = ft.ElevatedButton("Past to Clipborad", on_click=copy_clip)  #クリップボードから貼り付けボタン
    fetch_button = ft.ElevatedButton("変換＆URL取得", on_click=fetch_image)  #画像の変換表示、URL取得ボタン




    ###GUI設定###
    page.add(
        ft.Row([
            url,
            copy_button,
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ft.Column([
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




async def run_all():
    bot_task = asyncio.create_task(client.start(TOKEN))
    gui_task = asyncio.create_task(ft.app_async(target=main))
    await asyncio.gather(bot_task, gui_task)


if __name__ == "__main__":
    asyncio.run(run_all())

