# Rule34

Rule34 is a Python package that allows you to access the content from the famous adult website.

## Requirements
To use this library, you need to install the following dependencies:
* lxml
* requests

## Installation and updating
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Rule34 like below. 
Rerun this command to check for and install updates.
```bash
pip install git+https://github.com/ilNubis/Rule34
```

## All Method of Rule34 class:

### > build_link(self, tags: list[str, str], nPage: int) -> str
This method build the link of Rule34

### > is_url(self, url: str) -> bool
This method allows verifying if the URL belongs to Rule34

### > get_content_from_url(self, url: str) -> tuple[str, html.HtmlElement, str]
This method allows you to obtain the link, the tree, and the HTML

Example of usage:
```python
from Rule34 import Rule34

r34 = Rule34()

link. tree, html = r34.get_content_from_url(r34.build_link(["some tags"]))
```
### > last_page(self) -> int
This method allows you to obtain the maximum number of available pages for the selected tags

### > set_page(self, tags: list[str, str] = None, nPage: int = None) -> None
This method allows you to set the tags for the page you can navigate to

### > get_id_from_url(self, url: str) -> str
This method allows you to extract the ID from a post link

### > get_tags_from_url(self, url: str) -> str
This method allows you to extract the tags from a search link

### > getNpageFromUrl(self, url: str) -> int
This method allows you to extract the page number

### > get_posts(self) -> list[PostData, PostData]
This method allows you to obtain the list of all posts on the selected page

### > get_posts_from_page(self, nPage: int = None) -> list[PostData, PostData]
This method allows you to obtain the list of all posts by selecting a page

### > get_posts_form_pages(self, page: list[int, int]) -> dict[str:list[PostData, PostData]]
This method allows accessing different pages at same time

Example of usage:
```python
from Rule34 import Rule34

r34 = Rule34()
r34.set_page(["some tags"])

posts_pages = r34.get_posts_form_pages(range(0, 10))

print(posts_pages["page 1"]) # out: array with all posts of first page
```
### > get_posts_from_url(self, url: str) -> list[PostData, PostData] 
This method allows accessing pages with different tags without affecting the one currently being navigated

Example of usage:
```python
from Rule34 import Rule34

r34 = Rule34()
r34.setPage(["some tags"])

print(r34.link) # out: link of rule34 with some tags

otherPosts = r34.get_posts_from_url("generic rule34 link")

print(r34.link) # out: The same result as before executing get_posts_from_url().

```
### > get_post_from_url(self, url: str) -> PostData
This method allows you to retrieve multimedia information using the post link

### > get_post_from_id(self, id) -> PostData
This method allows you to retrieve multimedia information using the post ID

### > get_post_from_index(self, index: int) -> PostData
This method allows you to retrieve the multimedia information of a post on the selected page

Example of usage:
```python
from Rule34 import Rule34

r34 = Rule34()

r34.set_page(["some_tags", "some_tags", "some_tags", "some_tags"], 3) # the 3 is the page selector

print(r34.get_post_from_index(5)) # out the 5th post of page

```

## All attribute of PostData class:
* link -> str    <The link returned is not the link of the post, but of the multimedia content>
* type -> str    <Type of multimedia content>


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
MIT License

Copyright (c) 2023 Nubis

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
