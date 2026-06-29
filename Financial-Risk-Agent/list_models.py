from uipath.platform import UiPath
import asyncio

async def list_models():
    uipath = UiPath()
    models = await uipath.agenthub.get_available_llm_models()
    for model in models:
        print(f"Model: {model.name}, Provider: {model.provider}")

if __name__ == "__main__":
    asyncio.run(list_models())
