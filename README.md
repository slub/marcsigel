# marcsigel

marcsigel is a Python3 program that adds a Sigel to a given collection of binary MARC records (into MARC field 935 a; and optionally deduplicates this collection to another given collection)

## Requirements

* [argparse](https://docs.python.org/3/library/argparse.html#module-argparse)
* [pymarc](https://github.com/edsu/pymarc)

## Run

* clone this git repo or just download the [marcsigel.py](marcsigel/marcsigel.py) file
* run ./marcsigel.py
* for a hackish way to use marcsigel system-wide, copy to /usr/local/bin

### Install system-wide via pip

* via pip:
    ```
    sudo -H pip3 install --upgrade [ABSOLUTE PATH TO YOUR LOCAL GIT REPOSITORY OF MARCSIGEL]
    ```
    (which provides you ```marcsigel``` as a system-wide commandline command)

## Usage

    marcsigel [-h] -sigel SIGEL -input-collection INPUT_COLLECTION -output-collection OUTPUT_COLLECTION [-another-collection ANOTHER_COLLECTION]

required arguments:
  -sigel SIGEL                              the Sigel that should be added to the MARC records into MARC field 935 a (default: None)
  -input-collection INPUT_COLLECTION        an input file with binary MARC records, where the Sigel should be added into MARC field 935 a (default:None)
  -output-collection OUTPUT_COLLECTION      the output file with binary MARC records (incl. added Sigels and optionally deduplication against the other collection) (default: None)

optional arguments:
  -h, --help                                show this help message and exit
  -another-collection ANOTHER_COLLECTION    a file with binary MARC records that should be utilised for deduplication, i.e., the Sigel values from MARC field 935 a will be merged (default: None)

### Usage example

    marcsigel -sigel [SIGEL OF THE INPUT COLLECTION TO ADD] -input-collection [INPUT BINARY MARC RECORDS COLLECTION FILE] -output-collection [OUTPUT BINARY MARC RECORDS COLLECTION FILE WITH SIGELS]
