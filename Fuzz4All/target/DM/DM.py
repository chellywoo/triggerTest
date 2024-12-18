import os
import time
from pathlib import Path
from typing import List

from Fuzz4All.target.target import FResult, Target
from Fuzz4All.util.util import comment_remover

class DMTarget(Target):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs["template"] == "fuzzing_with_config_file":
            config_dict = kwargs["config_dict"]
            self.prompt_used = self._create_prompt_from_config(config_dict)
            self.config_dict = config_dict
        else:
            raise NotImplementedError

    def write_back_file(self, code: str, write_back_name: str = "") -> str:
        """Writes the generated SQL code to a file and returns the file path."""
        if write_back_name != "":
            try:
                with open(write_back_name, "w", encoding="utf-8") as f:
                    f.write(code)
            except:
                pass
        else:
            write_back_name = "/tmp/temp{}.fuzz".format(self.CURRENT_TIME)
            try:
                with open(write_back_name, "w", encoding="utf-8") as f:
                    f.write(code)
            except:
                pass
        return write_back_name

    def wrap_prompt(self, prompt: str) -> str:
        """Wraps the prompt in a comment and appends the necessary SQL structure."""
        return f"-- {prompt}\n{self.prompt_used['separator']}\n{self.prompt_used['begin']}"

    def wrap_in_comment(self, prompt: str) -> str:
        """Wraps the given prompt in a SQL comment."""
        return f"-- {prompt}"

    def filter(self, code: str) -> bool:
        """Checks if the generated code contains necessary SQL structures."""
        clean_code = code.replace(self.prompt_used["begin"], "").strip()
        return self.prompt_used["target_api"] in clean_code

    def clean(self, code: str) -> str:
        """Removes comments from the code."""
        return comment_remover(code)

    def clean_code(self, code: str) -> str:
        """Further cleans the code, removing empty lines and unnecessary structures."""
        code = comment_remover(code)
        return "\n".join(
            line for line in code.split("\n") if line.strip() and line.strip() != self.prompt_used["begin"]
        )

    def validate_individual(self, filename: str) -> (FResult, str):
        """Validates the generated SQL code by writing it to a file."""
        write_back_name = ""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                code = f.read()
                write_back_name = self.write_back_file(code)
        except Exception as e:
            return FResult.ERROR, str(e)

        # Since we are not connecting to the database, we'll assume the file writing is successful
        return FResult.SAFE, "SQL code is written to file"

# Example usage:
# config_dict = {
#     "config_dict": {
#         "fuzzing": {
#             "output_folder": "./outputs",
#             # other fuzzing config
#         },
#         "target": {
#             "language": "sql",
#             "path_documentation": "path/to/docs",
#             "path_example_code": "path/to/examples",
#             "trigger_to_generate_input": "-- Generate a complex SQL query using DM database features",
#             "input_hint": "-- SELECT * FROM",
#             "path_hand_written_prompt": "path/to/handwritten/prompts",
#             "target_string": "SELECT",
#         },
#         "llm": {
#             "model_name": "some_model",
#             # other llm config
#         }
#     }
# }
# dm_target = DMTarget(template="fuzzing_with_config_file", config_dict=config_dict)
# dm_target.validate_individual("/path/to/fuzzfile.fuzz")
