import sys
import re
import configparser
import tkinter as tk
import tkinter.messagebox as mb
from tkinterdnd2 import DND_FILES, TkinterDnD
from imagecropper import image_cropper

def main():
    config = read_config()
    gui(config)

# GUI ウィンドウ
def gui(config):
    # ウィンドウ設定
    root = TkinterDnD.Tk()
    root.title('Image Cropper')
    root.geometry('330x150')
    default_color = root.cget("bg")
    # 変数宣言
    left = tk.StringVar()
    left.set(config['left'])
    upper = tk.StringVar()
    upper.set(config['upper'])
    right = tk.StringVar()
    right.set(config['right'])
    lower = tk.StringVar()
    lower.set(config['lower'])
    # ボーダー設定
    border_frame = tk.Frame(root, height=130, width=150, pady=10, padx=10, relief=tk.SOLID, bg=default_color, bd=1)
    border_frame.place(x=10, y=10)
    # 左
    border_left_label = tk.Label(border_frame, text='Left：')
    border_left_label.place(x=0, y=10)
    border_left_input = tk.Entry(border_frame, textvariable=left, readonlybackground='white', justify=tk.CENTER)
    border_left_input.configure(validate='key', vcmd=(border_left_input.register(pre_validation_crop), '%s', '%P'))
    border_left_input.place(x=50, y=10, width=60, height=21)
    border_left_unit = tk.Label(border_frame, text='px')
    border_left_unit.place(x=110, y=10)
    # 上
    border_upper_label = tk.Label(border_frame, text='Upper：')
    border_upper_label.place(x=0, y=35)
    border_upper_input = tk.Entry(border_frame, textvariable=upper, readonlybackground='white', justify=tk.CENTER)
    border_upper_input.configure(validate='key', vcmd=(border_upper_input.register(pre_validation_crop), '%s', '%P'))
    border_upper_input.place(x=50, y=35, width=60, height=21)
    border_upper_unit = tk.Label(border_frame, text='px')
    border_upper_unit.place(x=110, y=35)
    # 右
    border_right_label = tk.Label(border_frame, text='Right')
    border_right_label.place(x=0, y=60)
    border_right_input = tk.Entry(border_frame, textvariable=right, readonlybackground='white', justify=tk.CENTER)
    border_right_input.configure(validate='key', vcmd=(border_right_input.register(pre_validation_crop), '%s', '%P'))
    border_right_input.place(x=50, y=60, width=60, height=21)
    border_right_unit = tk.Label(border_frame, text='px')
    border_right_unit.place(x=110, y=60)
    # 下
    border_lower_label = tk.Label(border_frame, text='Lower')
    border_lower_label.place(x=0, y=85)
    border_lower_input = tk.Entry(border_frame, textvariable=lower, readonlybackground='white', justify=tk.CENTER)
    border_lower_input.configure(validate='key', vcmd=(border_lower_input.register(pre_validation_crop), '%s', '%P'))
    border_lower_input.place(x=50, y=85, width=60, height=21)
    border_lower_unit = tk.Label(border_frame, text='px')
    border_lower_unit.place(x=110, y=85)
    # ドロップエリア
    drop_frame = tk.Frame(root, height=130, width=150, pady=10, padx=10, relief=tk.SOLID, bg=default_color, bd=1)
    drop_frame.drop_target_register(DND_FILES)
    drop_frame.dnd_bind('<<Drop>>', lambda e: drop(e.data, left.get(), upper.get(), right.get(), lower.get()))
    drop_frame.place(x=170, y=10)
    # ドロップテキストラベル
    drop_label = tk.Label(drop_frame, text='* Drop image file here')
    drop_label.place(x=65, y=55, anchor=tk.CENTER)
    # 各種タイトル
    border_label = tk.Label(root, text='Crop settings')
    border_label.place(x=20, y=0)
    dorp_label = tk.Label(root, text='Drop files')
    dorp_label.place(x=180, y=0)
    # 閉じるボタンの制御
    root.protocol("WM_DELETE_WINDOW", lambda: exit(left.get(), upper.get(), right.get(), lower.get()))
    # GUI描画
    root.mainloop()

# 画像処理
def drop(files, left, upper, right, lower):
    left = int(left or 0)
    upper = int(upper or 0)
    right = int(right or sys.maxsize)
    lower = int(lower or sys.maxsize)
    files = dnd2_parse_files(files)
    for file in files:
        print(file)
        for ext in image_cropper.IMAGE_EXTS:
            if re.search(f'\.{ext}$', file):
                image_cropper.image_crop(file, [left, upper, right, lower])

# DnD2 ファイルパスの解析
def dnd2_parse_files(files_str):
    start = 0
    length = len(files_str)
    files = []
    while start < length:
        if files_str[start] == '{':
            end = files_str.find('}', start+1)
            file = files_str[start+1 : end]
            start = end + 2
        else:
            end = files_str.find(' ', start)
            if end < 0:
                file = files_str[start:]
                start = length
            else:
                file = files_str[start : end]
                start = end + 1
        files.append(file)
    return files

# 終了処理
def exit(left, upper, right, lower):
    save_config(left, upper, right, lower)
    sys.exit()

# バリデーションチェック
def pre_validation_crop(before_word, after_word):
    return ((after_word.isdecimal() or after_word == '') and (len(after_word) <= 8 or len(after_word) == 0))

# 設定の読み込み
def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    default = config['DEFAULT']
    configs = {
        'left': default.get('left') if default.get('left') != None else ''
        , 'upper': default.get('upper') if default.get('upper') != None else ''
        , 'right': default.get('right') if default.get('right') != None else ''
        , 'lower': default.get('lower') if default.get('lower') != None else ''

    }
    return configs

# 設定の保存
def save_config(left, upper, right, lower):
    config = configparser.ConfigParser()
    config.set('DEFAULT', 'left', left)
    config.set('DEFAULT', 'upper', upper)
    config.set('DEFAULT', 'right', right)
    config.set('DEFAULT', 'lower', lower)
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    main()

# https://magicode.io/taraku3/articles/20c53c1f06cf4131b452271f214a73de
# https://teratail.com/questions/226925
