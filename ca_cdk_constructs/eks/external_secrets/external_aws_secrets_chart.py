from cdk8s import Chart
from constructs import Construct

from ca_cdk_constructs.eks.imports.io.external_secrets import SecretStoreSpecProviderAwsService
from ca_cdk_constructs.eks.external_secrets.external_secrets_aws_secret_store import (
    ExternalSecretsAwsSecretStore,
)
from ca_cdk_constructs.eks.external_secrets.external_secret import ExternalSecret
from ca_cdk_constructs.eks.external_secrets import ExternalSecretSource


class ExternalAwsSecretsChart(Chart):
    """
    cdk8s_lib chart for deploying ExternalSecrets from AWS SecretsManager or ParameterStore.
    The chart deploys a SecretStore object of the specified type (AWS SSM or ParameterStore)
    and one or more external secrets linked to the store.
    The chart assumes that access to the secrets is managed by an existing `ServiceAccount`.

    The secret types ( set in `~secret_sources~` ) must match the store type e.g setting `~secret_service~` to `SecretStoreSpecProviderAwsService.SECRETS_MANAGER`
    requires a list of `~ExternalSecretSource~`s where each `ExternalSecretSource` references an AWS SSM secret.

    To use secrets from both AWS SSM and Parameter store,
    deploy two instances of the chart, setting `~secret_service~` to the relevant value
    and passing a list of compatible secret sources.
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        service_account_name: str,
        region: str,
        secret_sources: list[ExternalSecretSource],
        secret_service: SecretStoreSpecProviderAwsService = SecretStoreSpecProviderAwsService.SECRETS_MANAGER,
        disable_resource_name_hashes: bool = False,
        labels: dict[str, str] = {},
        namespace: str = "",
    ):
        """
        Args:
            scope (Construct): _description_
            id (str): _description_
            service_account_name (str): the name of the `ServiceAccount` used by the `SecretStore` to access AWS secret services
            region (str): AWS region
            secret_sources (list[ExternalSecretSource]):  The secret sources to generate k8s secrets for
            secret_service (SecretStoreSpecProviderAwsService, optional): The service type which defines where to fetch the secrets_from. Defaults to SecretStoreSpecProviderAwsService.SECRETS_MANAGER.
            disable_resource_name_hashes: The autogenerated resource name by default is suffixed with a stable hash of the construct path. Setting this property to true drops the hash suffix. Default: false
            labels: Labels to apply to all resources in this chart. Default: - no common labels
            namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        """
        labels.setdefault("app.kubernetes.io/managed-by", "aws-cdk")
        labels.setdefault("app.kubernetes.io/component", "external-secrets")

        super().__init__(
            scope,
            id,
            disable_resource_name_hashes=disable_resource_name_hashes,
            labels=labels,
            namespace=namespace,
        )

        self._k8s_secret_names = [s.k8s_secret_name for s in secret_sources]

        store = ExternalSecretsAwsSecretStore(
            self,
            "SecretStore",
            region=region,
            service_account_name=service_account_name,
            secret_service=secret_service,
        )

        for secret_spec in secret_sources:
            ExternalSecret(
                self,
                f"{secret_spec.k8s_secret_name}-external-secret",
                secret_source=secret_spec,
                store_name=store.name,
            )

    @property
    def k8s_secret_names(self) -> list[str]:
        return self._k8s_secret_names
