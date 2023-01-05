import collections
import random
import shutil
import string
import sys
from pathlib import Path
from termcolor import colored

trash_dict = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".xls", ".xlsx", ".txt", ".pdf"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".gz", ".tar"],
    "programming": [".php", ".js", ".py", ".html", ".sql"]
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h",
    "ts",
    "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_",
    "_",
    "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")
TRANS = {}
for cyr_name, trans_name in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyr_name)] = trans_name
    TRANS[ord(cyr_name.upper())] = trans_name.upper()


def normalize(name_file):
    global TRANS
    return name_file.translate(TRANS)


def archive_unpacking(archive_path, path_to_unpack):
    return shutil.unpack_archive(archive_path, path_to_unpack)


def check_file_exists(search_file, file_directory):
    if search_file in file_directory.iterdir():
        add_symbols = ""
        for _ in range(3):
            ch = random.choice(string.ascii_letters + string.digits)
            add_symbols += str(ch)
        file_name = search_file.resolve().stem + f"({add_symbols})" + search_file.suffix
        file_path = Path(file_directory, file_name)
        return file_path
    return search_file


def check_fold_exists(search_folder, folder_directory):
    if folder_directory.exists():
        folder_sort(search_folder, folder_directory)
    else:
        Path(folder_directory).mkdir()
        folder_sort(search_folder, folder_directory)


def folder_sort(f_file, path_folder):
    trans_to_latin = normalize(f_file.name)
    renamed_file = Path(path_folder, trans_to_latin)
    exists_file = check_file_exists(renamed_file, path_folder)
    f_file.replace(exists_file)


def sort_file(p):
    global fold
    path = Path(p)

    for _ in range(2):
        for current_folder in path.iterdir():
            if current_folder.name in ("documents", "audio", "video", "images", "archives", "programming", "other"):
                continue
            if current_folder.is_file():
                flag = False
                for i_file, su_ffix in trash_dict.items():
                    if current_folder.suffix.lower() in su_ffix:
                        drctr = Path(fold, i_file)
                        check_fold_exists(current_folder, drctr)
                        flag = True
                    else:
                        continue
                if not flag:
                    drctr = Path(fold, "other")
                    check_fold_exists(current_folder, drctr)
            elif current_folder.is_dir():
                if len(list(current_folder.iterdir())) != 0:
                    sort_file(current_folder)
                else:
                    shutil.rmtree(current_folder)

        for archive in path.iterdir():
            if archive.name == "archives" and len(list(archive.iterdir())) != 0:
                for arch in archive.iterdir():
                    if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                        archive_folder_name = arch.resolve().stem
                        unpacking_path = Path(fold, "archives", archive_folder_name)
                        shutil.unpack_archive(arch, unpacking_path)
                    else:
                        continue


def main(p):
    sort_file(p)
    path = Path(p)
    total_dict = collections.defaultdict(list)
    for item in path.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    total_dict[item.name].append(file.suffix)
    text = colored('\n------------------------ Сортування файлів успішно виконано! ------------------------', 'green')
    print(text)
    print("\n-------------------------------------------------------------------------------------")
    print("| {:^15} | {:^17} | {:^43} |".format("Назва папки ", "Кількість файлів", "Розширення файлів"))
    print("|-----------------------------------------------------------------------------------|")
    for key, value in total_dict.items():
        nazva, kilkist, rozshyrennya = key, len(value), ", ".join(set(value))
        print("| {:<15} | {:^17} | {:<43} |".format(nazva, kilkist, rozshyrennya))
    print("-------------------------------------------------------------------------------------\n")


if __name__ == "__main__":
    first_path = sys.argv[1]
    fold = Path(first_path)
    main(first_path)