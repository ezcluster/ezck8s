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
from misc import setDefaultInMap,lookupRepository


CLUSTER = "cluster"
DATA = "data"
K8S = "k8s"
DISABLED = "disabled"
SECRET_GENERATOR = "secret_generator"
REPO_ID = "repo_id"
NAMESPACE = "namespace"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], SECRET_GENERATOR, {})
    setDefaultInMap(model[CLUSTER][K8S][SECRET_GENERATOR], DISABLED, False)

    if model[CLUSTER][K8S][SECRET_GENERATOR][DISABLED]:
        return False
    else:
        lookupRepository(model, None, "secret_generator", model[CLUSTER][K8S][SECRET_GENERATOR][REPO_ID])
        setDefaultInMap(model[CLUSTER][K8S][SECRET_GENERATOR], NAMESPACE, "kube-tools")
        return True
