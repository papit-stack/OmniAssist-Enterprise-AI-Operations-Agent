from deepeval.metrics import ToolCorrectnessMetric,ArgumentCorrectnessMetric
from deepeval.test_case import LLMTestCase,ToolCall
from deepeval import evaluate,assert_test
from app.evaluation.tool_eval_dataset import TOOL_EVAL_CASES
from app.agents.graph import run_agent
from deepeval.models import GeminiModel
from app.config import GEMINI_MODEL

eval_model=GeminiModel(model=GEMINI_MODEL)
tool_correctness_metrics=ToolCorrectnessMetric(model=eval_model,include_reason=True,threshold=0.9)
argument_correctness_metric = ArgumentCorrectnessMetric(
    model=eval_model,
    include_reason=True,
    threshold=0.9,
)

def build_dataset():
    test_cases=[]
    for idx, item in enumerate(TOOL_EVAL_CASES):
        print("\n" + "=" * 80)
        print(f"TEST {idx}")
        print(f"QUESTION: {item['input']}")
        print(f"EXPECTED TOOL: {item['expected_tool']}")

        result=run_agent(item['input'],f'ur-{idx}')
        print(f"ANSWER: {result['answer']}")
        actual_tool_calls=[
            ToolCall(
                name=tool["name"],
                input=tool.get("args", {}),
            )
            for tool in result["tools_called"]
        ]
        expected_tool_calls=[
            ToolCall(
                name=item['expected_tool'],
                input=item['expected_args']
            )
        ]

        test_case=LLMTestCase(
            input=item['input'],
            expected_tools=expected_tool_calls,
            tools_called=actual_tool_calls
        )
        test_cases.append(test_case)
    return test_cases


# def run_evaluation():
#     datasets = build_dataset()

#     evaluate(
#         test_cases=datasets,
#         metrics=[tool_correctness_metrics],
#         identifier="Tool Selection Evaluation v1",
#     )


def test_tool():
    datasets=build_dataset()
    for test_case in datasets:
        assert_test(test_case,metrics=[tool_correctness_metrics,argument_correctness_metric])


# if __name__=="__main__":
#     run_evaluation()