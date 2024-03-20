#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Amenity",
            "Place",
            "Review"
    }

    def emptyline(self):
        """Ignore empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        # Create a new class instance with given keys/values and print its id.
        try:
            if not line:
                raise SyntaxError()
            myList = line.split(" ")

            kwargs = {}
            for i in range(1, len(myList)):
                key, value = tuple(myList[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                    kwargs[key] = value

            if kwargs == {}:
                obj = eval(myList[0])()
            else:
                obj = eval(myList[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line): 
        # Prints the string representation of an instance
        try:
            if not line:
                raise SyntaxError()
            myList = line.split(" ")
            if myList[0] not in self.__classes:
                raise NameError()
            if len(myList) < 2:
                raise IndexError()
            obj = storage.all()
            key = myList[0] + '.' + myList[1]
            if key in obj:
                print(obj[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        # Deletes an instance based on the class name and id
        try:
            if not line:
                raise SyntaxError()
            myList = line.split(" ")
            if myList[0] not in self.__classes:
                raise NameError()
            if len(myList) < 2:
                raise IndexError()
            obj = storage.all()
            key = myList[0] + '.' + myList[1]
            if key in obj:
                del obj[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        # Usage: all or all <class> or <class>.all()
        if not line:
            alof = storage.all()
            print([alof[k].__str__() for k in alof])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            alof = storage.all(eval(args[0]))
            print([alof[k].__str__() for k in alof])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        # Updates an instanceby adding or updating attribute
        try:
            if not line:
                raise SyntaxError()
            myList = split(line, " ")
            if myList[0] not in self.__classes:
                raise NameError()
            if len(myList) < 2:
                raise IndexError()
            obj = storage.all()
            key = myList[0] + '.' + myList[1]
            if key not in obj:
                raise KeyError()
            if len(myList) < 3:
                raise AttributeError()
            if len(myList) < 4:
                raise ValueError()
            val = obj[key]
            try:
                val.__dict__[myList[2]] = eval(myList[3])
            except Exception:
                val.__dict__[myList[2]] = myList[3]
                val.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        # count the number of instances of a class
        counter = 0
        try:
            myList = split(line, " ")
            if myList[0] not in self.__classes:
                raise NameError()
            obj = storage.all()
            for key in obj:
                name = key.split('.')
                if name[0] == myList[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        # strips the argument and return a string
        new_list = []
        new_list.append(args[0])
        try:
            myDict = eval(
                    args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            myDict = None
        if isinstance(myDict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            new_list.append(((new_str.split(", "))[0]).strip('"'))
            new_list.append(myDict)
            return new_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        new_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in new_list)

    def default(self, line):
        # retrieve all instances of a class and
        # retrieve the number of instances
        myList = line.split('.')
        if len(myList) >= 2:
            if myList[1] == "all()":
                self.do_all(myList[0])
            elif myList[1] == "count()":
                self.count(myList[0])
            elif myList[1][:4] == "show":
                self.do_show(self.strip_clean(myList))
            elif myList[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(myList))
            elif myList[1][:6] == "update":
                args = self.strip_clean(myList)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
