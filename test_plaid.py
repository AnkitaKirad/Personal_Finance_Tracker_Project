import os
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid import Configuration, ApiClient
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Load keys from the env file
client_id = os.getenv("PLAID_CLIENT_ID")
secret = os.getenv("PLAID_SECRET")
plaid_env = os.getenv("PLAID_ENV", "sandbox")

# Step 1: Setup Plaid Configuration 
configuration = Configuration(
    host="https://sandbox.plaid.com",  # Using sandbox environment
    api_key={
        'clientId': client_id,
        'secret': secret,
    }
)

api_client = ApiClient(configuration)
#Setting up the client object for all the future endpoints call
client = plaid_api.PlaidApi(api_client)

# Step 2: Create a sandbox public token
request = SandboxPublicTokenCreateRequest(
    institution_id="ins_109508",  # Plaid Test Bank
    initial_products=[Products("transactions")],
    options={}
)

response = client.sandbox_public_token_create(request)
public_token = response['public_token']

print("Successfully generated sandbox public token:", public_token)
