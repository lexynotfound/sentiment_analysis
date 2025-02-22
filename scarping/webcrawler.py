import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# ========================= SETUP SELENIUM UNTUK SCRAPING PENCARIAN =========================
def get_search_results(query, num_results=10000, search_engine="duckduckgo"):
    """Melakukan pencarian berita di DuckDuckGo, Bing, dan Yahoo lalu mengambil URL dari hasil pencarian"""
    options = Options()
    options.add_argument("--headless")  # Mode tanpa UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    if search_engine == "duckduckgo":
        base_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&t=h_&ia=web"
    elif search_engine == "bing":
        base_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
    else:  # Yahoo sebagai alternatif tambahan
        base_url = f"https://search.yahoo.com/search?p={query.replace(' ', '+')}"

    driver.get(base_url)
    time.sleep(5)  # Tunggu halaman termuat

    links = set()
    page = 0

    while len(links) < num_results:
        # SCROLL BAWAH UNTUK MEMUAT SEMUA HASIL
        for _ in range(3):
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        search_results = []

        if search_engine == "duckduckgo":
            search_results = driver.find_elements(By.CSS_SELECTOR, "a.result__url")  # Perbaikan selector
        elif search_engine == "bing":
            search_results = driver.find_elements(By.CSS_SELECTOR, "li.b_algo h2 a")
        elif search_engine == "yahoo":
            search_results = driver.find_elements(By.CSS_SELECTOR, "h3.title a")

        for result in search_results:
            url = result.get_attribute("href")
            if url and "http" in url:
                links.add(url)

        # Jika sudah cukup berita, keluar dari loop
        if len(links) >= num_results:
            break

        # COBA KE HALAMAN BERIKUTNYA
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()
            time.sleep(5)
        except:
            print(f"⚠️ Tidak ada halaman berikutnya di {search_engine}. Berhenti scraping...")
            break  # Jika tidak ada tombol "Next", berhenti

        page += 1

    driver.quit()
    return list(links)


# ========================= SCRAPING KONTEN BERITA =========================
def scrape_content(url):
    """Mengambil konten berita dari sebuah URL"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Ambil judul berita
        title = soup.find("title").text.strip() if soup.find("title") else "No Title"

        # Ambil isi berita dari <p> tag
        paragraphs = soup.find_all("p")
        content = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()])

        return {"url": url, "title": title, "content": content}

    except Exception as e:
        print(f"⚠️ Gagal mengambil konten dari {url}: {e}")
        return None


# ========================= EKSEKUSI SCRAPING BERITA =========================
def scrape_news(queries, num_results=13500):
    """Scraping berita dari beberapa query tanpa berhenti sebelum mencapai 3.500 data"""
    print(f"🔎 Mencari berita dengan beberapa kata kunci: {queries}")

    articles = []  # Menggunakan list agar tidak error saat mengakses `article["url"]`
    collected_urls = set()  # Untuk menghindari duplikasi
    search_engines = ["duckduckgo", "bing", "yahoo"]

    for query in queries:
        print(f"🔍 Scraping dengan kata kunci: {query}")

        for engine in search_engines:
            urls = get_search_results(query, num_results // len(queries), search_engine=engine)
            print(f"✅ {len(urls)} hasil ditemukan dari {engine} untuk '{query}'")

            for url in urls:
                if url not in collected_urls:  # Hindari duplikasi
                    article = scrape_content(url)
                    if article:
                        articles.append(article)
                        collected_urls.add(url)
                        print(f"📄 Berhasil mengambil: {article['title']}")

                    if len(articles) >= num_results:
                        break  # Stop jika sudah mencapai jumlah minimum berita

            print(f"⏳ Saat ini terkumpul {len(articles)} berita...")

        if len(articles) >= num_results:
            break

    # Simpan ke CSV
    df = pd.DataFrame(articles)
    df.to_csv("../data/news_scraping_results.csv", index=False)
    print(f"✅ Scraping selesai! {len(df)} berita disimpan dalam 'data/news_scraping_results.csv'")


# ========================= JALANKAN SCRAPING =========================
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)  # Pastikan folder data ada
    listQuery = [
        "politik indonesia",
        "indonesia gelap",
        "makan siang gratis",
        "prabowo",
        "gibran rakabuming raka",
        "pemerintahan",
        "politics in indonesian",
        "goverment indonesian",
        "kabur aja dulu"
    ]

    for query in listQuery:
        scrape_news([query], num_results=3500 // len(listQuery))  # Proses kata kunci satu per satu
