from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    GEval,
)
from deepeval.test_case import LLMTestCaseParams
from deepeval.models import GeminiModel

from app.evaluation.eval_dataset import test_cases
from app.agents.graph import run_agent
from app.config import GEMINI_MODEL



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
    Evaluate whether the actual answer correctly answers the user's
    question according to the expected answer.

    The answer should:
    1. Be factually correct.
    2. Contain the important information required by the expected answer.
    3. Not contradict the expected answer.
    4. Directly answer the user's question.

    Give a high score when the actual answer is substantively correct
    even if the wording differs from the expected answer.
    """,
    evaluation_params=[
        LLMTestCaseParams.INPUT,
        LLMTestCaseParams.ACTUAL_OUTPUT,
        LLMTestCaseParams.EXPECTED_OUTPUT,
    ],
    model=eval_model,
)



# Build generation test cases


def build_test_cases():

    dataset = []

    for case in test_cases:

        question = case["input"]


        result = run_agent(
            question=question,
            user_id="user-10",
        )
        test_case = LLMTestCase(
            input=question,
            actual_output=result['answer'][0]['text'],
            expected_output=case["expected_output"],
            retrieval_context=result['retrieval_context'],
        )

        dataset.append(test_case)

    return dataset



# Run evaluation

def run_evaluation():

    dataset = build_test_cases()

    results = evaluate(
        test_cases=dataset,
        metrics=[
            faithfulness_metric,
            relevancy_metric,
            correctness_metric,
        ],
    )

    return results



if __name__ == "__main__":
    run_evaluation()
