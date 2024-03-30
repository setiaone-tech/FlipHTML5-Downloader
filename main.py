import requests, json, os, img2pdf

def get_link(url):
    if "online" in url:
        get_image(url)
    else:
        url = url.split("/")
        url[2] = "online.fliphtml5.com"
        url = "/".join(url[:5])
        get_image(f"{url}/")

def get_image(link):
    print("Msg : Downloading Image...")
    datas = []
    url = f"{link}javascript/config.js"
    res = requests.get(url)
    conf = json.loads(res.text.split('= ')[1].split(';')[0])
    title = conf['meta']['title']
    os.makedirs(title, exist_ok=True)
    page = conf["fliphtml5_pages"]
    num = 1
    printProgressBar(0, len(page), prefix = 'Progress:', suffix = 'Complete', length = 50)
    for p in range(len(page)):
        if 'jpg' in page[p]['n'][0]:
            link_img = page[p]['n'][0].split("./")[1]
            res = requests.get(f"{link}{link_img}")
            with open(f"{title}/pict{num}.png", "wb") as f:
                f.write(res.content)
            num += 1
        else:
            new_url = f"{link}files/large/{page[p]['n'][0]}"
            res = requests.get(new_url)
            with open(f"{title}/pict{num}.png", "wb") as f:
                f.write(res.content)
            datas.append(f"{title}/pict{num}.png")
            num += 1
        printProgressBar(p + 1, len(page), prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    cv2pdf(title, datas)

def cv2pdf(title, data):
    print("Msg : Converting to PDF... wait a moment")
    with open(f"{title}/{title}.pdf", "wb") as file:
        file.write(img2pdf.convert(data))
    print("Msg : Done!!")
    print(f"Location : {os.getcwd()}\{title}\{title}.pdf")

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def banner():
    print("""
  ______ _ _       _    _ _______ __  __ _      _____       _____                      _                 _           
 |  ____| (_)     | |  | |__   __|  \/  | |    | ____|     |  __ \                    | |               | |          
 | |__  | |_ _ __ | |__| |  | |  | \  / | |    | |__ ______| |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 |  __| | | | '_ \|  __  |  | |  | |\/| | |    |___ \______| |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |    | | | |_) | |  | |  | |  | |  | | |____ ___) |     | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |_|    |_|_| .__/|_|  |_|  |_|  |_|  |_|______|____/      |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
            | |                                                                                               v1.0   
            |_|                                                                                                      """)

if __name__ == '__main__':
    banner()
    link = input("Masukan link = ")
    get_link(link)