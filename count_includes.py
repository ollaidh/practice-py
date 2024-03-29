# counts number of includes in .h files which starts with Q recursively in a folder and subfolders
# writes the result to file

import os


def includes_stats_tofile(folderpath: str):
    includes = {}
    for subdir, dirs, files in os.walk(folderpath):
        for file in files:
            current_path = os.path.join(subdir, file)
            if not file.endswith(".h"):
                continue
            # print(current_path)
            with open(current_path) as f:
                for line in f:
                    if not line.startswith("#include <Q"):
                        continue
                    lib = line.lstrip("#include <Q").rstrip(">\n")
                    if lib not in includes:
                        includes[lib] = 0
                    includes[lib] += 1

    includes_sorted = {k: v for k, v in sorted(includes.items(), key=lambda item: -item[1])}
    with open(os.path.join(folderpath, "includes_stats.txt"), "w") as file:
        for key, value in includes_sorted.items():
            file.write(f'{key}: {value}\n')


def count_lines(folderpath: str) -> int:
    number_of_lines = 0
    for subdir, dirs, files in os.walk(folderpath):
        for file in files:
            current_path = os.path.join(subdir, file)
            if file.endswith(".h") or file.endswith(".cpp"):
                with open(current_path) as f:
                    for line in f:
                        number_of_lines += 1

    return number_of_lines


if __name__ == "__main__":
    includes_stats_tofile("/Users/maria/Downloads/src")
    print(count_lines("/Users/maria/Downloads/src"))
