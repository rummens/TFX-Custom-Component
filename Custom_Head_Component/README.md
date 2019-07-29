# Custom TFX Head Component

This folder contains everything you need to create a custom head component.
The actual implantation of the component can be found [here](assets/custom_head_component)
and this [pipeline](custom_head_component_pipeline.py)
gives an example how to use it. 

## How to customize
Change the inputs/outputs in the [component](assets/custom_head_component/component.py), 
update both the ComponentSpec and the Component itself. 

To change the executor's behaviour modify the Do function of the 
[executor](assets/custom_head_component/executor.py)