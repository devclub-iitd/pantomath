import facebook

graph = facebook.GraphAPI(access_token="", version="2.12")

page = graph.get_object(id='rendezvous.iitd')
print(page)