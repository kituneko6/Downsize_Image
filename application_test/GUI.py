# %% 

import customtkinter
import pyperclip, requests
from PIL import Image, ImageTk
from io import BytesIO

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

        self.label = customtkinter.CTkLabel(master=self, text="")
        self.label.grid(row=1)
        
        self.EX_button = customtkinter.CTkButton(master=self, text="read_Image", command=self.Get_images, font=self.fonts)
        self.EX_button.grid(row=2)
    

    def button_function(self): #copyボタンでtextboxにclipboadの内容をコピー
        try:
            clip = pyperclip.paste()
            self.textbox.delete(0, "end")
            self.textbox.insert(0, clip)
        except Exception as e:
            self.textbox.delete(0, "end")
            self.textbox.insert(0, f"エラー：{str(e)}")
        

    def scale_size(img, height):
        width = round(img.width * height / img.height)
        return img.resize((width, height))

    def Get_images(self):
        url = "https://ashhaddevlab.gallerycdn.vsassets.io/extensions/ashhaddevlab/customtkinter-snippets/4.0.0/1707726079732/Microsoft.VisualStudio.Services.Icons.Default"
        #url = self.textbox.get()
        try:
            respon = requests.get(url)
            respon.raise_for_status()

            img_data = BytesIO(respon.content)
            image = Image.open(img_data)

            out_image = self.scale_size(image, 1920)
            image = self.scale_size(image, 280)

            tk_image = ImageTk.PhotoImage(image)

            self.label.config(image=tk_image)
            self.label = tk_image
        
        except requests.exceptions.RequestException as e:
            print("画像の取得に失敗しました：", e)
    



if __name__ == "__main__":
    app = App()
    app.mainloop()



