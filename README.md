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
2. 実験を行う。ターミナルで`python main.py`と入力する
```
C:\Users\...\response_time_experiment> python main.py
```
3. 分析を行う。ターミナルで`python analysis.py`と入力する
```
C:\Users\...\response_time_experiment> python analysis.py
```

# ファイルの説明
- .gitignore: gitにあげないファイルをここで指定する（実験には関係なし）
- README.md: 説明用のファイル
- main.py: 実験用のファイル
- analysis.py: 実験データ分析用のファイル

# 参考文献
1. 東野利貴, 清水菜々子, 曽我真人. P300の潜時の違いによるModel Human Processorの検証. JSiSE Research Report vol. 33, no.7(2019-3). https://www.jsise.org/society/committee/2018/special/TR-033-07-D-007.pdf
2. Card, S. K., Moran, T. P., & Newell, A., “The psychology of human-computer interaction” , Hillsdale, NJ:Lawrence Erlbaum Associates(1983)
3. 天野成昭. 心理実験のキーポイント. 日本音響学会誌74巻12号(2018). https://www.jstage.jst.go.jp/article/jasj/74/12/74_641/_pdf
4. 黒田剛士, 蓮尾絵美. 早わかり心理物理学実験. 日本音響学会誌69巻12号(2013), pp.632−637. https://www.jstage.jst.go.jp/article/jasj/69/12/69_KJ00008988199/_pdf
5. TkDocs. Tkinter 8.5 reference: a GUI for Python. 5.4, Type fonts. https://tkdocs.com/shipman/fonts.html
