# Custom TFX components

## Disclaimer
This is not an official repo but an summary of this [dicussion](https://github.com/tensorflow/tfx/issues/322). 

## Anatomy of a Component
Each components consist of a Driver, Executor, Publisher. The driver and
publisher interact with the metadata store, while the Executor is the actual
entity that executes your code. Have a look the [official guide](https://www.tensorflow.org/tfx/guide) for a detailed 
explanation. 

## Concepts behind an Execution
- **Artifacts**: inputs / outputs of an execution. 
  The artifacts are things that are produced by upstream components and 
  consumed by downstream components. e.g. an example file, a model, etc
- **Execution properties**: other parameters that are used by an execution. 
  The impact of execution properties stay within the execution and is 
  used to describe / distinguish an execution.
- **Execution**: An execution takes input artifacts and process them based 
  on potential execution properties and produces output artifacts.
- **Channel**: Channel stands for a collection of Artifacts that share the 
  same Artifact type and (optional) other properties. Thus, any 
  TfxArtifact in a Channel should have the same type.
  
 
 You can think of an artifact as some kind of file. Your executor takes 
 the input file(s), makes some changes to it and then writes it back to the
 output file(s).
 
## Head Component vs. Upstream Component
A Head component is the first component in the pipeline, so it has to 
manually create the first artifact(s). All other upstream component only 
use the artifacts from its downstream components, so they don't have to 
create artifacts themselves since they have been created by their downstream
components


## Concepts in Code

- An artifact is represented as *TfxArtifact* (*tfx.utils.types*)
- A channel is represented as *Channel* (*tfx.utils.channel*)
- A Executor can be overloaded from a *BaseExecutor* (*tfx.components.base.base_executor*)
- A Component can be overloaded from a *BaseComponent* (*tfx.components.base.base_component*)
- Each Component expects a *ComponentSpec* (*tfx.components.base.base_component*)
  consisting of:
    - Inputs of type *Channel*
    - Execution Parameter of no specific type
    - Outputs of type *Channel*
    
Every *Channel* consist of one or more *TfxArtifact*. They all have to share
the same *type_name*. The name itself can be chosen freely. 

## Examples
There are two examples in this repo, one for a [head component](./Custom_Head_Component) , assuming 
your component is the first or only to run. The second one for an [upstream
component](./Custom_Upstream_Component) (in this case a modified version of the Model Validator)
