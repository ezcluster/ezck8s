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

from misc import setDefaultInMap, ERROR

CLUSTER = "cluster"
K8S = "k8s"
CERT_MANAGER = "cert_manager"
DISABLED = "disabled"
CERT_MANAGER_ISSUER_BY_ID = "certManaagerIssuerById"
CONFIG = "config"
CERT_MANAGER_ISSUERS = "cert_manager_issuers"
DATA = "data"
NAME = "name"
ID = "id"
CLUSTER_ISSUERS = "cluster_issuers"


def groomIssuers(model):
    model[DATA][CERT_MANAGER_ISSUER_BY_ID] = {}
    if CERT_MANAGER_ISSUERS in model[CONFIG]:
        for issuer in model[CONFIG][CERT_MANAGER_ISSUERS]:
            if issuer[ID] in model[DATA][CERT_MANAGER_ISSUER_BY_ID]:
                ERROR("Cert_manager_issuer of id '{}' is defined twice in configuration file!".format(issuer[ID]))
            model[DATA][CERT_MANAGER_ISSUER_BY_ID][issuer[ID]] = issuer


def groom(_plugin, model):
    groomIssuers(model)
    setDefaultInMap(model[CLUSTER], K8S, {})
    setDefaultInMap(model[CLUSTER][K8S], CERT_MANAGER, {})
    setDefaultInMap(model[CLUSTER][K8S][CERT_MANAGER], DISABLED, False)
    if model[CLUSTER][K8S][CERT_MANAGER][DISABLED]:
        return False
    else:
        model[DATA][CLUSTER_ISSUERS] = []
        if CLUSTER_ISSUERS in model[CLUSTER][K8S][CERT_MANAGER]:
            for issuerDef in model[CLUSTER][K8S][CERT_MANAGER][CLUSTER_ISSUERS]:
                if issuerDef[ID] not in model[DATA][CERT_MANAGER_ISSUER_BY_ID]:
                    ERROR("Issuer of id '{}' is not defined in configuration file!".format(issuerDef[ID]))
                issuer = model[DATA][CERT_MANAGER_ISSUER_BY_ID][issuerDef[ID]]
                issuer[NAME] = issuerDef[NAME]
                model[DATA][CLUSTER_ISSUERS].append(issuer)
        return True
