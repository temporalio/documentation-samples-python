from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from activities import ssn_trace_activity

"""dacx
In the Temporal Python SDK programming model, a Workflow Definition is defined as a class.
The BackgroundCheck class below is an example of a basic Workflow Definition.
dacx"""


@workflow.defn
class BackgroundCheck:
    @workflow.run
    async def run(self, ssn: str) -> str:
        return await workflow.execute_activity(
            ssn_trace_activity,
            ssn,
            schedule_to_close_timeout=timedelta(seconds=5),
        )


"""dacx
Use the `@workflow.defn` decorator on the `BackgroundCheck` class to identify a Workflow.

Use the `@workflow.run` to mark the entry point method to be invoked. This must be set on one asynchronous method defined on the same class as `@workflow.defn`.

Run methods have positional parameters.

To spawn an [Activity Execution](notion://www.notion.so/activities#activity-execution), call `execute_activity()` inside your Workflow Definition.

This API is available from the `workflow` module from the `temporalio` package.

The `execute_activity` API call requires either `schedule_to_close_timeout` or `start_to_close_timeout`.

In this example, pass in the Activity name, `ssn_trace_activity` and an argument, `ssn`.
We get into the best practices around Workflow params and returns in the one of the next sections.

In regards to code organization, we recommend organizing Workflow code together with other Workflow code.
For example, in a small project like this, it is still a best practice to have a dedicated file for each Workflow.
dacx"""

""" @dacx
id: backgroundcheck-boilerplate-backgroundcheck-workflow
title: Boilerplate Workflow code
label: Workflow code
description: In the Temporal Python SDK programming model, a Workflow Definition is defined as a class.
tags:
- go sdk
- developer guide
- workflow
- code sample
lines: 8-11, 14-22
@dacx """

""" @dacx
id: backgroundcheck-boilerplate-workflow-details
title: Boilerplate Workflow code
label: Workflow code
description: In the Temporal Python SDK programming model, a Workflow Definition is defined as a class.
tags:
- go sdk
- workflow
- developer guide
lines: 25-43
@dacx """
