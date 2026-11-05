import glob, shutil

for f in glob.glob("*.inp"):
    for i in range(1,10):
        shutil.copy(f, f"mod_{i}_{f}")
