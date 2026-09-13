# AI/LLM-GENERATED FILE
# Purpose:
#   Build a controlled research prompt for Nemotron and request
#   one testable strategy improvement.
#
# Important architecture rule:
#   Nemotron proposes.
#   GitHub validates.
#   GitHub backtests.
#   GitHub evaluates.
#   GitHub decides whether an improvement is actually better.
#
# The AI does NOT directly modify files.

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
    3. Consider the previous result and error.
    4. Propose ONE meaningful improvement.
    5. Return the COMPLETE replacement strategy code.

    The AI does not directly modify files.

    run_research.py is responsible for:
    - receiving the response
    - extracting the candidate strategy
    - validating it
    - backtesting it
    - evaluating it
    """

    prompt = f"""
You are working inside an automated quantitative research laboratory.

Your role is to act as a quantitative research and Python strategy
analyst.

IMPORTANT RULES
===============

1. Analyze the current strategy carefully before proposing a change.

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

13. Keep the strategy compatible with the existing backtester.

14. Return the complete replacement strategy code,
not merely a code fragment.

15. The complete replacement strategy MUST appear after
this exact marker:

COMPLETE_STRATEGY_CODE

16. Put the complete strategy inside a Python code block:

```python
COMPLETE STRATEGY HERE
