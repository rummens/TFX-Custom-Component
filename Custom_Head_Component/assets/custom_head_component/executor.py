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
"""Example of a TFX custom executor integrating with slack.

This executor along with other custom component related code will only serve as
an example and will not be supported by TFX team.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
from typing import Any, Dict, List, Text
from tfx.components.base import base_executor
from tfx.utils import io_utils
from tfx.utils import types

# Default file name for stats generated.
_DEFAULT_FILE_NAME = 'output_example.txt'


class Executor(base_executor.BaseExecutor):
    """Executor for Slack component."""

    def Do(self, input_dict: Dict[Text, List[types.TfxArtifact]],
           output_dict: Dict[Text, List[types.TfxArtifact]],
           exec_properties: Dict[Text, Any]) -> None:
        """Get human review result on a model through Slack channel.

        Args:
          input_dict: Input dict from input key to a list of artifacts, including:
            - input_example: an example for an input

          output_dict: Output dict from key to a list of artifacts, including:
            - output_example: an example for an output
          exec_properties: A dict of execution properties, including:
            - string_parameter: An string execution parameter (only used in here, not persistent or shared up stream)
            - integer_parameter: An integer execution parameter (only used in here, not persistent or shared up stream)
            - input_config: not of concern here, only relevant for Driver
            - output_config: not of concern here, only relevant for Driver

        Returns:
          None
        """
        self._log_startup(input_dict, output_dict, exec_properties)

        # Fetch execution properties from exec_properties dict.
        string_parameter = exec_properties['string_execution_parameter']
        integer_parameter = exec_properties['integer_execution_parameter']

        # Fetch input URIs from input_dict.
        input_example_uri = types.get_single_uri(input_dict['input_example'])

        # Fetch output artifact from output_dict.
        output_example = types.get_single_instance(output_dict['output_example'])

        print("I AM RUNNING!")
        print(string_parameter)
        print(integer_parameter)
        print(input_example_uri)
        print(output_example)

        input_data = ""

        # load your input
        if tf.gfile.Exists(input_example_uri):
            with open(input_example_uri, "r") as file:
                input_data = file.read()

        # make some changes
        output_data = input_data + " changed by an awesome custom executor!"

        # update output uri for up stream components to know the filename
        output_example.uri = os.path.join(output_example.uri, _DEFAULT_FILE_NAME)

        # write the changes back to your output
        io_utils.write_string_file(output_example.uri, output_data)

        # you can also set custom properties to make checks in up stream components more quickly.
        # this is optional.
        output_example.set_string_custom_property('stringProperty', "Awesome")
        output_example.set_int_custom_property('intProperty', 42)


