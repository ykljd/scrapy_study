# Scrapy settings for chanel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "chanel"

SPIDER_MODULES = ["chanel.spiders"]
NEWSPIDER_MODULE = "chanel.spiders"
COMMANDS_MODULE = 'chanel.mycmd'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   "chanel.middlewares.ChanelSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    # 'chanel.middlewares.ProxyMiddleware': 100,
    'chanel.middlewares.ChanelDownloaderMiddleware': 543,
    'chanel.middlewares.RandomHeaderMiddleWare': 543
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scrapy.pipelines.images.ImagesPipeline": 1,  # 确保启用 Scrapy 的 ImagesPipeline
    "chanel.pipelines.ChanelPipeline": 2,
    "chanel.pipelines.ChanelImagesPipeline": 3,  # 如果有自定义的图片处理管道
}

FILE_STORE = 'chanel/files'
IMAGE_STORE = 'chanel/images'

# 90 days of delay for files expiration
FILES_EXPIRES = 90

# 30 days of delay for images expiration
IMAGES_EXPIRES = 30

IMAGES_THUMBS = {
    'small': (50, 50),
    'big': (270, 270),
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

FEED_EXPORT_ENCODING = "utf-8"

# 启用日志记录
LOG_ENABLED = True

# 设置日志级别为 DEBUG，记录所有级别的日志信息
LOG_LEVEL = 'DEBUG'

# 将日志输出到文件 'scrapy.log'
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, 'scrapy.log')
LOG_FILE = log_file_path

# 将日志同时输出到标准输出（控制台）
LOG_STDOUT = True

# 定义日志的格式
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

# 定义日志的时间格式
LOG_DATEFORMAT = "%Y-%m-%d %H:%M:%S"

# 启用重试中间件
RETRY_ENABLED = True

# 最大重试次数
RETRY_TIMES = 5

# 重试延迟
RETRY_DELAY = 5

# 重试延迟的最大倍数
RETRY_MAX_DELAY = 30

# 设置 SSL/TLS 方法
DOWNLOADER_CLIENT_TLS_METHOD = 'TLSv1.2'

FEEDS = {
    'items.json': {
        'format': 'json',
        'encoding': 'utf8',
        'store_empty': False,
        'indent': 4,
    },
}


