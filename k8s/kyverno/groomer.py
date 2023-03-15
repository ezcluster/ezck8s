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

import os
from misc import setDefaultInMap, lookupRepository


CLUSTER = "cluster"
DATA = "data"
K8S = "k8s"
KYVERNO = "kyverno"
DISABLED = "disabled"

NAMESPACE = "namespace"
POLICIES_HELM_VALUES = "policiesHelmValues"
REPO_ID = "repo_id"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], KYVERNO, {})
    setDefaultInMap(model[CLUSTER][K8S][KYVERNO], DISABLED, False)
    if model[CLUSTER][K8S][KYVERNO][DISABLED]:
        return False
    else:
        lookupRepository(model, None, "kyverno", model[CLUSTER][K8S][KYVERNO][REPO_ID])
        setDefaultInMap(model[CLUSTER][K8S][KYVERNO], NAMESPACE, "kyverno")
        setDefaultInMap(model[CLUSTER][K8S][KYVERNO], POLICIES_HELM_VALUES, "")
        return True
