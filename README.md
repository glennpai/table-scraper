# table-scraper

Just a basic site scraper which is pretty good for scraping tables of a particular shape and size. For data preservation and archival purposes only.

## Disclaimer

This project was created as an experiment in practice of data preservation and archival. This project is intended to be used for rapid downloading (scraping) of data from a table element on a target website. Using this script on some sites may incur penalties such as rate limits, timeouts, or IP bans on those sites depending on their terms of use. Use at your own risk, and use responsibly. 

I provide and/or claim no support, warranty, affiliation, or association, and am in no way responsible for, or related to, any individual or organization's use of the project herein. The project is provided as-is via MIT License (see below).

## Prerequisites

- Python 3.11
- `pip` (Python package installer)
- Docker (optional, for running the script in a container)

## Setup

1. Clone the repository and navigate to the project directory.
2. Create a `.env` file in the project root with the following content:

    ```sh
    URL=https://some_url
    BASE_DIR=/data
    DOCS_DIR=/data/docs
    CSV_FILE_PATH=/data/scraped_table.csv
    FILENAME_COL_IDX=0
    LINK_COL_IDX=2
    ```

3. Install the required Python libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Script Locally

1. Ensure the `.env` file is properly configured.
2. Run the script:

    ```sh
    python main.py
    ```

## Running the Script Using Docker

1. Build the Docker image:

    ```sh
    docker build -t table-scraper .
    ```

2. Run the Docker container:

    ```sh
    docker run --rm -v ./data:/data table-scraper
    ```

## Notes

- The example environment configuration provided is designed to work for pages which contain a 3 column table, the third column containing links to PDF files, and the first column used to name the files when downloaded.
- The script will create the necessary directories and download PDF files into the specified `DOCS_DIR`.
- The scraped data will be saved into the specified `CSV_FILE_PATH`.

## Licensing

MIT License

Copyright (c) 2025 github.com/glennpai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
