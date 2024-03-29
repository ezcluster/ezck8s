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

from misc import setDefaultInMap, ERROR, resolveDns, resolveDnsAndCheck
import logging

logger = logging.getLogger("ezcluster.groomer")

CLUSTER = "cluster"
K8S = "k8s"
ARGOCD = "argocd"
DISABLED = "disabled"
LOAD_BALANCER_IP = "load_balancer_ip"
INGRESS_NGINX_HOST = "ingress_nginx_host"
INGRESS_NGINX = "ingress_nginx"
EXTERNAL_IP = "external_ip"
DATA="data"
LOCAL_DNS="local_dns"
OFFLINE="offline"
IMAGE_PREFIX="image_prefix"


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
    setDefaultInMap(model[CLUSTER][K8S], ARGOCD, {})
    setDefaultInMap(model[CLUSTER][K8S][ARGOCD], DISABLED, False)
    if model[CLUSTER][K8S][ARGOCD][DISABLED]:
        return False
    else:
        setDefaultInMap(model[CLUSTER][K8S][ARGOCD], OFFLINE, {})
        setDefaultInMap(model[CLUSTER][K8S][ARGOCD][OFFLINE], IMAGE_PREFIX, "")
        if LOAD_BALANCER_IP in model[CLUSTER][K8S][ARGOCD]:
            model[CLUSTER][K8S][ARGOCD][LOAD_BALANCER_IP] = resolveDnsAndCheckWithLocal(model, model[CLUSTER][K8S][ARGOCD][LOAD_BALANCER_IP])
        if INGRESS_NGINX_HOST in model[CLUSTER][K8S][ARGOCD]:
            if INGRESS_NGINX in model[CLUSTER][K8S] and EXTERNAL_IP in model[CLUSTER][K8S][INGRESS_NGINX]:
                argocd_ip = resolveDnsWithLocal(model, model[CLUSTER][K8S][ARGOCD][INGRESS_NGINX_HOST])
                if argocd_ip is not None:
                    ingress_ip = resolveDnsAndCheckWithLocal(model, model[CLUSTER][K8S][INGRESS_NGINX][EXTERNAL_IP])
                    if argocd_ip != ingress_ip:
                        ERROR("k8s.argocd: 'ingress_nginx_host' and 'ingress_nginx.external_ip' must resolve on same ip ({} != {})".format(argocd_ip, ingress_ip))
                else:
                    logger.warning("Unable to resolve '{}' for now. May be this DNS entry will be created later.".format(model[CLUSTER][K8S][ARGOCD][INGRESS_NGINX_HOST]))

        return True
