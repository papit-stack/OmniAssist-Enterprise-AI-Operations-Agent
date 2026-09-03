from deepeval.metrics import ToolCorrectnessMetric, ArgumentCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval import assert_test

from app.evaluation.tool_eval_dataset import TOOL_EVAL_CASES
from app.agents.graph import run_agent
from deepeval.models import GeminiModel,OpenAIModel
from app.config import GEMINI_MODEL
import os

# Evaluation model

eval_model = GeminiModel(model=GEMINI_MODEL)

args_eval_model=OpenAIModel(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)



# Metrics

tool_correctness_metric = ToolCorrectnessMetric(
    model=args_eval_model,
    include_reason=True,
    threshold=0.9,
)

argument_correctness_metric = ArgumentCorrectnessMetric(
    model=eval_model,
    include_reason=True,
    threshold=0.7,
)


# Build DeepEval test cases

def build_dataset():

    test_cases = []
    for idx,item in enumerate(TOOL_EVAL_CASES):
        result = run_agent(
            item["input"],
            f"r-{idx}",
        )

        actual_tool_calls = [
                ToolCall(
                    name=tool["name"],
                    input_parameters=tool.get("args", {}),
                )
                for tool in result.get("tools_called", [])
                if tool.get("name")
            ]
        expected_tool_calls = [
            ToolCall(
                name=tool["name"],
                input_parameters=tool.get("args", {}),
            )
            for tool in item["expected_tool"]
        ]

        test_case = LLMTestCase(
                    input=item['input'],
                    tools_called=actual_tool_calls,
                    expected_tools=expected_tool_calls
        
        )
        # print(f"Expected tool calls: {expected_tool_calls}")

        test_cases.append(test_case)
    return test_cases


def test_tool():

    datasets = build_dataset()

    for test_case in datasets:

        assert_test(
            test_case,
            metrics=[tool_correctness_metric,argument_correctness_metric],
        )

if __name__=="__main__":
    test_tool()
    