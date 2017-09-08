cwlVersion: v1.0  # Which version of cwl should I use?
class: CommandLineTool       # Is it a cmdline tool?

baseCommand: irobotclient

hints:
  - class: DockerRequirement
    dockerPull: mercury/irobot-client:develop

inputs:

  - id: input_file
    type: string
    inputBinding:
      position: 1

  - id: output_dir
    type: string
    inputBinding:
      position: 2

  - id: irobot_url  # What about env vars?
    type: ["null", string]
    inputBinding:
      prefix: -u
      position: 3

  - id: arvados_token
    type: ["null", string]
    inputBinding:
      prefix: --arvados_token
      position: 4

  - id: basic_username
    type: ["null", string]
    inputBinding:
      prefix: --basic_username
      position: 5

  - id: basic_password
    type: ["null", string]
    inputBinding:
      prefix: --basic_password
      position: 6

  - id: force
    type: ["null", boolean]
    inputBinding:
      prefix: -f
      position: 7

  - id: no_index
    type: ["null", boolean]
    inputBinding:
      prefix: --no_index
      position: 8

outputs: []  # Empty? /TODO Return downloaded file to the users local area??????