#!/usgs/apps/anaconda/bin/python

import sys
import logging
import argparse
import json


from sqlalchemy import *
from sqlalchemy.orm.util import *


from pds_pipelines.RedisQueue import *
from pds_pipelines.db import db_connect
from pds_pipelines.models.pds_models import Files
from pds_pipelines.config import pds_info_loc, pds_log_loc

class Args:
    def __init__(self):
        pass

    def parse_args(self):

        parser = argparse.ArgumentParser(description='PDS DI Data Integrity')

        parser.add_argument('--archive', '-a', dest="archive", required=True,
                          help="Enter archive - archive to ingest")

        parser.add_argument('--volume', '-v', dest="volume",
                          help="Enter voluem to Ingest")

        parser.add_argument('--search', '-s', dest="search",
                          help="Enter string to search for")

        args = parser.parse_args()

        self.archive = args.archive
        self.volume = args.volume
        self.search = args.search


def main():

#    pdb.set_trace()
    args = Args()
    args.parse_args()

    logger = logging.getLogger('Thumbnail_Queueing.' + args.archive)
    logger.setLevel(logging.INFO)
    logFileHandle = logging.FileHandler(pds_log_loc + 'Process.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s, %(message)s')
    logFileHandle.setFormatter(formatter)
    logger.addHandler(logFileHandle)

    logger.info('Starting Process')

    PDSinfoDICT = json.load(open(pds_info_loc, 'r'))
    archiveID = PDSinfoDICT[args.archive]['archiveid']

    RQ = RedisQueue('Thumbnail_ReadyQueue')

    try:
        session, _ = db_connect('pdsdi_dev')
        logger.info('Database Connection Success')
    except:
        logger.error('Database Connection Error')
    
    if args.volume:
        volstr = '%' + args.volume + '%'
        qOBJ = session.query(Files).filter(Files.archiveid == archiveID, 
                                                Files.filename.like(volstr), 
                                                Files.upc_required == 't')
    else:
        qOBJ = session.query(Files).filter(Files.archiveid == archiveID, 
                                             Files.upc_required == 't')
    if qOBJ:
        addcount = 0
        for element in qOBJ:
            fname = PDSinfoDICT[args.archive]['path'] + element.filename
            fid = element.fileid
            RQ.QueueAdd((fname, fid, args.archive))
            addcount = addcount + 1

        logger.info('Files Added to Thumbnail Queue: %s', addcount)

if __name__ == "__main__":
    sys.exit(main())
