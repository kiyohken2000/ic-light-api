import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, file
from PIL import Image
import time
import requests
import io
import base64

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def main():
  try:
    print('関数の開始')

    start_time = time.time()  # 開始時間を記録
    
    # 受信したテキストを代入
    request_dict = request.get_json()
    recieved_image_url = str(request_dict['image_url'])
    prompt = str(request_dict['prompt'])
    bg_source = str(request_dict['bg_source'])
    print('受信したパラメーター')
    print(recieved_image_url)
    print(prompt)
    print(bg_source)

    # 画像を取得して解像度を決定
    input_fg_url = recieved_image_url
    # URLから画像データを取得
    input_fg_data = requests.get(input_fg_url, timeout=20).content
    input_fg_image = Image.open(io.BytesIO(input_fg_data))  # 画像データからPillowイメージを作成
    width, height = input_fg_image.size  # 画像の幅と高さを取得
    print('幅と高さ')
    print(width)
    print(height)

    # ユニックス秒をseedに割り当てる
    seed = int(time.time())
    
    # 画像の加工
    print('画像の加工 開始')
    client = Client("lllyasviel/IC-Light")
    result = client.predict(
      input_fg=file(recieved_image_url),
      prompt=prompt,
      image_width=width,  # 元の画像の幅を使用
      image_height=height,  # 元の画像の高さを使用
      num_samples=1,
      seed=seed,  # ユニックス秒をseedに使用
      steps=25,
      a_prompt="best quality",
      n_prompt="lowres, bad anatomy, bad hands, cropped, worst quality",
      cfg=2,
      highres_scale=1.5,
      highres_denoise=0.5,
      lowres_denoise=0.9,
      bg_source=bg_source,
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

    end_time = time.time()  # 終了時間を記録
    execution_time = end_time - start_time  # 実行時間を計算
    print(f"関数の実行時間: {execution_time:.2f}秒")

    # 結果をJSONフォーマットで返す
    api_result = {
      'base64_string': prefixed_base64_string,
      'execution_time': execution_time
    }
    return jsonify(api_result)

  except Exception as e:
    print('error', e)
    return jsonify({'error': str(e)})
  
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))