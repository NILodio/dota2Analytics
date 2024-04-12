# -*- coding: utf-8 -*-
import logging
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv
from open_dota import OpenDotaAPI


def save_data_name(data, output_filepath):
    """
    Save the data to a file.

    Args:
        data (pandas.DataFrame): Data to save.
        output_filepath (str): Filepath to save the data to.
    """
    data.to_csv(output_filepath, index=False)


@click.command()
@click.argument("output_filepath", type=click.Path())
@click.option("--num_matches", default=200, help="Number of matches to fetch.")
def main(output_filepath, num_matches=200):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("making final data set from raw data")
    data = OpenDotaAPI(output_filepath=output_filepath)
    matches_df = data.get_pro_matches(num_matches=num_matches)
    name = f"{output_filepath}/matches_{num_matches}.csv"
    save_data_name(matches_df, name)
    logger.info(f"Saved data to {name}")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
