import multiprocessing
import innovationScraping.innovationPointers.innovationCount as innovCount
import logging

logging.basicConfig(filename='multiProcessData52.log', format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info('Start multi data processing')


def run_data_process(index):
    print("innovCount " + str(index) + " start")
    logging.info("innovCount "+str(index)+" start")
    innovCount.calInnovCount(index)
    logging.info("innovCount "+str(index)+" end")
    print("innovCount " + str(index) + " end")
    return


if __name__ == '__main__':
    jobs = []
    for i in range(24):
        index = i
        p = multiprocessing.Process(target=run_data_process, args=(index,))
        jobs.append(p)
        p.start()
