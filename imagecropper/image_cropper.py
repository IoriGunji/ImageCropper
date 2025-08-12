import os
import re
import glob
import sys
from typing import Final, Tuple
from PIL import Image

IMAGE_EXTS: Final[Tuple[str, ...]] = ['png', 'jpg', 'jpeg', 'bmp']
CROP_BOX: Final[Tuple[int, ...]] = [100, 100, 500, 500] #左, 上, 右, 下　

def main():
    chdir = os.path.dirname(__file__)
    files = glob.glob(os.path.join(chdir, '*'))
    for file in files:
        for ext in IMAGE_EXTS:
            if re.search(f'\.{ext}$', file):
                image_crop(file, CROP_BOX)

def image_crop(img_path: str, crop_box: Tuple[int, ...]):
    # 画像読み込み
    try:
        img = Image.open(img_path)
        print(f'Loaded: {img_path}')
    except FileNotFoundError:
        print(f'Error: {img_path} not found. Please check the file name and path!')
        sys.exit()
    # 各種パスの取得
    dir, file = os.path.split(img_path)
    # 出力先ディレクトリの作成
    output = 'cropped'
    os.makedirs(os.path.join(dir, output), exist_ok=True)
    # 画像サイズの取得
    img_width, img_height = img.size
    # バリデーションチェック
    left, upper, right, lower = crop_box
    # 1. 座標の論理チェック
    if left >= right or upper >= lower:
        print(f'Error: The crop area coordinates are invalid!')
        print(f'Specified area: left={left}, upper={upper}, right={right}, lower={lower}')
        print('Area Conditions: left < right and upper < lower must be true.')
        sys.exit()
    # 2. 範囲外のチェック
    if left < 0 or upper < 0 or right > img_width or lower > img_height:
        print(f'Warning: The cropping area exceeds the image range.\nCrop to fit the image range.')
        # 座標を画像の範囲内に調整
        adjusted_left = max(0, left)
        adjusted_upper = max(0, upper)
        adjusted_right = min(img_width, right)
        adjusted_lower = min(img_height, lower)
        # 調整後に有効な切り抜き領域が残っているかチェック
        if adjusted_left >= adjusted_right or adjusted_upper >= adjusted_lower:
            print('Error: The specified crop area is completely outside the bounds of the image, so there is no valid area!')
            sys.exit()
        # 調整後のボックスで上書き
        crop_box = (adjusted_left, adjusted_upper, adjusted_right, adjusted_lower)
    # 画像のトリミング
    cropped_img = img.crop(crop_box)
    # トリミング後の画像の保存
    cropped_img.save(os.path.join(dir, output, file), quality = 100)
    print('Done: The image has been cropped.')

if __name__ == "__main__":
    main()
