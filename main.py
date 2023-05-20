"""
人間情報工学課題用プログラム
プログラム作成者：松本琉大桜
e-mail:u021626a[at]ecs.osaka-u.ac.jp

以下のフローでaからdについて行う
1. 画面を描画する
2. Enterで開始
3. 指示を表示する
4. Spaceを押す
5. ランダムの時間（0から5秒）待つ
6. 文字を表示し、その時刻を記録する
7. 反応する。yesならy, noならuを入力する。
8. ボタンを押した時間を記録する
9. 6と9の差を計算する
10. 続ける場合はSpaceを押し、3に戻る
11. 3~10を繰り返す
12. Escで終了
13. csvファイルに書き込む

実験a
内容：単純反応（何らかの情報が呈示されたときに行う反応）
指示：Press y when you see the letter. \n(If you are ready, press Space)
表示させる文字：レポート内の表参照

実験b
内容：物理的照合反応（呈示された情報が事前に記憶していた情報と同じときに行う反応）
指示：Press y if the displayed letter is the same as {指示単語}; if not, press u. \n(If you are ready, press Space)
指示単語：レポート内の表参照
表示させる文字：レポート内の表参照

実験c
内容：名称照合反応（呈示された情報が事前に記憶していた名称と同じ名称で表すことができるときに行う反応）
指示：Press y if the displayed letter reading is {指示単語}; if not, press u. \n(If you are ready, press Space)
指示単語：レポート内の表参照
表示させる文字：レポート内の表参照

実験d
内容：カテゴリー照合反応（呈示された情報が事前に記憶していたカテゴリーと同じカテゴリーで表すことができるときに行う反応）
指示：Press y if the displayed letter reading is the same group as {指示単語}; if not, press u. \n(If you are ready, press Space)
指示単語：レポート内の表参照
表示させる文字：レポート内の表参照
"""

import csv
import os
import random
import tkinter as tk
from datetime import datetime


class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Response Time Experiment")
        self.root.bind("<Key>", self.key_pressed)
        self.root.bind("<Escape>", self.exit_app)

        self.is_started = False
        self.is_explanation_started = False
        self.is_experiment_started = False
        self.after_id = None
        self.start_time = None
        self.end_time = None
        self.experiment_count = 0
        # 実験1回あたりの表示単語の情報を格納する
        self.displayed_letter_config = ["", ""]
        # 実験1回あたりの正解単語の情報を格納する
        self.answer_letters_config = [["", ""]]
        # 実験1回あたりの正解単語を格納する
        self.answer_letters = []
        # yesかnoかを格納する. yesならTrue, noならFalseを記録する。
        self.my_answer = None
        # すべての実験の結果を格納する
        self.answers = []
        ###############################
        # 本番かテストか
        self.is_test = True
        # 実験の種類を選択する
        self.experiment_type = "d"
        # 実験の回数を指定する
        self.experiment_count_max = 10
        print(f"実験の種類：{self.experiment_type}")
        ###############################
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=720, height=480, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.create_label()

    def create_label(self, text="Press Enter to start"):
        self.label = tk.Label(self.root, text=text, font=("Helvetica", 18), bg="white")
        self.label.grid(row=0, column=0, sticky="nsew")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def key_pressed(self, event):
        # 処理時間を短くするためにyとuを押したときの処理を一番上に持ってきている。
        if event.keysym == "y":
            # print("y")
            if self.is_experiment_started:
                self.end_time = datetime.now()
                self.is_experiment_started = False
                self.my_answer = True
                self.experiment_result()

        elif event.keysym == "u":
            # print("u")
            if self.is_experiment_started:
                self.end_time = datetime.now()
                self.is_experiment_started = False
                self.my_answer = False
                self.experiment_result()

        elif event.keysym == "Return":
            # print("Enter")
            if not self.is_started:
                self.is_started = True
                self.label.config(text="Press Space to start explanation")

        elif event.keysym == "space":
            # print("Space")
            if not self.is_started:
                # print("始まってません。Enterを押して下さい。")
                return

            if not self.is_explanation_started:
                self.is_explanation_started = True
                # ここで実験の説明をする
                self.expriment_explanation()
            else:
                self.is_explanation_started = False
                self.is_experiment_started = True
                self.experiment()

        elif event.keysym == "c":
            # print("c")
            if self.is_started:
                self.is_explanation_started = True
                self.expriment_explanation()

        elif event.keysym == "e":
            # print("e")
            self.exit_app(None)

    def expriment_explanation(self):
        if self.experiment_type == "a":
            # print("a explanation")
            # 小文字は290, 大文字は210（Cとcが3ほぼcmになる大きさ）
            a_letters_config = [
                ["a", 290], ["b", 290], ["c", 290], ["d", 290], ["e", 290], ["f", 290], ["g", 290], ["h", 290], ["i", 290], ["j", 290], ["k", 290], ["l", 290], ["m", 290], ["n", 290], ["o", 290], ["p", 290], ["q", 290], ["r", 290], ["s", 290], ["t", 290], ["u", 290], ["v", 290], ["w", 290], ["x", 290], ["y", 290], ["z", 290], ["A", 210], ["B", 210], ["C", 210], ["D", 210], ["E", 210], ["F", 210], ["G", 210], ["H", 210], ["I", 210], ["J", 210], ["K", 210], ["L", 210], ["M", 210], ["N", 210], ["O", 210], ["P", 210], ["Q", 210], ["R", 210], ["S", 210], ["T", 210], ["U", 210], ["V", 210], ["W", 210], ["X", 210], ["Y", 210], ["Z", 210], ["0", 210], ["1", 210], ["2", 210], ["3", 210], ["4", 210], ["5", 210], ["6", 210], ["7", 210], ["8", 210], ["9", 210], ["!", 210], ["#", 210], ["$", 210], ["%", 210], ["&", 210], ["(", 210], [")", 210]
            ]
            self.answer_letters_config = [random.choice(a_letters_config)]
            self.displayed_letter_config = self.answer_letters_config[0]
            self.label.config(text="Press y when you see the letter. \n(If you are ready, press Space)", font=("Helvetica", 18))

        elif self.experiment_type == "b":
            # print("b explanation")
            # C(c), I(l), O(o), P(p), S(s), U(u), V(v), W(w), X(x), Z(z), 0(o), 1(l)を消した
            # かっこ内は区別しづらいと判断した文字
            b_letters_config = [
                ["a", 290], ["b", 290], ["c", 290], ["d", 290], ["e", 290], ["f", 290], ["g", 290], ["h", 290], ["i", 290], ["j", 290], ["k", 290], ["l", 290], ["m", 290], ["n", 290], ["o", 290], ["p", 290], ["q", 290], ["r", 290], ["s", 290], ["t", 290], ["u", 290], ["v", 290], ["w", 290], ["x", 290], ["y", 290], ["z", 290], ["A", 210], ["B", 210], ["D", 210], ["E", 210], ["F", 210], ["G", 210], ["H", 210], ["J", 210], ["K", 210], ["L", 210], ["M", 210], ["N", 210], ["Q", 210], ["R", 210], ["T", 210], ["Y", 210], ["2", 210], ["3", 210], ["4", 210], ["5", 210], ["6", 210], ["7", 210], ["8", 210], ["9", 210], ["!", 210], ["#", 210], ["$", 210], ["%", 210], ["&", 210], ["(", 210], [")", 210], ["-", 290], ["=", 290],
            ]
            self.answer_letters_config = [random.choice(b_letters_config)]
            instruction_letter = self.answer_letters_config[0][0]

            # YesとNoが50%ずつ出現するようにする
            if random.randint(0, 1) == 0:
                # answer_letters_configの中のどれかを選ぶ
                self.displayed_letter_config = random.choice(self.answer_letters_config)
            else:
                # all_letters_configの中からanswer_letters_configに入っている単語以外のどれかを選ぶ
                self.displayed_letter_config = random.choice(
                    [letter_config for letter_config in b_letters_config if letter_config not in self.answer_letters_config]
                )
            self.label.config(
                text=f"Press y if the displayed letter is the same as {instruction_letter}; if not, press u. \n(If you are ready, press Space)"
            )

        elif self.experiment_type == "c":
            # C(c), I(l), O(o), P(p), S(s), U(u), V(v), W(w), X(x), Z(z), 0(o), 1(l)
            c_letters_configs = [
                {"reading": "エー", "letters": [["a", 290], ["A", 210]]},
                {"reading": "ビー", "letters": [["b", 290], ["B", 210]]},
                {"reading": "ディー", "letters": [["d", 290], ["D", 210]]},
                {"reading": "イー", "letters": [["e", 290], ["E", 210]]},
                {"reading": "エフ", "letters": [["f", 290], ["F", 210]]},
                {"reading": "ジー", "letters": [["g", 290], ["G", 210]]},
                {"reading": "エイチ", "letters": [["h", 290], ["H", 210]]},
                {"reading": "ジェー", "letters": [["j", 290], ["J", 210]]},
                {"reading": "ケー", "letters": [["k", 290], ["K", 210]]},
                {"reading": "エル", "letters": [["l", 290], ["L", 210]]},
                {"reading": "エム", "letters": [["m", 290], ["M", 210]]},
                {"reading": "エヌ", "letters": [["n", 290], ["N", 210]]},
                {"reading": "キュー", "letters": [["q", 290], ["Q", 210]]},
                {"reading": "アール", "letters": [["r", 290], ["R", 210]]},
                {"reading": "ティー", "letters": [["t", 290], ["T", 210]]},
                {"reading": "ワイ", "letters": [["y", 290], ["Y", 210]]}
            ]
            random_letter_configs = random.choice(c_letters_configs)
            self.answer_letters_config = random_letter_configs["letters"]
            instruction_letter = random_letter_configs["reading"]

            # YesとNoが50%ずつ出現するようにする
            if random.randint(0, 1) == 0:
                # answer_letters_configの中のどれかを選ぶ
                self.displayed_letter_config = random.choice(self.answer_letters_config)
            else:
                # all_letters_configの中からanswer_letters_configに入っている単語以外のどれかを選ぶ
                displayed_letters_config = random.choice(
                    [
                        letters_configs["letters"] for letters_configs in c_letters_configs if letters_configs != random_letter_configs
                    ]
                )
                self.displayed_letter_config = random.choice(displayed_letters_config)
            self.label.config(
                text=f"Press y if the displayed letter reading is {instruction_letter}; if not, press u. \n(If you are ready, press Space)"
            )

        elif self.experiment_type == "d":
            d_letters_configs = [
                {
                    "group": "lowercase",
                    "letters": [["a", 290], ["b", 290], ["d", 290], ["e", 290], ["f", 290], ["g", 290], ["h", 290], ["j", 290], ["k", 290], ["m", 290], ["n", 290], ["q", 290], ["r", 290], ["t", 290], ["y", 290]]
                },
                {
                    "group": "capital",
                    "letters": [["A", 210], ["B", 210], ["D", 210], ["E", 210], ["F", 210], ["G", 210], ["H", 210], ["J", 210], ["K", 210], ["L", 210], ["M", 210], ["N", 210], ["Q", 210], ["R", 210], ["T", 210], ["Y", 210]]
                },
                {
                    "group": "number",
                    "letters": [["2", 210], ["3", 210], ["4", 210], ["5", 210], ["6", 210], ["7", 210], ["8", 210], ["9", 210]]
                },
                {
                    "group": "symbol",
                    "letters": [["!", 210], ["#", 210], ["$", 210], ["%", 210], ["&", 210], ["(", 210], [")", 210], ["-", 290], ["=", 290]]
                }
            ]
            random_letter_configs = random.choice(d_letters_configs)
            self.answer_letters_config = random_letter_configs["letters"]
            instruction_letter = random.choice(self.answer_letters_config)[0]

            # YesとNoが50%ずつ出現するようにする
            if random.randint(0, 1) == 0:
                # answer_letters_configの中のどれかを選ぶ
                self.displayed_letter_config = random.choice(self.answer_letters_config)
            else:
                # all_letters_configの中からanswer_letters_configに入っている単語以外のどれかを選ぶ
                displayed_letters_config = random.choice(
                    [
                        letters_configs["letters"] for letters_configs in d_letters_configs if letters_configs != random_letter_configs
                    ]
                )
                self.displayed_letter_config = random.choice(displayed_letters_config)
            self.label.config(
                text=f"Press y if the displayed letter reading is the same group as {instruction_letter};\nif not, press u. \n(If you are ready, press Space)"
            )

    def experiment(self):
        # print("start experiment")
        self.experiment_count += 1
        # afterを使って0から5秒の間でランダムの時間待つ
        sleep_time = random.randint(1, 5)
        self.after_id = self.root.after(sleep_time * 1000, self.display_letters)

    def display_letters(self):
        print(self.displayed_letter_config)
        self.start_time = datetime.now()
        self.label.config(
            text=self.displayed_letter_config[0], font=("Helvetica", self.displayed_letter_config[1])
        )

    def experiment_result(self):
        if self.start_time is None and self.end_time is not None:
            # print("表示される前に入力されました。")
            self.root.after_cancel(self.after_id)
            self.after_id = None
        elif self.start_time is None or self.end_time is None:
            # print("start_timeかend_timeがNoneです。")
            self.root.after_cancel(self.after_id)
            self.after_id = None
        else:
            time_difference = self.end_time - self.start_time
            self.answer_letters = [
                answer_letter[0] for answer_letter in self.answer_letters_config
            ]
            # 正解
            correct_answer = self.displayed_letter_config in self.answer_letters_config
            if correct_answer == self.my_answer:
                is_correct = True
            else:
                is_correct = False
            # 実験回数、実験の種類、表示された文字、正解となる文字、正しい答え、自分の解答、正解か不正解か、開始時間、終了時間、応答時間
            self.answers.append(
                [
                    self.experiment_count,
                    self.experiment_type,
                    self.displayed_letter_config[0],
                    self.answer_letters,
                    correct_answer,
                    self.my_answer,
                    is_correct,
                    self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                    self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    str(time_difference.total_seconds())
                ]
            )
            print(f"==========実験{str(self.experiment_count)}回目==========")
            print("実験の種類: " + self.experiment_type)
            print("表示された文字: " + self.displayed_letter_config[0])
            print("正解となる文字: " + str(self.answer_letters))
            print("正しい答え: " + str(correct_answer))
            print("自分の解答: " + str(self.my_answer))
            print("正解か不正解か: " + str(is_correct))
            print("応答時間: " + str(time_difference.total_seconds()) + "秒")
        self.displayed_letter_config = ["", ""]
        self.answer_letters = []
        self.start_time = None
        self.end_time = None

        if self.experiment_count >= self.experiment_count_max:
            print("終了します")
            self.exit_app(None)

        # 続ける場合はc、終了する場合はeを押させる
        self.label.config(text="Press c to continue, press e to exit", font=("Helvetica", 18))

    def exit_app(self, event):
        self.export_answers()
        self.root.quit()

    def export_answers(self):
        # 現在の時刻を取得
        now = datetime.now()
        # is_testがTrueの場合は/test、Falseの場合は/mainに入れる
        directory = f"./data/test/{self.experiment_type}" if self.is_test else f"./data/main/{self.experiment_type}"
        output = now.strftime(f"{directory}/%Y%m%d_%H%M%S") + ".csv"
        with open(output, mode="w", newline="") as file:
            writer = csv.writer(file)
            # 実験回数、実験の種類、表示された文字、正解となる文字、正しい答え、自分の解答、正解か不正解か、開始時間、終了時間、応答時間
            writer.writerow(["Experiment Count", "Experiment Type", "Displayed Letter", "Answer Letters", "Correct Answer", "My Answer", "Is Correct", "Start Time", "End Time", "Time Difference (seconds)"])
            writer.writerows(self.answers)


def make_dirs():
    paths = ["./data/test/a", "./data/test/b", "./data/test/c", "./data/test/d", "./data/main/a", "./data/main/b", "./data/main/c", "./data/main/d"]
    for path in paths:
        os.makedirs(path, exist_ok=True)


if __name__ == "__main__":
    # もしフォルダがなかったら作成する
    make_dirs()

    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
