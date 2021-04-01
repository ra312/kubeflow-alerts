import os
import kfp
from kubernetes.client.models import V1EnvVar, V1ResourceRequirements, V1Volume, V1HostPathVolumeSource, V1SecretVolumeSource

from kcell_kfp_runners import HADOOP_VOLUMES
ALERT_IMAGE="artifactory.kraken.kcell.kz:6555/datalake-email-alert:latest"
KUBEFLOW_IMAGE="artifactory.kraken.kcell.kz:6555/datalake-jupyterlab-kubeflow:latest"
@kfp.dsl.component
def send_run_status_email_(name, sender, recipient,  subject, body, attachment_path=None, args=[]):
    return kfp.dsl.ContainerOp(
        name=name,
        image=ALERT_IMAGE,
        pvolumes=HADOOP_VOLUMES,
        arguments=args,
        container_kwargs={
            "resources": V1ResourceRequirements(limits={"cpu": "1", "memory": "1Gi"}),
            "env": [
                V1EnvVar("SENDER", sender),
                V1EnvVar("RECIPIENT", recipient),
                V1EnvVar("SUBJECT", subject),
                V1EnvVar("BODY", body),
                V1EnvVar("ATTACHMENT_PATH", attachment_path)
            ]
        },
        file_outputs={
            "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json"
        }
    )
@kfp.dsl.component
def failure_on_purpose(name='failure_on_purpose'):
    return kfp.dsl.ContainerOp(
        name='fail-on-purpose',
        image="artifactory.kraken.kcell.kz:6555/alpine:latest",
        command=['ash', '-c', '''  exit 1''']
    )

@kfp.dsl.component
def check_oracle_partitions(name):
    return kfp.dsl.ContainerOp(
        name=name,
        image='artifactory.kraken.kcell.kz:6555/datalake-jupyterlab-kubeflow:latest',
        command=['run-python.sh'],
        arguments=[],
        pvolumes={
            '/etc/oracle-secret': V1Volume(
                name="oracle-secret",
                secret={
                    "secretName": 'oracle-secret'
                }
            ),
        },
        container_kwargs={
            'resources': V1ResourceRequirements(limits={'cpu': '1', 'memory': '1Gi'}),
            'env': [
                V1EnvVar('PACKAGE', "kcell-kubeflow-alerts"),
                V1EnvVar('VERSION', "1.3"),
                V1EnvVar('MODULE', "kcell_kfp_alerts")
            ]
        }
    )
