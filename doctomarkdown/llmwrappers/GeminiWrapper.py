class GeminiVisionWrapper:
    def __init__(self, model):
        self.model = model  # Instance of GeminiModel

    def generate_content(self, messages):
        """
        Accepts a list of messages like [{"text": "prompt"}, image]
        Returns the response as plain text.
        """
        response = self.model.generate_content(messages)
        return response