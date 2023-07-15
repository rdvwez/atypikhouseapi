# AtypikHouse FLask REST API 

To use this API, you should first clone the  [repository](https://gitlab.com/Vwez/hatypikhouseapipython) from Gitlab.



You can  test this api in mode  Developpement mose: OnReadOnly and   OnWritable . 

##  Use HatypikHouse api OnWritable  developpement mode:


- Lunch docker compose on your tem: 
	
	 `
	 	sudo docker compose -f docker-compose.api.yml up
	 `
	 
	the API is running on  **[http://127.0.0.1:5000](http://127.0.0.1:5000)** 

    There is an administrator user created especially for you for testing purposes, here are their credentials:
	
	
	
		name : Doe
		firstname : Jhon
		email : Jhon.dor@@hatypikhouse.fr
		passwod: password
	

Enjoye Code :blush: 

##  Use HatypikHouse api OnReadOnly developpement mode:


<!-- - Connect database container with this commande:
Open a new term window, and type the following command `sudo docker compose exec hatypik_house_api_python-db-1 bash`

Once connected on database container , do the followind things:

 connect to mysql and run this commanse:

`mysql -u root -p <root password>`

- Create a new user:

`CREATE USER '<user>'@'localhost' IDENTIFIED BY '<user password>';`

- Grant him all privileges:


`GRANT ALL ON atypikhouse.* TO 'desir'@'localhost'` -->


## Code coverage

To produce the Code coverage, run the following command:

coverage run -m pytest
coverage html

To see the result, open the `index.html`  in `htmlcov` repository