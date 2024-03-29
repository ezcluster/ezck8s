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

from misc import setDefaultInMap, ERROR, resolveDnsAndCheck, lookupRepository
import ipaddress

CLUSTER = "cluster"
K8S = "k8s"
METALLB = "metallb"
DISABLED = "disabled"
EXTERNAL_IP_RANGES = "external_ip_ranges"
FIRST = "first"
LAST = "last"
DASHBOARD_IP = "dashboard_ip"
OFFLINE="offline"
IMAGE_PREFIX="image_prefix"
REPO_ID="repo_id"
DATA = "data"
LOCAL_DNS = "local_dns"
RELAX_PSP = "relax_psp"
PULL_SECRET_BY_PREFIX = "pull_secret_by_prefix"
DOCKERCONFIGJSON = "dockerconfigjson"

def resolveDnsAndCheckWithLocal(model, addr):
    if LOCAL_DNS in model[DATA] and addr in model[DATA][LOCAL_DNS]:
        return model[DATA][LOCAL_DNS][addr]
    else:
        return resolveDnsAndCheck(addr)


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], METALLB, {})
    setDefaultInMap(model[CLUSTER][K8S][METALLB], DISABLED, False)
    if model[CLUSTER][K8S][METALLB][DISABLED]:
        return False
    else:
        setDefaultInMap(model[DATA], K8S, {})
        setDefaultInMap(model[DATA][K8S], METALLB, {})
        setDefaultInMap(model[CLUSTER][K8S][METALLB], RELAX_PSP, False)
        setDefaultInMap(model[CLUSTER][K8S][METALLB], OFFLINE, {})
        setDefaultInMap(model[CLUSTER][K8S][METALLB][OFFLINE], IMAGE_PREFIX, "")

        lookupRepository(model, None, "metallb", model[CLUSTER][K8S][METALLB][REPO_ID])

        dashboard_ip = None  # Just to remove a warning
        dashboardInRange = False
        if DASHBOARD_IP in model[CLUSTER][K8S][METALLB]:
            model[CLUSTER][K8S][METALLB][DASHBOARD_IP] = resolveDnsAndCheckWithLocal(model, model[CLUSTER][K8S][METALLB][DASHBOARD_IP])
            dashboard_ip = ipaddress.ip_address(u"" + model[CLUSTER][K8S][METALLB][DASHBOARD_IP])
        for rangeip in model[CLUSTER][K8S][METALLB][EXTERNAL_IP_RANGES]:
            rangeip[FIRST] = resolveDnsAndCheckWithLocal(model, rangeip[FIRST])
            rangeip[LAST] = resolveDnsAndCheckWithLocal(model, rangeip[LAST])
            first_ip = ipaddress.ip_address(u"" + rangeip[FIRST])
            last_ip = ipaddress.ip_address(u"" + rangeip[LAST])
            if not last_ip > first_ip:
                ERROR("Invalid metallb.external_ip_range (first >= last)")
            if DASHBOARD_IP in model[CLUSTER][K8S][METALLB] and first_ip <= dashboard_ip <= last_ip:
                dashboardInRange = True
        if DASHBOARD_IP in model[CLUSTER][K8S][METALLB] and not dashboardInRange:
            ERROR("metallb.dashboard_ip is not included in one of metallb.external_ip_ranges")
        image_prefix = model[CLUSTER][K8S][METALLB][OFFLINE][IMAGE_PREFIX]
        if image_prefix != "" and image_prefix in model[DATA][K8S][PULL_SECRET_BY_PREFIX]:
            model[DATA][K8S][METALLB][DOCKERCONFIGJSON] = model[DATA][K8S][PULL_SECRET_BY_PREFIX][image_prefix]
        return True
