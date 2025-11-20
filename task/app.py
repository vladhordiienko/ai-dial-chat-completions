import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role

DEPLOYMENT_NAME = "gpt-4o"

async def start(custom: bool, stream: bool) -> None:
    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    # 1.2. Create CustomDialClient
    # 2. Create Conversation object
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    # 4. Use infinite cycle (while True) and get yser message from console
    # 5. If user message is `exit` then stop the loop
    # 6. Add user message to conversation history (role 'user')
    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
    # 8. Add generated message to history
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response

    if custom:
        client = CustomDialClient(DEPLOYMENT_NAME)
    else:
        client = DialClient(DEPLOYMENT_NAME)

    conversation = Conversation()

    sys_prompt = input("System prompt (empty for default): ").strip()

    if sys_prompt:
        conversation.add_message(Message(Role.SYSTEM, sys_prompt))
        print(sys_prompt)
    else:
        conversation.add_message(Message(Role.SYSTEM, DEFAULT_SYSTEM_PROMPT))
        print(DEFAULT_SYSTEM_PROMPT)
    print()

    print("Use on of these command 'exit' to quit or 'history' to show your history.")
    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            break
        elif user_input.lower() == "history":
            print(conversation.get_messages())
            continue

        conversation.add_message(Message(Role.USER, user_input))

        print("AI:")
        if stream:
            ai_message = await client.stream_completion(conversation.get_messages())
        else:
            ai_message = client.get_completion(conversation.get_messages())

        conversation.add_message(ai_message)


if __name__ == "__main__":
    asyncio.run(start(custom=False, stream=True))
