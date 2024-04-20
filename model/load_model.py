from google.cloud import aiplatform

def create_endpoint(project_id, location, model_resource_name):
    client = aiplatform.gapic.EndpointServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    endpoint = {
        "display_name": "example-endpoint",
        "description": "Endpoint for Gemini 1.5 Pro model",
    }
    operation = client.create_endpoint(parent=f"projects/{project_id}/locations/{location}", endpoint=endpoint)
    return operation.result()

def deploy_model_to_endpoint(model_name, endpoint_name):
    client = aiplatform.gapic.EndpointServiceClient(client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"})
    model = client.get_model(name=model_name)
    deployed_model = {
        "model": model.name,
        "display_name": "Deployment of Gemini 1.5 Pro",
        "dedicated_resources": {  # Define the machine resources
            "min_replica_count": 1,
            "max_replica_count": 1,
            "machine_spec": {
                "machine_type": "n1-standard-4",
            },
        },
    }
    operation = client.deploy_model(endpoint=endpoint_name, deployed_model=deployed_model)
    return operation.result()
