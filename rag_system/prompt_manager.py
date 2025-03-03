class PromptManager:
    def __init__(self, instructions: str):
        """
        Initialize with a set of instructions for the prompt.
        """
        self.instructions = instructions

    def create_prompt(self, context: str, query: str) -> str:
        """
        Create a full prompt using the provided context and user query.
        """
        prompt = (
            f"{self.instructions}\n\n"
            f"Context:\n{context}\n\n"
            f"Query:\n{query}\n\n"
            "Please provide a detailed answer referencing the context."
        )
        return prompt
