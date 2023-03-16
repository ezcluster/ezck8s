# Copyright (C) 2018 BROADSoftware
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

from misc import setDefaultInMap, appendPath, lookupHelper, ERROR, lookupRepository, lookupHttpProxy
import os

K8S = "k8s"
KUBESPRAY = "kubespray"
HELPERS = "helpers"
FOLDER = "folder"
DATA = "data"
ROLE_PATHS = "rolePaths"
CONFIG_FILE = "configFile"
CLUSTER = "cluster"
DISABLED = "disabled"
CLUSTER_NAME = "cluster_name"
K9S_REPO_ID = "k9s_repo_id"
HELM_REPO_ID = "helm_repo_id"
FILES_REPO_ID = "files_repo_id"
METRICS_SERVER = "metrics_server"
AUDIT = "audit"
POD_SECURITY_POLICIES = "pod_security_policies"
REPOSITORIES = "repositories"
DASHBOARD = "dashboard"
OFFLINE="offline"
DNS_DOMAIN="dns_domain"

PULL_SECRET_BY_PREFIX = "pull_secret_by_prefix"
IMAGE_PREFIX = "image_prefix"
DOCKERCONFIGJSON = "dockerconfigjson"
CONFIG = "config"

def groom(_plugin, model):
    setDefaultInMap(model[DATA], K8S, {})
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], KUBESPRAY, {})
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], DISABLED, False)
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], METRICS_SERVER, True)
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], AUDIT, False)
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], DASHBOARD, False)
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], OFFLINE, {})
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], POD_SECURITY_POLICIES, False)
    setDefaultInMap(model[CLUSTER][K8S][KUBESPRAY], DNS_DOMAIN, "cluster.local")

    if model[CLUSTER][K8S][KUBESPRAY][DISABLED]:
        return False
    else:
        setDefaultInMap(model[DATA], REPOSITORIES, {})  # As some templates expect this
        if 'docker_yum_repo_id' in model[CLUSTER][K8S][KUBESPRAY]:
            lookupRepository(model, None, "docker_yum", model[CLUSTER][K8S][KUBESPRAY]['docker_yum_repo_id'])
        if K9S_REPO_ID in model[CLUSTER][K8S][KUBESPRAY]:
            lookupRepository(model, "k9s", repoId=model[CLUSTER][K8S][KUBESPRAY][K9S_REPO_ID])
        if HELM_REPO_ID in model[CLUSTER][K8S][KUBESPRAY]:
            lookupRepository(model, "helm", repoId=model[CLUSTER][K8S][KUBESPRAY][HELM_REPO_ID])
        lookupHelper(model, KUBESPRAY, helperId=model[CLUSTER][K8S][KUBESPRAY]["helper_id"])
        lookupHttpProxy(model, model[CLUSTER][K8S][KUBESPRAY]["docker_proxy_id"] if "docker_proxy_id" in model[CLUSTER][K8S][KUBESPRAY] else None, "docker")
        lookupHttpProxy(model, model[CLUSTER][K8S][KUBESPRAY]["master_root_proxy_id"] if "master_root_proxy_id" in model[CLUSTER][K8S][KUBESPRAY] else None, "master_root")
        lookupHttpProxy(model, model[CLUSTER][K8S][KUBESPRAY]["yumproxy_id"] if "yum_proxy_id" in model[CLUSTER][K8S][KUBESPRAY] else None, "yum")
        model[DATA][ROLE_PATHS].add(appendPath(model[DATA][HELPERS][KUBESPRAY][FOLDER], "roles"))
        model[DATA]["dnsNbrDots"] = model[CLUSTER][K8S][KUBESPRAY][DNS_DOMAIN].count(".") + 1

        model[DATA][K8S][PULL_SECRET_BY_PREFIX] = {}
        for x in model[CONFIG][PULL_SECRET_BY_PREFIX]:
            model[DATA][K8S][PULL_SECRET_BY_PREFIX][x[IMAGE_PREFIX]] = x[DOCKERCONFIGJSON]

        return True
