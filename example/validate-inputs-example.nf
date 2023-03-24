#!/usr/bin/env nextflow

// docker img def
def docker_image_main = "ubuntu:18.04"
def docker_image_validate_params = "ghcr.io/uclahs-cds/validate:4.0.0"

process validate_file {
    container docker_image_validate_params

    input:
        path(file_to_validate)

    output:
        val(true), emit: validation_success

    script:
    """
    validate ${file_to_validate}
    """
}

process do_something {
    container docker_image_main

    input:
        path(a_file)
        val(validation_successful)

    output:
        path("out.txt")

    script:
    """
    echo ${a_file.getName()} > out.txt
    """
}

workflow {
    input_channel = Channel.of('</path/to/input>')
    validate_file(input_channel)
    do_something(input_channel, validate_file.out.validation_success)
}
