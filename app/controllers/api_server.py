import requests



def get_random_dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    if response.status_code==200:
        data = response.json()
        image_url = data["message"]
        breed = image_url.split('/')[-2]
        return {"breed":breed.capitalize(), "image_url":image_url}
    return None