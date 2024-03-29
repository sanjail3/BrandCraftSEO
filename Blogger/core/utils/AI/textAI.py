from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Clarifai
import os
import json
from langchain_core.output_parsers import StrOutputParser


class TextAI:
    def __init__(
        self,
        user_id="openai",
        app_id="chat-completion",
        model_id="GPT-3_5-turbo",
        model_version_id="4c0aec1853c24b4c83df8ba250f3b984",
    ):
        self.user_id = user_id
        self.app_id = app_id
        self.model_id = model_id
        self.model_version_id = model_version_id
        self.llm = Clarifai(
            user_id=self.user_id,
            app_id=self.app_id,
            model_id=self.model_id,
        )

    def predict(self, prompt_template, **kwargs):
        prompt = PromptTemplate(
            template=prompt_template["template"],
            input_variables=prompt_template["input_variables"],
        )
        input_variables = prompt_template["input_variables"]
        inputs = {}
        for variable in input_variables:
            inputs[variable] = kwargs[variable]

        print("Generating prediction")
        print("Prompt: " + prompt.template)
        try:
            params = dict(max_tokens=1024)
            chain = LLMChain(
                prompt=prompt,
                llm=self.llm,
                llm_kwargs={"inference_params": params},
                output_parser=StrOutputParser(),
            )
            blog_text = chain.invoke(inputs)
            blog_text = StrOutputParser().parse(text=blog_text["text"])
            return blog_text
        except Exception as e:
            print(e)
            raise Exception("Error occurred during prediction: " + str(e))


if __name__ == "__main__":
    from prompt.text_prompt import GENERATE_BLOG_FROM_BLOG
    from syntax.blog_syntax import HUGO
    import datetime
    from dotenv import load_dotenv

    load_dotenv()
    text_ai = TextAI()
    try:
        prediction = text_ai.predict(
            GENERATE_BLOG_FROM_BLOG,
            topic="How to write a blog post",
            syntax=HUGO,
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
        )
        print(prediction)
    except Exception as e:
        print("Error occurred: " + str(e))
