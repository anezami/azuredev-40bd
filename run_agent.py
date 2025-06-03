from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="eastus.api.azureml.ms;6c6c7ade-1d43-4a86-8aca-fa189cf11c3c;aifoundrytests;agentstest")

agent = project_client.agents.get_agent("asst_3e9j31K0MXuHIMOLjVNyVU5q")

thread = project_client.agents.get_thread("thread_wCm0ZjDCKiXRmsg0g0DqFeFR")

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Hello Agent"
)

run = project_client.agents.create_and_process_run(
    thread_id=thread.id,
    agent_id=agent.id)
messages = project_client.agents.list_messages(thread_id=thread.id)

for text_message in messages.text_messages:
    print(text_message.as_dict())