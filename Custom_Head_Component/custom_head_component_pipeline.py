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
from code2flow.code2flow import Code2Flow
from tfx.utils import channel
from tfx.utils.types import TfxArtifact

# <!---
# Don't remove this random comment with airflow and DAG in the file like this,
# since Airflow just uses a string search for the word airflow and DAG.
# ---!>
code2flow = Code2Flow(target=Code2Flow.LOCAL,
                      trigger_new_run=False,
                      pipeline_changed=True,
                      assets_changed=True,
                      pipeline_name="custom_head_component_pipeline",
                      root_directory_cluster=os.getenv("TFX_SRC_DIR", "/tfx-src"),
                      cluster_host="localhost:8080",
                      number_of_gpus=0  # keep in mind that you have to manually start enough GPU in the cluster
                      )

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

    return code2flow.create_pipeline(
        components=[
            my_first_awesome_component
        ],
        enable_cache=True,
        metadata_db_root=_metadata_db_root
    )


# Deploy
_ = code2flow.deploy(_create_pipeline())
