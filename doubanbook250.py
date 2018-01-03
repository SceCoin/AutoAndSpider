import requests 
from bs4 import BeautifulSoup
import codecs

URL = 'https://book.douban.com/top250'


#第一步: 用requests先获取网页内容
def getHTMLText(url):
    headers = {
        'Host': 'book.douban.com',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    try:
        r = requests.get(url, headers= headers)
        r.raise_for_status()
        data = r.text
        return data
    except:
        return 'fail'


#第二步: 获取后用beautifulSoup处理内容, 定位到需要的内容用List保存
def parse_html(html):

    soup = BeautifulSoup(html, 'html.parser')
    indent = soup.find('div', attrs={'class':'indent'})
    book_list = []

    for tr in indent.find_all('tr',attrs={'class':'item'}):
        bookdetail = tr.find('div', attrs={'class':'pl2'})
        bookname = bookdetail.find('a').getText()
        bookname = bookname.replace('\n','').replace(' ','')
        score = tr.find('div', attrs={'class':'star'}).find('span',attrs={'class':'rating_nums'}).string

        book_list.append([bookname,score])
    
    #翻页设置,在主函数里做循环
    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return book_list, next_page['href']
    return book_list, None



if __name__ == "__main__":
    url = URL

    with codecs.open('book.txt', 'wb', encoding='utf-8') as f:
        while url:
            html = getHTMLText(url)
            book, url = parse_html(html)
            for i in range(len(book)):
                f.write('{0}\t{1:<12}\n'.format(book[i][1],book[i][0]))
    f.close()