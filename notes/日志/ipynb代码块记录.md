# 记录print结果，即系统输出
```
import sys
import logging

# 配置 logging，将日志写入文件
logging.basicConfig(filename='/home/wangbo/logging.out', level=logging.INFO, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 创建一个日志记录器
logger = logging.getLogger()

# 重定向标准输出到 logging
class StreamToLogger(object):
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message):
        # 将输出消息转换为日志记录
        if message.rstrip() != "":
            self.logger.log(self.level, message.rstrip())

    def flush(self):
        pass

# 将标准输出重定向到 logger
sys.stdout = StreamToLogger(logger, logging.INFO)

# 现在，所有 print 函数的输出都会被记录到日志文件中
print("This will be logged to the log file")
```