# Set the base image
FROM genomicpariscentre/bcl2fastq2@sha256:50e6d0382a72e19ce9d3cf9091430499d39a89b15aefde4570dedbafcef2934c

# Only for testing
#ADD data /tmp/data
#ENV run_path /tmp/data/bcl2fastq/nextseq/151109_ML-P2-14_0029_AH00GGM_PoolR_TargetedRNA
#ENV sample_path /tmp/data/bcl2fastq/samples

# Copy entry script
COPY ./run_container.py /
# Install miniconda based on moble/miniconda-centos
RUN yum install -y wget bzip2 git curl grep sed dpkg gcc gcc-c++ && \
    mkdir -p /code && \
    echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm -f ~/miniconda.sh && \
    /opt/conda/bin/conda install -y -q -n root conda-build anaconda-client && \
    /opt/conda/bin/conda clean -y -a
ENV PATH /opt/conda/bin:$PATH
# Install library_to_samplesheet
RUN conda install -y python=3.7.3
RUN cd /tmp && \
    git clone https://github.com/meono/library_to_samplesheet.git && \
    cd library_to_samplesheet && \
    git checkout v0.1.6 && \
    pip install -e .

CMD python run_container.py

