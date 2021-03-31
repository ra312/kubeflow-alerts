import os

import kfp
import kubernetes as k8s
from kubernetes.client.models import V1EnvVar, V1ResourceRequirements, V1Volume, V1HostPathVolumeSource, V1SecretVolumeSource
from kcell_kfp_runners import HADOOP_VOLUMES
ALERT_IMAGE="artifactory.kraken.kcell.kz:6555/datalake-email-alert:latest"

@kfp.dsl.component
def send_run_status_email_(name, sender, recipient,  subject, body, args=[]):
    return kfp.dsl.ContainerOp(
        name=name,
        image=ALERT_IMAGE,
        pvolumes=HADOOP_VOLUMES,
        arguments=args,
        container_kwargs={
            "resources": k8s.V1ResourceRequirements(limits={"cpu": "1", "memory": "1Gi"}),
            "env": [
                k8s.V1EnvVar("SENDER", sender),
                k8s.V1EnvVar("RECIPIENT", recipient),
                k8s.V1EnvVar("TITLE", title),
                k8s.V1EnvVar("SUBJECT", subject),
                k8s.V1EnvVar("BODY", body)
            ]
        },
        file_outputs={
            "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json"
        }
    )
@kfp.dsl.component
def failure_on_purpose():
    return kfp.dsl.ContainerOp(
        name='fail-on-purpose',
        image="artifactory.kraken.kcell.kz:6555/alpine:latest",
        command=['ash', '-c', '''  exit 1''']
    )

