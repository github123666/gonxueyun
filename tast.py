import logging

logging.basicConfig(format='%(asctime)s %(name)s %(message)s', datefmt="%Y %m %d %I%M%S")
test = logging.getLogger("test")
try:
    raise Exception('test')
except Exception as e:
    test.info('tessssst', exc_info=True,stack_info=True)
url = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?reflow_source=reflow_page&a_bogus=64745b2b5bdc4e75b720a9a85b19867a&item_ids=7225261112281926947'
url2 = 'www.iesdouyin.com/aweme/v1/play/?ratio=1080p&line=0&video_id=v0d00fg10000ch2kgsrc77ubp2dt6510'