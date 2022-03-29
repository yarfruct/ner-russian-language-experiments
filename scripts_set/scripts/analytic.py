import sys
import os
import uuid

# sys.argv[1] - path to dir, where contains dir with TP cnt by neuro opinion and FN error by autoTest (statistic)
# sys.argv[2] - name of library
# sys.argv[3] - dir with auto test results



def read_file(path):
    content = []
    try:
        with open(r"" + path, 'r', encoding='utf-8', newline='') as file:
            for line in file:
                content.append(line)
    except UnicodeDecodeError:
        with open(r"" + path, 'r', encoding='windows-1251', newline='') as file:
            for line in file:
                content.append(line)
    return content


def calc_index(token_type):
    if token_type.rstrip() == "TP":
        return 0
    elif token_type.rstrip() == "FP":
        return 2
    else:
        return 1

# first cell - TP mark counter
# second cell - FN mark counter
# third cell - FP mark counter
loc_stat = [0]*3
org_stat = [0]*3
per_stat = [0]*3
misc_stat = [0]*3

tn_o = 0
fn_o = 0

tp_o_path = sys.argv[1]+"/"+sys.argv[2]
fn_o_path = sys.argv[1]+r"/AutoTestLastRun"
result_file_name = "test_outcome_"+uuid.uuid4().hex+".csv"
if not os.path.exists(tp_o_path):
    sys.exit("Dir with statistic data does not exists")
if not os.path.exists(sys.argv[3]):
    sys.exit("Dir with auto test data does not exists")

for file in os.listdir(tp_o_path):
    if file.endswith(".txt"):
        tn_o += int(read_file(tp_o_path + "/" + file)[0])

for file in os.listdir(fn_o_path):
    if file.endswith(".txt"):
        fn_o += int(read_file(fn_o_path + "/" + file)[0])
tn_o = tn_o - fn_o

for file in os.listdir(sys.argv[3]):
    if file.endswith(".txt"):
        all_lines = read_file(sys.argv[3] + "/" + file)
        for line in all_lines:
            line_in_fragments = line.rsplit(",", 2)
            index = calc_index(line_in_fragments[2])
            if line_in_fragments[1] == "LOC":
                loc_stat[index] += 1
            elif line_in_fragments[1] == "PER":
                per_stat[index] += 1
            elif line_in_fragments[1] == "ORG":
                org_stat[index] += 1
            else:
                misc_stat[index] += 1

export_file = open(r""+sys.argv[1]+r"/"+result_file_name, 'w', encoding="utf-8", newline='')
export_file.write("Tag,TP,TN,FP,FN\n")
export_file.write("O,-," + str(tn_o) + ",-," + str(fn_o)+",FN of O is contained in other FN cells. Does not count towards the total."+"\n")
export_file.write("LOC,"+str(loc_stat[0])+",-,"+str(loc_stat[2])+","+str(loc_stat[1])+"\n")
export_file.write("PER,"+str(per_stat[0])+",-,"+str(per_stat[2])+","+str(per_stat[1])+"\n")
export_file.write("ORG,"+str(org_stat[0])+",-,"+str(org_stat[2])+","+str(org_stat[1])+"\n")
export_file.write("MISC,"+str(misc_stat[0])+",-,"+str(misc_stat[2])+","+str(misc_stat[1])+"\n")
tp_total = str(loc_stat[0]+org_stat[0]+misc_stat[0]+per_stat[0])
fn_total = str(loc_stat[1]+ misc_stat[1] + org_stat[1] + per_stat[1])
fp_total = str(loc_stat[2]+org_stat[2]+misc_stat[2]+per_stat[2])
export_file.write("TOTAL," + tp_total + "," + str(tn_o) + "," + fp_total + "," + fn_total+"\n")
export_file.close()

