from dotenv import load_dotenv
from mira_sdk import MiraClient, Flow
from mira_sdk.exceptions import FlowError
import os
import glob

# Load environment variables
load_dotenv()
client = MiraClient(config={"API_KEY": os.getenv("MIRA_API_KEY")})

def deploy_flows():
    # Get all YAML files in the flows directory
    flow_files = glob.glob("flows/*.yaml")

    for flow_file in flow_files:
        try:
            # Create flow from YAML file
            flow = Flow(source=flow_file)

            # Deploy to platform
            client.flow.deploy(flow)

            # Get flow name from filename
            flow_name = os.path.splitext(os.path.basename(flow_file))[0]
            flow_id = f"gautamch/{flow_name}"
            print(f"Flow deployed successfully with ID: {flow_id}")

        except FlowError as e:
            print(f"Error deploying flow {flow_file}: {str(e)}")
        except Exception as e:
            print(f"Unexpected error with {flow_file}: {str(e)}")

def test_flow(flow_id, emotion, theme=None):
    try:
        # Inputs for the Hindi song lyrics generator
        inputs = {"emotion": emotion}
        if theme:
            inputs["theme"] = theme

        # Execute the flow with inputs
        result = client.flow.execute(flow_id, inputs)
        return result
    except FlowError as e:
        print(f"Error running flow: {str(e)}")
        return None

def main():
    # Deploy the flow
    print("Deploying flow...")
    deploy_flows()

    # Test the Hindi song lyrics generator
    print("\nTesting Hindi song lyrics generator...")
    emotion = "pyaar"  # Love
    theme = "chand"    # Moon

    result = test_flow("gautamch/hindisong", emotion, theme)
    if result:
        print("\nGenerated Hindi Song Lyrics:")
        print(result)

if __name__ == "__main__":
    main()
