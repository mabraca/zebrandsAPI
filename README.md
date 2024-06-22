# Zebrands API REST

It's a basic catalog system to manage products. A product should have basic info such as sku, name, price and brand.

In this system has at least two type of users: (i) admins to create / update / delete products and to create / update / delete other admins; and (ii) anonymous users who can only retrieve products information but can't make changes.

As a special requirement, whenever an admin user makes a change in a product (for example, if a price is adjusted), it notifies all other admins about the change via email

It also keeps track of the number of times every single product is queried by an anonymous user, so we can build some reports in the future.


## Status project

Something basic. It has integration test and it works 

## Installation

1. **Clone repository:**

   ```bash
   git clone https://github.com/mabraca/zebrandsAPI.git
   cd zebrands
   
2.  **CREATE DATABASE:**
    The project uses Postgres database. You need to follow this steps after download Postgres. In console, you need type:
    ```bash
       psql -U yourUser
       CREATE DATABASE catalog; 
       CREATE USER mariabracamonte WITH PASSWORD ''; 
       ALTER ROLE mariabracamonte SET client_encoding TO 'utf8'; 
       ALTER ROLE mariabracamonte SET default_transaction_isolation TO 'read committed'; 
       ALTER ROLE mariabracamonte SET timezone TO 'UTC'; 
       GRANT ALL PRIVILEGES ON DATABASE catalog TO mariabracamonte; 
    
        # if you want to create database with an specific user, just change the file settings.py with your credential for postgres

3. Install dependencies and do migrations
    Go to the root of the project zebrands/ and run
    ```bash
        pip install -r requirements.txt
        python manage.py makemigrations
        python manage.py migrate
   
4. Set environments variables in your system to send email from the app.
    ```bash
        EMAIL_HOST_USER=yourEmail@yourdomain.com 
        EMAIL_HOST_PASSWORD=yourPassword
   
6. Run an script in python to create a first admin user
    ```bash
        python manage.py setup
        #or if you want run the integration test run 
        python manage.py test
   
7. Run server:
    ```bash
        python manage.py runserver
        
   
The server runs in: http://localhost:8000/ 
There is a basic and horrible web page to see all the products or a specific product. 
The rest of the code is for API REST and these are the URLS.

You can check endpoints in http://localhost:8000/swagger 