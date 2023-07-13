# PlantPal

## Goal: 
 To provide valuable information about various plants, including specific needs for lighting and watering

## Target Users: 
 Plant enthusiasts, specifically targeting those who are new to plant care and cultivation

## API: 
 [The Perenual API](https://perenual.com/docs/api)
 
## Approach:
#### Database Schema: 
Registered users will be stored in the database. Login authentication information and data for saved plants will be stored for eachc user with Objection Relational Mapping(ORM).

![PlantPal (1)](https://github.com/domibee/PlantPal/assets/101384668/866d920c-de1d-475d-acac-a3f69b20f80c)


#### Potential API Problems: 
As we're relying on data from an external API, there is a possibility of the API no longer being available and diseappearing. 

#### Sensitive Information: 
Encryption will be used to secure sensitive user information, such as passwords, to protect user privacy.

#### Functionality: 
1. User registration and login
2. Plant search functionality
3. Displaying detailed plant information and needs
4. Plant favoriting functionality for registered users
5. Watering reminders

#### User Flow: 
1. Users will either registering or logging into their account
2. Search for plants
3. View comprehensive plant information
4. Registered users can save favorite plants to their profile
5. Set watering reminders

#### Additional Features: 
Incorporating social features like plant sharing, a community forum for plant enthusiasts, or personalized plant care recommendations.
