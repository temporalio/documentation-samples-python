from temporalio import activity

from your_dataobject_dacx import YourParams

"""
You can develop an Activity Definition by using the `@activity.defn` decorator.
Register the function as an Activity with a custom name through a decorator argument, for example `@activity.defn(name="your_activity")`.
"""

"""
Activity parameters are the function parameters of the function decorated with `@activity.defn`.
These can be any data type Temporal can convert, including dataclasses when properly type-annotated.
Technically this can be multiple parameters, but Temporal strongly encourages a single dataclass parameter containing all input fields.
"""

"""
An Activity Execution can return inputs and other Activity values.

The following example defines an Activity that takes a string as input and returns a string.
"""


@activity.defn
async def your_activity(input: YourParams) -> str:
    return f"{input.greeting}, {input.name}!"


""" @dac
id: how-to-develop-an-activity-definition-in-python
title: How to develop an Activity Definition in Python
label: Activity Definition
description: In the Temporal Go SDK programming model, an Activity Definition is an exportable function or a `struct` method.
lines: 6-8, 23-25
@dac """

""" @dac
id: how-to-define-activity-parameters-in-python
title: How to do define Activity parameters in Python
label: Activity parameters
description: The only required parameter is `context.Context`, but Activities can support many custom parameters.
lines: 11-13, 1-3, 23-25
@dac """

""" @dac
id: how-to-define-activity-return-values-in-python
title: How to define Activity return values in Python
label: Activity return values
description: A Go-based Activity Definition can return either just an `error` or a `customValue, error` combination.
lines: 17-19, 23-25
@dac """
