# Paper Prep

## Prerequisite

1. Python

2. Pdfminer

I you are in PRC, please check [here](https://mirrors.ustc.edu.cn/help/pypi.html) to have a better experience while using **pip**.

I recommand you set a new environment. But I know lots of people love mess. Only until they pay for it, they can understand the importance of tidiness.

NEVERMIND, type the following:

    pip install pdfminer.six

3. Beautifulsoup4

Type the following:

    pip install beautifulsoup4

4. Downloader

Type the following:

    pip install requests

## Usage

In the stript dir, in command lime interface, type:

    python get_paper.py [your papers, parer dirs or urls] [-d dst] [-s title_size_start title_size_end] [-t True|False]

For example, to download this [paper](https://www.jmir.org/2005/1/e1/pdf) in your "D:\\" disk, the command line is

    python get_paper.py https://www.jmir.org/2005/1/e1/pdf -d D:\

P.S. The backlash is different in Windows and Linux. Here, it's in Window system.

**Have fun!**

More details:

``` python
argparser.add_argument('objs', nargs='+', help='the file path, dir path or url')
argparser.add_argument('-d', '--dst', default='d:/papers', help="the dst path")
argparser.add_argument('-s', '--size', nargs=2, default=[18, 39], 
help="the range of title size")
argparser.add_argument('-t', '--test', type=bool, default=False, 
help="whether to output html file to see the title size, dst is this dir")
```

## Development

- [x] Friend ask
- [ ] Friend test