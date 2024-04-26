from google.cloud import aiplatform
import os

def init_client(location):
    """Initialize and return the AI Platform client."""
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    return aiplatform.gapic.EndpointServiceClient(client_options=client_options)

def create_endpoint(client, project_id, location, display_name="My Model Endpoint", description="Endpoint for a model"):
    """Create a new endpoint for deploying models."""
    endpoint = {"display_name": display_name, "description": description}
    parent = f"projects/{project_id}/locations/{location}"
    print("Creating endpoint...")
    operation = client.create_endpoint(parent=parent, endpoint=endpoint)
    return operation.result()

def deploy_model_to_endpoint(client, endpoint_name, model_name):
    """Deploy a machine learning model to an existing endpoint."""
    deployed_model = {
        "model": model_name,
        "display_name": "Deployment of Model",
        "dedicated_resources": {
            "min_replica_count": 1,
            "max_replica_count": 1,
            "machine_spec": {"machine_type": "n1-standard-4"},
        },
    }
    print(f"Deploying model {model_name} to endpoint {endpoint_name}...")
    operation = client.deploy_model(endpoint=endpoint_name, deployed_model=deployed_model)
    return operation.result()

def main():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')

    client = init_client(location)
    created_endpoint = create_endpoint(client, project_id, location)
    print(f"Created Endpoint: {created_endpoint.name}")

    model_name = 'projects/{}/locations/{}/models/YOUR_MODEL_ID'.format(project_id, location)
    deployment_result = deploy_model_to_endpoint(client, created_endpoint.name, model_name)
    print(f"Deployment Result: {deployment_result}")

if __name__ == '__main__':
    main()
