import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip


def pycutter(video_name, target_time, target_duration, search_frame, N, margin, time_offset):

    video_path = f"{video_name}.mp4"
    ###########################
    #main code
    ###########################
    # 動画を開く
    cap = cv2.VideoCapture(video_path)

    # 動画のFPSを取得
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 検出したい時間帯のフレームインデックスを取得
    target_frame_start = int(target_time * fps)
    target_frame_end = int((target_time + target_duration) * fps)
    print("検知開始時間[s]:", target_frame_start/fps, "検知終了時間[s]:", target_frame_end/fps)

    # フレームの読み込みと情報変化量の計算を行う関数
    def calc_frame_diff(frame):
        # グレースケール画像に変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 10フレーム分のグレースケール画像を取得
        frames = [gray]
        for i in range(search_frame):
            _, next_frame = cap.read()
            next_gray = cv2.cvtColor(next_frame, cv2.COLOR_BGR2GRAY)
            frames.append(next_gray)

        # 各フレーム間の差分を計算して合計する
        diff_sum = 0
        for i in range(search_frame):
            diff = cv2.absdiff(frames[i], frames[i + 1])
            diff_sum += diff.sum()

        return diff_sum


    # 検出したい時間帯のsearch_frameごとの情報変化量を計算
    diffs = []
    cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame_start)
    for i in range(target_frame_end - target_frame_start):
        ret, frame = cap.read()
        if not ret:
            break
        diff = calc_frame_diff(frame)
        diffs.append(diff)

    # 最大の情報変化量をもつフレームを計算
    max_diff = max(diffs)
    max_index = diffs.index(max_diff)

    # 検出したフレームのフレームインデックスを取得
    target_frame_index = target_frame_start + max_index

    # 動画を閉じる
    cap.release()

    # 検出した時間を表示
    detected_time = int(target_frame_index/fps)
    print("検出した秒数：", detected_time)



    # トリミングしたい範囲を指定
    t = detected_time + time_offset
    trim_ranges = [(t-margin, t+60+margin)]  # (開始時間, 終了時間)
    for i in range(1, N):
        trim_ranges.append((t+(60*i)-margin, t+(60*i)+60+margin))

    print("トリミングする区間[s]：", trim_ranges)

    for i, trim_range in enumerate(trim_ranges):
        # クリップオブジェクトを作成し、指定範囲でトリミング
        clip = VideoFileClip(video_path).subclip(*trim_range)

        # 出力ファイル名を指定
        output_file = f"{video_name}_trim_{i}.mp4"

        # トリミングしたクリップをファイルに書き出し
        clip.write_videofile(output_file)

if __name__=="__main__":
    ####################
    #Configure
    ####################
    # 動画ファイルの名前(拡張子除く)
    video_name = "1"
    # 検出したい基準の時間
    target_time = 65.0  # 検出を開始する時間 単位は秒
    target_duration = 15.0  #検出する範囲 単位は秒

    # 映像の時間変化を評価する時間 基本いじらなくていい　検出がうまく行かない場合は大きくする
    search_frame = 20

    # 映像に含まれる画面切り替えの回数
    N = 10
    # オープニング動画が暗転してから実験動画が始まるまでの時間
    time_offset = 30 # 単位は秒
    # 動画を切り取る際に検出誤差を考えて取るべきマージン
    margin = 1 # 単位は秒

    pycutter(video_name, target_time, target_duration, search_frame, N, margin, time_offset)
