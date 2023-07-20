from lxml import html
import requests
import os

class Rule34:
    BASE_LINK = 'https://rule34.xxx/'
    PHP_BASE = 'index.php?'
    BASE_RESEARCH = 'page=post&s=list&tags='
    BASE_POST = 'page=post&s=view&id='

    XPATH_POST_LIST = '//*[@id="post-list"]/div[2]/div[1]'
    XPATH_POST_LINK = 'a/@href'
    XPATH_IMAGE = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div[1]/img/@src'
    XPATH_VIDEO = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div[1]/div[3]/video/source/@src'
    #XPATH_POST_TAGS = 'a/img/@alt'

    XPATH_LASTPAGE = '//*[@id="paginator"]/div/a[@alt="last page"]/@href'

    PAGE_SELECTOR = '&pid='
    U_PID = 42  # questo deve essere moltiplicato per in numero della pagina che vogliamo selezionare
    # esempio utilizzo f'{BASE_LINK}{PHP_BASE}{BASE_RESEARCH}{tags}{PAGE_SELECTOR}{U_PID*numeropagina}'
    PID = 0

    def __init__(self):
        self.nPage = 0

    def build_link(self, tags: list[str, str] = None, nPage: int = None) -> str:
        if page: # Manage None page
            self.nPage = nPage

        if page < 0:  # Manage negative numbers
            self.nPage = self.lastPage()

        self.tags = tags
        if not tags: # Manage None tags
            self.tags = 'all'

        return f'{self.BASE_LINK}{self.PHP_BASE}{self.BASE_RESEARCH}{"+".join(self.tags)}{self.PAGE_SELECTOR}{self.U_PID * self.nPage}'

    def is_url(self, url: str) -> bool:
        return self.BASE_LINK in url

    def get_content_from_url(url: str) -> tuple[str, html.HtmlElement]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return html.fromstring(response.content), response.text
        else:
            return None

    def last_page(self) -> int:
        if url := self.tree.xpath(self.XPATH_LASTPAGE).__len__() != 0: # Prevent error
            return int(url[0].split('&pid=')[-1])
        return 0

    def set_page(self, tags: list[str, str] = None, nPage: int = None) -> None:
        self.link = self.build_link(tags, nPage)
        self.tree, self.html = self.get_content_from_url(self.link)

    def get_id_from_url(self, url: str) -> str:
        return url.split("&id=")[0]

    def get_tags_from_url(self, url: str) -> str:
        url = url.split('&tags=')[-1]
        if '&pid=' in url:
            return url.split('&pid=')[0]
        return url.replace('+', ', ')

    def get_npage_from_url(self, url: str) -> int:
        if '&pid=' in url:
            return int(url.split('&pid=')[-1])//self.U_PID
        return 0

    def get_posts(self) -> list[dict[str:str, str:str, str:str], dict[str:str, str:str, str:str]]:
        posts = []
        for post in self.tree.xpath(self.XPATH_POST_LIST)[0]:
            posts.append(self.get_postdata_from_url(f'{self.BASE_LINK}{post.xpath(self.XPATH_POST_LINK)[0]}'))

        return posts

    def get_posts_from_page(self, nPage: int = None) -> list[dict[str:str, str:str, str:str]]:
        self.setPage(page=nPage)

        return self.get_posts()

    def get_posts_form_pages(self, page: list[int, int]) -> dict[str:list[ dict[str:str, str:str, str:str] ]]:
        # Ex of use: get_posts_form_pages(range(0, 10))

        posts_pages = { } # Example: "page 1": [ UrlPosts ]
        for n_page in page:
            posts_pages[f"page {n_page}"] = self.get_posts_from_page(n_page)
        return posts_pages

    def get_posts_from_url(self, url: str) -> list[dict[str:str, str:str, str:str]]:
        tree, _ = self.get_content_from_url(url)

        posts = []
        for post in tree.xpath(self.XPATH_POST_LIST)[0]:
            posts.append(self.get_postdata_from_url(f'{self.BASE_LINK}{post.xpath(self.XPATH_POST_LINK)[0]}'))
        return posts

    def get_post_from_url(self, url: str) -> dict[str:str, str:str, str:str]:
        return self.get_postdata_from_url(url)

    def get_post_from_id(self, id) -> dict[str:str, str:str, str:str]:
        return self.get_postdata_from_url(f"{self.BASE_LINK}{self.PHP_BASE}{self.BASE_POST}{id}")

    def get_post_from_index(self, index: int) -> dict[str:str, str:str, str:str]:
        return self.get_posts_from_page()[index]
    
    def get_postdata_from_url(self, url: str) -> dict[str:str, str:str, str:str]:
        tree, html = self.get_content_from_url(url)

        link = self.tree.xpath(self.XPATH_IMAGE)  # Get image from post
        type = 'image'  # Set type as a image

        if link.__len__() == 0:  # Prevent type error
            link = tree.xpath(self.XPATH_VIDEO)  # Get video from post
            type = 'video'  # Set type as a video

        if link.__len__() == 0:
            link = 'Empty'
            type = 'none'


        return {
            'id': url.split('&id=')[-1],
            'type': type,
            'source': link
        }
