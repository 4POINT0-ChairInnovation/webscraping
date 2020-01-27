import innovationPointers.innovationCount as innovCount
import logging
logging.basicConfig(filename='processData.log',format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.info('Start data processing')
logging.info('Start innovation variable counting')
innovCount.calInnovCount(0)
logging.info('End innovation variable counting')
# backlinkCount.calBackLinkCount()
# techStack.calTechStack()
logging.info('End data processing')