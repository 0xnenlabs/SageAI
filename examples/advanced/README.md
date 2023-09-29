## Advanced Example

This example shows a more advanced version of `SageAI` with 3 functions, `get_current_weather`, `get_forecast_weather`, 
and `get_random_number`.

You can also nest your function folders; for example, you can have a folder called `weather` and
inside that folder you can have folders called `get_current_weather` and `get_forecast_weather`, each containing their
own implementation. This is useful if you have a lot of functions and want to organize them into folders.

We also demonstrate how to use your own custom vector database implementation, which in this example uses `vectordb` 
instead of `qdrant`.
