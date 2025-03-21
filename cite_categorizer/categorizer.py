from urllib.request import urlopen
import re
import pandas as pd

class CiteCategorizer:
    def __init__(self, palabra):
        self.palabra = palabra
        self.url = f"https://hjg.com.ar/vocbib/art/{palabra}.html"
        self.cites = []
        self.a1_lect_libros = {"Gen", "Gn", "Ex", "Lev", "Num", "Dt", "Jos", "Jue", "Rut", "1Sa", "2Sa", "1Re", "2Re", "1Par", "2Par", "Esd", "Neh", "Tob", "Jdt", "Est", "1Mac", "2Mac"}
        self.a2_lect_libros = {"Job", "Sal", "Prov", "Ecl", "Cant", "Sab", "Eclo", "Is", "Jer", "Lam", "Bar", "Ez", "Dan", "Os", "Jl", "Am", "Abd", "Jon", "Miq", "Naj", "Hab", "Sof", "Ag", "Zac", "Mal"}
        self.a3_lect_libros = {"Rom", "1Cor", "2Cor", "Ga", "Ef", "Flp", "Col", "1Tes", "2Tes", "1Tim", "2Tim", "Tit", "Flm", "Heb", "Sant", "1Pe", "2Pe", "1Jn", "2Jn", "3Jn", "Jds", "Ap"}
        self.ev_lect_libros = {"Mt", "Mc", "Lc", "Jn"}
        self.a1_lect, self.a2_lect, self.a3_lect, self.ev_lect = [], [], [], []

    def fetch_webpage(self):
        try:
            page = urlopen(self.url)
            html_bytes = page.read()
            return html_bytes.decode("utf-8", errors="ignore")
        except Exception as e:
            print(f"Failed to fetch webpage: {e}")
            return ""

    def extract_cites(self, html):
        return re.findall(r"<cite>(.*?)</cite>", html)

    def normalize_cites(self, cites):
        normalized = []
        last_book = None
        for cite in cites:
            match = re.match(r"^(\d*[A-Za-z]+)", cite)
            if match:
                last_book = match.group(0)
            else:
                cite = last_book + cite  # Prepend last seen book
            normalized.append(cite)
        return normalized

    def classify_cite(self, cite):
        book = re.match(r"^\d*[A-Za-z]+", cite).group()
        if book in self.a1_lect_libros:
            self.a1_lect.append(cite)
        elif book in self.a2_lect_libros:
            self.a2_lect.append(cite)
        elif book in self.a3_lect_libros:
            self.a3_lect.append(cite)
        elif book in self.ev_lect_libros:
            self.ev_lect.append(cite)

    def pad_list(self, lst, length):
        return lst + [""] * (length - len(lst))

    def create_excel(self):
        max_length = max(len(self.a1_lect), len(self.a2_lect), len(self.a3_lect), len(self.ev_lect))
        df = pd.DataFrame({
            "1a Lectura": self.pad_list(self.a1_lect, max_length),
            "2a Lectura": self.pad_list(self.a2_lect, max_length),
            "3a Lectura": self.pad_list(self.a3_lect, max_length),
            "Evangelio": self.pad_list(self.ev_lect, max_length)
        })
        filename = f"lecturas_{self.palabra}.xlsx"
        df.to_excel(filename, index=False, engine="openpyxl")
        print(f"Excel file '{filename}' created successfully!")

    def run(self):
        html = self.fetch_webpage()
        if not html:
            print("No HTML content fetched. Exiting.")
            return

        cites = self.extract_cites(html)
        normalized_cites = self.normalize_cites(cites)

        for cite in normalized_cites:
            self.classify_cite(cite)

        self.create_excel()
