import json
import os
import re
import shutil
from datetime import datetime

from ai.ai_researcher import request_improvement

from engine.backtester import (
    download_data,
    run_backtest
)

from engine.evaluator import (
    calculate_metrics,
    calculate_score,
    is_better
)

from engine.validator import (
    validate_strategy_code
)


PARAMETERS_FILE = "config/parameters.json"

INSTRUCTIONS_FILE = (
    "instructions/instructions.txt"
)

STRATEGY_FILE = (
    "strategies/strategy.py"
)

BEST_STRATEGY_FILE = (
    "strategies/best_strategy.py"
)


def load_json(path):

    with open(path, "r") as file:
        return json.load(file)


def save_json(path, data):

    with open(path, "w") as file:
        json.dump(
            data,
            file,
            indent=2
        )


def read_text(path):

    with open(path, "r") as file:
        return file.read()


def write_text(path, text):

    with open(path, "w") as file:
        file.write(text)


def extract_strategy(ai_response):
    """
    Extract the complete Python strategy from
    the AI response.
    """

    pattern = (
        r"COMPLETE_STRATEGY_CODE\s*"
        r"```python\s*"
        r"(.*?)"
        r"```"
    )

    match = re.search(
        pattern,
        ai_response,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            "AI did not return COMPLETE_STRATEGY_CODE."
        )

    return match.group(1).strip()


def main():

    parameters = load_json(
        PARAMETERS_FILE
    )

    instructions = read_text(
        INSTRUCTIONS_FILE
    )

    print("=" * 70)
    print("AI QUANTITATIVE RESEARCH LABORATORY")
    print("=" * 70)

    print(
        f"Maximum iterations: "
        f"{parameters['max_iterations']}"
    )

    print(
        f"Symbol: "
        f"{parameters['symbol']}"
    )

    print("=" * 70)

    # Download data once.
    print("\nDownloading market data...")

    df = download_data(
        parameters["symbol"],
        parameters["period"],
        parameters["interval"]
    )

    print(
        f"Downloaded {len(df)} market bars."
    )

    # Load current strategy.
    current_strategy = read_text(
        STRATEGY_FILE
    )

    best_metrics = None

    previous_result = "No previous result."

    previous_error = "No previous error."

    consecutive_failures = 0

    last_score = None

    same_result_count = 0

    for iteration in range(
        1,
        parameters["max_iterations"] + 1
    ):

        print("\n")
        print("#" * 70)
        print(
            f"ITERATION {iteration}"
        )
        print("#" * 70)

        try:

            print("\nRunning current strategy...")

            # Dynamically import the strategy.
            namespace = {}

            exec(
                current_strategy,
                namespace
            )

            generate_signals = namespace[
                "generate_signals"
            ]

            backtest = run_backtest(
                df,
                generate_signals,
                parameters[
                    "starting_capital"
                ],
                parameters[
                    "transaction_cost"
                ]
            )

            metrics = calculate_metrics(
                backtest
            )

            score = calculate_score(
                metrics
            )

            metrics["score"] = round(
                score,
                6
            )

            print("\nCURRENT RESULTS")

            for key, value in metrics.items():
                print(
                    f"{key}: {value}"
                )

            previous_result = json.dumps(
                metrics,
                indent=2
            )

            previous_error = (
                "No execution error."
            )

            # Determine whether this is the best result.
            if is_better(
                metrics,
                best_metrics
            ):

                print(
                    "\nNEW BEST STRATEGY"
                )

                best_metrics = metrics.copy()

                shutil.copyfile(
                    STRATEGY_FILE,
                    BEST_STRATEGY_FILE
                )

                print(
                    "Best strategy updated."
                )

            # Detect stagnation.
            if (
                last_score is not None
                and score == last_score
            ):
                same_result_count += 1
            else:
                same_result_count = 0

            last_score = score

            if (
                same_result_count
                >= parameters[
                    "max_same_result"
                ]
            ):

                print(
                    "\nStopping: repeated result."
                )

                break

            consecutive_failures = 0

        except Exception as error:

            error_text = (
                f"{type(error).__name__}: "
                f"{error}"
            )

            print(
                "\nSTRATEGY ERROR"
            )

            print(error_text)

            previous_error = error_text

            consecutive_failures += 1

            if (
                consecutive_failures
                >= parameters[
                    "max_consecutive_failures"
                ]
            ):

                print(
                    "\nStopping: too many "
                    "consecutive failures."
                )

                break

        # Last iteration does not need another AI call.
        if iteration >= parameters[
            "max_iterations"
        ]:
            break

        print(
            "\nSending current situation "
            "to AI researcher..."
        )

        try:

            ai_response = request_improvement(
                instructions,
                current_strategy,
                previous_result,
                previous_error
            )

            print(
                "\nAI RESPONSE"
            )

            print(ai_response)

            candidate_strategy = (
                extract_strategy(
                    ai_response
                )
            )

            print(
                "\nValidating AI candidate..."
            )

            valid, validation_message = (
                validate_strategy_code(
                    candidate_strategy
                )
            )

            print(validation_message)

            if not valid:

                print(
                    "Candidate rejected."
                )

                continue

            # Save candidate temporarily.
            write_text(
                STRATEGY_FILE,
                candidate_strategy
            )

            current_strategy = (
                candidate_strategy
            )

            print(
                "\nCandidate accepted for "
                "the next iteration."
            )

        except Exception as error:

            print(
                "\nAI RESEARCH ERROR"
            )

            print(
                f"{type(error).__name__}: "
                f"{error}"
            )

            # Restore the previous strategy.
            write_text(
                STRATEGY_FILE,
                current_strategy
            )

    # Final report.
    print("\n")
    print("=" * 70)
    print("RESEARCH COMPLETE")
    print("=" * 70)

    print(
        json.dumps(
            best_metrics,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
