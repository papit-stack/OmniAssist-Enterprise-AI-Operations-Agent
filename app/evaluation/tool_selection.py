from deepeval.metrics import ToolCorrectnessMetric
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval import assert_test,evaluate
from app.evaluation.tool_eval_dataset import TOOL_EVAL_CASES
from app.agents.new_agent import test_agent
from deepeval.models import GeminiModel
import json
import os
from app.config import GEMINI_MODEL


model=GeminiModel(model=GEMINI_MODEL)
tool_correctness_metrics=ToolCorrectnessMetric(model=model,threshold=0.9,include_reason=True)


def build_test_case():
    dataset=[]
    for idx,test_case in enumerate(TOOL_EVAL_CASES):
        result=test_agent(test_case['input'],f"test-agent-{idx}")
        print(f"ID: {idx}")
        print(f"Input: {test_case['input']}")
        print(f"Expected tool: {test_case['expected_tool']}")
        print(f"Expected args: {test_case['expected_args']}")
        print(f"Tool result: {result['tools_called']}")

        dataset.append({
            'input': test_case['input'],
            'expected_tool': test_case['expected_tool'],
            'expected_args': test_case['expected_args'],
            'actual_tool' : result["tools_called"]
        })
    # Load existing results if the file exists
    if os.path.exists('tool_test_cases.json'):
        with open('tool_test_cases.json', "r",) as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Append this run's results
    existing_data.extend(dataset)

    # Save everything back
    with open('tool_test_cases.json','w') as f:
        json.dump(existing_data,f, indent=2, ensure_ascii=False)


def run_evaluation():
    with open('tool_test_cases.json','r') as f:
        dataset=json.load(f)
        
        for idx,case in enumerate(dataset):
            actual_tools=[]
            for tool in case['actual_tool']:
                actual_tools.append(
                    ToolCall(name=tool['name'],arguments=tool["args"])
                )
            expected_tools = []
            for tool_name, args in zip(case["expected_tool"],case["expected_args"]):
                if tool_name is None:
                    continue
                expected_tools.append(
                    ToolCall(name=tool_name,arguments=args)
                )
            test_case = LLMTestCase(
                input=case["input"],
                tools_called=actual_tools,
                expected_tools=expected_tools,
            )
            print(f"\nEvaluating test case {idx + 1}/{len(dataset)}")
            evaluate([test_case],metrics=[tool_correctness_metrics])

        


if __name__=="__main__":
    run_evaluation()