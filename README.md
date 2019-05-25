# paper_prepare

## Prerequisite

1. downloader [aria2c](https://aria2.github.io/)

Make sure this downloader is in you PC environment.

2. python

Just Google what it is.

3. pdfminer

I you are in PRC, please check [here](https://mirrors.ustc.edu.cn/help/pypi.html) to have a better experience while using **pip**.

I recommand you set a new environment. But I know lots of people love mess. Only until they pay for it, they can understand the importance of tidiness.

No matter what, type the following:

    pip install pdfminer.six

4. beautifulsoup4

Type the following:

    pip install beautifulsoup4

## Usage

In the stript dir, in command lime interface, type:

    python yuyu.py [your papers, parer dirs or urls] [-d dst] [-s title_size_start title_size_end] [-t True|False]

Have fun!

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

- [x] Girlfriend asks
- [x] Girlfriend is unhappy
- [ ] Girlfriend tests
- [ ] Girlfriend's mood