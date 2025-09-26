from mlflow.deployments import get_deploy_client
from databricks.sdk import WorkspaceClient
from openai import OpenAI
import uuid


def _query_endpoint(
    endpoint_name: str, messages: list[dict[str, str]], user_access_token
) -> list[dict[str, str]]:
    """Calls a model serving endpoint."""
    client = OpenAI(
        api_key=user_access_token,
        base_url="https://dbc-8d504ecc-d614.cloud.databricks.com//serving-endpoints",
    )
    res = client.responses.create(model=endpoint_name, input=messages)
    return [{"role": res.output[0].role, "content": res.output[0].content[0].text}]


def query_endpoint(endpoint_name, messages, user_access_token):
    """
    Query a chat-completions or agent serving endpoint
    If querying an agent serving endpoint that returns multiple messages, this method
    returns the last message
    ."""
    return _query_endpoint(endpoint_name, messages, user_access_token)[-1]
