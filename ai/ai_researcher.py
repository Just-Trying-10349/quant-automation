from ai.ai_client import ask_ai


def build_prompt(
    instructions,
    strategy_code,
    previous_result,
    previous_error
):
    """
    Construct the complete research request for the AI.

    The AI is asked to:
    1. Understand the research instructions.
    2. Understand the current strategy.
    3. Consider the previous result/error.
    4. Propose ONE improvement.
    5. Return the COMPLETE replacement strategy code.

    The AI does not directly modify files.
    run_research.py is responsible for receiving,
    extracting, validating, and testing the candidate.
    """

    prompt = f"""
You are working inside an automated quantitative
research laboratory.

Your role is to act as a quantitative research
and Python strategy analyst.

IMPORTANT RULES
===============

1. Analyze the strategy carefully before proposing changes.

2. Propose ONE meaningful improvement at a time.

3. Do not modify files yourself.

4. Do not provide Git commands.

5. Do not provide GitHub Actions YAML.

6. Do not modify configuration files.

7. Do not modify secrets or environment variables.

8. Do not introduce network requests into the strategy.

9. Do not use look-ahead bias or future market information.

10. Preserve the required strategy interface:

    def generate_signals(df):

11. The function must return a pandas Series.

12. Signals must contain only:
       0 = no position
       1 = long position

13. Keep the strategy compatible with the existing
    backtester.

14. Return the complete replacement strategy code,
    not merely a code fragment.

15. The complete replacement strategy MUST appear
    after this exact marker:

    COMPLETE_STRATEGY_CODE

16. Put the complete strategy inside a Python
    code block:

    ```python
    COMPLETE STRATEGY HERE
    ```

17. Do not put explanations inside the strategy code.

========================
USER RESEARCH INSTRUCTIONS
========================

{instructions}

========================
CURRENT STRATEGY CODE
========================

```python
{strategy_code}

{previous_result}

{previous_error}

Analyze the current strategy and previous result/error.

Then propose ONE concrete improvement.

Your response MUST contain the following sections:

ANALYSIS

Explain what the current strategy is doing and identify
the most important potential weakness.

PROPOSED_IMPROVEMENT

Explain exactly ONE change you recommend.

EXPECTED_EFFECT

Explain what you expect the change to improve.

RISKS

Explain how the change could make the strategy worse.

COMPLETE_STRATEGY_CODE

After this exact marker, provide the COMPLETE replacement
strategy.

The replacement strategy must be valid Python and must
contain:

def generate_signals(df):

Do not omit any required imports.

Do not provide pseudocode.

Do not provide partial code.

Remember:

The deterministic GitHub evaluator, not you, decides
whether the proposed strategy is better.

Your job is to propose a testable improvement.

COMPLETE_STRATEGY_CODE
"""

return prompt

def request_improvement(
instructions,
strategy_code,
previous_result,
previous_error
):
"""
Build the research prompt and send it to the
configured AI provider.
"""

prompt = build_prompt(
    instructions,
    strategy_code,
    previous_result,
    previous_error
)

return ask_ai(prompt)
