import spacy
import sys
import os
import re

#sys.argv[1] - source
#sys.argv[2] - target
#sys.argv[3] - path to dir where other tag counter will be written (statistic)

testText = ''

try:
    with open(r"" + sys.argv[1], 'r', encoding='utf-8', newline='') as file:
        for line in file:
                testText += line
except UnicodeDecodeError:
    with open(r"" + sys.argv[1], 'r', encoding='windows-1251', newline='') as file:
        for line in file:
                testText += line

nlp = spacy.load("ru_core_news_lg")
doc = nlp(testText)
exportFile = open(r"" + sys.argv[2], 'w', encoding='utf-8', newline='')
listOfEntities=doc.ents

for entity in listOfEntities:
        output_line = re.sub(r"(?<=\S)\r\n(?=\S)", " ", entity.text+ "," + entity.label_ + "\n")
        exportFile.write(output_line)
exportFile.close()

print("Current text: "+sys.argv[1])
#print(nlp.get_pipe('ner').labels)

cnt = 0
for token in doc:
    if token.ent_iob_=="O":
        cnt+=1


if not os.path.exists(sys.argv[3]):
    os.makedirs(sys.argv[3])
spacy_statistic_dir = sys.argv[3]+r"/Spacy"
if not os.path.exists(sys.argv[3]+r"/Spacy"):
    os.makedirs(sys.argv[3]+r"/Spacy")

exportFile = open(spacy_statistic_dir+r"/OCnt_"+sys.argv[1].rsplit("/",1)[-1], 'w', encoding='utf-8', newline='')
exportFile.write(str(cnt))
exportFile.close()
