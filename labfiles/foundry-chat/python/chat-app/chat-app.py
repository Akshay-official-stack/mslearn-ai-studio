import os
from dotenv import load_dotenv

# import namespaces
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# import namespaces for async
import asyncio
from openai import AsyncOpenAI



async def main(): 
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Get configuration settings 
        load_dotenv()
        azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")
        foundry_api_key = os.getenv("FOUNDRY_API_KEY")

        # Initialize the OpenAI client
        # Initialize the OpenAI client with default credential
        # token_provider = get_bearer_token_provider(
        #     DefaultAzureCredential(), "https://ai.azure.com/.default"
        # )

        # openai_client = OpenAI(
        #     base_url=azure_openai_endpoint,
        #     api_key=token_provider
        # )

        # Initialize the OpenAI client with key
        openai_client = OpenAI(
        api_key=foundry_api_key,
        base_url=azure_openai_endpoint,
        )
        
        # Initialize an async OpenAI client with key
        async_client = AsyncOpenAI(
        base_url=azure_openai_endpoint,
        api_key=foundry_api_key,
        )
        
        # Track responses
        last_response_id = None
        
        try:

            # Loop until the user wants to quit
            while True:
                input_text = input('\nEnter a prompt (or type "quit" to exit): ')
                if input_text.lower() == "quit":
                    break
                if len(input_text) == 0:
                    print("Please enter a prompt.")
                    continue
            
                try:
                    # Get a response from chat completions API
                    # completion = openai_client.chat.completions.create(
                    #     model=model_deployment,
                    #     messages=[
                    #         {
                    #             "role": "system",
                    #             "content": "You are a helpful AI assistant that answers questions and provides information."
                    #         },
                    #         {
                    #             "role": "user",
                    #             "content": input_text
                    #         }
                    #     ]
                    # )
                    # print(completion.choices[0].message.content)
                    
                    # Get a response from RESPOSNE API
                    # response = openai_client.responses.create(
                    #             model=model_deployment,
                    #             instructions="You are a helpful AI assistant that answers questions and provides information.",
                    #             input=input_text,
                    #             previous_response_id=last_response_id,
                    # )
                    # print(response.output_text)
                    # last_response_id = response.id
                    
                    # Await an asynchronous response from RESPONSE API
                    response = await async_client.responses.create(
                                model=model_deployment,
                                instructions="You are a helpful AI assistant that answers questions and provides information.",
                                input=input_text,
                                previous_response_id=last_response_id
                    )
                    assistant_text = response.output_text
                    print("Assistant:", assistant_text)
                    last_response_id = response.id
                            

                    # Get a Stream response from Response
                    # stream = openai_client.responses.create(
                    #             model=model_deployment,
                    #             instructions="You are a helpful AI assistant that answers questions and provides information.",
                    #             input=input_text,
                    #             previous_response_id=last_response_id,
                    #             stream=True
                    # )
                    # for event in stream:
                    #     if event.type == "response.output_text.delta":
                    #         print(event.delta, end="")
                    #     elif event.type == "response.completed":
                    #         last_response_id = event.response.id
                    # print()


                    # Await the asynchronous response from the OpenAI endpoint
                    response = await async_client.responses.create(
                            model=model_deployment,
                            instructions="You are a helpful AI assistant that answers questions and provides information.",
                            input=input_text,
                            previous_response_id=last_response_id
                    )

                    assistant_text = response.output_text
                    print(f"\nAssistant: {assistant_text}")
                    last_response_id = response.id

                except Exception as api_err:
                    print(f"API Error during call: {api_err}")

        finally:
        # Properly close the async HTTP connection pool when exiting
            await async_client.close()
    except Exception as ex:        
        print(ex)

if __name__ == '__main__':
    # asyncio.run() sets up the event loop, executes main(), and tears down the loop
    asyncio.run(main())

# if __name__ == '__main__': 
#     main()
