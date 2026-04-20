import datetime
from datetime import date

from bs4 import BeautifulSoup


# def parse_page_links(html: str, start_date: date, end_date: date, url: str):
#     """
#     Парсит ссылки на бюллетени с одной страницы:
#     <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
#     """
#     results = []
#     soup = BeautifulSoup(html, "html.parser")
#     links = soup.find_all("a", class_="accordeon-inner__item-title link xls")
#
#     for link in links:
#         href = link.get("href")
#         if not href:
#             continue
#
#         href = href.split("?")[0]
#         if "/upload/reports/oil_xls/oil_xls_" not in href or not href.endswith(".xls"):
#             continue
#
#         try:
#             date = href.split("oil_xls_")[1][:8]
#             file = datetime.datetime.strptime(date, "%Y%m%d").date()
#             if start_date <= file <= end_date:
#                 u = href if href.startswith("http") else f"https://spimex.com{href}"
#                 results.append((u, file))
#             else:
#                 print(f"Ссылка {href} вне диапазона дат")
#         except Exception as e:
#             print(f"Не удалось извлечь дату из ссылки {href}: {e}")
#
#     return results
class LinkParser:
    # Константы для быстрого доступа и их изменения при необходимости
    BASE_URL = 'https://spimex.com'
    DATE_FORMAT = '%Y%m%d'
    CSS_CLASSES = 'accordeon-inner__item-title link xls'

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def parse(self, html: str, start_date: date, end_date: date, url: str) -> list[tuple[str, date]]:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a', class_=self.CSS_CLASSES)

        for element in links:
            href = element.get("href")
            if not href or "/upload/reports/oil_xls/oil_xls_" not in href:
                continue

            file_date = self._extract_date(href)

            if file_date and start_date <= file_date <= end_date:
                full_url = self._build_full_url(href)
                results.append((full_url, file_date))   # добавление кортежа в список вида ('ссылка', дата)

        return results

    def _extract_date(self, href: str) -> date | None:
        """ Метод для извлечения даты из ссылки """
        try:
            date_str = href.split('oil_xls_')[1][:8]
            return datetime.datetime.strptime(date_str, self.DATE_FORMAT).date()
        except ValueError:
            return None

    def _build_full_url(self, href: str) -> str:
        """ Сборка полной ссылки с помощью функции urljoin() """
        from urllib.parse import urljoin
        return urljoin(self.base_url, href)
