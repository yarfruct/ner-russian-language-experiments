import os
import sys
import subprocess

# sys.argv[1] - source dir
# sys.argv[2] - target dir
# sys.argv[3] - path to executable py file
# sys.argv[4] - absolute path to dir where will be written number of O tag tokens
# sys.argv[5] - prefix for results files names

sources_files = []

for file in os.listdir(sys.argv[1]):
    if file.endswith(".txt"):
        sources_files.append(os.path.join(sys.argv[1], file))

if not sources_files:
    sys.exit("Got an empty source directory. Add source txt files.")
if not os.path.exists(sys.argv[2]):
    os.makedirs(sys.argv[2])
if not os.path.exists(sys.argv[4]):
    os.makedirs(sys.argv[4])

for source in sources_files:
    target_name = sys.argv[2] + "/" + sys.argv[5] + "_" + source.rsplit('/', 1)[-1]
    subprocess.run(["python3", sys.argv[3], source, target_name, sys.argv[4]])
