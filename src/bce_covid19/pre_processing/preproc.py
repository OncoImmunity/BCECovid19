def pre_proc(data_path: str, file_name) -> None:
    """
    Main pre-process function.

    It will process a single fasta file and filter it in order to fit the Predictors running parameters.

    That is: At most 50 sequences and 300,000 amino acids per submission;
            each sequence not less than 10 and not more than 6000 amino acids.

    Args:
        data_path: the path to load raw data and save the pre-processed data.
        file_name: the raw file to process, should be fasta.

    Returns: Nothing, saves junks of files in data_path with same name as file_name and suffix: "pre_proc_ID"
            where the ID varies on junks. Each of those junk should be separately given to the algorithm then in order
            to predict.

    """
