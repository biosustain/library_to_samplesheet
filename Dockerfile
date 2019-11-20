# Set the base image
#FROM genomicpariscentre/bcl2fastq2:latest
FROM moble/miniconda-centos@sha256:f203076a0d4660d93702b8ae13f13bf5ae0a697690e9ad623897ee260375b68c

# Only for testing
#ADD data /tmp/data
#ENV run_path /tmp/data/bcl2fastq/nextseq/151109_ML-P2-14_0029_AH00GGM_PoolR_TargetedRNA
#ENV sample_path /tmp/data/bcl2fastq/samples

# Copy entry script
COPY ./run_container.py /

# Install library_to_samplesheet
RUN conda install -y -c Freenome bcl2fastq
RUN conda install -y python=3.7.3
RUN cd /tmp && \
    git clone https://github.com/meono/library_to_samplesheet.git && \
    cd library_to_samplesheet && \
    git checkout v0.1.5 && \
    pip install -e .

CMD python run_container.py

