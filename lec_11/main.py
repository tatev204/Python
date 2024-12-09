import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = response.json()
print(posts[:5])

filtered_posts_by_title = [
    post for post in posts if len(post['title'].split()) <= 6
]

filtered_posts_by_title = [
    post for post in filtered_posts_by_title if post['body'].count('\n') <= 3
]

new_post = {
    "title": "My New Post",
    "body": "This is the body of my new post.",
    "userId": 1
}
response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
print(response.json())

response = requests.put("https://jsonplaceholder.typicode.com/posts/1", json=new_post)
print(response.json())

response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")
print(response.status_code)
