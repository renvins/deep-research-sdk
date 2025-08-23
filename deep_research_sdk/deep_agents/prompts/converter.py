def convert_to_llm_message(system_prompt: str, user_prompt: str | None = None):
    if not system_prompt:
        # raise error
        pass
    messages = [{"role": "system", "content": system_prompt}]
    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})
    return messages