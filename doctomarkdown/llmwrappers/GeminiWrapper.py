class GeminiVisionWrapper:
    def __init__(self, model):
        self.model = model  # Instance of GeminiModel

    async def generate_content_async(self, messages):
        import asyncio
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.model.generate_content(messages))
    
    def generate_content(self, messages):
        """
        Accepts a list of messages like [{"text": "prompt"}, image]
        Returns the response as plain text.
        """
        response = self.model.generate_content(messages)
        return response