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
AWS = "aws"
AWS_CSI = "aws_csi"
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
CONTROLLER_ON_CONTROL_PLANE="controller_on_control_plane"

def groom(_plugin, model):
    setDefaultInMap(model[CLUSTER], K8S, {})
    if AWS_CSI in model[CLUSTER][K8S]:
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], DISABLED, False)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], EBS_VOLUME_SCHEDULING, True)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], EBS_VOLUME_SNAPSHOT, False)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], EBS_VOLUME_RESIZING, False)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], CONTROLLER_ON_CONTROL_PLANE, True)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], EBS_CONTROLER_REPLICAS, 1)
        setDefaultInMap(model[CLUSTER][K8S][AWS_CSI], EBS_PLUGIN_IMAGE_TAG, "latest")
        if model[CLUSTER][K8S][AWS_CSI][DISABLED]:
            del model[CLUSTER][K8S][AWS_CSI]
        else:
            model[DATA][K8S][PERSISTENT_VOLUMES_ENABLED] = True
            # Ensure we will have an instance role for all node allowed to use EBS CSI driver
            for roleName, role in model[DATA][ROLE_BY_NAME].items():
                setDefaultInMap(role[AWS], EBS_CSI_ENABLED, False)
                if role[AWS][EBS_CSI_ENABLED]:
                    if INSTANCE_ROLE_NAME not in role[AWS]:
                        ERROR("AWS instance role was not enabled for Role '{}' while 'ebs_csi_enabled' is set ! (Set also 'create_instance_role' switch)".format(roleName))
    return True
