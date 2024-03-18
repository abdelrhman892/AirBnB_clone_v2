#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import re
import os
import uuid
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
        # Parse the command line to extract the class name, command, and arguments.
        _cmd = _cls = _id = _args = ''

        # Split the line into components
        parts = line.split()

        # Check if the line contains a class name
        if len(parts) >= 1 and parts[0] in HBNBCommand.dot_cmds:
            _cmd = parts[0]
        else:
            return line

        # Check if the line contains a command
        if len(parts) >= 2:
            _cls = parts[1]
        else:
            print("** class name missing **")
            return line

        if _cls not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return line

        # Check if the line contains an object ID
        if len(parts) >= 3:
            _args = ' '.join(parts[2:])

        # Construct the modified line with correct components
        line = '{} {} {}'.format(_cmd, _cls, _args)

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
        ignored_attrs = ('id', 'created_at', 'updated_at', '__class__')
        class_name = ''
        name_pattern = r'(?P<name>(?:[a-zA-Z]|_)(?:[a-zA-Z]|\d|_)*)'
        class_match = re.match(name_pattern, args)
        obj_kwargs = {}
        if class_match is not None:
            class_name = class_match.group('name')
            params_str = args[len(class_name):].strip()
            params = params_str.split(' ')
            str_pattern = r'(?P<t_str>"([^"]|\")*")'
            float_pattern = r'(?P<t_float>[-+]?\d+\.\d+)'
            int_pattern = r'(?P<t_int>[-+]?\d+)'
            param_pattern = '{}=({}|{}|{})'.format(
                    name_pattern,
                    str_pattern,
                    float_pattern,
                    int_pattern
                    )
            for param in params:
                param_match = re.fullmatch(param_pattern, param)
                if param_match is not None:
                    key_name = param_match.group('name')
                    str_v = param_match.group('t_str')
                    float_v = param_match.group('t_float')
                    int_v = param_match.group('t_int')
                    if float_v is not None:
                        obj_kwargs[key_name] = float(float_v)
                    elif int_v is not None:
                        obj_kwargs[key_name] = int(int_v)
                    elif str_v is not None:
                        obj_kwargs[key_name] = str_v[1:-1].replace('_', ' ')
        else:
            class_name = args
        if not class_name:
            print("** class name missing **")
            return
        elif class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            if 'id' not in obj_kwargs:
                obj_kwargs['id'] = str(uuid.uuid4())
            if 'created_at' not in obj_kwargs:
                obj_kwargs['created_at'] = str(datetime.now())
            if 'updated_at' not in obj_kwargs:
                obj_kwargs['updated_at'] = str(datetime.now())
            new_instance = HBNBCommand.classes[class_name](**obj_kwargs)
            new_instance.save()
            print(new_instance.id)
        else:
            new_instance = HBNBCommand.classes[class_name]()
            for key, value in obj_kwargs.items():
                if key not in ignored_attrs:
                    setattr(new_instance, key, value)
            new_instance.save()
            print(new_instance.id)

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
