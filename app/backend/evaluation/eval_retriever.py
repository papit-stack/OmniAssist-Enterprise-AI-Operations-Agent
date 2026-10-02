from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from app.backend.evaluation.eval_dataset import test_cases
from deepeval.metrics import ContextualPrecisionMetric,ContextualRecallMetric
from app.backend.config import GEMINI_MODEL
from deepeval.models import GeminiModel,OpenAIModel,OllamaModel
import os
from app.backend.rag.retriever import use_retriever

# Local Ollama judge
judge_model = OllamaModel(
    model="llama3.2:3b",
    base_url="http://localhost:11434",
    temperature=0,
)


def build_test_cases():
    dataset=[]
    for test_case in test_cases:
        context,metadata=use_retriever(test_case['input'])
        retrieval_context = context.split("\n\n")
        test=LLMTestCase(
            input=test_case['input'],
            expected_output=test_case['expected_output'],
            retrieval_context=retrieval_context,
            # expected_retrieval_context=test_case['expected_retrieval_context']
        )
        dataset.append(test)
    return dataset

eval_model=GeminiModel(model=GEMINI_MODEL)

eval_model_precision = OpenAIModel(
    model="nvidia/nemotron-3.5-lightning:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0,
)

glm_model = OpenAIModel(
    model="zai-org/GLM-5.3-Flash",
    api_key=os.getenv("HF_TOKEN"),
    base_url="https://router.huggingface.co/v1",
    temperature=0,
)


recall_metrics=ContextualRecallMetric(model=eval_model,threshold=0.9,include_reason=True,async_mode=False)
precision_metrics=ContextualPrecisionMetric(model=eval_model,threshold=0.8,include_reason=True,async_mode=False)

def run_evaluation():
    dataset=build_test_cases()
    for i, test_case in enumerate(dataset):
        print(f"\nEvaluating test case {i + 1}/{len(dataset)}")

        evaluate(
            [test_case],
            metrics=[precision_metrics,recall_metrics]
        )


if __name__=="__main__":
    run_evaluation()