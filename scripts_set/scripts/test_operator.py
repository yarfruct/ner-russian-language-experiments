import os
import sys
import subprocess
import re

# sys.argv[1] - full path to source (corpus marked files) dir
# sys.argv[2] - full path to target (neuro marked files) dir
# sys.argv[3] - path to dir where result of autotest will be written
# sys.argv[4] - path to dir where will be written number of FN o tag tokens (statistic)
# sys.argv[5] - path to AutoTest.py
# sys.argv[6] - permission to handle misc tag (misc or no_misc)
# sys.argv[7] - (optional) - mode of checked ne tagging (normal - FN experimental - CF)

source_files = []
target_files = []
key_dict = {}
target_dict = {}
target_id = []

if not os.path.exists(sys.argv[1]):
    sys.exit("Sources directory does not exists")
if not os.path.exists(sys.argv[2]):
    sys.exit("Target directory does not exists")

for file in os.listdir(sys.argv[1]):
    if file.endswith(".txt"):
        source_files.append(os.path.join(sys.argv[1], file))
        key_dict[re.search(r"\d+(?=.)",file).group(0)]=os.path.join(sys.argv[1], file)


for file in os.listdir(sys.argv[2]):
    if file.endswith(".txt"):
        target_files.append(os.path.join(sys.argv[2], file))
        current_id = re.search(r"\d+(?=.)",file).group(0)
        target_id.append(current_id)
        target_dict[current_id] = os.path.join(sys.argv[2], file)
        

if not source_files:
    sys.exit("Got an empty source directory. Add source txt files.")

if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])

if not os.path.exists(sys.argv[3]):
    os.makedirs(sys.argv[3])

if not os.path.exists(sys.argv[4]):
    os.makedirs(sys.argv[4])

for i in target_id:
    if len(sys.argv) == 8:
        subprocess.run(["python3", sys.argv[5], key_dict.get(i), target_dict.get(i), sys.argv[3], sys.argv[4], sys.argv[6], sys.argv[7]])
    else:
        subprocess.run(["python3", sys.argv[5], key_dict.get(i), target_dict.get(i), sys.argv[3], sys.argv[4], sys.argv[6]])
    
