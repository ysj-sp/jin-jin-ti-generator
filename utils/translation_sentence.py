# Google Translation API from Github (unofficial)
# ref: https://github.com/ssut/py-googletrans

from googletrans import Translator

translator = Translator()

translated_line = translator.translate("謝立軒好帥", dest="en", src="zh-Tw")

print(translated_line.text)
