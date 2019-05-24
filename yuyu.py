import os
import sys
import re
import argparse
import string
from io import BytesIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from bs4 import BeautifulSoup

def download(url, dst):
    try:
        os.system("aria2c {} -d {}".format(url, dst))
    except Exception as e:
        print('{} download error'.format(url))
        print(e)
        raise RuntimeError
    else:
        print('{} download done'.format(obj))

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

def get_title(html):
    bs = BeautifulSoup(html, 'html.parser')
    # with open('t.html', 'w', encoding='utf8') as test:
    #     test.write(str(html))
    title = bs.find('span', {'style':re.compile('font-size:1[8-9]|2[0-9]|3[0-1]px')})
    return clean_title(title.get_text())

def is_url(path:str):
    return path.startswith('http')

def get_latest(dir_p):
    return max((os.path.join(dir_p, fn) for fn in os.listdir(dir_p)
     if fn.endswith('pdf')), key=os.path.getctime)

def get_files(dir_p):
    return [os.path.join(item[0], fn) for item in os.walk(dir_p) for fn in item[2] if item[2]]

def change_name(f_p):
    try:
        html = convert_pdf(f_p)
        title = get_title(html)
        f_n = "{}.pdf".format(title)
        os.rename(f_p, os.path.join(os.path.dirname(f_p), f_n))
    except Exception as e:
        print('{} convert error'.format(f_p))
        print(e)
    else:
        print('{} rename done'.format(f_p))
    
if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="""Auto-download papers and rename it by title in pdf
. BTW, Yuyu, please be happy! ^_^""")
    argparser.add_argument('objs', nargs='+', help='the file path, dir path or url')
    argparser.add_argument('-d', '--dst', default='d:/papers', help="the dst path")
    command = argparser.parse_args()

    for obj in command.objs:
        if is_url(obj):
            dst = command.dst
            os.makedirs(dst, exist_ok=True)
            try:
                download(obj, dst)
            except RuntimeError:
                continue
            else:
                f_p = get_latest(dst)
                change_name(f_p)
        
        elif os.path.isdir(obj):
            for f_p in filter(lambda x:x.endswith('pdf'), get_files(obj)):
                change_name(f_p)
            
        elif os.path.isfile(obj):
            change_name(obj)