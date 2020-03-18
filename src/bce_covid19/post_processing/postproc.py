import os
import re

import numpy

from bce_covid19.utils.csv_handler import csv_reader, csv_writer
from bce_covid19.utils.fasta import parse_fasta


def post_proc(data_path: str, junk_prefix: str, post_file_name: str) -> None:
    """
    Use the predicted results in order to post process them in a better format.

    TOdo this can be refactored much better but I leave it like this for now.

    Args:
        data_path:   the path to load raw data and save the pre-processed data.
        junk_prefix: this is the file name, before the _predicted_id suffix. Used for both the pre_proc and the predicted
        post_file_name: the new file name to create as csv for all the sequences

    Returns: Nothing, creates a CSV file on the disc with suffix _post_proc.csv and post_file_name prefix.
    """
    # list the files:
    pre_proc_pattern = f"{junk_prefix}_pre_proc_"
    pre_proc_files = [f for f in os.listdir(data_path) if f.startswith(pre_proc_pattern)]
    predicted_pattern = f"{junk_prefix}_predicted_"
    predicted_files = [f for f in os.listdir(data_path) if f.startswith(predicted_pattern)]

    # sort files in correct order:
    pre_proc_idx = numpy.array([int(re.search(rf"{pre_proc_pattern}(.+).fasta", f).group(1)) for f in pre_proc_files])
    pre_proc_files = numpy.array(pre_proc_files)[numpy.argsort(pre_proc_idx)]

    predicted_idx = numpy.array(
        [int(re.search(rf"{predicted_pattern}(.+).csv", f).group(1)) for f in predicted_files])
    predicted_files = numpy.array(predicted_files)[numpy.argsort(predicted_idx)]

    if not numpy.array_equal(pre_proc_idx.sort(), predicted_idx.sort()):
        raise ValueError("The total files are not the same for the pre-proc and predicted")

    # create global CSV file to save into:
    post_csv = list()

    # loop through the junks together:
    for pre_proc_junk, predicted_junk in zip(pre_proc_files, predicted_files):

        # create dict with keys the fasta ids as presented in the predicted csv, and values the full fasta ids.
        fasta_desc_junk = {a.id.replace("|", "_"): a.description for a in
                           parse_fasta(data_path=data_path, file_name=pre_proc_junk)}

        # scan the csv file of the predictions
        # append dict of entry to list: this is per amino acid:
        for aa_entry in csv_reader(csv_path=os.path.join(data_path, predicted_junk), header_lines=0):
            post_csv.append({"Entry": fasta_desc_junk[aa_entry["Entry"]],
                             "Position": aa_entry["Position"],
                             "AminoAcid": aa_entry["AminoAcid"],
                             "EpitopeProbability": aa_entry["EpitopeProbability"]})

    # save the CSV:
    csv_writer(csv_path=os.path.join(data_path, f"{post_file_name}_post_proc.csv"),
               obj=post_csv, fieldnames=["Entry", "Position", "AminoAcid", "EpitopeProbability"])
