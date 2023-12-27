import asyncio
from lib.stability.api import StabilityAPI

async def test():
    client = StabilityAPI(api_key="sk-XXH02mCvlnEOwQf2noHRHd2gNprIlvkwBYNuG2iDQuyJW7RJ")
    print("Generating images...")
    images = ["A red ball, 3D render", "A blue ball, 3D render", "A green ball, 3D render"]
    coros = []
    print("Generated images:")
    for image in images:
        print("Generating prompt: " + image)
        coros.append(client.text_to_image(image))

    print("Waiting for images to generate...")
    await asyncio.gather(*coros)
    print("Images generated!")

asyncio.run(test())