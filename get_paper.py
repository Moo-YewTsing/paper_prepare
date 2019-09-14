import os
import random
import re
import argparse
from io import BytesIO
import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from bs4 import BeautifulSoup
import requests

MAX = 10 ** 5
logger = logging.getLogger('Downloader')
logging.basicConfig(format='%(asctime)s: %(message)s')
logger.setLevel(logging.INFO)

def title_px(start=18, end=39):
    assert start < end, """end is larger than start\
 and match only one title font size is meaningless"""
    s_str = str(start)
    e_str = str(end)
    assert len(s_str) == 2 and len(e_str) == 2, "title's font-size is double-digit"
    heads = list(range(int(s_str[0]), int(e_str[0])+1))
    ends = []
    num_heads = len(heads)
    if num_heads > 1:
        for idx in range(num_heads):
            if idx == 0:
                if s_str[1] == "9":
                    ends.append("9")
                else:
                    ends.append("[{}-9]".format(s_str[1]))
            elif idx == num_heads - 1:
                if e_str[1] == "0":
                    ends.append("0")
                else:
                    ends.append("[0-{}]".format(e_str[1]))
            else:
                ends.append("[0-9]")
    else:
        ends.append("[{}-{}]".format(s_str[1], e_str[1]))
    return '|'.join((str(head)+end for head, end in zip(heads, ends)))

def download(url, ret):
    try:
        with open(ret, 'wb') as f_:
            rq = requests.get(url, stream=True)
            for chunk in rq.iter_content(chunk_size=1024):
                f_.write(chunk)
    except Exception as e:
        raise RuntimeError('{} download error for {}'.format(url, e))
    else:
        logger.info('{} download done'.format(url))

def convert_pdf(path, codec='utf-8'):
    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, caching=caching, check_extractable=True):
        interpreter.process_page(page)
    text = retstr.getvalue().decode()
    fp.close()
    device.close()
    retstr.close()
    return text

def clean_title(title:str):
    title = title.replace('\n', ' ')
    title = re.sub(r'[^\w\s]', '', title)
    return re.sub(r'\s+$', '', title)

def get_title(html, start, end):
    bs = BeautifulSoup(html, 'html.parser')
    title_size = title_px(start=start, end=end)
    title = bs.find('span', {'style':re.compile('font-size:{}px'.format(title_size))})
    return clean_title(title.get_text())

def is_url(path:str):
    return path.startswith('http')

# def get_latest(dir_p):
#     return max((os.path.join(dir_p, fn) for fn in os.listdir(dir_p)
#      if fn.endswith('pdf')), key=os.path.getctime)

def get_files(dir_p):
    return [os.path.join(item[0], fn) for item in os.walk(dir_p) for fn in item[2] if item[2]]

def save_html(html, name):
    with open('{}.html'.format(name), 'w', encoding='utf8') as test:
        test.write(html)

def change_name(f_p, start, end, test=False):
    try:
        html = convert_pdf(f_p)
        if test:
            save_html(html, os.path.basename(f_p[:-4]))
        title = get_title(html, start, end)
        if title == '':
            raise RuntimeError('{} title detection fail, try to change the "--size" parameter')
        else:
            f_n = "{}.pdf".format(title)
            os.rename(f_p, os.path.join(os.path.dirname(f_p), f_n))
    except Exception:
        logger.exception('%s convert error', f_p)

    else:
        logger.warning('%s has been renamed to %s', f_p, f_n)
    
def force_clean(f_p, source):
    try:
        os.remove(f_p)
    except FileNotFoundError:
        pass
    else:
        logger.warning('%s file has been cleaned. YOU MAY HAVE AREADAY DOWNLOADED THIS FILE',
                        source)

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="""Auto-download papers and rename it \
by title in pdf.""")
    argparser.add_argument('objs', nargs='+', help='the file path, dir path or url')
    argparser.add_argument('-d', '--dst', default='d:/papers', help="the dst path")
    argparser.add_argument('-s', '--size', nargs=2, default=[20, 39], 
    help="the range of title size")
    argparser.add_argument('-t', '--test', type=bool, default=False, 
    help="whether to output html file to see the title size, dst is this dir")
    command = argparser.parse_args()
    start = command.size[0]
    end = command.size[1]
    test = command.test
    for obj in command.objs:
        if is_url(obj):
            dst = command.dst
            os.makedirs(dst, exist_ok=True)
            try:
                ret = os.path.join(dst, f'temp{random.randint(0, MAX):05d}.pdf')
                download(obj, ret)
            except RuntimeError as download_e:
                logger.exception(download_e)
                continue
            else:
                change_name(ret, start, end, test=test)
                force_clean(ret, obj)

        elif os.path.isdir(obj):
            for f_p in filter(lambda x:x.endswith('.pdf'), get_files(obj)):
                change_name(f_p, start, end, test=test)
            
        elif os.path.isfile(obj):
            change_name(obj, start, end, test=test)