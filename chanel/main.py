import asyncio
import platform
import logging
# from twisted.internet import asyncioreactor
from twisted.internet import reactor
import sys
import os
import signal
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from chanel.spiders.chanel_parse import ChanelParseSpider
from chanel.spiders.allchanel_parse import ChanelSpider
from scrapy.utils.project import get_project_settings

# from scrapy.crawler import execute

# 设置事件循环政策
# if platform.system() == 'Windows':
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# 检查是否已经安装了反应器
# if not reactor.running:
#     try:
#         asyncioreactor.install()
#     except Exception as e:
#         print(f"反应器安装失败: {e}")


def signal_handler(sig, frame):
    print('程序被 Ctrl+C 终止')
    reactor.callFromThread(reactor.stop)  # 确保在 Twisted 的主线程中停止 Reactor
    sys.exit(0)

# 设置信号处理函数
signal.signal(signal.SIGINT, signal_handler)

# 用来设置工程目录，有了它才可以让命令行生效
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
 
#os.path.abspath(__file__)  用来获取当前py文件的路径
#os.path.dirname()    用来获取文件的父亲的路径
 
# # #调用execute()函数执行scarpy的命令 scary crawl 爬虫文件名字
# execute(['scarpy','crawl','chanel_parse'])

# 获取项目设置
settings = get_project_settings()

# 配置日志
configure_logging(settings)


runner = CrawlerRunner(settings)

# @defer.inlineCallbacks
# def crawl():
#     breaker("开始爬取")
#     bug = runner.crawl(ChanelParseSpider)
#     reactor.close()
#     yield bug
runner.crawl(ChanelParseSpider)
# runner.crawl(ChanelSpider)


d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()
 # the script will block here until the crawling is finished

logging.info('all finished.')
    