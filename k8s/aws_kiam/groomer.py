# Copyright (C) 2021 BROADSoftware
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
KIAM = "kiam"
DISABLED = "disabled"
VERSION="version"
SERVER_REPLICAS="server_replicas"


def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], KIAM, {})
    setDefaultInMap(model[CLUSTER][K8S][KIAM], DISABLED, False)
    setDefaultInMap(model[CLUSTER][K8S][KIAM], VERSION, "v4.1")
    if model[CLUSTER][K8S][KIAM][DISABLED]:
        return False
    else:
        return True
