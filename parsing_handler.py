from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import PromptTemplate
def get_parsing_output_parser():
    location_schema=ResponseSchema(
        name='Location',
        description='the location where that artifact is located in the museum'
                                   )
    lifespan_schema=ResponseSchema(
        name='Lifespan',
        description="""the lifespan of that artifact from the date it was born to the date it died represented in dates and symbols only no letters or words """
    )
    response_schema=[location_schema,lifespan_schema]
    return StructuredOutputParser.from_response_schemas(response_schema)
def get_parsing_prompt():
    prompt="""200you're a smart assistant that extracts the location of the artifact and it's lifespan from the user input
    extract the location of the artifact in the museum and format the artifact lifespan 
    based on the user input:
    {input}
    Respond only in json format as follows:
    {formated_instructions}
    """
    return PromptTemplate(
        input_variables=['input','formated_instructions'],
        template=prompt
    )

