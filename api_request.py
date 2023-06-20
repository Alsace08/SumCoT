# -!- coding: utf-8 -!-
import openai


class Decoder:
    def __init__(self, api_key):
        self.api_key = api_key

    def decode(self, input, model, max_length):
        response = self.decoder_for_gpt3(model, input, max_length)
        return response

    def decoder_for_gpt3(self, model, input, max_length):
        openai.api_key = self.api_key

        if model == "gpt3":
            engine = "text-ada-001"
        elif model == "gpt3-medium":
            engine = "text-babbage-001"
        elif model == "gpt3-large":
            engine = "text-curie-001"
        elif model == "gpt3-xl":
            engine = "text-davinci-002"
        else:
            raise ValueError("model is not properly defined ...")

        response = openai.Completion.create(
            engine=engine,
            prompt=input,
            max_tokens=max_length,
            temperature=0,
            stop=None
        )

        return response["choices"][0]["text"]