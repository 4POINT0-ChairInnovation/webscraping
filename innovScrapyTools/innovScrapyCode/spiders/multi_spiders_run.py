from scrapy.crawler import CrawlerProcess
from innovationScraping.innovScrapyTools.innovScrapyCode.spiders.customized_web_crawler import InnovSpider
from scrapy.utils.project import get_project_settings
import multiprocessing
import logging

def run_spider(index, settings):
    process = CrawlerProcess(settings)
    process.crawl(InnovSpider, fileIndex=index)

    logging.info("spider "+str(index)+" start")
    process.start()
    logging.info("spider "+str(index)+" end")
    return


if __name__ == '__main__':
    jobs = []
    settings = get_project_settings()
    logging.basicConfig(filename='NAICS01P.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
    logging.info('Start NAICS01P processing')

    for i in range(24):
        index = i
        settings['LOG_FILE'] = 'NAICS01P'+str(index)+'.log'
        p = multiprocessing.Process(target=run_spider, args=(index, settings))
        jobs.append(p)
        p.start()
