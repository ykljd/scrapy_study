import os
from scrapy.commands import ScrapyCommand
from scrapy.utils.conf import arglist_to_dict
from scrapy.utils.python import without_none_values
from scrapy.exceptions import UsageError

# 自定义命令类，继承自 ScrapyCommand
class Command(ScrapyCommand):

    # 表示该命令需要在 Scrapy 项目中运行
    requires_project = True

    # 定义命令的语法格式
    def syntax(self):
        return "[options] <spider>"

    # 定义命令的简短描述
    def short_desc(self):
        return "Run a spider"

    # 添加命令行选项
    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)
        # 添加 -a 选项，用于传递参数给爬虫
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")
        # 添加 -o 选项，用于指定输出文件
        parser.add_option("-o", "--output", metavar="FILE",
                          help="dump scraped items into FILE (use - for stdout)")
        # 添加 -t 选项，用于指定输出格式
        parser.add_option("-t", "--output-format", metavar="FORMAT",
                          help="format to use for dumping items with -o")

    # 处理命令行选项
    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)
        try:
            # 将 -a 参数转换为字典
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            # 如果参数格式错误，抛出 UsageError
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)
        # 如果指定了输出文件
        if opts.output:
            # 如果输出文件为 '-'，则输出到标准输出
            if opts.output == '-':
                self.settings.set('FEED_URI', 'stdout:', priority='cmdline')
            else:
                # 否则，设置 FEED_URI 为指定的文件路径
                self.settings.set('FEED_URI', opts.output, priority='cmdline')
            # 获取所有可用的 Feed 导出器
            feed_exporters = without_none_values(
                self.settings.getwithbase('FEED_EXPORTERS'))
            # 获取所有有效的输出格式
            valid_output_formats = feed_exporters.keys()
            # 如果未指定输出格式，则根据文件扩展名推断
            if not opts.output_format:
                opts.output_format = os.path.splitext(opts.output)[1].replace(".", "")
            # 如果指定的输出格式无效，抛出 UsageError
            if opts.output_format not in valid_output_formats:
                raise UsageError("Unrecognized output format '%s', set one"
                                 " using the '-t' switch or as a file extension"
                                 " from the supported list %s" % (opts.output_format,
                                                                  tuple(valid_output_formats)))
            # 设置 FEED_FORMAT 为指定的输出格式
            self.settings.set('FEED_FORMAT', opts.output_format, priority='cmdline')

    # 运行命令
    def run(self, args, opts):
        # 获取所有可用的爬虫名称
        spd_loader_list = self.crawler_process.spider_loader.list()
        # 遍历所有爬虫名称或命令行参数中的爬虫名称
        for spname in spd_loader_list or args:
            # 启动爬虫，并传递参数
            self.crawler_process.crawl(spname, **opts.spargs)
            # 打印当前启动的爬虫名称
            print("此时启动的爬虫：" + spname)
        # 启动爬虫进程
        self.crawler_process.start()