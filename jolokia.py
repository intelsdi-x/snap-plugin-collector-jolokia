#!/usr/bin/env python

# http://www.apache.org/licenses/LICENSE-2.0.txt
#
# Copyright 2016 Intel Corporation
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

import urllib.request as urlrq
import json
import time
import logging
import snap_plugin.v1 as snap

LOG = logging.getLogger(__name__)
BASIC_TYPES = (int, bytes, float, str, bool)


class Jolokia(snap.Collector):

    def get_config_policy(self):
        return snap.ConfigPolicy(
            [
                "jolokia",
                [
                    (
                        "jolokia_host_path",
                        snap.StringRule(required=True)
                    )
                ]
            ]
        )

    def update_catalog(self, config):
        metrics = []
        path = config["jolokia_host_path"]

        response = json.loads(urlrq.urlopen(path).read().decode("utf-8"))
        for lib in response["value"]:  # ex. java.lang
            types = response["value"][lib]
            for typ in types:  # ex. type=Threading
                if "name=" not in typ and "attr" in types[typ]:
                    for att in types[typ]["attr"]:  # ex. ThreadCount
                        text = typ + "/" + att
                        text = text.replace("/", "|")
                        metric = snap.Metric(
                            namespace=[
                                snap.NamespaceElement(value="intel"),
                                snap.NamespaceElement(value="jolokia"),
                                snap.NamespaceElement(value=lib),
                                snap.NamespaceElement(value=text)
                            ],
                            version=1,
                            tags={},
                            Description="Jolokia metric {}.".format(text),
                        )
                        metrics.append(metric)
        return metrics

    @staticmethod
    def _get_data(metric):
        fullpath = (metric.config["app_endpoint"] + "/" +
                    metric.namespace[2].value + ":" + metric.namespace[3].value)
        fullpath = fullpath.replace("|", "/")

        response = json.loads((urlrq.urlopen(fullpath).read()).decode('utf-8'))

        if "value" in response and isinstance(response["value"], BASIC_TYPES):
            return response["value"]
        else:
            if "value" in response:
                LOG.info("Failed to read:" + fullpath +
                         "| returned value was incorrect type:" +
                         str(type(response["value"])))
            else:
                LOG.info("Failed to read:" + fullpath +
                         "| there was no \"value\" field in response")
            return "failedToReadValue"

    def collect(self, metrics):

        for metric in metrics:
            metric.data = Jolokia._get_data(metric)
            metric.timestamp = time.time()
        return metrics

if __name__ == "__main__":
    Jolokia("jolokia", 1).start_plugin()
