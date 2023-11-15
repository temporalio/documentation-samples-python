import json
import uuid

import pytest
from temporalio.client import WorkflowHistory
from temporalio.testing import ActivityEnvironment, WorkflowEnvironment
from temporalio.worker import Replayer, Worker

from backgroundcheck import BackgroundCheck
from ssntraceactivity import ssn_trace_activity


@pytest.mark.asyncio
async def test_ssn_trace_activity() -> str:
    activity_environment = ActivityEnvironment()
    expected_output = "pass"
    assert expected_output == await activity_environment.run(
        ssn_trace_activity, "55-55-555"
    )


@pytest.mark.asyncio
async def test_execute_workflow():
    task_queue_name = str(uuid.uuid4())
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker(
            env.client,
            task_queue=task_queue_name,
            workflows=[BackgroundCheck],
            activities=[ssn_trace_activity],
        ):
            assert "pass" == await env.client.execute_workflow(
                BackgroundCheck.run,
                "555-55-5555",
                id=str(uuid.uuid4()),
                task_queue=task_queue_name,
            )
"""dacx
Add the Replay test to the set of application tests.
The Replayer is available from the [Replayer](https://python.temporal.io/temporalio.worker.Replayer.html) class in the SDK.
Register the Workflow Definition and then specify an existing Event History to compare to.

Run the tests in the test directory (pytest).
If the Workflow Definition and the Event History are incompatible, then the test fails.
dacx"""

@pytest.mark.asyncio
async def test_replay_workflow_history_from_file():
    async with await WorkflowEnvironment.start_time_skipping():
        with open("tests/backgroundcheck_workflow_history.json", "r") as f:
            history_json = json.load(f)
            await Replayer(workflows=[BackgroundCheck]).replay_workflow(
                WorkflowHistory.from_json("backgroundcheck_workflow", history_json)
            )

""" @dacx
id: add-replay-test-to-background-check-workflow
title: Add a Replay test
description: Define the code needed to run a Worker Process in Python.
label: Add Replay test
lines: 38-54
tags:
- testing
- replay test
- replayer
@dacx """