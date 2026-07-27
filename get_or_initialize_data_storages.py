from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import os
import chromadb
from get_image_embedding import get_image_embedding
from chromadb.errors import NotFoundError
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE=1000
CHUNK_OVERLAP=100
ARTIFACTS_NAMES=['akhenaten','hatshepsut','nefertiti','ramses2','tutankhamun']
embedding_obj=HuggingFaceEmbeddings(model_name=MODEL_NAME)
def get_or_init_doc_storage(name):
    if os.path.exists(f"{name}_db"): # if indices for each artifact were already made "initialization was done"
        print("document storage is already created just get it")
        vectordb=FAISS.load_local(folder_path=f"{name}_db",embeddings=embedding_obj,allow_dangerous_deserialization=True)
        return vectordb
    print("create document storage")
    vector_databases={}
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    for name in ARTIFACTS_NAMES: #create an index for each artifact "initialization"
        documents=PyPDFLoader(f"data/{name}.pdf").load()
        print(documents)
        chunks = text_splitter.split_documents(documents)
        vectordb = FAISS.from_documents(chunks, embedding_obj)
        vectordb.save_local(folder_path=f"{name}_db")
        vector_databases[name]=vectordb
    return vector_databases[name]
def get_or_init_img_storage():
    print("start retrieving the storage")
    client=chromadb.PersistentClient("museum_photo_db")
    try:
        collection=client.get_collection(name="museum_images")
        print("collection is found,get it")
        collection_exists=True
    except NotFoundError :
        print("collection is not found, creating one")
        collection=client.create_collection(name="museum_images")
        collection_exists = False
        print("created!")
    if not collection_exists:
        print("create our image database")
        for idx,photo in enumerate(Path('image_data').iterdir()):
            photo_name=photo.name
            embedding= get_image_embedding(f"image_data/{photo_name}") # get the embedding of the photo
            print("adding the embedding of image to collection")
            collection.add(            #**note** each value is wrapped in a list since we can add more than one entry to the collection at once
            ids=[f"image_{idx+1}"],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "artifact_id": idx+1,
                "artifact_name": photo_name[:photo_name.index('_')] # get the name of statue only for ex: ramses2_7 ---> ramses2
            }], )
        return collection
    else:
        return collection

