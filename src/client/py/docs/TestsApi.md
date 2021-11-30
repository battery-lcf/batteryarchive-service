# openapi_client.TestsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_test**](TestsApi.md#create_test) | **POST** /cells/{cellId}/tests | Create a test for Cell
[**list_tests**](TestsApi.md#list_tests) | **GET** /tests | List all Tests
[**show_tests_for_cell_by_id**](TestsApi.md#show_tests_for_cell_by_id) | **GET** /cells/{cellId}/tests | Info for all Tests on Cell


# **create_test**
> create_test(cell_id)

Create a test for Cell

### Example


```python
import time
import openapi_client
from openapi_client.api import tests_api
from openapi_client.model.error import Error
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tests_api.TestsApi(api_client)
    cell_id = "cellId_example" # str | The id of the cell to retrieve

    # example passing only required values which don't have defaults set
    try:
        # Create a test for Cell
        api_instance.create_test(cell_id)
    except openapi_client.ApiException as e:
        print("Exception when calling TestsApi->create_test: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cell_id** | **str**| The id of the cell to retrieve |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Null response |  -  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tests**
> Tests list_tests()

List all Tests

### Example


```python
import time
import openapi_client
from openapi_client.api import tests_api
from openapi_client.model.error import Error
from openapi_client.model.tests import Tests
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tests_api.TestsApi(api_client)
    limit = 1 # int | How many items to return at one time (max 100) (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # List all Tests
        api_response = api_instance.list_tests(limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling TestsApi->list_tests: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| How many items to return at one time (max 100) | [optional]

### Return type

[**Tests**](Tests.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A paged array of cells |  * x-next - A link to the next page of responses <br>  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **show_tests_for_cell_by_id**
> Tests show_tests_for_cell_by_id(cell_id)

Info for all Tests on Cell

### Example


```python
import time
import openapi_client
from openapi_client.api import tests_api
from openapi_client.model.error import Error
from openapi_client.model.tests import Tests
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = tests_api.TestsApi(api_client)
    cell_id = "cellId_example" # str | The id of the cell to retrieve

    # example passing only required values which don't have defaults set
    try:
        # Info for all Tests on Cell
        api_response = api_instance.show_tests_for_cell_by_id(cell_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling TestsApi->show_tests_for_cell_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cell_id** | **str**| The id of the cell to retrieve |

### Return type

[**Tests**](Tests.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Expected response to a valid request |  -  |
**0** | unexpected error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

