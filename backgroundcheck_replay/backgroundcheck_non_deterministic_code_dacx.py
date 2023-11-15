import asyncio
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from random import randint
    from ssntraceactivity import ssn_trace_activity

"""dacx
Referred to as "intrinsic non-determinism" this kind of "bad" Workflow code can prevent the Workflow code from completing because the Workflow can take a different code path than the one expected from the Event History.

The following are some common operations that **can't** be done inside of a Workflow Definition:

- Generate and rely on random numbers.
    - Use `workflow.random()` as a replacement for `randint()`
- Accessing / mutating external systems or state.
This includes calling an external API, conducting a file I/O operation, talking to another service, etc. (use Activities instead).
- Relying on system time.
    - Use `workflow.Now()` as a replacement for `time.Now()`.
    - Use `workflow.Sleep()` as a replacement for `time.Sleep()`.
- Iterating over data structures with unknown ordering.
This includes iterating over maps using `range`, because with `range` the order of the map's iteration is randomized.
Instead you can collect the keys of the map, sort them, and then iterate over the sorted keys to access the map.
This technique provides deterministic results.
You can also use a Side Effect or an Activity to process the map instead.
- Storing or evaluating the run Id.

If a Workflow Execution performs a non-deterministic event, an exception is thrown, which results in failing the Task Worker.

The Workflow will not progress until the code is fixed.

For example, if you try to produce a non-deterministic error by using a random number to sleep inside the Workflow, you'll receive the following Restricted Workflow Access Error:

```python
temporalio.worker.workflow_sandbox._restrictions.RestrictedWorkflowAccessError:
```

From the following example code:
dacx"""


@workflow.defn()
class BackgroundCheckNonDeterministic:
    @workflow.run
    async def run(self, ssn: str) -> str:
        random_number = randint(1, 100)
        if random_number < 50:
            await asyncio.sleep(60)
            workflow.logger.info("Sleeping for 60 seconds")
        return await workflow.execute_activity(
            ssn_trace_activity,
            ssn,
            schedule_to_close_timeout=timedelta(seconds=5),
        )


"""dacx
This is because, Workflows in the Python SDK run in a sandbox, by default, to help avoid non-determinism code.

The sandbox is not foolproof and non-determinism can still occur. You are encouraged to define Workflows in files without side effects.

For information on the Sandbox, see []().
dacx"""

""" @dacx
id: backgroundcheck-replay-intrinsic-non-determinism
title: Intrinsic non-deterministic logic
description: This kind of logic prevents the Workflow code from executing to completion because the Workflow can take a different code path than the one expected from the Event History.
label: intrinsic-non-deterministic-logic
lines: 1-55
tags:
- tests
- replay
- event history
@dacx """

""" @dacx
id: backgroundcheck-replay-inspecting-the-non-deterministic-error
title: Intrinsic non-deterministic logic
description: This kind of logic prevents the Workflow code from executing to completion because the Workflow can take a different code path than the one expected from the Event History.
label: intrinsic-non-deterministic-logic
lines: 58-64
tags:
- tests
- replay
- event history
@dacx """
