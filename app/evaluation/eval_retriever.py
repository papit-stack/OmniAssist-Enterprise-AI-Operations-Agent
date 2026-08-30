from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from app.evaluation.eval_dataset import test_cases
from deepeval.metrics import ContextualPrecisionMetric,ContextualRecallMetric
from app.config import GEMINI_MODEL
from deepeval.models import GeminiModel
from app.rag.retriever import use_retriever

def build_test_cases():
    dataset=[]
    for test_case in test_cases:
        context,metadata=use_retriever(test_case['input'])
        retrieval_context = context.split("\n\n")
        test=LLMTestCase(
            input=test_case['input'],
            expected_output=test_case['expected_output'],
            retrieval_context=retrieval_context,
            expected_retrieval_context=test_case['expected_retrieval_context']
        )
        dataset.append(test)
    return dataset

eval_model=GeminiModel(model=GEMINI_MODEL)
recall_metrics=ContextualRecallMetric(model=eval_model,threshold=0.85,include_reason=True,async_mode=False)
precision_metrics=ContextualPrecisionMetric(model=eval_model,threshold=0.85,include_reason=True,async_mode=False)

def run_evaluation():
    dataset=build_test_cases()
    evaluate(dataset,metrics=[recall_metrics,precision_metrics])

if __name__=="__main__":
    run_evaluation()