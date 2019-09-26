# -*- coding: utf-8 -*-

"""Main module."""

from xml.etree import ElementTree
from library_to_samplesheet.adapters import adapters


def parse_run_parameters(file_path: str) -> list:
    """
    Takes file path to "RunParameters.xml and returns read length parameters
    required for samplesheet.
    :param file_path: file path to "RumParamters.xml".
    :return: list with header title and read lengths.
    """

    run_paramters = ElementTree.parse(file_path)
    read_lengts = list()
    for param in ['Setup/Read1', 'Setup/Read2']:
        if run_paramters.find(param):
            read_lengts.append(run_paramters.find(param).text)

    return ['[Reads]'] + read_lengts


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
    segments['[Header]'] = {param.split(',')[0]: param.split(',')[1]
                            for param in segments['[Header]']}

    return segments


def write_sample_sheet(file_path: str, run_paramters: dict, library: dict):
    """
    Generates sample sheet to be used with bcl2fastq.
    :param file_path: destination and name for the sample sheet.
    :param run_paramters: read lengths.
    :param library: details from library sheet.
    """

    with open(file_path, 'w') as file:
        # write read lengths
        file.writelines([param+'\n' for param in run_paramters])

        # write adapters
        library_prep_kit = library['[Header]']['LibraryPrepKit']
        settings = ['[Settings]\n'] + \
                   [f'{key},{value}\n'
                    for key, value in adapters[library_prep_kit].items()]
        file.writelines(settings)

        # adapt and write library data
        index = library['[Data]'][0].split(',').index('Index2Sequence')
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

        data = ['[Data]\n'] + \
               [library['[Data]'][0].replace('SampleID', 'Sample_ID')
                                    .replace('Name', 'Sample_Name')
                                    .replace('Well', 'Sample_Well')
                                    .replace('Index1Name', 'I7_Index_ID')
                                    .replace('Index1Sequence', 'index')
                                    .replace('Index2Name', 'I5_Index_ID')
                                    .replace('Index2Sequence', 'index2')
                                    .replace('Project', 'Sample_Project') +
                '\n'] + \
               [','.join(sample[0:index] +
                         ["".join(complement.get(base, base)
                                  for base in reversed(sample[9]))] +
                         sample[index+1:]) for sample in library['[Data]'][1:]]
        file.writelines(data)

    return


