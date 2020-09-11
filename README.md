
# library_to_samplesheet

A simple package to convert library sheets used for NextSeq runs to sample
 sheets suitable for bcl2fastq.

Contains a `Dockerfile` for bcl2fastq conversion and script (`run_container
.py`) for it's end-to-end operation in an ACI setup. Unfortunately, ACI is
 limited in its memory options and some runs fail conversion because of it.

 As an alternative, AVM is set up and a new

Not a general purpose process - meant to work only for our specific use case.



# Credits

This package was created with [Cookiecutter][Cookiecutter] and the [`audreyr/cookiecutter-pypackage`][audreyr/cookiecutter-pypackage] project template.

 [Cookiecutter]: https://github.com/audreyr/cookiecutter
 [audreyr/cookiecutter-pypackage]: https://github.com/audreyr/cookiecutter-pypackage

