async def generate_images(prompt: str):
    """
    Generate images based on the provided prompt using Hugging Face API.
    """
    async def query(payload):
        try:
            response = requests.post(Api_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.content
        except requests.RequestException as e:
            print(f"Error querying API: {e}")
            return None

    Api_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {'Authorization': f'Bearer {YOUR_API_KEY}'}  # Replace with your API key

    async def generate_images_internal(prompt):
        tasks = []
        for _ in range(4):  # Generate 4 different images
            payload = {
                "inputs": f"{prompt}, quality=4k, sharpness+maximum, seed={randint(0, 1000000)}",
            }
            task = asyncio.create_task(query(payload))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        return results

    # Await the coroutine to execute its asynchronous tasks
    results = await generate_images_internal(prompt)
    for result in results:
        if result:
            open_image(prompt, result)

# Example usage
# if __name__ == "__main__":
#     prompt = input("Enter your prompt for image generation: ")
#     asyncio.run(generate_images(prompt))
