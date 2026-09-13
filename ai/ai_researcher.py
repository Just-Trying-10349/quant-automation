from ai.ai_client import ask_ai


def build_prompt(
    instructions,
    strategy_code,
    previous_result,
    previous_error
):
    """
    Construct the complete research request.
    """

    prompt = f"""
You are working inside an automated quantitative
research laboratory.

========================
USER RESEARCH INSTRUCTIONS
========================

{instructions}


========================
CURRENT STRATEGY CODE
========================

```python
{strategy_code}
