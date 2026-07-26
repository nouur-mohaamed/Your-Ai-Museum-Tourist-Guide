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
    if os.path.exists(f"{name}_db"):
        print("document storage is already created just get it")
        vectordb=FAISS.load_local(folder_path=f"{name}_db",embeddings=embedding_obj,allow_dangerous_deserialization=True)
        return vectordb
    print("create document storage")
    vector_databases={}
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    for name in ARTIFACTS_NAMES:
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
        print("collection is found,get it")
        collection=client.get_collection(name="museum_images")
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
            print(photo_name)
            remove_char_start=photo_name.index('_')
            print(photo_name[:remove_char_start])
            embedding= get_image_embedding(f"image_data/{photo_name}")
            print("adding the embedding of image to collection")
            collection.add(
            ids=[f"image_{idx+1}"],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "artifact_id": idx+1,
                "artifact_name": photo_name[:remove_char_start]
            }], )
        return collection
    else:
        return collection

