"""
Project 7: Concurrent Programming
Student: Tri Trang
I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes
cheating, and that I will receive a zero on this project if I am found in violation of this policy.
"""

import requests
from pathlib import Path
import os
import time
import concurrent.futures as ft


main_folder = Path().cwd()
Flags_path = main_folder / "Flags"
Flags_text_path = main_folder / "flags.txt"

with open(Flags_text_path, 'r') as f:
    countries = f.read().splitlines()


def get_flag(country):
    flag_file = f"{country}.jpg"
    response = requests.get(f"https://www.sciencekids.co.nz/images/pictures/flags680/{flag_file}")
    if os.path.exists(Flags_path / flag_file):
        os.remove(Flags_path / flag_file)

    with open(Flags_path / f"{country}.jpg", 'wb') as f1:
        f1.write(response.content)

    return len(response.content)


def main():
    start_time = time.perf_counter()
    with ft.ThreadPoolExecutor(max_workers=25) as pool:
        bytes_downloaded_list = pool.map(get_flag, countries)
    bytes_downloaded = sum(bytes_downloaded_list)
    end_time = time.perf_counter()
    with open("summary.txt", 'w') as f2:
        f2.write(f"Elapsed time: {end_time - start_time} \n")
        f2.write(f"{bytes_downloaded} bytes downloaded")


if __name__ == "__main__":
    main()
