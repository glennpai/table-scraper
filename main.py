import os
import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
BASE_DIR = os.getenv("BASE_DIR")
DOCS_DIR = os.getenv("DOCS_DIR")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
FILENAME_COL_IDX = int(os.getenv("FILENAME_COL_IDX"))
LINK_COL_IDX = int(os.getenv("LINK_COL_IDX"))

os.makedirs(DOCS_DIR, exist_ok=True)

def fetch_webpage(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(content):
    return BeautifulSoup(content, "lxml")

def extract_table(soup):
    table = soup.find("table")
    if not table:
        raise ValueError("No table found on the page")
    return table

def extract_headers(table):
    headers = [th.text.strip() for th in table.find_all("th")]
    headers.append("PDF File Path")
    return headers

def generate_filename(base_filename, count):
    if base_filename in count:
        count[base_filename] += 1
        return f"{base_filename}-{count[base_filename]}.pdf"
    else:
        count[base_filename] = 1
        return f"{base_filename}.pdf"

def download_pdf(pdf_url, path):
    pdf_response = requests.get(pdf_url, stream=True)
    pdf_response.raise_for_status()
    with open(path, "wb") as pdf_file:
        for chunk in pdf_response.iter_content(1024):
            pdf_file.write(chunk)
    print(f"Downloaded: {path}")

def process_table_rows(table, url, docs_dir):
    rows = []
    filename_count = {}
    for tr in table.find_all("tr")[1:]:
        cells = [td.text.strip() for td in tr.find_all("td")]
        if len(cells) <= max(FILENAME_COL_IDX, LINK_COL_IDX):
            continue
        base_filename = cells[FILENAME_COL_IDX].replace(" ", "_").replace("/", "_").replace("\\", "_")
        pdf_link_tag = tr.find_all("td")[LINK_COL_IDX].find("a", href=True)
        if pdf_link_tag:
            pdf_url = urljoin(url, pdf_link_tag["href"])
            try:
                head_response = requests.head(pdf_url, allow_redirects=True, timeout=5)
                content_type = head_response.headers.get("Content-Type", "")
                if "pdf" in content_type.lower():
                    filename = generate_filename(base_filename, filename_count)
                    pdf_path = os.path.join(docs_dir, filename)
                    download_pdf(pdf_url, pdf_path)
                    cells.append(pdf_path)
                else:
                    print(f"Skipping non-PDF link: {pdf_url}")
                    cells.append("")
            except requests.exceptions.RequestException as e:
                print(f"Failed to process {pdf_url}: {e}")
                cells.append("")
        else:
            cells.append("")
        rows.append(cells)
    return rows

def write_to_csv(file_path, headers, rows):
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Data saved to {file_path}")

def main():
    html_content = fetch_webpage(URL)
    soup = parse_html(html_content)
    table = extract_table(soup)
    headers = extract_headers(table)
    rows = process_table_rows(table, URL, DOCS_DIR)
    write_to_csv(CSV_FILE_PATH, headers, rows)

if __name__ == "__main__":
    main()
