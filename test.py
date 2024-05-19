from gradio_client import Client, file
from PIL import Image
import os
import time
import requests
import io
import base64

def iclight():
  try:
    start_time = time.time()  # 開始時間を記録
    print('関数の開始')

    input_fg_url = 'https://i.ibb.co/WGMS9RC/9e2a786089bc.jpg'
    input_fg_data = requests.get(input_fg_url).content  # URLから画像データを取得
    input_fg_image = Image.open(io.BytesIO(input_fg_data))  # 画像データからPillowイメージを作成
    width, height = input_fg_image.size  # 画像の幅と高さを取得
    print('幅と高さ')
    print(width)
    print(height)

    # ユニックス秒をseedに割り当てる
    unix_seconds = int(time.time())
    
    print('画像の加工 開始')
    client = Client("lllyasviel/IC-Light")
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
      api_name="/process_relight",
    )
    print("Result:", result)  # resultの内容を出力

    # 生成された画像のパスを取得
    generated_image_path = result[1][0]['image']
    print("Generated image path:", generated_image_path)  # 生成された画像のパスを出力

    # 画像を読み込む
    image = Image.open(generated_image_path)

    # 画像をBase64エンコードされた文字列に変換
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_string = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # プレフィックスを追加
    prefixed_base64_string = f"data:image/jpeg;base64,{base64_string}"

    # Base64エンコードされた文字列をresult.txtに保存
    with open('result.txt', 'w') as file_output:
      file_output.write(prefixed_base64_string)

    end_time = time.time()  # 終了時間を記録
    execution_time = end_time - start_time  # 実行時間を計算
    print(f"関数の実行時間: {execution_time:.2f}秒")

    # Base64エンコードされた文字列をコンソールに表示

  except Exception as e:
    print('error', e)
    return f'Error: {e}'