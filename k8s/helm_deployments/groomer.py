# Copyright (C) 2020 BROADSoftware
#
# This file is part of EzCluster
#
# EzCluster is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# EzCluster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with EzCluster.  If not, see <http://www.gnu.org/licenses/lgpl-3.0.html>.


from misc import setDefaultInMap

# from datetime import datetime

CLUSTER = "cluster"
K8S = "k8s"
HELM_DEPLOYMENTS = "helm_deployments"
NAME = "name"
DISABLED = "disabled"
_OPTIONS_ = "_options_"
VERSION = "version"
REPO = "repo"
VALUES = "values"
_VALUES_ = "_values_"
STATE = "state"
NAMESPACE = "namespace"
_VALUES_FILE_ = "_valuesFile_"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], HELM_DEPLOYMENTS, [])
    for deployment in model[CLUSTER][K8S][HELM_DEPLOYMENTS]:
        setDefaultInMap(deployment, DISABLED, False)
        if not deployment[DISABLED]:
            setDefaultInMap(deployment, VALUES, {})
            setDefaultInMap(deployment, STATE, "present")
            deployment[_OPTIONS_] = ""
            if VERSION in deployment and deployment[VERSION] != "":
                deployment[_OPTIONS_] += " --version {}".format(deployment[VERSION])
            if REPO in deployment and deployment[REPO] != "":
                deployment[_OPTIONS_] += " --repo {}".format(deployment[REPO])
            # As xxxx.value is forbidden in jinja2 templating.
            deployment[_VALUES_] = deployment[VALUES]
            del (deployment[VALUES])
            # deployment[_VALUES_FILE_] = "/tmp/helm_{}_{}.yaml".format(deployment[NAME], datetime.now().strftime("%Y%m%d_%H%M%S"))
            deployment[_VALUES_FILE_] = "/tmp/helm_{}.yaml".format(deployment[NAME])

    return True
