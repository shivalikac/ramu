# RAMU
**RAMU** (Real-time Assistant for Meal Upkeep) is an intelligent tool designed to assist students with meal planning and kitchen management. 

The goal of RAMU is to help students plan their meals for the week, generate grocery lists, and discover simple recipes. By taking into account a student’s current groceries, food preferences, time constraints, and mood, RAMU provides personalized suggestions that save time and reduce decision fatigue. This tool is especially helpful for students new to cooking, enabling them to eat healthier, manage their time more effectively, and make meal preparation easier.

## Features of the Tool:
### 1. Personalized Meal Suggestions:
- Input current groceries, food preferences, and cooking experience through an interactive questionnaire.
- Track the student’s mood, time availability, and energy level to offer appropriate meal options.
- Suggest recipes based on available ingredients, cooking utensils, and time constraints.

### 2. Meal Planning & Grocery List Generation:
- Provide weekly meal plan options based on the student’s calendar, assignments, and workload.
- Generate grocery lists for the week based on meal plans, current stock, and available kitchen utensils.
- Track utensil and grocery inventories to avoid re-entry of data.
- Suggest ideal times for grocery shopping based on the student’s schedule, local weather, and nearby grocery store locations.

### 3. Adaptive Recipe Recommendations:
- Suggest beginner-friendly or advanced recipes based on the student’s cooking experience.
- Integrate with popular recipe platforms (e.g., Instagram Reels, YouTube) and provide user feedback on recipes.
- Allow students to input specific dishes they want to cook or recommend new recipes based on their preferences.

### 4. Time and Effort Optimization:
- Take into account deadlines, assignments, and calendar events to suggest quick meals during busy periods.
- Consider post-meal cleanup by recommending recipes with minimal utensil use when the student has limited time.

### 5. Progress Tracking & Growth:
- Track cooking skills over time and progressively suggest more complex recipes as the student gains confidence.
- Help students improve their cooking and time management skills, gradually offering more detailed or advanced meals.

## To Do List:
### Week 4: Planning and Set Up
1. **Project Outline**:
   - Create a basic outline for page layouts and interactions. Document these for reference during development.
   
2. **Backend Setup**:
   - Decide between Flask and Django as the backend framework.
   - Set up the database and connect it to the project.
   - Establish the basic project structure.
   - Install required libraries and drivers for execution.

3. **User Creation & Authentication**:
   - Implement basic user registration, login, and logout functionality.
   - Set up authentication with sessions/cookies to track user history.

4. **Define Data Models**:
   - Create models for `User`, `Groceries`, `Utensils`, `Meal Plans`, and `Recipes`.

5. **Basic Frontend Layout**:
   - Create a basic responsive frontend layout.
   - Design login, registration, and dashboard pages.

### Week 5: Interactive Meal Planning Features
1. **Implement Interactive Questionnaire**:
   - Add a questionnaire for users to input groceries, preferences, and utensils.
   - Capture responses and store them in the database.

2. **Basic Recipe Suggestion System**:
   - Use APIs to implement recipe suggestions based on the user's inputs.

3. **Meal Planning Logic**:
   - Create an algorithm for daily and weekly meal planning.

4. **Grocery List Generation**:
   - Implement grocery list generation based on meal plans and current food stock.

5. **Frontend Pages**:
   - Build frontend pages for meal suggestions and grocery list generation.

### Week 6: Adaptive Features and Integration
1. **Time and Mood Integration**:
   - Add fields to the questionnaire for mood, time constraints, and energy levels.
   - Adapt the recipe suggestion algorithm to factor in time availability and mood (e.g., quick recipes during exams, comfort meals during stress).

2. **Calendar Integration**:
   - Integrate a calendar feature (Google Calendar, Outlook) to align meal planning with student schedules.

3. **API Integration**:
   - Connect to weather and location APIs to enhance meal planning.

4. **Frontend Enhancements**:
   - Add UI components for tracking mood, time, and energy.
   - Dynamically display meal suggestions based on these factors.

### Week 7: Optimization and Advanced Features
1. **Post-meal Cleanup Suggestions**:
   - Suggest meals that require fewer utensils when students are pressed for time.

2. **Inventory Management**:
   - Implement automatic tracking of groceries and utensils after meals.
   - Allow users to update their inventory in real-time.

3. **Frontend Refinement**:
   - Refine UI/UX for smoother interaction.
   - Implement an inventory tracking dashboard to visualize current groceries and utensils.

4. **Progressive Learning**:
   - Track cooking skill development over time (optional based on progress).
   - Suggest recipes of increasing difficulty as the student improves.

### Week 8: Final Touches and Testing
1. **Testing & Debugging**:
   - Thoroughly test the application.
   - Gather feedback and refine features.

2. **Documentation**:
   - Create comprehensive documentation, including setup instructions, API integrations, and a user manual.

3. **Final Demo & Submission**:
   - Prepare a final demo of the product.
   - Package code and documentation for submission.
