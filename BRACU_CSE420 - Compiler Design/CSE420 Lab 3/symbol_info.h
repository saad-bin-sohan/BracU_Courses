#include <iostream>
#include <string>
#include <vector>
#include <list>

using namespace std;

class symbol_info
{
private:
    string name;
    string type;
    bool is_float;
    symbol_info *next;


    string data_type;
    bool is_array;
    int array_size;

  
    bool is_function;
    string return_type;
    vector<pair<string, string> > parameters;
    bool is_operation;
    bool is_undefined_function;

public:
   
    symbol_info()
    {
        next = NULL;
        is_array = false;
        array_size = 0;
        is_function = false;
        is_operation = false;
        is_undefined_function = false;
    }
    symbol_info(string name, string type)
    {
        this->name = name;
        this->type = type;
        next = NULL;
        is_array = false;
        array_size = 0;
        is_function = false;
        is_operation = false;
        is_undefined_function = false;
    }
    symbol_info(string name, string type, string data_type)
    {
        this->name = name;
        this->type = type;
        this->data_type = data_type;
        next = NULL;
        is_array = false;
        array_size = 0;
        is_function = false;
        is_operation = false;
        is_undefined_function = false;
    }
    symbol_info(string name, string type, string data_type, int array_size)
    {
        this->name = name;
        this->type = type;
        this->data_type = data_type;
        this->array_size = array_size;
        this->is_array = true;
        next = NULL;
        is_function = false;
        is_operation = false;
        is_undefined_function = false;

    }
    symbol_info(string name, string type, string return_type, vector<pair<string, string> > params)
    {
        this->name = name;
        this->type = type;
        this->return_type = return_type;
        this->parameters = params;
        this->is_function = true;
        next = NULL;
        is_array = false;
        array_size = 0;
    }
    string getname() { return name; }
    string gettype() { return type; }
    symbol_info *getnext() { return next; }
    string get_data_type() { return data_type; }
    bool get_is_array() { return is_array; }
    int get_array_size() { return array_size; }
    bool get_is_function() { return is_function; }
    string get_return_type() { return return_type; }
    bool get_is_float() { return is_float; }
    vector<pair<string, string> > get_parameters() { return parameters; }
    bool get_is_operation() { return is_operation; }
    bool get_is_undefined_function() { return is_undefined_function; }
    void setname(string name) { this->name = name; }
    void settype(string type) { this->type = type; }
    void set_is_float(bool fl) { this->is_float = fl; }
    void set_is_array(bool arr) { this->is_array = arr; }
    void setnext(symbol_info *next) { this->next = next; }
    void set_data_type(string data_type) { this->data_type = data_type; }
    void set_is_operation() { this->is_operation = true; }
    void set_is_undefined_function() { this->is_undefined_function = true; }
    void set_array_size(int size)
    {
        this->array_size = size;
        this->is_array = true;
    }
    void set_as_function(string return_type, vector<pair<string, string> > params)
    {
        this->is_function = true;
        this->return_type = return_type;
        this->parameters = params;
    }
    ~symbol_info()
    {
        if (next)
            delete next;
    }
};