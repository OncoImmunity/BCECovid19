from typing import Tuple

from bce_covid19.utils.fasta import parse_fasta, save_fasta_file


def pre_proc(data_path: str, file_name, junk_name: str) -> Tuple[int, int, int]:
    """
    Main pre-process function.

    It will process a single fasta file and filter it in order to fit the Predictors running parameters.

    That is: At most 50 sequences and 300,000 amino acids per submission;
            each sequence not less than 10 and not more than 6000 amino acids.

    Args:
        data_path: the path to load raw data and save the pre-processed data.
        file_name: the raw file to process, should be fasta.
        junk_name: the name to give in common junks (will be suffixed)

    Returns: Tuple with the total parsed sequences, the total filtered ones and the total junks created.
            Also it saves junks of files in data_path with same name as file_name and suffix: "pre_proc_ID"
            where the ID varies on junks. Each of those junk should be separately given to the algorithm then in order
            to predict.

    """
    # define counters:
    tot_parsed_seq = 0  # the total parsed sequences so far
    tot_seq_filtered = 0  # the leftover sequences in the junks
    aa_per_junk = 0  # counter for the allowed AA per file junk. (max 300000)
    junk_id = 0  # ID for the saved junk files.
    # define junk data:
    junk_seq = list()

    # loop and filter and create junks.
    for record in parse_fasta(data_path=data_path, file_name=file_name):
        tot_parsed_seq += 1
        # take length of sequence:
        record_len = len(record)  # total AA.
        # check if it is in the thresholds
        if (record_len < 10) | (record_len > 6000):
            continue  # not passing the filters

        # check if to save the file based the totals allowed:
        if (len(junk_seq) == 50) | (aa_per_junk + record_len >= 300000):
            # save previous and recreate
            save_fasta_file(fasta_id=f"{junk_name}_pre_proc_{junk_id}", fasta_rec=junk_seq,
                            fasta_path=data_path)
            # new counter:
            junk_id += 1
            junk_seq = list()
            aa_per_junk = 0

        # save new record:
        junk_seq.append(record)
        aa_per_junk += record_len
        tot_seq_filtered += 1

    return tot_parsed_seq, tot_seq_filtered, junk_id+1
