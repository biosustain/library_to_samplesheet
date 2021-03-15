# -*- coding: utf-8 -*-

"""Main module."""

from xml.etree import ElementTree
from library_to_samplesheet.adapters import adapters
from click import BadParameter


def parse_run_parameters(file_path: str) -> list:
    """
    Takes file path to "RunParameters.xml and returns read length parameters
    required for samplesheet.
    :param file_path: file path to "RumParamters.xml".
    :return: list with header title and read lengths.
    """

    run_parameters = ElementTree.parse(file_path)
    read_lengths = list()
    for param in ['Setup/Read1', 'Setup/Read2']:
        if run_parameters.find(param) is not None:
            read_lengths.append(run_parameters.find(param).text)

    # check if read lengths are collected, fail if not.
    if len(read_lengths) == 0:
        raise BadParameter('RunParamter.xml does not contain expected read '
                           'length branch.')

    return ['[Reads]'] + read_lengths


def parse_library_sheet(file_path: str) -> dict:
    """
    Takes file path for library sheet and returns header/data parameters
    required for samplesheet.
    :param file_path: file path to library sheet.
    :return: dictionary with header (as keys) and parameters (as values).
    """

    # read and segment the library sheet (header and data segnments will be
    # used.
    with open(file_path, 'r') as file:
        segments = dict()
        for line in file.readlines():
            line = line.rstrip().rstrip(',')
            if line == '':
                continue
            elif line.startswith('['):  # I'll assume all files start with '['
                segment_title = line
                segments[segment_title] = list()
            else:
                segments[segment_title].append(line)

    # put header segment in dictionary
    segments['[Header]'] = {param.split(',')[0]:
                                (param.split(',')[1] if ',' in param else '')
                            for param in segments['[Header]']}

    return segments


def write_sample_sheet(file_path: str, run_parameters: list, library: dict):
    """
    Generates sample sheet to be used with bcl2fastq.
    :param file_path: destination and name for the sample sheet.
    :param run_paramters: read lengths.
    :param library: details from library sheet.
    """

    with open(file_path, 'w') as file:
        # write read lengths
        file.writelines([param + '\n' for param in run_parameters])

        # write adapters
        library_prep_kit = library['[Header]']['LibraryPrepKit']
        settings = ['[Settings]\n'] + \
                   [f'{key},{value}\n'
                    for key, value in adapters[library_prep_kit].items()]
        file.writelines(settings)

        # adapt and write library data
        index = library['[Data]'][0].split(',').index('Index2Sequence')

        data = ['[Data]\n'] + \
               [adjust_data_header(library['[Data]'][0], library_prep_kit) + '\n'] + \
               [adjust_sample(sample, index, library_prep_kit) + '\n'
                for sample in library['[Data]'][1:]]
        file.writelines(data)

    return


def adjust_data_header(header: str, library_prep_kit: str) -> str:
    """
    Returns data header with adjusted column names.
    :param header: data header string
    :param library_prep_kit: library type used to determine which headers to use
    :return: adjusted data header string
    """
    replacements = {'SampleID': 'Sample_ID',
                    'Name': 'Sample_Name',
                    'Well': 'Sample_Well',
                    'Index1Name': 'I7_Index_ID',
                    'Index1Sequence': 'index',
                    'Index2Name': 'I5_Index_ID',
                    'Index2Sequence': 'index2',
                    'Project': 'Sample_Project'
                    }
    if library_prep_kit == 'plexWell_i7_only':
        return ','.join([replacements[col] if col in replacements else col
                         for col in header.split(',')
                         if col not in ['Index2Name', 'Index2Sequence']])
    else:
        return ','.join([replacements[col] if col in replacements else col
                           for col in header.split(',')])



def adjust_sample(sample: str, index: int, library_prep_kit: str) -> str:
    """
    Takes in a sample line from library sheet anc adjust for use in samplesheet.
    :param sample: sample line from library sheet
    :param index: list index for Index2Sequence
    :param library_prep_kit: library type used to determine which indexes to use
    :return: sample line suitable for samplesheet
    """

    sample = sample.split(',')
    if library_prep_kit == 'plexWell_i7_only':
        return ','.join(sample[0:index-1])
    else:
        return ','.join(sample[0:index] +
                        [reverse_complement(sample[index])] +
                        sample[index + 1:])


def reverse_complement(sequence: str) -> str:
    """
    A simple function that returns a reverse complement of a given DNA (ATGC)
    sequence.
    :param sequence: all capital DNA sequence as string
    :return: reverse complemented sequence
    """
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join([complement.get(base, base) for base in reversed(sequence)])
