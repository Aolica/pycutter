# pycutter
動画の差分を検知して切り取る簡易スクリプト
# 必要ライブラリ
- opencv: `pip install opencv-python`で追加
- moviepy: `pip install moviepy`で追加

# 使い方
`pycutter(video_name, target_time, target_duration, search_frame, N, margin, time_offset)`を呼ぶだけ


`video_name`: 入力したい動画の名前 拡張子は除く
`target_time`: 差分検知を行いはじめる時間　秒で指定
`target_duration`: `target_time`から何秒後まで検知するかの時間　秒で指定
`search_frame`: 映像の変化を評価する時間の長さ
`N`: 検出後に切り取る個数(画面切り替えの回数)
`margin`: 検出誤差を考えて取るべきマージン
`time_offset`: オープニングの暗転から実験動画が始まるまでの時間(つまり検知された時間から切り取り始めるまでのオフセット時間) 秒で指定
