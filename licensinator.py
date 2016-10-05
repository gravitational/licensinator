import os
import sys
import os.path
from difflib import SequenceMatcher

class License(object):
    def __init__(self, filename, contents):
        self.parts = [(filename, contents)]

    def merge(self, other):
        if len(other.parts) > 1:
            return False
        one = self.parts[0][1]
        another = other.parts[0][1]
        ratio = SequenceMatcher(None, one, another).ratio()
        if ratio > 0.8:
            self.parts.append(other.parts[0])
            return True
        return False


def collect_licenses(directories):
    licenses = []
    for i, directory in enumerate(directories):
        for (dirpath, dirnames, filenames) in os.walk(directory):
            for filename in filenames:
                if "license" in filename.lower():
                    full_path = os.path.join(dirpath, filename)
                    with open(full_path, "r") as f:
                        licenses.append(License(full_path, f.read()))
    return licenses


def deduplicate_licenses(licenses):
    for i in range(len(licenses)):
        print i, "out of", len(licenses)
        for j in range(len(licenses)):
            if i == j:
                continue
            if licenses[i] is None or licenses[j] is None:
                continue
            if licenses[i].merge(licenses[j]):
                licenses[j] = None

def print_licenses(licenses):
    for i, v in enumerate(licenses):
        if v is not None:
            print "-----------License Group---------------"
            print "---------------------------------------"
            for part in v.parts:
                print "FILE:", part[0]
                print "LICENSE:",part[1]
            

if __name__ == '__main__':
    target_dirs = sys.argv[1:]
    print target_dirs
    licenses = collect_licenses(target_dirs)
    deduplicate_licenses(licenses)
    print_licenses(licenses)
