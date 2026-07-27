from get_or_initialize_data_storages import get_or_init_doc_storage,get_or_init_img_storage
from get_image_embedding import get_image_embedding
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain
from parsing_handler import get_parsing_prompt,get_parsing_output_parser
from pypdf import PdfReader
import os
def extract_pdf_info(name,llm):
    if os.path.exists(f"{name}_pdf_extracted_text.txt"):
        with open(f"{name}_pdf_extracted_text.txt",'r',encoding='utf-8') as file:
            return file.read()
    reader = PdfReader(f"data/{name}.pdf")
    text=''

    prompt="""512you're a helpful,smart assistant that can take an extracted page of a pdf:{page_text} and Summarize the that page.

Requirements:
- Keep every important historical fact.
- Keep names, dates and events.
- Remove repetition and unnecessary details.
- Write at most 150 words."""
    summarizing_prompt=PromptTemplate(input_variables=['page_text'],template=prompt)
    summarizing_chain=LLMChain(llm=llm,prompt=summarizing_prompt)
    for page in reader.pages:
        page_text = page.extract_text()
        page_summary=summarizing_chain.run({'page_text':page_text})
        if page_summary:  # Prevent NoneType errors
            text += page_summary + "\n"
    with open(f"{name}_pdf_extracted_text.txt",'w',encoding='utf-8') as file:
        file.write(text)
    return text
def get_name_of_statue(query_image_embedding):
    collection = get_or_init_img_storage()
    print("start similarity search")
    results = collection.query(
    query_embeddings=[query_image_embedding.tolist()],
    n_results=5
    )
    return results['metadatas'][0][0]['artifact_name']

def get_context(text:str,name,k):
    docs = get_or_init_doc_storage(name).similarity_search(text, k=k) #return the index compatible with name of artifact and search in it
    retrieved_context = "\n\n".join([doc.page_content for doc in docs])
    return retrieved_context

def get_statue_info(image_url,llm):
    embedding=get_image_embedding(image_url=image_url)
    name=get_name_of_statue(embedding)
    #output parsing chain
    parsing_input=get_context(f"what is the location of the artifact of {name}?\nwhat is the start date and the end date of {name}?",name,3)
    output_parser=get_parsing_output_parser()
    formatted_instruction=output_parser.get_format_instructions()
    parsing_chain=LLMChain(llm=llm,prompt=get_parsing_prompt()) #create output parsing chain
    parsing_response=parsing_chain.run({ #get the parsed output
        'input':parsing_input,
        'formated_instructions':formatted_instruction
    })
    parsing_response=output_parser.parse(parsing_response) #transform from str back to python dictionary
    #tourist guide initial info chain
    context = extract_pdf_info(name,llm)
    info_prompt=PromptTemplate(
        input_variables=["name","context"],
        template="""storyyou're a friendly museum tourist guide,based on the provided context: {context} execute the order below
        order: tell me everything related to the name:{name} provided in a story style,don't exclude any information."""
    )
    info_chain=LLMChain(llm=llm,prompt=info_prompt)
    info_response=info_chain.run(
        {
            'name':name,
            'context':context
        })
    return{
        'name': name,
        'location':parsing_response['Location'],
        'lifespan':parsing_response['Lifespan'],
        'statue_info_text':info_response
    }
def answer_statue_related_questions(query_related_context,query,llm):
    QandA_prompt=PromptTemplate(input_variables=['query_related_context','query'],template="""256
You are a very smart and friendly AI museum tourist guide.

The Context below is the ONLY source of information you are allowed to use.

Rules:
1. Use ONLY the Context.
2. Do NOT use any outside knowledge.
3. Do NOT guess or infer facts not explicitly stated.
4. If the answer is not explicitly present in the Context, reply exactly:
"I don't know based on the provided context."
5. Keep the answer concise.

### Context ###
{query_related_context}

### End Context ###

Question:
{query}

Answer:
"""
)
    QandA_chain=LLMChain(llm=llm,prompt=QandA_prompt)
    return QandA_chain.run(
        {
            'query_related_context':query_related_context,
            'query':query
        }
    )
