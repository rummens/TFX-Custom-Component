# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example of a TFX custom component integrating with slack.

This component along with other custom component related code will only serve as
an example and will not be supported by TFX team.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tfx.components.base.base_component import ChannelParameter
from tfx.utils import channel
from tfx.utils import types
from typing import Optional, Text
from tfx.components.base import base_component
from tfx.components.base.base_component import ExecutionParameter
from tfx.components.example_gen import driver
from tfx.proto import example_gen_pb2
from tfx.components.example_gen import utils
from code2flow.code2flow import Code2Flow

# import custom executor (must be in same folder as component.py and named executor.py)
custom_executor = Code2Flow.import_custom_executor(path_to_calling_file=__file__)


class CustomHeadComponentSpec(base_component.ComponentSpec):
    """Example for a ComponentSpec of a Custom TFX Head Component."""

    COMPONENT_NAME = 'Custom_Head_Component'
    PARAMETERS = {
        'string_execution_parameter': ExecutionParameter(type=Text),
        'integer_execution_parameter': ExecutionParameter(type=int),

        # don't change these two:
        'input_config': ExecutionParameter(type=example_gen_pb2.Input),
        'output_config': ExecutionParameter(type=example_gen_pb2.Output)
    }
    INPUTS = {
        'input_example': ChannelParameter(type_name='RandomTypeNameForInput')
    }
    OUTPUTS = {
        'output_example': ChannelParameter(type_name='RandomTypeNameForOutput')
    }


class CustomHeadComponent(base_component.BaseComponent):
    """Custom TFX Head Component.

    This custom component serves as an example for a head component (i.e. being the first in the pipeline)
    """

    SPEC_CLASS = CustomHeadComponentSpec
    EXECUTOR_CLASS = custom_executor.Executor
    DRIVER_CLASS = driver.Driver

    def __init__(self,
                 input_example: channel.Channel,
                 string_execution_parameter: Text,
                 integer_execution_parameter: int,
                 output_example: Optional[channel.Channel] = None,

                 # don't change these three:
                 input_config: Optional[example_gen_pb2.Input] = None,
                 output_config: Optional[example_gen_pb2.Output] = None,
                 name: Optional[Text] = None):
        """Constructs a Head Component.

        Args:
          input_example: A Channel of 'RandomTypeNameForInput' type, (type can be any string, as long as it
            consistent in the channel, spec and artifacts)
          string_execution_parameter: An string execution parameter (only used in executor, not persistent or shared up stream)
          integer_execution_parameter: An integer execution parameter (only used in executor, not persistent or shared up stream)
          output_example: Optional output channel of 'RandomTypeNameForOutput' (type can be any string, as long as it
            consistent in the channel, spec and artifacts); will be created for you if not specified.
          input_config: An optional example_gen_pb2.Input instance, providing input
            configuration. If unset, the files under input_base (must set) will be
            treated as a single split.
          output_config: An optional example_gen_pb2.Output instance, providing
            output configuration. If unset, default splits will be 'train' and
        '   eval' with size 2:1.
          name: Optional unique name. Necessary if multiple Pusher components are
            declared in the same pipeline.
        """

        # Configure inputs and outputs (don't change).
        input_config = input_config or utils.make_default_input_config()
        output_config = output_config or utils.make_default_output_config(
            input_config)

        output_example = output_example or channel.Channel(
            type_name='RandomTypeNameForOutput',
            artifacts=[types.TfxArtifact('RandomTypeNameForOutput')])

        spec = CustomHeadComponentSpec(
            input_example=input_example,
            integer_execution_parameter=integer_execution_parameter,
            string_execution_parameter=string_execution_parameter,
            input_config=input_config,
            output_config=output_config,
            output_example=output_example)

        super(CustomHeadComponent, self).__init__(spec=spec, name=name)
