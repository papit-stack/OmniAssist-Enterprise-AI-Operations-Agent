from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    GEval,
)
from deepeval.test_case import LLMTestCaseParams
from deepeval.models import GeminiModel
from app.backend.evaluation.eval_dataset import test_cases
from app.backend.agents.agent import test_agent
from app.backend.config import GEMINI_MODEL
import json


# Evaluation model

eval_model = GeminiModel(
    model=GEMINI_MODEL
)

# Metrics
faithfulness_metric = FaithfulnessMetric(
    model=eval_model,
    threshold=0.85,
    include_reason=True,
    async_mode=False,
)

relevancy_metric = AnswerRelevancyMetric(
    model=eval_model,
    threshold=0.85,
    include_reason=True,
    async_mode=False,
)

correctness_metric = GEval(
    name="Answer Correctness",
    criteria="""
    The answer should contain the core information necessary to answer the
    user's question. Do not penalize the answer for omitting additional
    information from the expected answer if that information is not necessary
    to answer the user's specific question.

    """,
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model=eval_model,
    threshold=0.9
)



# Build generation test cases
def build_test_cases():

    dataset = []

    for idx,case in enumerate(test_cases):

        question = case["input"]
        result = test_agent(
            question=question,
            user_id=f"yohohooooo-{idx}",
        )

        dataset.append({
            "input": question,
            "actual_output": result['answer'][0]['text'],
            "expected_output": case["expected_output"],
            "retrieval_context": result["retrieval_context"],
            "tools_called": result["tools_called"],
        })

    with open("test_cases.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)


#run evaluation
def run_evaluation():
    with open("test_cases.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    # Convert dataset to DeepEval test cases
    for idx,case in enumerate(dataset):
        test_case = LLMTestCase(
            input=case["input"],
            actual_output=case["actual_output"],
            expected_output=case["expected_output"],
            retrieval_context=case["retrieval_context"],
        )
        print(f"\nEvaluating test case {idx + 1}/{len(dataset)}")
        evaluate([test_case],metrics=[relevancy_metric,faithfulness_metric,correctness_metric])
     




if __name__ == "__main__":
    run_evaluation()
