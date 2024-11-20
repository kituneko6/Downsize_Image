# %% 

import customtkinter
import pyperclip, requests
from PIL import Image, ImageTk
from io import BytesIO

proxies_dic = {"http": "http://g3.konicaminolta.jp:8080",
                "https": "http://g3.konicaminolta.jp:8080",}

FONT_TYPE = "meirio"

class App(customtkinter.CTk):
    def __init__(self):     #windowの設定
        super().__init__()

        self.fonts = (FONT_TYPE, 15)
        self.geometry("460x320")
        self.title("test")

        self.setup_form()
    

    def setup_form(self):   #GUIのForm設定
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        self.textbox = customtkinter.CTkEntry(master=self, placeholder_text="リンクを入力", width=220, font=self.fonts)
        self.textbox.grid(row=0, column=0, padx=10, pady=20)

        self.button = customtkinter.CTkButton(master=self, text="copy", command=self.button_function, font=self.fonts)
        self.button.grid(row=0, column=1, padx=10, pady=20)

        self.label = customtkinter.CTkLabel(master=self, text="------")
        self.label.grid(row=1)
        
        self.EX_button = customtkinter.CTkButton(master=self, text="read_Image", command=self.Get_images, font=self.fonts)
        self.EX_button.grid_columnconfigure(0, weight=1)
        self.EX_button.grid(row=2)

        self.text_label = customtkinter.CTkLabel(master=self, text="")
        self.text_label.grid(row=3)
    

    def button_function(self): #copyボタンでtextboxにclipboadの内容をコピー
        try:
            clip = pyperclip.paste()
            self.textbox.delete(0, "end")
            self.textbox.insert(0, clip)
        except Exception as e:
            self.textbox.delete(0, "end")
            self.textbox.insert(0, f"エラー：{str(e)}")
        

    def scale_size(self, image, hei):
        x_size = image.width
        y_size = image.height

        if x_size > hei or y_size > hei: #指定されたサイズよりも小さい場合そのまま返す
            return image
        else:
            if x_size < y_size: #大きい方の辺を主にしてリサイズ()
                re_size = (image.width, round(image.height * x_size))
            else:
                re_size = (round(image.width * y_size), hei)
            return image.resize(re_size)


    def Get_images(self):
        url = "https://ashhaddevlab.gallerycdn.vsassets.io/extensions/ashhaddevlab/customtkinter-snippets/4.0.0/1707726079732/Microsoft.VisualStudio.Services.Icons.Default"
        #url = self.textbox.get()
        try:
            respon = requests.get(url, proxies=proxies_dic)
            respon.raise_for_status()

            img_data = BytesIO(respon.content)
            image = Image.open(img_data)
            
            out_image = self.scale_size(image, 1920)
            image = self.scale_size(image, 280)

            ctk_image = customtkinter.CTkImage(light_image=image, size=(image.width, image.height))

            self.label.configure(image=ctk_image)
            self.label.image = ctk_image

            self.text_label.configure(text="画像を正常に取得しました！", text_color="green")
        except requests.exceptions.RequestException as e:
            self.text_label.configure(text="画像の取得に失敗しました", text_color="red")
            print("画像の取得に失敗しました：", e)
    



if __name__ == "__main__":
    app = App()
    app.mainloop()



