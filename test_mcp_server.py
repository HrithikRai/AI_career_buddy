from mcp import ClientSession
from mcp.client.sse import sse_client

async def run():
    async with sse_client(url="http://localhost:8000/sse") as streams:
        async with ClientSession(*streams) as session:

            await session.initialize()
            tools = await session.list_tools()
            resources = await session.list_resource_templates()
            prompts = await session.list_prompts()
            print(tools)
            print(resources)
            print(prompts)
            
            response = await session.call_tool("career_advice", arguments={"user_details":"user loves graphic design"})
            print(response.content[0].text)
            # tool calling
            # action = await session.call_tool("add", arguments={"a":1,"b":2})
            # resource = await session.read_resource("career_advice://hrithik's_details")
            # prompt = await session.get_prompt(
            #    "beautify", arguments={"message":"roadmap"}
            # )
            # print(action.content[0].text)
            # print(resource.contents[0].text)
            # print(prompt.contents[0].text)
      
if __name__ == "__main__":
    import asyncio
    asyncio.run(run())