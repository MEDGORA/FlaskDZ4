"""Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
"""
# пример:
#str = "https://www.google.ru/, https://gb.ru/, https://ya.ru/, https://www.python.org/, https://habr.com/ru/all/, https://img.goodfon.ru/original/2331x1750/1/c7/leopard-vzglyad-lezhit-leopard.jpg, https://gagaru.club/uploads/posts/2023-02/1676083963_gagaru-club-p-krasivaya-pchela-vkontakte-58.jpg, https://img.razrisyika.ru/kart/137/1200/544003-fotografiy-v-horoshem-kachestve-29.jpg"

import argparse
import aiohttp
import requests
import threading
from multiprocessing import Process
import asyncio
import time

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="Выбранным вами способом реализации многозадачности скачивает только изображение формата '.jpg' из введённых URL-адресов")
    parser.add_argument("process_name", metavar="process_name", type= str, help="Введите вид много задачности: threading, multiprocessing или asyncio, тип str")
    parser.add_argument("urls", metavar="urls", type= str, help="Введите список URL-адресов через запятую в одну строку, тип str")
    args = parser.parse_args()
    input_str = args.urls
    process_name = args.process_name

    list_in_file = input_str.split(", ")
    urls = []

    def get_file_info(file_path) :
        list = file_path.split("/")
        file = list[-1]
        list.pop()
        name_of_file = ""
        count = 0
        for i in file :
            if i == "." :
                count += 1
            if count > 1 :
                name_of_file = file.split(".")
                name_of_file.pop()
                name_of_file = ".".join(name_of_file)
            else :
                name_of_file = file.split(".")[0]
        if file.split(".")[-1] == "file" :
            return "/".join(list) + "/", "", "." + file.split(".")[-1]
        elif "/".join(list) == "":
            return "/".join(list), name_of_file, "." + file.split(".")[-1]
        else :
            return "/".join(list) + "/", name_of_file, "." + file.split(".")[-1]

    def download(url):
        response = requests.get(url)
        filename = get_file_info(url)[1] + ".jpg"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Загружен файл {filename} за {time.time()-start_time:.2f} секунды")

    async def acync_download(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                img = await response.read()
                filename = get_file_info(url)[1] + ".jpg"
                with open(filename, "wb") as f:
                    f.write(img)
                print(f"Downloaded {url} in {time.time() -start_time:.2f} seconds")

    def threading_process():
        threads = []

        for url in urls:
            thread = threading.Thread(target=download, args=[url])
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()

    def multiprocessing_process() :
        processes = []

        if __name__ == '__main__':
            for url in urls:
                process = Process(target=download, args=(url,))
                processes.append(process)
                process.start()

            for process in processes:
                process.join()

    def async_process():
        async def main():
            tasks = []

            for url in urls:
                task = asyncio.ensure_future(acync_download(url))
                tasks.append(task)
            await asyncio.gather(*tasks)

        if __name__ == '__main__':
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())


    for i in list_in_file :
        if get_file_info(i)[2] == ".jpg" :
            urls.append(i)

    start_time = time.time()
    method = ""

    if process_name == "threading" :
        method = "многопоточный"
        threading_process()
    elif process_name == "multiprocessing" :
        method = "многопроцессорный"
        multiprocessing_process()
    elif process_name == "asyncio":
        method = "асинхронный"
        async_process()

    print(f"Общее время выполнения: {time.time()-start_time:.2f} секунды, был использован {method} метод")