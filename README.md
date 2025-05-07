# 📄 WebScraping Downloader

A simple web scraping tool to bulk-download PDF files from a sectioned website behind a login and CAPTCHA barrier. The tool uses a Chrome browser session for authentication and then allows you to input specific tags for targeted downloads.

## 🛠️ Prerequisites

* Python 3.7+
* Google Chrome installed
* ChromeDriver compatible with your version of Chrome
* Git (for cloning the repository)

## 📦 Setup

1. Clone this repository:

```bash
git clone https://github.com/PeterRiek/scrapers.git
cd scrapers
```

2. Create and activate a virtual environment:

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure that ChromeDriver is in your PATH or in the root of the project.

## 🚀 Usage

Start the script using:

```bash
python downloader.py
```

Chrome will open the login page of the target website.

Follow these steps:

1. Log in manually using your credentials in the Chrome window.
2. Complete any CAPTCHA challenge.
3. Once logged in and redirected to the main page, return to the terminal and press Enter.

You’ll be prompted to enter a section tag for bulk downloading.

Downloads will be saved under the downloaded\_pdfs directory, preserving their folder structure.

## 🧪 Example Session

```plaintext
(.venv) C:\Users\root\git\scrapers>python downloader.py
Log in using your browser and afterwards press enter to start.

Enter a section tag for which to start the bulk download.
(Enter "exit" to quit)
Prävention und Gesundheitsörderung
Starting download for tag: "Prävention und Gesundheitsörderung"...
Done downloading 0 items!
Enter a section tag for which to start the bulk download.
(Enter "exit" to quit)
Prävention und Gesundheitsförderung
Starting download for tag: "Prävention und Gesundheitsförderung"...
Downloaded: downloaded_pdfs\...\Praevention SS2005 Klausur.pdf
...
Done downloading 9 items!
Enter a section tag for which to start the bulk download.
(Enter "exit" to quit)
exit
```

## 📁 Output

All files will be downloaded into:

```
downloaded_pdfs/
  └── <section structure>/
        └── <file>.pdf
```

## 💡 Notes

* Be precise when entering section tags (watch out for special characters and typos).
* CAPTCHA must be completed manually during login.

## 🔐 License

[MIT License](LICENSE)

Would you like me to generate a requirements.txt file or .gitignore as well?
