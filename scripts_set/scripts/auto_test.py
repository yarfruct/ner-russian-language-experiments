import re
import sys
import os
import difflib
from collections import Counter


# sys.argv[1] - source(standard) file path
# sys.argv[2] - target(test) file path
# sys.argv[3] - path to dir, where results will be written
# sys,argv[4] - path to dir with statistic (work with O tag)
# sys.argv[5] - permission to handle misc tag (misc or no_misc)
# sys.argv[6] (optional) - mode of checked ne tagging (normal - FN experimental - CF)


def main():
    print("SOURCE: "+sys.argv[2]+"\nKEY: "+sys.argv[1])
    fn_o_tag_cnt = 0
    standard_file_content = read_file(sys.argv[1])
    test_file_content = read_file(sys.argv[2])
    standard_file_name = sys.argv[1].rsplit('/', 1)[-1]
    lcs_info = reveal_lcs(standard_file_content, test_file_content)
    results_data = []

    if not test_file_content:
        for line in standard_file_content:
            results_data.append(line.rstrip() + ",FN\n")
        create_test_result_file(results_data, sys.argv[3], standard_file_name, len(standard_file_content))
        return

    matched_standard = full_ne(standard_file_content, lcs_info[0])
    matched_test = full_ne(test_file_content, lcs_info[1])

    # after this block standard_file_content and test_file content will be contained extra entities from its owns files
    # block start
    remove_matches(standard_file_content, lcs_info[0])
    remove_matches(test_file_content, lcs_info[1])
    # block end
    check_matches(matched_standard, matched_test, results_data)
    fn_o_tag_cnt += distribute_extra_ne(standard_file_content, test_file_content, results_data)
    create_test_result_file(results_data, sys.argv[3], standard_file_name, fn_o_tag_cnt)


# get uncut named entity by index list
def full_ne(raw_ne, ne_indexes):
    selected_ne = []
    for i in ne_indexes:
        selected_ne.append(raw_ne[i].rstrip())
    return selected_ne


def get_all_digits(string):
    return re.findall(r"\d+", string)


# return list of special characters token in named entity
def get_all_spec(string):
    return list(filter(None, re.split(r"\s+", re.sub(r"(\d+)|(\w)", " ", string))))


# return list of words token in named entity
def get_all_words(string):
    return list(filter(None, re.split(r"\s+", re.sub(r"(\d+)|(\W)", " ", string))))


# calc set difference between standard named entity and testing named entity in words
def calc_word_diff(standard_str, test_str):
    result_set = Counter(get_all_words(standard_str)) - Counter(get_all_words(test_str))
    return sum(result_set.values())


# calc set difference between standard named entity and testing named entity in digits
def calc_digit_diff(standard_str, test_str):
    result_set = Counter(get_all_digits(standard_str)) - Counter(get_all_digits(test_str))
    return sum(result_set.values())


# calc set difference between standard named entity and testing named entity in special characters
def calc_spec_diff(standard_str, test_str):
    result_set = Counter(get_all_spec(standard_str)) - Counter(get_all_spec(test_str))
    return sum(result_set.values())


# sum of calc_word_diff, calc_spec_diff and calc_digit_diff
def detect_fn_diff(standard_str, test_str):
    cnt = calc_word_diff(standard_str, test_str) + calc_spec_diff(standard_str, test_str)
    return cnt + calc_digit_diff(standard_str, test_str)


# works with named entities that have no full match. Only FN and FP marks
# Detects an occurrence in a substring
# If standard is substring of test string -- mark standard as FP
# If test string is substring of standard string - mark standard as FN (missed part of entity)
# Else -- FN mark (full named entity is missed)
def distribute_extra_ne(extra_standard, extra_test, results_data):
    fn_o_tag_cnt = 0
    while True:
        if not extra_standard:
            for ne in extra_test:
                results_data.append(ne.rstrip() + ",FP\n")
            break
        if not extra_test:
            for ne in extra_standard:
                results_data.append(ne.rstrip() + ",FN\n")
                fn_o_tag_cnt += detect_fn_diff(ne.rsplit(',', 1)[0], "")
            break
        matched = False
        for ne in extra_test:
            ne_standard = extra_standard[0].rstrip().rsplit(",", 1)[0]
            ne_current_test = ne.rstrip().rsplit(",", 1)[0]
            substring_info = check_substring(ne_standard, ne_current_test)
            if substring_info[0]:
                results_data.append(extra_standard[0].rstrip() + ",FP\n")
                del extra_standard[0]
                extra_test.remove(ne)
                matched = True
                break
            elif substring_info[1]:
                results_data.append(extra_standard[0].rstrip() + ",FN\n")
                del extra_standard[0]
                extra_test.remove(ne)
                matched = True
                fn_o_tag_cnt += detect_fn_diff(ne_standard, ne_current_test)
                break
        if not matched:
            results_data.append(extra_standard[0].rstrip() + ",FN\n")
            fn_o_tag_cnt += detect_fn_diff(extra_standard[0].rsplit(',', 1)[0], "")
            del extra_standard[0]
    return fn_o_tag_cnt


# Check tags with matched entities. CF - confusion (right borders and wrong tag -- only experimental mode!)
# Set only TP or FN(CF)
def check_matches(standard_list, test_list, results_list):
    mode = "normal"
    if len(sys.argv) == 7:
        if sys.argv[6] == "experimental":
            mode = "experimental"
    if mode != "experimental":
        error_tag = "FN"
    else:
        error_tag = "CF"
    for i in range(len(standard_list)):
        if standard_list[i].rstrip() == test_list[i].rstrip():
            results_list.append(standard_list[i].rstrip() + ",TP\n")
        else:
            results_list.append(standard_list[i].rstrip() + "," + error_tag + "\n")


# Write number of missed tokens in special file. Analytic script must work with these files.
def create_test_result_file(data, path, file_name, fn_o_tag_cnt):
    if not os.path.exists(path):
        os.makedirs(path)
    export_file = open(r"" + path + r"/autoTest-" + file_name, 'w', encoding='utf-8', newline='')
    for line in data:
        export_file.write(line)
    export_file.close()
    if not os.path.exists(sys.argv[4]):
        os.makedirs(sys.argv[4])
    auto_test_stat_dir = sys.argv[4] + r"/AutoTestLastRun"
    if not os.path.exists(auto_test_stat_dir):
        os.makedirs(auto_test_stat_dir)
    export_file = open(r"" + auto_test_stat_dir + r"/ODiff-" + file_name, 'w', encoding='utf-8', newline='')
    export_file.write(str(fn_o_tag_cnt))
    export_file.close()


def read_file(path):
	content = []
	try:
		with open(r"" + path, 'r', encoding='utf-8', newline='') as file:
			for line in file:
				tag = line.rsplit(",",1)[1].rstrip()
				if tag == "MISC":
					if sys.argv[5] == "misc":
						content.append(line)
				else:
					content.append(line)
	except UnicodeDecodeError:
		with open(r"" + path, 'r', encoding='windows-1251', newline='') as file:
			for line in file:
				tag = line.rsplit(",",1)[1].rstrip()
				if tag == "MISC":
					if sys.argv[5] == "misc":
						content.append(line)
				else:
					content.append(line)
	return content


def check_substring(str_standard, str_test):
    results = [bool(re.match(r'.*' + re.escape(str_standard) + r'.*', str_test)),
               bool(re.match(r'.*' + re.escape(str_test) + r'.*', str_standard))]
    # 1 cell: is str_standard is substring of str_test?
    # 2 cell: is str_test is substring of str_standard?
    return results


# remove matched elements
def remove_matches(ner_list, matches_index_list):
    index = len(matches_index_list) - 1
    while index >= 0:
        del ner_list[matches_index_list[index]]
        index -= 1


# highlight ne in ne,tag pairs
def ne_highlight(ner_list):
    ne_list = []
    for i in range(len(ner_list)):
        ne_list.append(ner_list[i].rsplit(',', 1)[0].replace('\u200e', ''))
    return ne_list


# reveal lcs info.
# function returns: indexes of matched named entity in standard, indexes of matched named entity in test and lcs
def reveal_lcs(standard_list, test_list):
    ne_standard = ne_highlight(standard_list)
    ne_test = ne_highlight(test_list)
    diff = difflib.Differ(linejunk=None, charjunk=None)
    diff_content = list(diff.compare(ne_standard, ne_test))
    index_standard = 0
    index_test = 0
    lcs = []
    match_index_standard = []
    match_index_test = []
    for ne in diff_content:
        if ne[0] == " ":
            lcs.append(ne.strip())
            match_index_standard.append(index_standard)
            match_index_test.append(index_test)
            index_standard += 1
            index_test += 1
        elif ne[0] == "+":
            index_test += 1
        elif ne[0] == "-":
            index_standard += 1
    complex_result = [match_index_standard, match_index_test, lcs]
    return complex_result


main()
