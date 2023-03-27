import openai

recommender_prompt_wrapper = """Write some recommendations for things to do for the following national park: 
---
{input}
--- """

def set_openai_key(key):
    """Sets OpenAI key."""
    openai.api_key = key

class GeneralModel:
    def __init__(self):
        print("Model Intilization--->")
        # set_openai_key(API_KEY)

    def query(self, prompt, myKwargs={}):
        """
        wrapper for the API to save the prompt and the result
        """

        # arguments to send the API
        kwargs = {
            "engine": "text-davinci-002",
            "temperature": 0.85,
            "max_tokens": 600,
            "best_of": 1,
            "top_p": 1,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "stop": ["###"],
        }


        for kwarg in myKwargs:
            kwargs[kwarg] = myKwargs[kwarg]


        r = openai.Completion.create(prompt=prompt, **kwargs)["choices"][0][
            "text"
        ].strip()
        return r

    def model_prediction(self, input, api_key):
        """
        wrapper for the API to save the prompt and the result
        """
        # Setting the OpenAI API key got from the OpenAI dashboard
        set_openai_key(api_key)
        output = self.query(recommender_prompt_wrapper.format(input = input))
        return output