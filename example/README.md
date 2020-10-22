# Validation in Nextflow pipelines
> Quickstart into implementing the validation into your nextflow pipelines.

## how-to
1) Copy all your existing simple input channels into a separate channel named "channel_name_validate". Remember to use ".set" instead of ".into" for multiple channels.
2) Set the input of a "validate_inputs" process as one giant flat channel, using the ".mix" operator. Each path item should be emitted individually.
3) Test to make sure you are getting the correct messages "File is valid" or errors per each file when running the script. It should be written in the command output, or your pipeline-run-name.log when running on the SLURM cluster.
4) Then copy any complex channels (like csv input channels), and flatten it accordingly. Mix it into the validate process.
5) Test again.
6) Repeat steps for any pipeline outputs!

If you have any question or bugs, feel free to reach out.
