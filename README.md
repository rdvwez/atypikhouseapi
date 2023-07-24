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
		email : Jhon.doe@hatypikhouse.fr
		passwod: password
	

Enjoye Code :blush: 
##  Use HatypikHouse api OnReadOnly developpement mode:

comming soon .....

## User right presentation



Three user rigth are defne in Hatypik House: Admin, Owner and Customer
See in the following the table summarizing the accesses to the different parts of the perimeter according to the rights of the users





<table border="1">
    	<th>
    	    <td>Operations</td>
            <td>Admin</td>
            <td>Owner</td>
            <td>Customer</td>
        </th>
        <tr>
            <td rowspan="4">Categories</td>
            <td >Create</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Read</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr >
            <td>Delete</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
         <tr>
            <td rowspan="4">Thematics</td>
            <td >Create</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Read</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        <tr>
            <td>Delete</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td rowspan="4">Reservations</td>
            <td >Create</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Read</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Update</td>
             <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Delete</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td rowspan="4">Houses</td>
            <td >Create</td>
            <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Read</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Update</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Delete</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td rowspan="4">Properties</td>
            <td >Create</td>
             <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Read</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
             <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Delete</td>
             <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td rowspan="4">Vlues</td>
            <td >Create</td>
            <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Read</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
              <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Delete</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td rowspan="4">Images</td>
            <td >Create</td>
              <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Read</td>
            <td>✅️</td>
            <td>✅️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
              <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Delete</td>
              <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td rowspan="4">Users</td>
            <td >Create</td>
            <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Read</td>
            <td>✅️</td>
            <td>❌️</td>
            <td>❌️</td>
        </tr>
        <tr>
            <td>Update</td>
             <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
        <tr>
            <td>Delete</td>
            <td>✅️</td>
            <td>✅️</td>
            <td>✅️</td>
        </tr>
</table>

## Dashboard lists and accessbilities

|| Admin | Owner | Customer |
|:--------------|:--------------|:-------------:|--------------:|
| Category | ✅️ | ❌️ | ❌️|
| Thematic |  ✅️ | ❌️ | ❌️|
| House |  ✅️ | ✅️ | ❌️|
| Property |  ✅️ | ❌️ | ❌️|
| Value |  ✅️ | ✅️ | ❌️|
| Reservation |  ✅️ | ✅️ | ✅️|
| Image |  ✅️ | ✅️ | ✅️|
| User |  ✅️ | ❌️ | ❌️|



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