import multiprocessing
import nameAnalyze.findTeamPage as findTeamPage
import nameAnalyze.findNameOnPage as findTeamNames
import nameAnalyze.countNameOnWeb as countName
import logging

logging.basicConfig(filename='nameAnalyze.log', format='%(asctime)s %(message)s', level=logging.DEBUG)


def run_data_process(index):
    logging.info("nameAnalyze "+str(index)+" start")
    findTeamPage.findTeamPages(index)
    findTeamNames.explore_team_pages(index)
    countName.count_name_on_web(index)
    logging.info("nameAnalyze "+str(index)+" end")
    return


if __name__ == '__main__':
    jobs = []
    logging.info('Start multi nameAnalyze processing')
    for i in range(1):
        index = i
        p = multiprocessing.Process(target=run_data_process, args=(index,))
        jobs.append(p)
        p.start()