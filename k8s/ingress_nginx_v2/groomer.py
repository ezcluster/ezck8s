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

import logging
from misc import setDefaultInMap, ERROR, resolveDns, resolveDnsAndCheck, lookupRepository

logger = logging.getLogger("ezcluster.groomer")

CLUSTER = "cluster"
K8S = "k8s"
INGRESS_NGINX = "ingress_nginx"
DISABLED = "disabled"
EXTERNAL_IP = "external_ip"
ENABLE_SSL_PASSTHROUGH = "enable_ssl_passthrough"
DASHBOARD_HOST = "dashboard_host"
COMMAND_LINE_ARGUMENTS = "command_line_arguments"
OFFLINE = "offline"
IMAGE_PREFIX = "image_prefix"
REPO_ID = "repo_id"
PULL_SECRET_BY_PREFIX = "pull_secret_by_prefix"
DOCKERCONFIGJSON = "dockerconfigjson"


DATA="data"
LOCAL_DNS="local_dns"

def resolveDnsAndCheckWithLocal(model, addr):
    if LOCAL_DNS in model[DATA] and addr in model[DATA][LOCAL_DNS]:
        return model[DATA][LOCAL_DNS][addr]
    else:
        return resolveDnsAndCheck(addr)

def resolveDnsWithLocal(model, addr):
    if LOCAL_DNS in model[DATA] and addr in model[DATA][LOCAL_DNS]:
        return model[DATA][LOCAL_DNS][addr]
    else:
        return resolveDns(addr)

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], INGRESS_NGINX, {})
    setDefaultInMap(model[CLUSTER][K8S][INGRESS_NGINX], DISABLED, False)
    setDefaultInMap(model[CLUSTER][K8S][INGRESS_NGINX], ENABLE_SSL_PASSTHROUGH, False)
    if model[CLUSTER][K8S][INGRESS_NGINX][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][K8S][INGRESS_NGINX], OFFLINE, {})
        setDefaultInMap(model[CLUSTER][K8S][INGRESS_NGINX][OFFLINE], IMAGE_PREFIX, "")
        setDefaultInMap(model[DATA], K8S, {})
        setDefaultInMap(model[DATA][K8S], INGRESS_NGINX, {})

        lookupRepository(model, None, "ingress_nginx", model[CLUSTER][K8S][INGRESS_NGINX][REPO_ID])

        if EXTERNAL_IP in model[CLUSTER][K8S][INGRESS_NGINX]:
            model[CLUSTER][K8S][INGRESS_NGINX][EXTERNAL_IP] = resolveDnsAndCheckWithLocal(model, model[CLUSTER][K8S][INGRESS_NGINX][EXTERNAL_IP])
        if DASHBOARD_HOST in model[CLUSTER][K8S][INGRESS_NGINX]:
            dashboard_ip = resolveDnsWithLocal(model, model[CLUSTER][K8S][INGRESS_NGINX][DASHBOARD_HOST])
            if dashboard_ip is not None:
                if EXTERNAL_IP in model[CLUSTER][K8S][INGRESS_NGINX] and model[CLUSTER][K8S][INGRESS_NGINX][EXTERNAL_IP] != dashboard_ip:
                    ERROR("k8s.ingress_nginx: 'external_ip' and 'dashboard_host' must resolve on same ip ({} != {})".format(model[CLUSTER][K8S][INGRESS_NGINX][EXTERNAL_IP], dashboard_ip))
            else:
                logger.warning("Unable to resolve '{}' for now. May be this DNS entry will be created later.".format(model[CLUSTER][K8S][INGRESS_NGINX][DASHBOARD_HOST]))
            enableSslPassthrough = False
            if COMMAND_LINE_ARGUMENTS in model[CLUSTER][K8S][INGRESS_NGINX]:
                for cla in model[CLUSTER][K8S][INGRESS_NGINX][COMMAND_LINE_ARGUMENTS]:
                    if cla == "enable-ssl-passthrough":
                        enableSslPassthrough = True
            if not enableSslPassthrough:
                ERROR("k8s.ingress_nginx: Dashbaord access require '--enable-ssl-passthrough' command line argument to be defined")
        image_prefix = model[CLUSTER][K8S][INGRESS_NGINX][OFFLINE][IMAGE_PREFIX]
        if image_prefix != "" and image_prefix in model[DATA][K8S][PULL_SECRET_BY_PREFIX]:
            model[DATA][K8S][INGRESS_NGINX][DOCKERCONFIGJSON] = model[DATA][K8S][PULL_SECRET_BY_PREFIX][image_prefix]
        return True
