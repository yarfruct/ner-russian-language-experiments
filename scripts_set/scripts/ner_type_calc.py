import os
import sys

# sys.argv[1] -- path to dir with keys


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


mics = 0
org = 0
per = 0
loc = 0
texts = []

for file in os.listdir(sys.argv[1]):
    if file.endswith(".txt"):
        texts.append(os.path.join(sys.argv[1], file))

for current_text in texts:
    data = read_file(current_text)
    for cur_line in data:
        tag = cur_line.rsplit(",", 1)[-1].rstrip()
        if tag == "MISC":
            mics += 1
        elif tag == "PER":
            per += 1
        elif tag == "ORG":
            org += 1
        elif tag == "LOC":
            loc += 1
        else:
            print("ERROR: " + tag)
print("MISC="+str(mics)+"\nORG="+str(org)+"\nPER="+str(per) + "\nLOC=" + str(loc))
