# Cooking Buddy

## Goal: 
Cooking Buddy is a web application that provides valuable information about various recipes, cooking instructions, and ingredients. It utilizes the Spoonacular API to fetch recipe data and display it to users.

## Target Users: 
Cooking enthusiasts, food lovers, and anyone looking for new and exciting recipes to try out in the kitchen.

## API: 
 [Spoonacular API](https://spoonacular.com/food-api/docs)
 
## Approach:
#### Database Schema: 
Registered users will be stored in the database. Login authentication information and data for saved recipes will be stored for each user using Object-Relational Mapping (ORM).

![Cooking Buddy Database](https://dbdiagram.io/d/64ace75c02bd1c4a5ed89b2f)

#### Potential API Problems: 
As we're relying on data from an external API, there is a possibility of the API no longer being available. We should have proper error handling in place to handle such situations gracefully. 

#### Sensitive Information: 
Encryption will be used to secure sensitive user information, such as passwords, to protect user privacy.

### Functionality:
1. User registration and login
2. Recipe search functionality
3. Displaying detailed recipe information, including ingredients and instructions
4. Recipe favoriting functionality for registered users

### User Flow:
1. Users will either register or log into their account.
2. Search for recipes based on keywords, ingredients, or categories.
3. View comprehensive recipe information, including ingredients and instructions.
4. Registered users can save favorite recipes to their profile.

### Additional Features:
1. **Cooking Timer:** Users can set cooking timers for each recipe to help them stay organized while cooking.
2. **Meal Planning:** Implement a meal planning feature where users can save recipes for different meals throughout the week.
3. **Recipe Sharing:** Allow users to share their favorite recipes with others via email or social media.
4. **Rating and Reviews:** Add a rating and review system, enabling users to provide feedback on recipes they've tried.
5. **Cooking Tips:** Include cooking tips and tricks for specific recipes or ingredients to help users improve their cooking skills.

By incorporating these features, Cooking Buddy can become a comprehensive and user-friendly web application for cooking enthusiasts to discover and explore new recipes while enhancing their culinary experiences.