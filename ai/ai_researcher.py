# AI/LLM-GENERATED FILE
#
# Purpose:
#   Build a controlled research prompt for Nemotron and request
#   one testable quantitative-strategy improvement.
#
# Architecture:
#   Nemotron proposes.
#   GitHub validates.
#   GitHub backtests.
#   GitHub evaluates.
#   GitHub decides whether an improvement is better.
#
# The AI does NOT directly modify repository files.

from ai.ai_client import ask_ai


def build_prompt(
    instructions,
    strategy_code,
    previous_result,
    previous_error
):
    """
    Build the complete research prompt sent to Nemotron.

    The AI receives:
    - the research instructions
    - the current strategy
    - the previous result
    - the previous error

    The AI must return one complete replacement strategy.

    It does not modify files itself.
    """

    prompt = f'''
You are working inside an automated quantitative research laboratory.

Your role is to act as a quantitative research and Python strategy analyst.

IMPORTANT ARCHITECTURE RULE
===========================

The AI is a RESEARCHER and PROPOSAL GENERATOR.

The AI proposes changes.

GitHub independently:
1. validates the proposed Python code,
2. runs the backtest,
3. calculates metrics,
4. calculates the objective score,
5. compares the candidate with the current best strategy.

The AI is NOT the final judge of performance.

The AI must NOT directly modify files.

IMPORTANT RULES
===============

1. Analyze the current strategy before proposing a change.

2. Propose exactly ONE meaningful improvement.

3. Do not provide Git commands.

4. Do not provide GitHub Actions YAML.

5. Do not modify configuration files.

6. Do not modify secrets.

7. Do not modify environment variables.

8. Do not introduce network requests into the strategy.

9. Do not use look-ahead bias.

10. Do not use future market information.

11. Preserve the required strategy interface:

def generate_signals(df):

12. The function must return a pandas Series.

13. Signals must contain only:

0 = no position
1 = long position

14. Keep the strategy compatible with the existing backtester.

15. Return the COMPLETE replacement strategy.

16. Do not return a partial code fragment.

17. Do not return pseudocode.

18. Do not provide multiple alternative strategies.

19. Do not create files.

20. Do not attempt to execute the strategy yourself.

21. The deterministic GitHub evaluator is the final judge.

22. The proposed strategy must be ordinary Python code.

23. Use only data available at the time of each trading decision.

24. Avoid unnecessary complexity unless it has a clear research purpose.

CURRENT RESEARCH INSTRUCTIONS
=============================

{instructions}

CURRENT STRATEGY CODE
=====================

The following is the strategy currently being tested:


{strategy_code}


# PREVIOUS RESULT

{previous_result}

# PREVIOUS ERROR

{previous_error}

# TASK

Study the research instructions, current strategy, previous result,
and previous error.

Then propose exactly ONE concrete improvement.

Your response must contain these sections:

## ANALYSIS

Explain briefly what the current strategy does.

Identify the most important weakness or research opportunity.

## PROPOSED_IMPROVEMENT

Describe exactly ONE change.

Do not propose several unrelated changes.

## EXPECTED_EFFECT

Explain what you expect the proposed change to improve.

## RISKS

Explain how the proposed change could make performance worse.

## COMPLETE_STRATEGY_CODE

After this exact marker, provide the COMPLETE replacement strategy.

The replacement must:

* be valid Python,
* contain def generate_signals(df):,
* return a pandas Series,
* produce only 0 or 1 signals,
* remain compatible with the existing backtester,
* avoid look-ahead bias,
* contain all required imports.

Put the complete replacement strategy inside a Python code block.

Do not provide partial code.

Do not provide multiple strategies.

Do not provide pseudocode.

The final evaluator will independently determine whether the
candidate strategy is actually better.

Your job is only to produce ONE testable research proposal.

COMPLETE_STRATEGY_CODE
'''

return prompt

def request_improvement(
instructions,
strategy_code,
previous_result,
previous_error
):
"""
Request one strategy improvement from the configured AI provider.
"""

 
prompt = build_prompt(
    instructions,
    strategy_code,
    previous_result,
    previous_error
)

response = ask_ai(prompt)

if not response:
    raise RuntimeError(
        "AI researcher returned an empty response."
    )

return response
