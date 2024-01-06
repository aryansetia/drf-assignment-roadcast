# Project Overview
## This project provides a Django-based API for user management, authentication, and friend requests. It includes API endpoints for user signup, login, searching users, managing friend requests, listing friends, and handling pending friend requests as a part of assginment round at RoadCast.

## Getting Started
### Follow the steps below to set up and run the project locally.

## Prerequisites
### Docker installed on your machine.
## Installation
### Clone the repository:

```bash 
git clone <repository_url>
cd <project_directory>
```

### Build the Docker image:
```bash
docker build -t restful-social-app .
```

### Running the Container
Run the Docker container on port 8000:

```bash
docker run -p 8000:8000 restful-social-app
```

The API should now be accessible at http://localhost:8000/.

## API Endpoints
### 1. Signup
- Endpoint: /signup/
- Method: POST
- Permission: AllowAny
- Description: Create a new user account.

### 2. Login
- Endpoint: /login/
- Method: POST
- Permission: AllowAny
- Description: Authenticate and receive JWT tokens for a user.

### 3. Search Users
- Endpoint: /search_users/
- Method: GET
- Authentication: JWTAuthentication
- Permission: IsAuthenticated
- Description: Search for users by email or partial name.

### 4. Manage Friend Request
- Endpoint: /manage_friend_request/
- Method: POST
- Authentication: JWTAuthentication
- Permission: IsAuthenticated
- Description: Accept or reject a friend request.

### 5. List Friends
- Endpoint: /list_friends/
- Method: GET
- Authentication: JWTAuthentication
- Permission: IsAuthenticated
- Description: List friends for the authenticated user.

### 6. Pending Requests
- Endpoint: /pending_requests/
- Method: GET
- Authentication: JWTAuthentication
- Permission: IsAuthenticated
- Description: List pending friend requests for the authenticated user.

### 7. Send Request
- Endpoint: /send_request/
- Method: POST
- Authentication: JWTAuthentication
- Permission: IsAuthenticated
- Description: Send a friend request to another user.

### Postman Collection
A Postman collection is provided in the repository (postman_collection.json). You can import this collection into Postman to quickly test the API endpoints. Set the base URL to http://localhost:8000/ and generate the token through sign up and then log in, each token is valid for 7 days. To interact with authenticated endpoints, you need to include the Authorization Bearer Token in your requests.



