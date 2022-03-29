import sys
import os
import re
from deeppavlov import configs, build_model

# sys.argv[1] - source file
# sys.argv[2] - target file (will be rewritten)
# sys.argv[3] - path to dir where other tag counter will be written

open_brackets = {'“','(','[','{','<','«'}
close_brackets = {'”',')',']','}','>','»'}
punct_mark = {',','.','!','`','?',':',';','-','&','/','’'}
MDash = '—'

def write_ne(result):
	exportFile = open(r"" + sys.argv[2], 'w', encoding='utf-8', newline='')
	for ne in result:
		new_line_ne = re.sub(r"\s{2,}"," ",ne)
		new_line_ne = new_line_ne + "\n"
		exportFile.write(new_line_ne)
	exportFile.close()


def write_cnt(cnt):
	exportFile = open(r"" + sys.argv[3]+"/DeepPavlov"+r"/OCnt_"+sys.argv[1].rsplit("/",1)[-1], 'w', encoding='utf-8', newline='')
	exportFile.write(str(cnt))
	exportFile.close()
	

def read_file(path):
    content = []
    try:
        with open(r"" + path, 'r', encoding='utf-8', newline='') as file:
            for line in file:
                content.append(line.rstrip())
    except UnicodeDecodeError:
        with open(r"" + path, 'r', encoding='windows-1251', newline='') as file:
            for line in file:
                content.append(line.rstrip())
    return content


def select_entities(words, marks):
	open_br_before = False
	close_br_before = False
	MDash_before = False
	short_dash_before = False
	dot_before = False
	slash_before = False
	ampersant_before = False
	apostrof_before = False
	entities = []
	entity = ""
	cnt_O = 0
	whitespace_one = ""
	whitespace_two = ""
	ner_type = "None"
	pos_tag = "O"
	
	for i,mark in enumerate(marks, start=0):
		pos_tag = mark[0]
		current_ner_type = re.search(r"(^O$)|((?<=-)\w+$)", mark).group(0)
		
		#whitespace prediction starts
		if open_br_before or short_dash_before or dot_before or ampersant_before or slash_before or apostrof_before:
			whitespace_one = ""
			whitespace_two = ""
			if open_br_before and not(len(words[i])==1 and words[i] in close_brackets):
				open_br_before = False
			if short_dash_before and not(len(words[i])==1 and words[i] == '-'):
				short_dash_before = False
			if dot_before and not(len(words[i]) == 1 and words[i] == '.'):
				dot_before = False
			if ampersant_before and not(len(words[i]) == 1 and words[i] == '&'):
				ampersant_before = False
			if slash_before and not(len(words[i]) == 1 and words[i] == '/'):
				slash_before = False
			if apostrof_before and not(len(words[i]) == 1 and words[i] == '’'):
				apostrof_before = False
		elif len(words[i])==1:
			is_mdash = words[i] == MDash
			is_open_br = words[i] in open_brackets
			is_close_br = words[i] in close_brackets
			is_punct = words[i] in punct_mark
			if is_mdash or is_open_br or is_close_br or is_punct:
				if is_punct:
					if words[i] == '-':
						short_dash_before = True
					if words[i] == '.':
						dot_before = True
					if words[i] == '&':
						ampersant_before = True
					if words[i] == '/':
						slash_before = True
					if words[i] == '’':
						apostrof_before = True
					whitespace_one = ""
					whitespace_two = ""
				if is_open_br or is_mdash:
					if is_open_br:
						open_br_before = True
					whitespace_one = " "
					whitespace_two = ""
				if is_close_br:
					whitespace_one = ""
					whitespace_two = " "
		else:
			whitespace_one =" "
			whitespace_two = ""	
		#whitespace prediction ends
		
		if pos_tag == "B" and entity == "":
			entity = words[i]
			ner_type = current_ner_type
			continue
		if pos_tag == "B" and entity != "":
			entities.append(entity.rstrip()+","+ner_type)
			entity = words[i]
			ner_type = current_ner_type
			continue
		if pos_tag == "I" and entity != "":
			entity += whitespace_one + words[i] + whitespace_two
			continue
		if pos_tag == "O" and entity != "":
			entities.append(entity.rstrip()+","+ner_type)
			entity = ""
			ner_type = "None"
			cnt_O += 1
			continue
		if pos_tag == "O":
			cnt_O += 1
	if entity!="":
		entities.append(entity.rstrip()+","+ner_type)
	result = [entities, cnt_O]
	return result
			

ner_model = build_model(configs.ner.ner_rus_bert_torch, download=False)

list_of_sentences = []

content = read_file(sys.argv[1])


data = (ner_model(content))

result = []
total_O_cnt = 0
for i in range(len(data[0])):
	sentence_ne = select_entities(data[0][i], data[1][i])
	for ne in sentence_ne[0]:
		result.append(ne)
	total_O_cnt += sentence_ne[1]

write_ne(result)
write_cnt(total_O_cnt)
