import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
  from activities import SsnTraceInput, ssn_trace_activity

"""dacx
This initial implementation of the BackgroundCheck Workflow includes a simple sleep function after executing an activity.
The Workflow takes a Social Security Number (SSN) input and performs a trace activity, followed by a 360-second sleep.
This represents the basic logic before any updates are introduced.
dacx"""

@workflow.defn
class BackgroundCheck:
  @workflow.run
  async def run(self, input: SsnTraceInput) -> str:
    results = await workflow.execute_activity(
      ssn_trace_activity,
      input,
      schedule_to_close_timeout=timedelta(seconds=5),
    )
    await asyncio.sleep(360)
    return results

""" @dacx
id: workflow-patching-initial-logic
title: Initial Workflow Logic Before Patching
sidebar_label: Initial Workflow Logic
description: Describes the initial logic of Temporal workflows before applying patches, setting the stage for updates.
tags:
  - guide-python-temporal
  - initial-workflow-logic
lines: 1-25
@dacx """
