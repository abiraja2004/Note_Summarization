from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import nltk.data # split text on sentences
import re # for regular expression

rsrcmgr = PDFResourceManager()
retstr = io.StringIO()
laparams = LAParams()
device = TextConverter(rsrcmgr, retstr, codec = 'UTF-8', laparams = laparams)
# fp = open('Subject Index.pdf', 'rb')
fp = open('book\\Chapter 1.pdf', 'rb')
interpreter = PDFPageInterpreter(rsrcmgr, device)
maxpages = 0
pagenos = set()

PageContentList = []
for page in PDFPage.get_pages(fp, pagenos, maxpages = maxpages, password = '', caching = True, check_extractable = True):
	# read_position = retstr.tell() # it will be 0 on the first page
	interpreter.process_page(page)
	# retstr.seek(read_position, 0)
	# PageContentList.append(retstr.read())
text = retstr.getvalue()
fp.close()
device.close()
retstr.close()
# print (text)
SentenceList = []
# nltk.download('punkt')
senTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
SentenceList = senTokenizer.tokenize(text) #corpus

i = 0
while i < len(SentenceList):
	while 1:
		if re.search('\.[A-Z]\w', SentenceList[i]) == None and '' not in SentenceList[i]:
			i += 1
			break
		if re.search('\.[A-Z]\w', SentenceList[i]) != None:
			result = re.search('\.[A-Z]\w', SentenceList[i]).group(0)
			print (result)
			if '' in SentenceList[i] and SentenceList[i].find('') < SentenceList[i].find(result):
				prev = SentenceList[i][:SentenceList[i].find('')]
				post = SentenceList[i][SentenceList[i].find('') + 1:]
			else:
				prev = SentenceList[i][:SentenceList[i].find(result) + 1]
				post = SentenceList[i][SentenceList[i].find(result) + 1:]
			SentenceList[i] = prev
			i += 1
			SentenceList.insert(i, post)
		if '' in SentenceList[i]:
			prev = SentenceList[i][:SentenceList[i].find('')]
			post = SentenceList[i][SentenceList[i].find('') + 1:]
			SentenceList[i] = prev
			i += 1
			SentenceList.insert(i, post)
		i += 1


# for i in range(len(SentenceList)):
# 	print (i, '\t', SentenceList[i])
# print (SentenceList)


with open ('book\\Book.txt', 'w', encoding = 'UTF-8') as outFile:
	for sentence in SentenceList:
		try:
			# while sentence[0] == ' ':
			# 	sentence = sentence[1:]
			# sentence = sentence.replace('', '')
			outFile.write(sentence + '\n')
		except Exception as e:
			print ('Exception:', e)


# from docx import *

# ''' read docx '''
# FILE_NAME = 'Subject Index.docx'

# d = Document(FILE_NAME)
# for p in d.paragraphs:
# 	print (p.text)
