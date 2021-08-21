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
AWS_K8S = "aws_k8s"
K8S = "k8s"
AWS = "aws"
EBS_CSI = "ebs_csi"
EBS_VOLUME_SCHEDULING = "volume_scheduling"
EBS_VOLUME_SNAPSHOT = "volume_snapshot"
EBS_VOLUME_RESIZING = "volume_resizing"
EBS_CONTROLER_REPLICAS = "controller_replicas"
EBS_PLUGIN_IMAGE_TAG = "plugin_image_tag"
DISABLED = "disabled"
DATA = "data"
ROLE_BY_NAME = "roleByName"
INSTANCE_ROLE_NAME = "instance_role_name"
EBS_CSI_ENABLED = "ebs_csi_enabled"
PERSISTENT_VOLUMES_ENABLED = "persistentVolumesEnabled"


def groom(_plugin, model):
    if K8S not in model[CLUSTER]:
        ERROR("'aws_k8s' plugin could not be used if no 'k8s' plugin")
    if AWS not in model[CLUSTER]:
        ERROR("'aws_k8s' plugin could not be used if no 'aws' plugin")
    setDefaultInMap(model[CLUSTER], AWS_K8S, {})
    if EBS_CSI in model[CLUSTER][AWS_K8S]:
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], DISABLED, False)
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], EBS_VOLUME_SCHEDULING, True)
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], EBS_VOLUME_SNAPSHOT, False)
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], EBS_VOLUME_RESIZING, False)
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], EBS_CONTROLER_REPLICAS, 1)
        setDefaultInMap(model[CLUSTER][AWS_K8S][EBS_CSI], EBS_PLUGIN_IMAGE_TAG, "latest")
        if model[CLUSTER][AWS_K8S][EBS_CSI][DISABLED]:
            del model[CLUSTER][AWS_K8S][AWS_K8S]
        else:
            model[DATA][K8S][PERSISTENT_VOLUMES_ENABLED] = True
            # Ensure we will have an instance role for all node allowed to use EBS CSI driver
            for roleName, role in model[DATA][ROLE_BY_NAME].items():
                setDefaultInMap(role[AWS], EBS_CSI_ENABLED, False)
                if role[AWS][EBS_CSI_ENABLED]:
                    if INSTANCE_ROLE_NAME not in role[AWS]:
                        ERROR("AWS instance role was not enabled for Role '{}' while 'ebs_csi_enabled' is set ! (Set also 'create_instance_role' switch)".format(roleName))
    return True
