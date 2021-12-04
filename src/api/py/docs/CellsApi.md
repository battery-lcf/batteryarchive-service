# openapi_client.CellsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_cells**](CellsApi.md#get_cells) | **GET** /cells | Fetches all Cells


# **get_cells**
> Cells get_cells()

Fetches all Cells

### Example


```python
import time
import openapi_client
from openapi_client.api import cells_api
from openapi_client.model.cells import Cells
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
    api_instance = cells_api.CellsApi(api_client)
    limit = 1 # int | How many items to return at one time (max 100) (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Fetches all Cells
        api_response = api_instance.get_cells(limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling CellsApi->get_cells: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**| How many items to return at one time (max 100) | [optional]

### Return type

[**Cells**](Cells.md)

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

