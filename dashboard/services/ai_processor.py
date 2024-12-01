from langchain_community.llms import LlamaCpp
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from .data_processor import load_data_from_file
import pandas as pd
import os


def prepare_data_context():
    df = load_data_from_file()
    return {
        'total_devs': len(df['developer'].unique()),
        'total_tasks': len(df),
        'date_range': f"{df['Creada'].min():%Y-%m-%d} to {df['Creada'].max():%Y-%m-%d}",
        'avg_completion_time': df['time_to_complete'].mean(),
        'top_performers': df.groupby('developer')['story_points'].sum().nlargest(3).to_dict()
    }


def get_ai_response(question: str):
    try:
        context = prepare_data_context()
        llm = LlamaCpp(
            model_path="models/tinyllama.gguf",
            temperature=0.7,
            top_p=0.9,
            max_tokens=128,
            n_ctx=512,
            n_batch=1024,
            n_threads=8,
            f16_kv=True
        )

        template = """Analyze this data carefully:
        - Team Size: {total_devs} developers
        - Total Tasks: {total_tasks}
        - Time Period: {date_range}
        - Average Task Completion: {avg_completion_time:.2f} days
        - Performance Data: {top_performers}

        Based on story points completed, task completion time, and number of tasks, provide a data-driven answer to: {question}"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = LLMChain(llm=llm, prompt=prompt)
        return {'response': chain.run(question=question, **context)}
    except Exception as e:
        return {'error': str(e)}

