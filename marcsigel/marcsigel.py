#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import argparse

from pymarc import MARCReader, Field

SIGEL_TAG = '935'
SIGEL_IND1 = ' '
SIGEL_IND2 = ' '
SIGEL_CODE = 'a'


def get_marc_record_id(marc_record):
    marc_record_id_list = marc_record.get_fields('001')
    if marc_record_id_list is not None and len(marc_record_id_list) == 1:
        return marc_record_id_list[0].data

    raise Exception("could not determine record id from MARC record")


def read_marc_collection(marc_collection_file_path):
    marc_collection = dict()
    with open(marc_collection_file_path, 'rb') as marc_collection_file:
        marc_reader = MARCReader(marc_collection_file)
        for marc_record in marc_reader:
            marc_record_id = get_marc_record_id(marc_record)
            marc_collection[marc_record_id] = marc_record

    return marc_collection


def add_sigel(marc_record, sigel):
    marc_record.add_field(
        Field(
            tag=SIGEL_TAG,
            indicators=[SIGEL_IND1, SIGEL_IND2],
            subfields=[
                SIGEL_CODE, sigel
            ]))

    return marc_record


def get_sigels(marc_record):
    sigel_field_candidates = marc_record.get_fields(SIGEL_TAG)
    if sigel_field_candidates is None or len(sigel_field_candidates) == 0:
        return None
    sigels = []
    for sigel_field_candidate in sigel_field_candidates:
        sigels_from_subfield = sigel_field_candidate.get_subfields(SIGEL_CODE)
        if sigels_from_subfield is not None and len(sigels_from_subfield) > 0:
            for sigel_from_subfield in sigels_from_subfield:
                sigels.append(sigel_from_subfield)
    if len(sigels) < 1:
        return None

    return sigels


def run():
    parser = argparse.ArgumentParser(prog='marcsigel',
                                     description='adds a Sigel to a given collection of binary MARC records (into MARC field 935 a; and optionally deduplicates this collection to another given collection)',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-sigel', type=str,
                                    help='the Sigel that should be added to the MARC records into MARC field 935 a',
                                    required=True)
    required_arguments.add_argument('-input-collection', type=str,
                                    help='an input file with binary MARC records, where the Sigel should be added into MARC field 935 a',
                                    required=True, dest='input_collection')
    required_arguments.add_argument('-output-collection', type=str,
                                    help='the output file with binary MARC records (incl. added Sigels and optionally deduplication against the other collection)',
                                    required=True, dest='output_collection')
    optional_arguments.add_argument('-another-collection', type=str,
                                    help='a file with binary MARC records that should be utilised for deduplication, i.e., the Sigel values from MARC field 935 a will be merged',
                                    dest='another_collection')

    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()

    sigel = args.sigel
    input_collection_file_path = args.input_collection
    output_collection_file_path = args.output_collection

    if args.another_collection is not None:
        another_collection = read_marc_collection(args.another_collection)
    else:
        another_collection = dict()

    dedup_records = set()
    sigel_count = 0
    overall_count = 0

    with open(input_collection_file_path, 'rb') as input_collection_file:
        input_collection_reader = MARCReader(input_collection_file)
        output_collection_file = open(output_collection_file_path, 'wb')
        for marc_record in input_collection_reader:
            marc_record_id = get_marc_record_id(marc_record)
            current_marc_record = marc_record
            if marc_record_id in another_collection:
                current_marc_record = another_collection[marc_record_id]
                dedup_records.add(marc_record_id)
            existing_sigels = get_sigels(current_marc_record)
            if existing_sigels is None or sigel not in existing_sigels:
                current_marc_record = add_sigel(current_marc_record, sigel)
                sigel_count += 1
            output_collection_file.write(current_marc_record.as_marc())
            overall_count += 1
        # write all records left from another collection
        for another_marc_record_id, another_marc_record in another_collection.items():
            if another_marc_record_id not in dedup_records:
                output_collection_file.write(another_marc_record.as_marc())
                overall_count += 1
        output_collection_file.close()

    print('wrote sigels to {:d} MARC record(s) and wrote {:d} MARC record(s) overall (incl. {:d} merged)'.format(
        sigel_count, overall_count, len(dedup_records)))


if __name__ == "__main__":
    run()
