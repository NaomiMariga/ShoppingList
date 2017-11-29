## [Shopping List](https://naomimariga.github.io/ShoppingList "Visit Page")
Shopping list provides a platform for users to record and share items they want to spend their money on while keeping track of their spending.

Dummy login enabled by clicking the login button for testing

[![Build Status](https://travis-ci.org/NaomiMariga/ShoppingList.svg?branch=develop)](https://travis-ci.org/NaomiMariga/ShoppingList)
[![Coverage Status](https://coveralls.io/repos/github/NaomiMariga/ShoppingList/badge.svg?branch=develop)](https://coveralls.io/github/NaomiMariga/ShoppingList?branch=develop)
#### Functionalities and Features
###### Landing Page
[Index](/ShoppingList/blob/develop/designs/screenshots/index_page.png)

- User Registration
- User Login
    > - User is redirected to the dashboard
- Password Reset
    > - Upon requesting for password reset, a new password is sent to the user email
###### Main Page
[Dashboard](/ShoppingList/blob/develop/designs/screenshots/dashboard.png)

   - User is redirected to this page after successful login
   - From this point the user can manage the account by changing the password and perform other activities as listed below
        > - create shopping lists
        > - Edit Shopping lists
        > - Delete Shopping lists
        > - Shopping list
        > - Add items to a particular shoppinglist
        > - View Shoppinglist items
        > - Delete a shoppinglist item
        > - Edit a shoppinglist item
#### Extra features
- Automatic cost calculation
- Change password
#### Design style
- DOM implementation for fast page operation
#### Languages
  - python3.6
#### Dependencies
  - Flask
#### Testing the Application locally
- Clone the repository
    ```sh
    https://github.com/NaomiMariga/ShoppingList.git ShoppingList
    git checkout develop
    ```
- Change to the project directory
    ```sh
    cd ShoppingList
    ```
 - Set up the virtual environment
    - systemwide installation
        ```sh
         apt install python3.6 venv
        ```
    - create a virtual environment folder for the project
      ```sh
       python3.6 -m venv venv
      ```
- Install the dependencies
  ```sh
  pip install -r requirements.txt
  ```
- Activate virtual environment
  ```sh
  . venv/bin/activate
  ```
- Run the application
  ```sh
  python server.py
  ```
- In your browser, the application should be running on host: 0.0.0.0 and port: 5000
#### Testing the Online Shoppinglist Application
 ###### [Click to view Shopping List Application online](http://naomishoppinglist.herokuapp.com)