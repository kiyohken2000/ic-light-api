from gradio_client import Client, file
from PIL import Image
import os
import time
import requests
import io

def iclight():
  try:
    start_time = time.time()  # 開始時間を記録
    print('関数の開始')
    client = Client("lllyasviel/IC-Light")

    input_fg_url = 'https://i.ibb.co/2Ff9fkC/cd50e12b2ede.jpg'
    input_fg_data = requests.get(input_fg_url).content  # URLから画像データを取得
    input_fg_image = Image.open(io.BytesIO(input_fg_data))  # 画像データからPillowイメージを作成
    width, height = input_fg_image.size  # 画像の幅と高さを取得

    # ユニックス秒をseedに割り当てる
    unix_seconds = int(time.time())
    
    result = client.predict(
      input_fg=file(input_fg_url),
      prompt="indoors, bedroom, day",
      image_width=width,  # 元の画像の幅を使用
      image_height=height,  # 元の画像の高さを使用
      num_samples=1,
      seed=unix_seconds,  # ユニックス秒をseedに使用
      steps=25,
      a_prompt="best quality",
      n_prompt="lowres, bad anatomy, bad hands, cropped, worst quality",
      cfg=2,
      highres_scale=1.5,
      highres_denoise=0.5,
      lowres_denoise=0.9,
      bg_source="None",
      api_name="/process_relight"
    )
    print(result)

    # 生成された画像のパスを取得
    generated_image_path = result[1][0]['image']

    # 画像を読み込む
    image = Image.open(generated_image_path)

    # 現在のディレクトリを取得
    current_dir = os.getcwd()

    # UNIXミリ秒をファイル名に使用
    unix_milliseconds = int(time.time() * 1000)
    save_filename = f"{unix_milliseconds}.jpg"

    # JPGで保存するパスを作成
    save_path = os.path.join(current_dir, save_filename)

    # JPGで保存
    image.save(save_path, 'JPEG')

    print(f"生成された画像を {save_path} に保存しました。")

    end_time = time.time()  # 終了時間を記録
    execution_time = end_time - start_time  # 実行時間を計算
    print(f"関数の実行時間: {execution_time:.2f}秒")

  except Exception as e:
    print('error', e)
    return f'Error: {e}'