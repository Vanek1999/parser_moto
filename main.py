#-----Разраб:pedro&ento_Vanek-----
import requests
import asyncio
import eel
from time import sleep
from bs4 import BeautifulSoup


# -----Av-----
async def parseAv(url: str, data: list) -> None:
    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    for block in soup.find_all("div", class_="listing-item__about"):
        data.append("https://moto.av.by" + block.find("a", class_="listing-item__link").get("href"))

# -----Kufar-----
async def parseKufar(url:str, data:list) -> None:
    for link in BeautifulSoup(requests.get(url).text, features="html.parser").find_all("a"):
        data.append(link.get("href"))

async def Data() -> list:
    data = []
    # -----Honda(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-honda?cur=BYR&mtc=r:10,27", data)
    # -----Suzuki(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-suzuki?cur=BYR&mtc=r:10,27", data)
    # -----Yamaha(Kufar)-----
    await parseKufar("https://auto.kufar.by/l/skuter-yamaha?cur=BYR&mtc=r:10,27", data)

    # -----Honda(Av)-----
    await parseAv("https://moto.av.by/filter?category_type=2&brands[0][brand]=383&engine_capacity[max]=80", data)
    # -----Suzuki(Av)-----
    await parseAv("https://moto.av.by/filter?category_type=2&brands[0][brand]=1155&engine_capacity[max]=80", data)
    # -----Yamaha(Av)-----
    await parseAv("https://moto.av.by/filter?category_type=2&brands[0][brand]=2875&engine_capacity[max]=80", data)

    return data
  
@eel.expose
def start():
    new_data = asyncio.run(Data())
    with open("config\\data.txt", "r+") as data_file:
        data = data_file.read().split("\n")
        # -----Сравнение-----
        if new_data != data:
            new_ads = list(set(new_data) - set(data))
            for item in new_ads:
                data_file.write(item + "\n")
                requests.post("https://api.telegram.org/bot5143736659:AAHgUVXtQzbTb644cnPPcWaZdzyCjFQYkbc/sendMessage?chat_id=961053185&text=" + str(item))

if __name__ == "__main__":
    eel.init("config\\web\\")
    eel.start("index.html", mode="chrome", size=(350, 160))
