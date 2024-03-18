#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
               }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
            'number_rooms': int, 'number_bathrooms': int,
            'max_guest': int, 'price_by_night': int,
            'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # Parse line left to right
            pline = line[:]

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple
                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) == dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])
        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
            return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return

        # Define current_time
        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

        # Split the arguments into class name and parameters
        args_list = args.split()
        class_name = args_list[0]

        # Check if the class exists
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # check if the class exists
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Initialize an empty dictionary to store parameters
        params = {}

        # Check if parameters are provided
        if len(args_list) > 1:
            # Iterate through remaining arguments
            for arg in args_list[1:]:
                # Split each arguments
                key, value = arg.split('=')

                #Process the value according to its syntax
                if value.startswith('"') and value.endswith('"'):
                    #String value
                    value = value[1:-1]  # Remove quotes
                    value = value.replace('_',' ')  # Replace underscores with spaces
                    value = value.replace('\\"','"')  # Unescape double quotes
                elif '.' in value:
                    # Float value
                    try:
                        value = float(value)
                    except ValueError:
                        # Skip this parameter if it can't be converted to float
                        continue
                else:
                    # Integer Value
                    try:
                        value = int(value)
                    except ValueError:
                        # Skip this parameter if it can't be converted to integer
                        continue

                # Add the parameter to the dictionary
                params[key] = value

        # Set the updates_at attribute to current datetime
        if 'updated_at' not in params:
            params['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
            if 'created_at' not in params:
                params['created_at'] = current_time
            if 'updated_at' not in params:
                params['updated_at'] = current_time
        
        # Create an instance of te specified class with the extracted parameters
        try:
             new_instance = HBNBCommand.classes[class_name](**params)
             new_instance.save()
             print(new_instance.id)
        except Exception as e:
             print("** Error creating instance: {} **".format(e))

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            obj = storage.all()[key]
            print(obj)
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        # Done with the update
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        # Retrieve the object from the storage by the given
        # class name and ID
        try:
            obj = storage.all()[key]
            if obj:
                del storage.all()[key]
                storage.save()
                print("Deleted: ", key)
            else:
                print("** no instance found**")
        except Exception as e:
            print("** Error: ", str(e))

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        # Done with some more fixing
        
        if args:
            class_name = args.split()[0]  # Extract class name from args

            if class_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return

            # Retrieve objects of specified class
            objects = storage.all(class_name).values()
            print_list = [str(obj) for obj in objects]
        else:
            # Retrieve all objects from database
            objects = storage.all().values()
            print_list = [str(obj) for obj in objects]

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        # Done
        if not args:
            print("** class name missing **")
            return

        class_name = args.split()[0]  # Extract class name from args

        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Retrieve objects of the specified class
        objects = storage.all().values()
        count = sum(1 for obj in objects
                    if obj.__class__.__name__ == class_name)

        print(count)

    def help_count(self):
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        # Done update
        c_name = c_id = att_name = att_val = kwargs = ''

        # Parse arguments
        args_list = args.split()
        if len(args_list) < 4:
            print("** Not enough arguments **")
            return

        # Extract class name, ID, attribute name, and attribute value
        c_name = args_list[0]
        c_id = args_list[1]
        att_name = args_list[2]
        att_val = " ".join(args_list[3:])

        # check of class name exists
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Generate key from class name and ID
        key = c_name + "." + c_id

        # check of objects exist
        if key not in storage.all():
            print("** no instance found **")
            return

        # Retrieve the object from storage
        obj = storage.all()[key]

        # Update the attribute with new value
        setattr(obj, att_name, att_val)
        obj.save()

        print("Object updated successfully")

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
