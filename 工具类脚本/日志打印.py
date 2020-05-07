import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d][Level:%(levelname)s] %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S')

# logging.basicConfig(level=logging.DEBUG,
#                 format='%(asctime)s %(filename)s[line:%(lineno)d][Level:%(levelname)s] %(message)s',
#                 datefmt='%a, %d %b %Y %H:%M:%S',
#                 filename='test.log',
#                 filemode='w')
test = 123
logging.info(test)