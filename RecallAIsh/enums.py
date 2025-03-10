from enum import Enum


class ScrapperType(Enum):
    BEAUTIFULSOUP = "BeautifulSoup"
    PLAYWRIGHT = "Playwright"
    SELENIUM = "Selenium"
