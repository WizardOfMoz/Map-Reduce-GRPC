import shutil
import os
#remove all directories in data directory
if os.path.exists("Intermediate_data"):
    shutil.rmtree("Intermediate_data")
os.mkdir("Intermediate_data")

#remove all directiories in FinalData directory
if os.path.exists("FinalData"):
    shutil.rmtree("FinalData")
os.mkdir("FinalData")