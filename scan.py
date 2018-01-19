import hashlib
import argparse
import os


# https://stackoverflow.com/a/3431838/625688
def md5sum(fileName):
    hash_md5 = hashlib.md5()
    with open(fileName, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


parser = argparse.ArgumentParser(description='Detect, and optionally remove, duplicate files in a given directory.')
parser.add_argument('--delete', action='store_true', help='delete duplicate files')
parser.add_argument('path', help='directory to scan for duplicate files')
args = parser.parse_args()

hashMap = {}
for fileName in os.listdir(args.path):
    absolutePath = os.path.join(args.path, fileName)
    md5 = md5sum(absolutePath)
    if md5 not in hashMap:
        hashMap[md5] = []
    hashMap[md5].append(absolutePath)

duplicates = {key:value for key, value in hashMap.items() if len(value) > 1}
for hash, files in duplicates.items():
    files.sort(key=lambda file: os.path.getctime(file))
    
    while len(files) > 1:
        file = files.pop()
        if args.delete:
            print("rm ", file)
            os.remove(file)
        else:
            print(file)