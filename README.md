# jin-jin-ti-generator
Give a Traditional Chinese sentence and return an another sentence combined with English and Traditional Chinese.

### Schedule

1. Collect sentences from `messengers` or `line`. (About 500 sentences) -> [excel](https://docs.google.com/spreadsheets/d/12HLFguNa2jFWDOFP5_UzaAjZ9u5NhPJhUQGr8193WIs/edit?usp=sharing)
2. split sentences into list of words with NLP tools
3. Give data a label
4. Design modal
5. Training data
6. Put predicted result to the website (working on it)

### Tools
1. Tensorflow (1.14)
2. Google Sheet API
3. [Ckiptagger](https://github.com/ckiplab/ckiptagger) (for split words from sentence)
4. [googletrans 2.4.0](https://pypi.org/project/googletrans/)
5. word vector `cna.cbow.512d.0.txt` from [科技大擂台](https://fgc.stpi.narl.org.tw/activity/videoDetail/4b1141305ddf5522015de5479f4701b1)

### Start application by docker
1. build docker image
```
docker build -t jjtg .
```

2. Run docker image
```
docker run -it --rm --name my-running-app jjtg
```

3. Input Chinese sentence after this line show up
```
Enter your sentence with Chinese or exit to close application: 我好帥
```

4. Enter exit if you want to close the application
```
exit
```

### How it works

1. Collect sentence manually add store into google sheet
2. Use `split_sentence.py` to split sentenct ex:
``` python
['我是大帥哥'] => [['我', '是', '大', '帥哥']]
```
3. Input `label` manually in google sheet. Use `*` character to be the word that need to transalte (Which word should be translated is by my own experience)
3. Use word vector to replace word to index ex:
``` python
[['我', '是', '大', '帥哥']] => [[1, 3, 456, 789]]
```
4. Use `LSGM` to train model. (Should make all input to be same length which is `20` for now)
5. Get prediction by the trained model
6. Translate words that have been marked by the prediction

### Obstacle
1. Which word should be translated is very subjective so the prediction should not be precise for everyone.
2. The translation is by single word but not a sentence so sometimes will get strange translation ex:
```
男人 => the man
女人 => woman
```

