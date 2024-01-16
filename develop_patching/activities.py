from dataclasses import dataclass

from temporalio import activity

"""dacx
Consider a background check application where, initially, only a social security number is required:
dacx"""

@dataclass
class SsnTraceInput:
    ssn: str


@activity.defn
async def ssn_trace_activity(input_data: SsnTraceInput) -> str:
    return "pass"


@activity.defn
async def federal_background_check_activity(input_data: SsnTraceInput) -> str:
    return "pass"

"""@dacx
id: workflow-data-classes-example
title: Adapting Workflows to New Data Types
sidebar_label: Data Class Examples
description: Provides examples of how to adapt Temporal workflows to new data types using data classes.
tags:
  - guide-python-temporal
  - data-class-examples
lines: 5-11
@dacx"""