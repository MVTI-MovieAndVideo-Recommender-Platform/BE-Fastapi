def individual_serial(content) -> dict:
  return{
    "id": str(content["_id"]),
    "index": content["index"],
    "name": content["name"],
    "img_url": content["img_url"], 
    "flatrate": content["flatrate"],  
    "overview": content["overview"],
    "country": content["country"],
    "age_rating": content["age_rating"], 
    "year": content["year"], 
    "genres": content["genres"],
    "content_type": content["content_type"]
  }