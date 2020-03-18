"""
Post-processing for NCBI ENTREZ COVID19

It uses the predicted files that should end with predicted_ID.csv and the
pre-processed files that should end with pre_proc_ID.fasta to make a final csv file of all the information

"""
import logging
import os

from bce_covid19 import paths
from bce_covid19.post_processing.postproc import post_proc
from bce_covid19.utils.logging import create_logging_file

if __name__ == '__main__':
    # ----------
    # create logger file:
    # ----------
    logger_file_name = "ncbi_entrez_covid_19_post_proc"
    create_logging_file(logger_file_name=logger_file_name, save_path=os.path.dirname(__file__))
    logger = logging.getLogger(__name__)
    logger.info("=================================================")
    logger.info("===== Post-processing ncbi_entrez_covid_19 =======")
    logger.info("=================================================")
    # ----------
    # run the pre-processing:
    # ----------
    post_proc(data_path=paths.get_ncbi_entrez_covid_19_path(),
              junk_prefix="ncbi_entrez_covid_19",
              post_file_name="ncbi_entrez_covid_19")
    logger.info("Done")
