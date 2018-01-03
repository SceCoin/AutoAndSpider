import requests 
from bs4 import BeautifulSoup
import bs4
import codecs
#beautifulsoup的find可以一直一层一层的寻找下去

DOWNLOAD_URL = 'https://movie.douban.com/top250'

def download_page(url):
    headers = {
        'Host': 'movie.douban.com',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.content
    return data


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    #find和select的差异在于find返回的是bs4的Tag对象,select返回的是List
    # movie_list_soup = soup.find('ol', attrs={'class':'grid_view'})
    movie_list_soup = soup.select('ol[class="grid_view"]')[0]

    movie_list = []

    for li in movie_list_soup.find_all('li'):

        detail = li.find('div', attrs={'class':'hd'})  #获取head下的内容
        movie_name = detail.find('span', attrs={'class': 'title'}).string

        descore = li.find('div', attrs={'class':'bd'})
        score = descore.find('span', attrs={'class':'rating_num'}).string
        inq = descore.find('span', attrs={'class':'inq'}).string

        movie_list.append([movie_name,score,inq])

    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return movie_list,DOWNLOAD_URL + next_page['href']
    return movie_list, []


if __name__ == "__main__":
    url = DOWNLOAD_URL
    with codecs.open('movies.txt', 'wb', encoding='utf-8') as fp:  #codecs.open可以解决编码转换问题,防止写入成功.
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            for i in range(len(movies)):
                # print(movies[i][0])
                fp.write('{0}\t{1:<12}\t{2:<20}\n'.format(movies[i][1],movies[i][0],movies[i][2],chr(12288)))
    fp.close()
