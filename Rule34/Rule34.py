from lxml import html
import requests
import os

def getHTML(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return html.fromstring(response.content), response.text
    else:
        return None

class PostData:
    XPATH_IMAGE = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div[1]/img/@src'
    XPATH_VIDEO = '/html/body/div[5]/div/div[2]/div[1]/div[2]/div[1]/div[3]/video/source/@src'

    def __init__(self, url: str):
        self.tree, self.html = getHTML(url)  # Requests post page

        self.id = int(url.split('&id=')[-1]) # Get Id from url

        self.link = self.tree.xpath(self.XPATH_IMAGE) # Get image from post
        self.type = 'image' # Set type as a image

        if self.link.__len__() == 0: # Prevent type error
            self.link = self.tree.xpath(self.XPATH_VIDEO) # Get video from post
            self.type = 'video' # Set type as a video

        if self.link.__len__() == 0:
            self.link = 'Empty posts'
            self.type = 'none'

class Rule34:
    BASE_LINK = 'https://rule34.xxx/'
    PHP_BASE = 'index.php?'
    BASE_RESEARCH = 'page=post&s=list&tags='
    BASE_POST = 'page=post&s=view&id='

    XPATH_POST_LIST = '//*[@id="post-list"]/div[2]/div[1]'
    XPATH_POST_LINK = 'a/@href'
    #XPATH_POST_TAGS = 'a/img/@alt'

    XPATH_LASTPAGE = '//*[@id="paginator"]/div/a[@alt="last page"]/@href'

    PAGE_SELECTOR = '&pid='
    U_PID = 42  # questo deve essere moltiplicato per in numero della pagina che vogliamo selezionare
    # esempio utilizzo f'{BASE_LINK}{PHP_BASE}{BASE_RESEARCH}{tags}{PAGE_SELECTOR}{U_PID*numeropagina}'
    PID = 0

    def __init__(self):
        self.nPage = 0

    def build(self, tags: list[str, str] = None, nPage: int = None) -> str:
        if page: # Manage None page
            self.nPage = nPage

        if page < 0:  # Manage negative numbers
            self.nPage = self.lastPage()

        self.tags = tags
        if not tags: # Manage None tags
            self.tags = 'all'

        return f'{self.BASE_LINK}{self.PHP_BASE}{self.BASE_RESEARCH}{"+".join(self.tags)}{self.PAGE_SELECTOR}{self.U_PID * self.nPage}'

    def verify(self, url: str) -> bool:
        return self.BASE_LINK in url

    def connect(self, url: str) -> tuple[str, html.HtmlElement, str]:
        return url, *getHTML(url)#link tree, html

    def lastPage(self) -> int:
        if url := self.tree.xpath(self.XPATH_LASTPAGE).__len__() != 0: # Prevent error
            return int(url[0].split('&pid=')[-1])
        return 0

    def setPage(self, tags: list[str, str] = None, nPage: int = None) -> None:
        self.link, self.tree, self.html = self.connect(self.build(tags, nPage))

    def getIdFromUrl(self, url: str) -> str:
        return url.split("&id=")[0]

    def getTagsFromUrl(self, url: str) -> str:
        url = url.split('&tags=')[-1]
        if '&pid=' in url:
            return url.split('&pid=')[0]
        return url.replace('+', ', ')

    def getNpageFromUrl(self, url: str) -> int:
        if '&pid=' in url:
            return int(url.split('&pid=')[-1])//self.U_PID
        return 0

    def getPosts(self) -> list[PostData, PostData]:
        posts = []
        for post in self.tree.xpath(self.XPATH_POST_LIST)[0]:
            posts.append(PostData(f'{self.BASE_LINK}{post.xpath(self.XPATH_POST_LINK)[0]}'))

        return posts

    def getPostsFromPage(self, nPage: int = None) -> list[PostData, PostData]:
        self.setPage(page=nPage)

        return self.getPosts()

    def getPostsFormPages(self, page: list[int, int]) -> dict[str:list[PostData, PostData]]:
        # Ex of use: getPostsFormPages(range(0, 10))

        postsPages = { } # Example: "page 1": [ UrlPosts ]
        for nPage in page:
            postsPages[f"page {nPage}"] = self.getPostsFromPage(nPage)
        return postsPages

    def getPostsFromUrl(self, url: str) -> list[PostData, PostData]:
        _, tree, _ = self.connect(url)

        posts = []
        for post in tree.xpath(self.XPATH_POST_LIST)[0]:
            posts.append(PostData(f'{self.BASE_LINK}{post.xpath(self.XPATH_POST_LINK)[0]}'))
        return posts

    def getPostFromUrl(self, url: str) -> PostData:
        return PostData(url)

    def getPostFromId(self, id) -> PostData:
        return PostData(f"{self.BASE_LINK}{self.PHP_BASE}{self.BASE_POST}{id}")

    def getPostFromIndex(self, index: int) -> PostData:
        return self.getPostsFromPage()[index]



def main():
    pass


if __name__ == '__main__':
    main()
