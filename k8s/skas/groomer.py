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

AUTH_WEBHOOK_URL = "auth_webhook_url"
AUTH_CERT_NAME = "auth_cert_name"
NAMESPACE = "namespace"
HELM_RELEASE_NAME = "helm_release_name"
HELM_VALUES = "helm_values"
USERS_HELM_RELEASE_name = "users_helm_release_name"
USERS_HELM_VALUES = "users_helm_values"
REPO_ID = "repo_id"
REPLICA_COUNT = "replica_count"
ENABLE_LOGIN_SERVICE = "enable_login_service"
CONTROL_PLANE = "control_plane"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], SKAS, {})
    setDefaultInMap(model[CLUSTER][K8S][SKAS], DISABLED, False)

    if model[CLUSTER][K8S][SKAS][DISABLED]:
        return False
    else:
        lookupRepository(model, None, "skas", model[CLUSTER][K8S][SKAS][REPO_ID])
        setDefaultInMap(model[CLUSTER][K8S][SKAS], AUTH_WEBHOOK_URL, "https://skas-auth.skas-system.svc/v1/tokenReview")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], AUTH_CERT_NAME, "skas-auth-cert")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], NAMESPACE, "skas-system")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], HELM_RELEASE_NAME, "skas")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], USERS_HELM_RELEASE_name, "skusers")
        setDefaultInMap(model[CLUSTER][K8S][SKAS], REPLICA_COUNT, 1)
        setDefaultInMap(model[CLUSTER][K8S][SKAS], ENABLE_LOGIN_SERVICE, False)
        setDefaultInMap(model[CLUSTER][K8S][SKAS], CONTROL_PLANE, False)
        return True
