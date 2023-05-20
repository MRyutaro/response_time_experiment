# 実行環境
- Python

# 実行方法
1. main.py内のこの部分を変更する
```
76. ###############################
77. # 本番かテストか
78. self.is_test = True
79. # 実験の種類を選択する
80. self.experiment_type = "a"
81. # 実験の回数を指定する
82. self.experiment_count_max = 10
83. ###############################
```
2. main.pyを実行する。ターミナルで`python main.py`と入力する
```
C:\Users\...\response_time_experiment> python main.py
```

# ファイルの説明
- .gitignore: gitにあげないファイルをここで指定する（実験には関係なし）
- README.md: 説明用のファイル
- main.py: 実験用のファイル

# 参考文献
- 清水菜々子他. Model Human Processorと運動準備電位の出現頻度の比較と検討. 2019. https://www.jstage.jst.go.jp/article/pjsai/JSAI2019/0/JSAI2019_1E4J1204/_pdf/-char/ja
- 清水菜々子他. P300の潜時の違いによるModel Human Processorの検証. 2019.
https://www.jsise.org/society/committee/2018/special/TR-033-07-D-007.pdf