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

from misc import setDefaultInMap, ERROR, resolveDnsAndCheck
import ipaddress

CLUSTER = "cluster"
K8S = "k8s"
METALLB = "metallb"
DISABLED = "disabled"
EXTERNAL_IP_RANGES = "external_ip_ranges"
FIRST = "first"
LAST = "last"
DASHBOARD_IP = "dashboard_ip"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], METALLB, {})
    setDefaultInMap(model[CLUSTER][K8S][METALLB], DISABLED, False)
    if model[CLUSTER][K8S][METALLB][DISABLED]:
        return False
    else:
        dashboard_ip = None  # Just to remove a warning
        dashboardInRange = False
        if DASHBOARD_IP in model[CLUSTER][K8S][METALLB]:
            model[CLUSTER][K8S][METALLB][DASHBOARD_IP] = resolveDnsAndCheck(model[CLUSTER][K8S][METALLB][DASHBOARD_IP])
            dashboard_ip = ipaddress.ip_address(u"" + model[CLUSTER][K8S][METALLB][DASHBOARD_IP])
        for rangeip in model[CLUSTER][K8S][METALLB][EXTERNAL_IP_RANGES]:
            rangeip[FIRST] = resolveDnsAndCheck(rangeip[FIRST])
            rangeip[LAST] = resolveDnsAndCheck(rangeip[LAST])
            first_ip = ipaddress.ip_address(u"" + rangeip[FIRST])
            last_ip = ipaddress.ip_address(u"" + rangeip[LAST])
            if not last_ip > first_ip:
                ERROR("Invalid metallb.external_ip_range (first >= last)")
            if DASHBOARD_IP in model[CLUSTER][K8S][METALLB] and first_ip <= dashboard_ip <= last_ip:
                dashboardInRange = True
        if DASHBOARD_IP in model[CLUSTER][K8S][METALLB] and not dashboardInRange:
            ERROR("metallb.dashboard_ip is not included in one of metallb.external_ip_ranges")
        return True
