import datetime
import itertools
import os
import sys
# FutureWarningを表示しないようにする
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as st

warnings.simplefilter('ignore', FutureWarning)


def make_dirs(dirs):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def yes_and_no_probabilities(data_path):
    experiment_type = ""
    yes_count = 0
    no_count = 0

    # ファイル走査
    files = os.listdir(data_path)
    for file in files:
        # ファイル読み込み
        df = pd.read_csv(os.path.join(data_path, file), header=0)
        # Experiment Typeを読み込み
        experiment_type = df["Experiment Type"][0]
        # Correct AnswerがTrueならYes, FalseならNoをカウント
        yes_count += df["Correct Answer"].sum()
        no_count += len(df) - df["Correct Answer"].sum()

    if files:
        # YesとNoの割合を計算
        yes_prob = yes_count / (yes_count + no_count)
        no_prob = no_count / (yes_count + no_count)
        print(f"==================== Experiment Type {experiment_type} ====================")
        print(f"Yes Probability -> {yes_prob}, No Probability -> {no_prob}")


def read_response_time(data_path):
    # DataFrameを作成
    response_time = pd.Series()

    # ファイル走査
    files = os.listdir(data_path)
    if not files:
        raise Exception("No files in the directory.")

    # Experiment Typeを読み込み
    df = pd.read_csv(os.path.join(data_path, files[0]), header=0)
    experiment_type = df["Experiment Type"][0]

    for file in files:
        # ファイル読み込み
        df = pd.read_csv(os.path.join(data_path, file), header=0)
        # Is CorrectがTrueのもののみ抽出
        correct_df = df[df["Is Correct"]]
        # Time Differenceを追加
        response_time = response_time.append(correct_df["Time Difference (seconds)"])

    # 番号を振り直す
    response_time.reset_index(drop=True, inplace=True)
    # numpy配列に変換
    response_time = np.array(response_time)

    return experiment_type, response_time


def draw_histograms(experiment_type, response_time):
    # 実験回数を表示
    print(f"Number of Experiments: {len(response_time)}")

    # binsの数を指定
    bins_num = 20
    hist, bins = np.histogram(response_time, bins=bins_num, weights=np.ones(len(response_time)) / len(response_time))
    # ビンの中央値を計算
    bin_centers = 0.5 * (bins[:-1] + bins[1:])

    # 正規分布のパラメータ推定
    mu, std = st.norm.fit(response_time)
    print(f"Normal Distribution -> Avarage: {mu}, Standard deviation: {std}")

    # 正規分布を描画
    # グラフの比較をしやすいようにするために横軸の範囲を固定
    max_time_difference = 1.0
    x = np.linspace(min(response_time), max_time_difference, 100)
    y = st.norm.pdf(x, mu, std)
    # ヒストグラムと同じ総面積になるようにスケーリング
    y_scaled = y * sum(hist) * (bins[1] - bins[0])

    # ヒストグラムを描画
    plt.bar(bin_centers, hist, width=bins[1] - bins[0], alpha=0.7, label='Histogram')
    plt.plot(x, y_scaled, 'r-', label=fr'Normal Distribution $(\mu={mu:.2f},\ \sigma={std:.2f})$')

    # グラフの設定
    plt.xlim(min(response_time), max_time_difference)

    plt.title(f'Experiment Type {experiment_type} (data size = {len(response_time)})')
    plt.xlabel('Response Time [s]')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.savefig(f"./data/analysis/{experiment_type}.png")
    # plt.show()
    plt.close()

    return mu, std


def welchs_test(response_times_configs):
    # 有意水準を指定
    p = 0.05
    for response_times_configs_combs in itertools.combinations(response_times_configs, 2):
        response_times_configs_0 = response_times_configs_combs[0]
        response_times_configs_1 = response_times_configs_combs[1]
        p_value = st.ttest_ind(response_times_configs_0["response_time"], response_times_configs_1["response_time"], equal_var=False).pvalue
        exists_significance_difference = True if p_value < p else False
        print(
            f"Experiment Type {response_times_configs_0['experiment_type']} and {response_times_configs_1['experiment_type']} -> p-value: {p_value}, Significance Difference: {exists_significance_difference}"
        )


def draw_result(response_times_configs):
    # 縦軸が平均値、横軸が各実験の種類の棒グラフを描画
    plt.bar(
        [response_times_config["experiment_type"] for response_times_config in response_times_configs],
        [response_times_config["average"] for response_times_config in response_times_configs],
        yerr=[response_times_config["standard_deviation"] for response_times_config in response_times_configs],
        capsize=10,
    )

    # グラフの設定
    plt.title("Response Time of Each Experiment Type")
    plt.xlabel("Experiment Type")
    plt.ylabel("Response Time [s]")
    plt.savefig("./data/analysis/result.png")
    # plt.show()
    plt.close()


if __name__ == "__main__":
    dir_paths = [
        "./data/analysis",
        "./data/log",
    ]
    make_dirs(dir_paths)

    data_paths = [
        "./data/main/a",
        "./data/main/b",
        "./data/main/c",
        "./data/main/d",
    ]
    response_times_configs = []

    # 現在の時間を取得
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # 標準出力をファイルにリダイレクト
    sys.stdout = open(f"./data/log/{now}.txt", "w")

    for data_path in data_paths:
        # YesとNoの確率を計算
        yes_and_no_probabilities(data_path)
        # Time Differenceを読み込み
        experiment_type, response_time = read_response_time(data_path)
        # ヒストグラムを描画
        mu, std = draw_histograms(experiment_type, response_time)
        response_times_configs.append(
            {
                "experiment_type": experiment_type,
                "response_time": response_time,
                "average": mu,
                "standard_deviation": std,
            }
        )

    # 正規分布間に有意差があるかどうかを検定
    welchs_test(response_times_configs)

    # 各実験のまとめグラフを描画
    draw_result(response_times_configs)

    # 標準出力を元に戻す
    sys.stdout.close()
    sys.stdout = sys.__stdout__
