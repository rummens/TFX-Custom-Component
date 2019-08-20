# Custom TFX Downstream Component

To customize an downstream component is quite simple:
1. choose the component you want to customize from the available [official component](https://github.com/tensorflow/tfx/tree/master/tfx/components)  
2. Copy its folder (containing component.py, executor.py etc.) to your dev environment
3. If you only want to change the behaviour of the component and don't
   need additional Executor Parameters to do so, just change the executor of 
   the Component:
   
   ```
   class <<YOUR COMPONENT>>(base_component.BaseComponent):
   
   ...
   
   EXECUTOR_CLASS = <<YOUR EXECUTOR>>
     ```
4. If you need more/different execution parameters, change the *ComponentSpec*
   and the *Component's init* function to reflect your needs. You can find an
   example [here](../Custom_Head_Component/assets/custom_head_component/component.py) 
   or [here](./assets/custom_upstream_component/component.py). 
   You should use the provided import function to abstract it from the 
   deployment target.
   
   Keep in mind that you you cannot delete any input/output parameters, as the down- and
   upstream components expect this interface, otherwise you have to change 
   these as well.  

5. Modify the Executor, keeping the input/output interface. You can find 
   an example below.

6. Integrate your new components into your pipeline, using the provided import
   function.  
  
  
  
## Example
The following [example](./custom_upstream_component_pipeline.py) creates an downstream 
component which replaced the Model Validator to integrate it with Slack. 
It was taken from the [official repo](https://github.com/tensorflow/tfx/tree/master/tfx/examples/custom_components/slack).

It was changed to fit our deployment strategy and follows the steps above.

It will most probably fail at some point if you don't provide a valid Slack token.
