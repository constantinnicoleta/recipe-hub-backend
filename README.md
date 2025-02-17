## Recipe Hub -Backend ##


The API will serve as the backend for a React-based frontend. Endpoints have been designed to enable efficient communication between the frontend and backend, including:
- RESTful API endpoints for CRUD operations.
- JWT-based authentication to protect resources and maintain user sessions.

Live API-  [Clickhere](https://recipe-hub-backend-project-3024dae0e274.herokuapp.com/)

Click here to view the deployed API 

# Planning Overview #

## Backend Goals ##

- Secure API: Provide robust authentication and data protection.

- Efficient Data Management: Use Django ORM and PostgreSQL for structured storage.

- Scalable API Endpoints: Allow seamless interactions between frontend and backend.

- Agile Methodology & GitHub Project Management via a Kanban Board to manage project progress effectively.


# Core Functionalities #

## User Authentication ##
Secure login and registration using JWT.

## Recipe Management ##
CRUD functionality for recipes.

## User Engagement ##
Implement feed and follows.

## Category-Based Organization ## 
Enable recipe filtering by categories.

## Database Design ##

### Key Models ###

### User ###
Handles authentication and stores user profile details.

### Recipe ### 
Stores user-created recipes with title, description, ingredients, category.

### Category ###
Organizes recipes into specific groups.


### Follow ###
Manages relationships between users following each other.

# API Documentation #

## Authentication & Security ##

- Uses JWT Authentication: Secure access using token-based authentication.

- Protected Endpoints: Only authenticated users can create, edit, or delete recipes.

# API Endpoints #

## Authentication ##

- POST /api/auth/register/ → User registration

- POST /api/auth/login/ → User login

- POST /api/auth/logout/ → User logout

## Recipes ##

- GET /api/recipes/ → Get all recipes

- POST /api/recipes/ → Create a new recipe

- GET /api/recipes/:id/ → Get details of a recipe

- PUT /api/recipes/:id/ → Update a recipe

- DELETE /api/recipes/:id/ → Delete a recipe

## Categories ##

- GET /api/categories/ → Get all categories

-GET /api/categories/:id/ → Get recipes under a category

## Follows ##

POST /api/users/:id/follow/ → Follow a user


# Manual Testing #

Manual Testing

1. - Create Recipe - Test Description: Submit a recipe with valid data, including a title, ingredients, and preparation steps.

Expected Outcome: The recipe is successfully created and returned in the response with a unique ID and associated user.

2. - Follow a User - Test Description: Send a request to follow another user.

Expected Outcome: The user is successfully followed, and the follower count updates.

3. - Login- Test Description: Provide valid credentials to the login endpoint.

Expected Outcome: The user is authenticated and receives a JWT token.

4. - Access Unauthorized Endpoint -Test Description: Attempt to access a protected endpoint without providing a valid JWT token.

Expected Outcome: The request is denied with a 401 Unauthorized error message.


5. - nvalid Data Submission- Test Description: Attempt to submit a request with missing required fields or incorrect data types (e.g., submitting a recipe without a title).
Expected Outcome: The system returns an appropriate validation error message indicating the missing or incorrect fields.

6. Logout- Test Description: Send a request to the logout endpoint while being authenticated.
Expected Outcome: The user session is invalidated, and the token is no longer usable for authentication.

7. - Edit Recipe- Test Description: Update an existing recipe by modifying its title or ingredients.
Expected Outcome: The recipe is successfully updated, and the new data is reflected in the response.

8. - Delete Recipe- Test Description: Send a request to delete an existing recipe.

Expected Outcome: The recipe is removed from the database and is no longer accessible.

9. - Browse Recipes Without Login- Test Description: Try accessing the list of recipes without authentication.
Expected Outcome: Recipes are visible, but actions like creating, editing, or deleting recipes are restricted to authenticated users.

10. - Access Admin-Only Features- Test Description: Attempt to create, update, or delete a category as a non-admin user.
Expected Outcome: The request is denied with a 403 Forbidden error.

# Security Measures # 

### Authentication ###

JWT-based authentication ensures secure API access.
Passwords are hashed and managed using Django's auth framework.

### CSRF Protection ####

Django's built-in CSRF middleware is enabled to prevent cross-site request forgery.
Environment Variables

Sensitive information like SECRET_KEY and DATABASE_URL is stored securely in environment variables.

### Allowed Hosts ###

Configured to allow only specific domains (e.g., *.herokuapp.com).


# Technologies Used #

### Django REST Framework ###
 For building the API.

### PostgreSQL ### 
 For database management.

### JWT Authentication ###
 For secure login sessions.

### Cloudinary ####
 For storing recipe images.

### Backend Deployment ###
 via (Heroku)

**Heroku App Setup**

  - Register & Log In with heroku
  - Navigate to `New > Create New App`
  - Select Name of the app that is unique
  - Select your region, and click "Create App.
  - Navigate to `Settings > Reveal Config Vars`
  - Add all variables from `env.py` to ConfigVars of Heroku App (your PostgreSQL database URL & Secret Key)
  - Add the Heroku app URL into `ALLOWED HOSTS` in `settings.py`
  - In root create file name `Procfile`
  - Navigate to `Deploy > GitHub > Connect`
  - Navigate to `Deploy > Deploy Branch`
  - Optionally, you can enable automatic deploys
  - See the deployment log - if the deployment was successful, you will be prompted with option to see live page 

### the env.py file
With the database created, certain variables need to be kept private and should not be published to GitHub.

In order to keep these variables hidden, it is important to create an env.py file and add it to .gitignore.
At the top import os and set the DATABASE_URL variable using the os.environ method. Add the URL copied from instance created above to it, like so: `os.environ[“DATABASE_URL”] = ”copiedURL”`
The Django application requires a SECRET_KEY to encrypt session cookies. Set this variable to any string you like or generate a secret key on this MiniWebTool. `os.environ[“SECRET_KEY”] = ”longSecretString”`

## Forking and Cloning the GitHub Repository

1. Fork the GitHub Repository

Steps:
- Locate the GitHub repository.
- Click on 'Fork', in the top right-hand corner.
This will take you to your own repository to a fork with the same name as the original branch.

2. Creating a Local Clone

Steps:
- Go to the GitHub repository.
Click on 'Code' to the right of the screen. This will open a dropdown. Click on HTTPs and copy the link.
- Open Git Bash in your IDE and change the current working directory to the location where you want the cloned directory.
- Type git clone, paste the URL you copied earlier, and press Enter to create your local clone.

## Credits ##

Backend structure inspired by best practices in Django development.

Live API-  [Clickhere](https://recipe-hub-backend-project-3024dae0e274.herokuapp.com/)

