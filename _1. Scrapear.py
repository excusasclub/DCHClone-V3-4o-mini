import csv
from newspaper import Article
import pandas as pd
import time

def extraer_contenido(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.title, article.text, article.top_image

def main():
    archivo_unificado = "3. Unificado.csv"
    archivo_scrapeado = "4. Scrapeado.csv"
    df_unificado = pd.read_csv(archivo_unificado, encoding='utf-8')
    total_urls = len(df_unificado)
    urls_procesadas = 0
    with open(archivo_scrapeado, 'w', newline='', encoding='utf-8') as file_scrapeado:
        csv_writer = csv.writer(file_scrapeado)
        csv_writer.writerow(['URL', 'Keywords', 'Titulo', 'Contenido', 'Portada'])
        for index, row in df_unificado.iterrows():
            url = row['URL'].strip()
            keywords = row['Keywords'].strip()
            if not url:
                continue
            try:
                titulo, contenido, portada = extraer_contenido(url)
                csv_writer.writerow([url, keywords, titulo, contenido, portada])
                urls_procesadas += 1
                print(f"[{urls_procesadas}/{total_urls}] Contenido extraído de {url}")
                time.sleep(0)
            except Exception as e:
                print(f"No se pudo extraer contenido de {url}. Error: {str(e)}")

if __name__ == "__main__":
    main()
