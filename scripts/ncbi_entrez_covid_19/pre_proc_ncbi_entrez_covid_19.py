"""
Pre-processing for NCBI ENTREZ COVID19

It will use the fasta file ncbi_entrez_covid_19.fa and process it in order to be able to run in the predictor.

This means some filtering and possibly junking the the file into smaller ones.

All of the files need to be run the predictor one by one.
"""
import logging
import os

from bce_covid19.pre_processing.preproc import pre_proc
from bce_covid19.utils.logging import create_logging_file
from bce_covid19 import paths

if __name__ == '__main__':
    # ----------
    # create logger file:
    # ----------
    logger_file_name = "ncbi_entrez_covid_19_pre_proc"
    create_logging_file(logger_file_name=logger_file_name, save_path=os.path.dirname(__file__))
    logger = logging.getLogger(__name__)
    logger.info("=================================================")
    logger.info("===== Pre-processing ncbi_entrez_covid_19 =======")
    logger.info("=================================================")
    # ----------
    # run the pre-processing:
    # ----------
    tot_parsed_seq, tot_seq_filtered, junk_id = pre_proc(data_path=paths.get_ncbi_entrez_covid_19_path(),
                                                         file_name="ncbi_entrez_covid_19.fa",
                                                         junk_name="ncbi_entrez_covid_19")
    logger.info(f"Total parsed sequences: {tot_parsed_seq}")
    logger.info(f"Total filtered sequences: {tot_seq_filtered}")
    logger.info(f"Total junks created: {junk_id}")
    logger.info("Done")
