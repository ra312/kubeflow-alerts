FROM artifactory.kraken.kcell.kz:6555/datalake-email-alert:latest

RUN pip install --user kcell-kubeflow-alerts --extra-index-url https://artifactory.kcell.kz:6555/api/pypi/getindata-pypi/simple

COPY entrypoint.ash /opt/

CMD ['/entrypoint.ash']
