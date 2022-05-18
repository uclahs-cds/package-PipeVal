#!/usr/bin/env nextflow

// docker img def
def docker_image_main = "ubuntu:18.04"
def docker_image_validate_params = "blcdsdockerregistry/validate:1.0.0"

// create channels for each input file type
Channel // complex input channel, reading from csv
   .fromPath(params.input_csv)
   .splitCsv(header:true)
   .map { row ->
      def read_group_name = "@RG" +
         "\\tID:" + row.read_group_identifier + ".Seq" + row.lane +
         "\\tCN:" + row.sequencing_center +
         "\\tLB:" + row.library_identifier +
         "\\tPL:" + row.platform_technology +
         "\\tPU:" + row.platform_unit +
         "\\tSM:" + row.sample

      return tuple(row.library_identifier,
         row.lane,
         read_group_name,
         row.read1_fastq,
         row.read2_fastq
      )
   }
   .into { input_ch_samples_validate; input_ch_samples } // copy into two channels, one for validation

input_ch_samples_validate // flatten tuples channel and return only file paths
   .flatMap { library, lane, read_group_name, read1_fastq, read2_fastq ->
      [read1_fastq, read2_fastq]
   }
   .set { input_ch_2_samples_validate } // send to new channel

Channel // simple input channel
   .fromPath(params.reference_fasta)
   .into { input_ch_reference_fasta_validate; input_ch_reference_fasta } // copy into two channels

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
    path(file_to_validate) from input_ch_2_samples_validate.mix(
      input_ch_reference_fasta_validate,
      input_ch_reference_dict_validate,
      input_ch_reference_index_files_validate
   ) // combine and mix all input file channels into one channel

    output:
      val(true) into output_ch_validate_inputs

    script:
    """
    set -euo pipefail

    validate -t file-input ${file_to_validate}
    """
}

// do pipeline stuff
process do_stuff  {
   container docker_image_main
   containerOptions "--volume ${params.temp_dir}:/temp_dir"

   publishDir path: params.output_dir, mode: 'copy'

   input: // add and structure any channels you need
      tuple(val(library),
         val(lane),
         val(read_group_name),
         path(read1_fastq),
         path(read2_fastq)
      ) from input_ch_samples
      each file(ref_fasta) from input_ch_reference_fasta
      each file(ref_dict) from input_ch_reference_dict
      file(ref_idx_files) from input_ch_reference_index_files.collect()

   output:
      file("stuff.txt") into output_ch_stuff

   script:
   """
   echo "${ref_fasta.getName()}, ${ref_dict.getName()}" > stuff.txt
   """
}
