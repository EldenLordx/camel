# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
import asyncio
import logging

from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import BrowserNonVisualToolkit
from camel.types import ModelPlatformType, ModelType

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler('browser_dom_debug.log'),  # File output
    ],
)

logging.getLogger('camel.agents').setLevel(logging.INFO)
logging.getLogger('camel.models').setLevel(logging.INFO)

USER_DATA_DIR = r"D:/User_Data"

model_backend = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI,
    model_type=ModelType.GPT_4_1,
    model_config_dict={"temperature": 0.0, "top_p": 1},
)

web_toolkit = BrowserNonVisualToolkit(
    headless=False,
)

agent = ChatAgent(
    model=model_backend,
    tools=[*web_toolkit.get_tools()],
    max_iteration=10,
)

TASK_PROMPT = """Click "Sign in to Google Account" on Google.
If a CAPTCHA appears requiring user input, call the wait_user function — 
wait 5 seconds each time and keep waiting until you detect that the snapshot 
no longer contains content requiring user action.
Make sure not to help the user fill in their account or CAPTCHA information.
Before the task is completed, you must call the tool in every session and 
use the wait_user function whenever needed.

"""


async def main() -> None:
    response = await agent.astep(TASK_PROMPT)

    print("Task:", TASK_PROMPT)
    print(f"Using user data directory: {USER_DATA_DIR}\n")
    print("Response from agent:")
    print(response.msgs[0].content if response.msgs else "<no response>")


if __name__ == "__main__":
    asyncio.run(main())
