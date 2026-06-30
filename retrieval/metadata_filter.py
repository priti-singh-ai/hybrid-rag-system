def filter_documents(results, year):

    filtered=[]

    for doc in results:

        if year in doc["source"]:

            filtered.append(doc)

    return filtered