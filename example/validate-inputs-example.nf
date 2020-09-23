#!/usr/bin/env nextflow

// docker img def
def docker_image_main = "ubuntu:18.04"
def docker_image_validate_params = "blcdsdockerregistry/validate:1.0.0"

// create channels for each input file type
Channel
   .fromPath(params.reference_fasta)
   .into { input_ch_reference_fasta_validate; input_ch_reference_fasta } // copy into two channels, one for validation

Channel
   .fromPath(params.reference_fasta_dict)
   .into { input_ch_reference_dict_validate; input_ch_reference_dict }

Channel
   .fromPath(params.reference_fasta_index_files)
   .into { input_ch_reference_index_files_validate; input_ch_reference_index_files }

// input validation process
process validate_inputs {
    container docker_image_validate_params // docker img reference

    input:
    path(file_to_validate) from input_ch_reference_fasta_validate.mix(
      input_ch_reference_dict_validate,
      input_ch_reference_index_files_validate
    ) // combine and mix all input file channels into one channel

    output:
      val(true) into output_ch_validate_inputs

    script:
    """
    set -euo pipefail

    python -m validate -t file-input ${file_to_validate}
    """
}

// TODO: debug pre-process stop

// do pipeline stuff
process do_stuff  {
   container docker_image_main
   containerOptions "--volume ${params.temp_dir}:/temp_dir"

   publishDir path: params.output_dir, mode: 'copy'

   input: // add and structure any channels you need
      file(ref_fasta) from input_ch_reference_fasta
      file(ref_dict) from input_ch_reference_dict
      file(ref_idx_files) from input_ch_reference_index_files.collect()

   output:
      file("stuff.txt") into output_ch_stuff

   script:
   """
   echo "${ref_fasta.getName()}, ${ref_dict.getName()}" > stuff.txt
   """
}
