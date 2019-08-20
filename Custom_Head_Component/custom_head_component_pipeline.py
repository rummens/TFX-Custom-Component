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
"""Chicago taxi example using TFX."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
import os
from tfx.utils import channel
from tfx.utils.types import TfxArtifact

# <!---
# Don't remove this random comment with airflow and DAG in the file like this,
# since Airflow just uses a string search for the word airflow and DAG.
# ---!>
_pipeline_name = 'chicago_taxi_simple'

# This example assumes that the taxi data is stored in ~/taxi/data and the
# taxi utility function is in ~/taxi.  Feel free to customize this as needed.
_taxi_root = os.path.join(os.environ['HOME'], 'taxi')
_data_root = os.path.join(_taxi_root, 'data', 'simple')
# Python module file to inject customized logic into the TFX components. The
# Transform and Trainer both require user-defined functions to run successfully.
_module_file = os.path.join(_taxi_root, 'taxi_utils.py')
# Path which can be listened to by the model server.  Pusher will output the
# trained model here.
_serving_model_dir = os.path.join(_taxi_root, 'serving_model', _pipeline_name)

# Directory and data locations.  This example assumes all of the chicago taxi
# example code and metadata library is relative to $HOME, but you can store
# these files anywhere on your local filesystem.
_tfx_root = os.path.join(os.environ['HOME'], 'tfx')
_pipeline_root = os.path.join(_tfx_root, 'pipelines', _pipeline_name)
# Sqlite ML-metadata db path.
_metadata_path = os.path.join(_tfx_root, 'metadata', _pipeline_name,
                              'metadata.db')

# Airflow-specific configs; these will be passed directly to airflow
_airflow_config = {
    'schedule_interval': None,
    'start_date': datetime.datetime(2019, 1, 1),
}

# import the component (must happen this way because the path will change depending on deployment target).
# the component_name must be equal to the directory name holding the component file (component.py),
# but can be any string
custom_component = code2flow.import_custom_component(component_name="custom_upstream_component",
                                                     path_to_calling_file=__file__)

_taxi_root = code2flow.assets_root
_tfx_root = os.path.join(_taxi_root, 'tfx')
_data_root = os.path.join(_taxi_root, 'data')
_metadata_db_root = os.path.join(_tfx_root, 'metadata')


def _create_pipeline():
    """Implements an example pipeline with a custom head component"""

    input_artifact = TfxArtifact(type_name="RandomTypeNameForInput")
    input_artifact.uri = os.path.join(_data_root, "input_example.txt")

    input_channel = channel.Channel(artifacts=[input_artifact], type_name="RandomTypeNameForInput")

    my_first_awesome_component = custom_component.CustomHeadComponent(input_example=input_channel,
                                                                      string_execution_parameter="My awesome string",
                                                                      integer_execution_parameter=42)
  
    return pipeline.Pipeline(
      pipeline_name=pipeline_name,
      pipeline_root=pipeline_root,
      components=[
          my_first_awesome_component
      ],
      enable_cache=True,
      metadata_connection_config=metadata.sqlite_metadata_connection_config(
          metadata_path))
  
  


# Deploy
airflow_pipeline = AirflowDAGRunner(_airflow_config).run(
    _create_pipeline(
        pipeline_name=_pipeline_name,
        pipeline_root=_pipeline_root,
        data_root=_data_root,
        module_file=_module_file,
        serving_model_dir=_serving_model_dir,
        metadata_path=_metadata_path))
