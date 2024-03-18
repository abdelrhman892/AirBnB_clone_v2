<center> <h1>HBNB - The Console</h1> </center>

This project is a Command Line Interface (CLI) for managing Airbnb listings.
    It provides functionalities to interact with Airbnb listings through the command line,
    enabling users to search for properties, book accommodations,
    manage reservations, and more

<center><h3>Repository Contents by Project Task</h3> </center>

| Tasks | Files | Description |
| ----- | ----- | ------ |
| 0: Authors/README File | [AUTHORS](https://github.com/justinmajetich/AirBnB_clone/blob/dev/AUTHORS) | Project authors |
| 1: Pep8 | N/A | All code is pep8 compliant|
| 2: Unit Testing | [/tests](https://github.com/justinmajetich/AirBnB_clone/tree/dev/tests) | All class-defining modules are unittested |
| 3. Make BaseModel | [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Defines a parent class to be inherited by all model classes|
| 4. Update BaseModel w/ kwargs | [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Add functionality to recreate an instance of a class from a dictionary representation|
| 5. Create FileStorage class | [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) [/models/_ _init_ _.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/__init__.py) [/models/base_model.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/base_model.py) | Defines a class to manage persistent file storage system|
| 6. Console 0.0.1 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) | Add basic functionality to console program, allowing it to quit, handle empty lines and ^D |
| 7. Console 0.1 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) | Update the console with methods allowing the user to create, destroy, show, and update stored data |
| 8. Create User class | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py) | Dynamically implements a user class |
| 9. More Classes | [/models/user.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/user.py) [/models/place.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/place.py) [/models/city.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/city.py) [/models/amenity.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/amenity.py) [/models/state.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/state.py) [/models/review.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/review.py) | Dynamically implements more classes |
| 10. Console 1.0 | [console.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/console.py) [/models/engine/file_storage.py](https://github.com/justinmajetich/AirBnB_clone/blob/dev/models/engine/file_storage.py) | Update the console and file storage system to work dynamically with all  classes update file storage |
<br>
<br>
<center> <h2>General Use</h2> </center>

1. First plz clone this repository.

3. Once the repository is cloned locate the "console.py" file and run it as follows:
```
/AirBnB_clone$ ./console.py
```
4. When this command is run the following prompt should appear:
```
(hbnb)
```
5. This prompt designates you are in the "HBnB" console. There are a variety of commands available within the console program.

## How to Use
    Once the command interpreter is running,
    you can use various commands to interact with Airbnb listings.
    The prompt  will be (hbnb).
    Here are some of the basic commands:

| Commands      | How to use                                                                                                                                 |
|---------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| ```quit```    | Quits the console                                                                                                                          |
| ```Ctrl+D```  | Quits the console `EOF`                                                                                                                    |
| ```help```    | ```help <command>``` Displays all commands or Displays instructions for a specific command                                                 |
| ```create```  | ```create <class_name>``` Creates an object of type , saves it to a JSON file, and prints the objects ID                                   |
| ```show```    | ```show <class_name> <id>``` Shows string representation of an object                                                                      |
| ```destroy``` | ```destroy <class> <ID>``` Deletes an objects                                                                                              |
| ```all```     | ```all <class>``` Prints all string representations of all objects or Prints all string representations of all objects of a specific class |
| ```update```  | ```update <class> <id> <attribute name> "<attribute value>"``` Updates an object with a certain attribute (new or existing)                |
| ```count```   | ```Return number of object instances by class```

## examples 
    
```
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update
```    
```
(hbnb) create BaseModel
7fa29982-fe32-4dcc-aca5-35a4a249a517
```
```
(hbnb) all
["[BaseModel] (7fa29982-fe32-4dcc-aca5-35a4a249a517) {'id': '7fa29982-fe32-4dcc-aca5-35a4a249a517',
 'created_at': datetime.datetime(2024, 2, 11, 0, 37, 56, 34761),
 'updated_at': datetime.datetime(2024, 2, 11, 0, 37, 56, 35762)}"]
```
```
(hbnb) show BaseModel 7fa29982-fe32-4dcc-aca5-35a4a249a517
[BaseModel] (7fa29982-fe32-4dcc-aca5-35a4a249a517) {
'id': '7fa29982-fe32-4dcc-aca5-35a4a249a517', 
'created_at': datetime.datetime(2024, 2, 11, 0, 37, 56, 34761), 
'updated_at': datetime.datetime(2024, 2, 11, 0, 37, 56, 35762)}
```
```
(hbnb) update BaseModel 7fa29982-fe32-4dcc-aca5-35a4a249a517 first_name "jhin"
(hbnb) show BaseModel 7fa29982-fe32-4dcc-aca5-35a4a249a517
[BaseModel] (7fa29982-fe32-4dcc-aca5-35a4a249a517) {
 'id': '7fa29982-fe32-4dcc-aca5-35a4a249a517',
 'created_at': datetime.datetime(2024, 2, 11, 0, 37, 56, 34761),
 'updated_at': datetime.datetime(2024, 2, 11, 0, 42, 9, 309604), 
 'first_name': 'jhin'}
```
```
(hbnb) destroy BaseModel 7fa29982-fe32-4dcc-aca5-35a4a249a517
(hbnb) show BaseModel 7fa29982-fe32-4dcc-aca5-35a4a249a517
** no instance found **
```
```
(hbnb) quit {you closed the project}
(hbnh) EOF {you closed the project}
```

