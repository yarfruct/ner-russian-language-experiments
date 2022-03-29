import sys
import subprocess
import os

# sys.argv[1] - path to raw texts folder
# sys.argv[2] - path to neuro network dir where results (marked files by neuro network) will be written
# sys.argv[3] - path to neuro script
# sys.argv[4] - path to statistic folder
# sys.argv[5] - prefix for neuro network outcome files
# sys.argv[6] - path to marked (standard) files dir
# sys.argv[7] - path to auto test result's dir
# sys.argv[8] - name of testing library
# sys.argv[9] - permission to handle misc tag (misc or no_misc)
# sys.argv[10] - (optional) mode for AutoTest.py (normal or experimental). Normal by default.

my_own_path = os.path.dirname(os.path.realpath(__file__))
print(os.path.dirname(os.path.realpath("run_scripts.py")))

neuro_operator_path = my_own_path + r"/scripts/neuro_operator.py"

# execute neuro network
print("Executing neural network")
subprocess.call(["python3", neuro_operator_path, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]])
print("Done")

auto_test_path = my_own_path + r"/scripts/auto_test.py"
test_operator_path = my_own_path + r"/scripts/test_operator.py"

# execute auto test system
print("Executing automatical testing system")
if len(sys.argv) == 11:
    subprocess.call(["python3", test_operator_path, sys.argv[6], sys.argv[2], sys.argv[7], sys.argv[4], auto_test_path, sys.argv[9], sys.argv[10]])
else:
    subprocess.call(["python3", test_operator_path, sys.argv[6], sys.argv[2], sys.argv[7], sys.argv[4], auto_test_path, sys.argv[9]])
print("Done")

# execute analytic module

analytic_path = my_own_path+r"/scripts/analytic.py"
print("Executing analytic module")
subprocess.call(["python3", analytic_path, sys.argv[4], sys.argv[8], sys.argv[7]])
print("Done")
