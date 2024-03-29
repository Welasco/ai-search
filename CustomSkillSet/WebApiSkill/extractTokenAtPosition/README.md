# Custom Web API SkillSet
Indexers in Azure AI Search supports mappingFunction to manipulate data prior to the ingestion into a Index.

There is a built-in mappingFunction called extractTokenAtPosition which is extremely valuable to split text prior to the ingestion into a index.

This is documented here:

[Field mappings and transformations using Azure AI Search indexers](https://learn.microsoft.com/en-us/azure/search/search-indexer-field-mappings)

[extractTokenAtPosition function](https://learn.microsoft.com/en-us/azure/search/search-indexer-field-mappings?tabs=rest#extractTokenAtPositionFunction)

Unfortunately it's not possible to use a mappingFunction when you have a skillset that is utilizing indexProjections to output custom data.

Documentation about indexProjections can be found here:

[Index projections in Azure AI Search](https://learn.microsoft.com/en-us/azure/search/index-projections-concept-intro)

For workaround this limitation I created a Function App that receives the same Input as extractTokenAtPosition mappingFunction to give the same expected expirience.

Skill Set Definition:
```json
{
    "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
    "name": "extractTokenAtPosition",
    "description": null,
    "context": "/document/content",
    "uri": "https://xxxxx.azurewebsites.net/api/extractTokenAtPosition",
    "httpMethod": "POST",
    "timeout": "PT3M",
    "batchSize": 10,
    "degreeOfParallelism": 10,
    "inputs": [
        {
            "name": "text",
            "source": "/document/url"
        },
        {
            "name": "delimiter",
            "source": "='/'"
        },
        {
            "name": "position",
            "source": "='-2'"
        }
    ],
    "outputs": [
        {
            "name": "folder",
            "targetName": "folder"
        }
    ],
    "httpHeaders": {}
}
'''

To use this workaround just create an Azure Function App with the content under the folder function.

The Function App Code is available here:

[Function App extractTokenAtPosition](./function/function_app.py)