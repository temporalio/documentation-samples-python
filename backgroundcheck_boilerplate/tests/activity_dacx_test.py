import pytest
from temporalio.testing import ActivityEnvironment
from activities import ssn_trace_activity


"""dacx
This is a unit test written in Python using the pytest library. It tests the ssn_trace_activity function from the activities module. The function takes a social security number as input and returns a string indicating whether the SSN is valid or not. The test checks if the function returns "pass" when given the SSN "55-55-555".
dacx"""


@pytest.mark.asyncio
async def test_ssn_trace_activity() -> str:
    activity_environment = ActivityEnvironment()
    expected_output = "pass"
    assert expected_output == await activity_environment.run(
        ssn_trace_activity, "55-55-555"
    )
