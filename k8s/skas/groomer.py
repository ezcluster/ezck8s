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
SKAS = "skas"
DISABLED = "disabled"

AUTH_WEBHOOK_URL = "authWebhookUrl"
AUTH_CERT_NAME = "authCertName"
NAMESPACE = "namespace"
HELM_RELEASE_NAME = "helmReleaseName"
HELM_VALUES = "helmValues"
USERS_HELM_RELEASE_name = "usersHelmReleaseName"
USERS_HELM_VALUES = "usersHelmValues"
REPO_ID = "repo_id"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], SKAS, {})
    setDefaultInMap(model[CLUSTER][K8S][SKAS], DISABLED, False)

    if model[CLUSTER][K8S][SKAS][DISABLED]:
        return False
    else:
        lookupRepository(model, None, "skas", model[CLUSTER][K8S][SKAS][REPO_ID])
        setDefaultInMap(model[CLUSTER][K8S][SKAS], AUTH_WEBHOOK_URL, "https://skas-auth.skas-system.svc:7014/v1/tokenReview")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], AUTH_CERT_NAME, "skas-auth-cert")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], NAMESPACE, "skas-system")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], HELM_RELEASE_NAME, "skas")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], USERS_HELM_RELEASE_name, "skusers")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], USERS_HELM_VALUES, "")
        return True
