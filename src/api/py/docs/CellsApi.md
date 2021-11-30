# openapi_client.CellsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_cells**](CellsApi.md#create_cells) | **POST** /cells | Create a Cell
[**list_cells**](CellsApi.md#list_cells) | **GET** /cells | List all Cells
[**show_cell_by_id**](CellsApi.md#show_cell_by_id) | **GET** /cells/{cellId} | Info for a specific Cell


# **create_cells**
> create_cells()

Create a Cell

### Example


```python
import time
import openapi_client
from openapi_client.api import cells_api
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

    # example, this endpoint has no required or optional parameters
    try:
        # Create a Cell
        api_instance.create_cells()
    except openapi_client.ApiException as e:
        print("Exception when calling CellsApi->create_cells: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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

# **list_cells**
> Cells list_cells()

List all Cells

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
        # List all Cells
        api_response = api_instance.list_cells(limit=limit)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling CellsApi->list_cells: %s\n" % e)
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

# **show_cell_by_id**
> Cell show_cell_by_id(cell_id)

Info for a specific Cell

### Example


```python
import time
import openapi_client
from openapi_client.api import cells_api
from openapi_client.model.error import Error
from openapi_client.model.cell import Cell
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
    cell_id = "cellId_example" # str | The id of the cell to retrieve

    # example passing only required values which don't have defaults set
    try:
        # Info for a specific Cell
        api_response = api_instance.show_cell_by_id(cell_id)
        pprint(api_response)
    except openapi_client.ApiException as e:
        print("Exception when calling CellsApi->show_cell_by_id: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cell_id** | **str**| The id of the cell to retrieve |

### Return type

[**Cell**](Cell.md)

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

