%{

#include "symbol_table.h"

#include <cstring>

#define YYSTYPE symbol_info*

extern FILE *yyin;
int yyparse(void);
int yylex(void);
extern YYSTYPE yylval;

// symbol table here.
symbol_table *table;

// global variables 
string current_type;
string current_func_name;
string current_func_return_type;
vector<pair<string, string> > current_func_params;
//helper functions
bool is_function_definition = false;
bool error_found = false;

int lines = 1;
ofstream outlog;
ofstream errlog;

int error_count = 0;

void yyerror(const char *s)
{
    outlog << "Error at line " << lines << ": " << s << endl << endl;
    error_found = true;
}

// check for function declaration 
bool is_function_declared(string name) {
    symbol_info* temp = new symbol_info(name, "ID");
    symbol_info* found = table->lookup(temp);
    delete temp;
    return found != NULL && found->get_is_function();
}

// check for variable in current scope
bool is_variable_declared_current_scope(string name) {
    symbol_info* temp = new symbol_info(name, "ID");
    symbol_info* found = table->lookup_current_scope(temp);
    delete temp;
    return found != NULL;
}

symbol_info* get_variable_info(string name) {
	symbol_info* temp = new symbol_info(name, "ID");
	symbol_info* found = table->lookup(temp);
	delete temp;
	return found;
}

%}

%token IF ELSE FOR WHILE DO BREAK INT CHAR FLOAT DOUBLE VOID RETURN SWITCH CASE DEFAULT CONTINUE PRINTLN ADDOP MULOP INCOP DECOP RELOP ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD COMMA SEMICOLON CONST_INT CONST_FLOAT ID

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%

start : program
	{
		outlog << "At line no: " << lines << " start : program " << endl << endl;
		table->print_all_scopes(outlog);
	}
	;

program : program unit
	{
		outlog << "At line no: " << lines << " program : program unit " << endl << endl;
		outlog << $1->getname() + "\n" + $2->getname() << endl << endl;
		$$ = new symbol_info($1->getname() + "\n" + $2->getname(), "program");
	}
	| unit
	{
		outlog << "At line no: " << lines << " program : unit " << endl << endl;
		outlog << $1->getname() << endl << endl;
		$$ = new symbol_info($1->getname(), "program");
	}
	;

unit : var_declaration
	 {
		outlog << "At line no: " << lines << " unit : var_declaration " << endl << endl;
		outlog << $1->getname() << endl << endl;
		$$ = new symbol_info($1->getname(), "unit");
	 }
     | func_definition
     {
		outlog << "At line no: " << lines << " unit : func_definition " << endl << endl;
		outlog << $1->getname() << endl << endl;
		$$ = new symbol_info($1->getname(), "unit");
	 }
     ;

func_definition : type_specifier ID LPAREN parameter_list RPAREN {
			// Create and insert function symbol before compound statement
		
			if(!is_function_declared($2->getname()) && !is_variable_declared_current_scope($2->getname())) {

				vector<pair<string, string> > params = current_func_params;
				current_func_name= $2->getname();
				symbol_info* func = new symbol_info($2->getname(), "ID", $1->getname());
				func->set_as_function($1->getname(), params);
				table->insert(func);
			}else{
				outlog << "At line no: " << lines << ": Multiple declaration of function " << $2->getname() << endl << endl;
				errlog << "At line no: " << lines << ": Multiple declaration of function " << $2->getname() << endl << endl;
				error_count++;
			}

		    // The function definition is complete.
            // You can now insert necessary information about the function into the symbol table
           // However, note that the scope of the function and the scope of the compound statement are different.

		} compound_statement
		{	
			outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement " << endl << endl;
			outlog << $1->getname() << " " << $2->getname() << "(" + $4->getname() + ")\n" << $7->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + " " + $2->getname() + "(" + $4->getname() + ")\n" + $7->getname(), "func_def");	
			
			// Clear function parameters for next function
			current_func_params.clear();
			
		}
		| type_specifier ID LPAREN RPAREN {
			// Create and insert function symbol before compound statement
			if(!is_function_declared($2->getname())) {
				vector<pair<string, string> > params;
				symbol_info* func = new symbol_info($2->getname(), "ID", $1->getname());
				func->set_as_function($1->getname(), params);
				table->insert(func);
			}
			
		} compound_statement
		{
			outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN RPAREN compound_statement " << endl << endl;
			outlog << $1->getname() << " " << $2->getname() << "()\n" << $6->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + " " + $2->getname() + "()\n" + $6->getname(), "func_def");	
		}
		;

parameter_list : parameter_list COMMA type_specifier ID
		{
			outlog << "At line no: " << lines << " parameter_list : parameter_list COMMA type_specifier ID " << endl << endl;
			outlog << $1->getname() << "," << $3->getname() << " " << $4->getname() << endl << endl;
					
			$$ = new symbol_info($1->getname() + "," + $3->getname() + " " + $4->getname(), "param_list");
			
			// Store parameter info
			pair<string, string> param($3->getname(), $4->getname());
			if(!current_func_params.empty()) {
				for(auto param : current_func_params) {
					if(param.second==$4->getname()) {
						outlog << "At line no: " << lines << ": Multiple declaration of parameter " << $4->getname() << " in a parameter of " << current_func_name <<endl << endl;
						errlog << "At line no: " << lines << ": Multiple declaration of parameter " << $4->getname() << " in a parameter of " << current_func_name <<endl << endl;
						error_count++;
					}
				}
			}

			current_func_params.push_back(param);
		}
		| parameter_list COMMA type_specifier
		{
			outlog << "At line no: " << lines << " parameter_list : parameter_list COMMA type_specifier " << endl << endl;
			outlog << $1->getname() << "," << $3->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + "," + $3->getname(), "param_list");
			
			//storing  the necessary information about the function parameters
			// They will be needed when you want to enter the function into the symbol table
			pair<string, string> param($3->getname(), "");
			current_func_params.push_back(param);
		}
 		| type_specifier ID
 		{
			outlog << "At line no: " << lines << " parameter_list : type_specifier ID " << endl << endl;
			outlog << $1->getname() << " " << $2->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + " " + $2->getname(), "param_list");
			
			//storing  the necessary information about the function parameters
			// They will be needed when you want to enter the function into the symbol table

			pair<string, string> param($1->getname(), $2->getname());
			current_func_params.push_back(param);
		}
		| type_specifier
		{
			outlog << "At line no: " << lines << " parameter_list : type_specifier " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "param_list");
			
			// Store parameter info without name
			pair<string, string> param($1->getname(), "");
			current_func_params.push_back(param);
		}
 		;

compound_statement : LCURL {
		// Enter a new scope
		table->enter_scope();
		
		// If we're in a function definition, add parameters to current scope
		if(!current_func_params.empty()) {
			for(auto param : current_func_params) {
				if(!param.second.empty()) {
					symbol_info* param_symbol = new symbol_info(param.second, "ID", param.first);
					table->insert(param_symbol);
				}
			}
		}
	} statements RCURL
	{ 
		outlog << "At line no: " << lines << " compound_statement : LCURL statements RCURL " << endl << endl;
		outlog << "{\n" + $3->getname() + "\n}" << endl << endl;
		
		// Print current scope before exiting
		table->print_current_scope();
		
		// Exit the current scope
		table->exit_scope();
		
		$$ = new symbol_info("{\n" + $3->getname() + "\n}", "comp_stmnt");
	}
	| LCURL {
		// Enter a new scope
		table->enter_scope();
	} RCURL
	{ 
		outlog << "At line no: " << lines << " compound_statement : LCURL RCURL " << endl << endl;
		outlog << "{\n}" << endl << endl;
		
		// Print current scope before exiting
		table->print_current_scope();
		
		// Exit the current scope
		table->exit_scope();
		
		$$ = new symbol_info("{\n}", "comp_stmnt");
	}
	;
 		    
var_declaration : type_specifier declaration_list SEMICOLON
		 {
			outlog << "At line no: " << lines << " var_declaration : type_specifier declaration_list SEMICOLON " << endl << endl;
			outlog << $1->getname() << " " << $2->getname() << ";" << endl << endl;
			
			$$ = new symbol_info($1->getname() + " " + $2->getname() + ";", "var_dec");
			
			// Store the current type for use in declaration_list
			current_type = $1->getname();
			if (current_type == "void") {
				outlog << "At line no: " << lines << " variable type cannot be void" << endl << endl;
				errlog << "At line no: " << lines << " variable type cannot be void" << endl << endl;
				error_count++;
			}
		 
			
			
			if(current_type == "void") {
				yyerror("Variable type cannot be void");
			}
		 }
 		 ;

type_specifier : INT
		{
			outlog << "At line no: " << lines << " type_specifier : INT " << endl << endl;
			outlog << "int" << endl << endl;
			
			$$ = new symbol_info("int", "type");
			current_type = "int";
	    }
 		| FLOAT
 		{
			outlog << "At line no: " << lines << " type_specifier : FLOAT " << endl << endl;
			outlog << "float" << endl << endl;
			
			$$ = new symbol_info("float", "type");
			current_type = "float";
	    }
 		| VOID
 		{
			outlog << "At line no: " << lines << " type_specifier : VOID " << endl << endl;
			outlog << "void" << endl << endl;
			
			$$ = new symbol_info("void", "type");
			current_type = "void";
	    }
 		;

declaration_list : declaration_list COMMA ID
		  {
 		  	outlog << "At line no: " << lines << " declaration_list : declaration_list COMMA ID " << endl << endl;
 		  	outlog << $1->getname() + "," << $3->getname() << endl << endl;
			$$ = new symbol_info($1->getname() + "," + $3->getname(), "decl_list");

            // check if variable already declared in current scope
            if(is_variable_declared_current_scope($3->getname())) {
                $$ = new symbol_info($1->getname() + "," + $3->getname(), "decl_list");
				outlog << "At line no: " << lines << ": Multiple declaration of variable " << $3->getname() << endl << endl;
				errlog << "At line no: " << lines << ": Multiple declaration of variable " << $3->getname() << endl << endl;
				error_count++;
				
            } else {
                // Create and insert new variable
                symbol_info* new_var = new symbol_info($3->getname(), "ID", current_type);
                table->insert(new_var);
                $$ = new symbol_info($1->getname() + "," + $3->getname(), "decl_list");
            }
 		  }
 		  | declaration_list COMMA ID LTHIRD CONST_INT RTHIRD //array after some declaration
 		  {
 		  	outlog << "At line no: " << lines << " declaration_list : declaration_list COMMA ID LTHIRD CONST_INT RTHIRD " << endl << endl;
 		  	outlog << $1->getname() + "," << $3->getname() << "[" << $5->getname() << "]" << endl << endl;
			$$ = new symbol_info($1->getname() + "," + $3->getname() + "[" + $5->getname() + "]", "decl_list");

            // Check if array already declared in current scope
            if(is_variable_declared_current_scope($3->getname())) {
                // Silently ignore multiple declarations
				outlog << "At line no: " << lines << ": Multiple declaration of variable " << $3->getname() << endl << endl;
				errlog << "At line no: " << lines << ": Multiple declaration of variable " << $3->getname() << endl << endl;
				error_count++;
                $$ = new symbol_info($1->getname() + "," + $3->getname() + "[" + $5->getname() + "]", "decl_list");
            } else {
                // Create and insert new array
                int size = stoi($5->getname());
                symbol_info* new_array = new symbol_info($3->getname(), "ID", current_type, size);
                table->insert(new_array);
                $$ = new symbol_info($1->getname() + "," + $3->getname() + "[" + $5->getname() + "]", "decl_list");
            }
 		  }
 		  |ID
 		  {
 		  	outlog << "At line no: " << lines << " declaration_list : ID " << endl << endl;
			outlog << $1->getname() << endl << endl;
			$$ = new symbol_info($1->getname(), "decl_list");

            // Check if variable already declared in current scope
            if(is_variable_declared_current_scope($1->getname())) {
                // Silently ignore multiple declarations
				outlog << "At line no: " << lines << ": Multiple declaration of variable " << $1->getname() << endl << endl;
				errlog << "At line no: " << lines << ": Multiple declaration of variable " << $1->getname() << endl << endl;
				error_count++;
                $$ = new symbol_info($1->getname(), "decl_list");
            } else {
                // Create and insert new variable
                symbol_info* new_var = new symbol_info($1->getname(), "ID", current_type);
                table->insert(new_var);
                $$ = new symbol_info($1->getname(), "decl_list");
            }
 		  }
 		  | ID LTHIRD CONST_INT RTHIRD //array
 		  {
 		  	outlog << "At line no: " << lines << " declaration_list : ID LTHIRD CONST_INT RTHIRD " << endl << endl;
			outlog << $1->getname() << "[" << $3->getname() << "]" << endl << endl;
			$$ = new symbol_info($1->getname() + "[" + $3->getname() + "]", "decl_list");

            // Check if array already declared in current scope
            if(is_variable_declared_current_scope($1->getname())) {
                // Silently ignore multiple declarations
				outlog << "At line no: " << lines << ": Multiple declaration of variable " << $1->getname() << endl << endl;
				errlog << "At line no: " << lines << ": Multiple declaration of variable " << $1->getname() << endl << endl;
				error_count++;
                $$ = new symbol_info($1->getname() + "[" + $3->getname() + "]", "decl_list");
            } else {
                // Create and insert new array
                int size = stoi($3->getname());
                symbol_info* new_array = new symbol_info($1->getname(), "ID", current_type, size);
                table->insert(new_array);
                $$ = new symbol_info($1->getname() + "[" + $3->getname() + "]", "decl_list");
            }
 		  }
 		  ;
 		  

statements : statement
	   {
	    	outlog << "At line no: " << lines << " statements : statement " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "stmnts");
	   }
	   | statements statement
	   {
	    	outlog << "At line no: " << lines << " statements : statements statement " << endl << endl;
			outlog << $1->getname() << "\n" << $2->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + "\n" + $2->getname(), "stmnts");
	   }
	   ;
	   
statement : var_declaration
	  {
	    	outlog << "At line no: " << lines << " statement : var_declaration " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "stmnt");
	  }
	  | func_definition
	  {
	  		outlog << "At line no: " << lines << " statement : func_definition " << endl << endl;
            outlog << $1->getname() << endl << endl;

            $$ = new symbol_info($1->getname(), "stmnt");
	  		
	  }
	  | expression_statement
	  {
	    	outlog << "At line no: " << lines << " statement : expression_statement " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "stmnt");
	  }
	  | compound_statement
	  {
	    	outlog << "At line no: " << lines << " statement : compound_statement " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "stmnt");
	  }
	  | FOR LPAREN expression_statement expression_statement expression RPAREN statement
	  {
	    	outlog << "At line no: " << lines << " statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement " << endl << endl;
			outlog << "for(" << $3->getname() << $4->getname() << $5->getname() << ")\n" << $7->getname() << endl << endl;
			
			$$ = new symbol_info("for(" + $3->getname() + $4->getname() + $5->getname() + ")\n" + $7->getname(), "stmnt");
	  }
	  | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
	  {
	    	outlog << "At line no: " << lines << " statement : IF LPAREN expression RPAREN statement " << endl << endl;
			outlog << "if(" << $3->getname() << ")\n" << $5->getname() << endl << endl;
			
			$$ = new symbol_info("if(" + $3->getname() + ")\n" + $5->getname(), "stmnt");
	  }
	  | IF LPAREN expression RPAREN statement ELSE statement
	  {
	    	outlog << "At line no: " << lines << " statement : IF LPAREN expression RPAREN statement ELSE statement " << endl << endl;
			outlog << "if(" << $3->getname() << ")\n" << $5->getname() << "\nelse\n" << $7->getname() << endl << endl;
			
			$$ = new symbol_info("if(" + $3->getname() + ")\n" + $5->getname() + "\nelse\n" + $7->getname(), "stmnt");
	  }
	  | WHILE LPAREN expression RPAREN statement
	  {
	    	outlog << "At line no: " << lines << " statement : WHILE LPAREN expression RPAREN statement " << endl << endl;
			outlog << "while(" << $3->getname() << ")\n" << $5->getname() << endl << endl;
			
			$$ = new symbol_info("while(" + $3->getname() + ")\n" + $5->getname(), "stmnt");
	  }
	  | PRINTLN LPAREN ID RPAREN SEMICOLON
	  {
	    	outlog << "At line no: " << lines << " statement : PRINTLN LPAREN ID RPAREN SEMICOLON " << endl << endl;
			outlog << "printf(" << $3->getname() << ");" << endl << endl; 

			symbol_info * var_info = get_variable_info($3->getname());
			if (var_info==NULL){
				outlog << "At line no: " << lines << " Undeclared variable " << $3->getname() << endl << endl;
				errlog << "At line no: " << lines << " Undeclared variable " << $3->getname() << endl << endl;
				error_count++;
			}
			
			$$ = new symbol_info("printf(" + $3->getname() + ");", "stmnt");
	  }
	  | RETURN expression SEMICOLON
	  {
	    	outlog << "At line no: " << lines << " statement : RETURN expression SEMICOLON " << endl << endl;
			outlog << "return " << $2->getname() << ";" << endl << endl;
			
			$$ = new symbol_info("return " + $2->getname() + ";", "stmnt");
	  }
	  ;
	  
expression_statement : SEMICOLON
			{
				outlog << "At line no: " << lines << " expression_statement : SEMICOLON " << endl << endl;
				outlog << ";" << endl << endl;
				
				$$ = new symbol_info(";", "expr_stmt");
	        }			
			| expression SEMICOLON 
			{
				outlog << "At line no: " << lines << " expression_statement : expression SEMICOLON " << endl << endl;
				outlog << $1->getname() << ";" << endl << endl;
				
				$$ = new symbol_info($1->getname() + ";", "expr_stmt");
	        }
			;
	  
variable : ID 	
      {
	    outlog << "At line no: " << lines << " variable : ID " << endl << endl;
		outlog << $1->getname() << endl << endl;
		symbol_info* var_info = get_variable_info($1->getname());
		

		if (var_info==NULL){
			outlog << "At line no: " << lines << " Undeclared variable " << $1->getname() << endl << endl;
			errlog << "At line no: " << lines << " Undeclared variable " << $1->getname() << endl << endl;
			error_count++;
			$$ = new symbol_info($1->getname(), "Not_declared_var");
			$$->set_is_undefined_function();
		}
		else{
			$$ = new symbol_info($1->getname(), "varbl");
			$$->set_data_type(var_info->get_data_type());
			if (lines==44){
			}  // Set float flag if var_info is float
		}

		if (var_info!=NULL && var_info->get_is_array()){
			outlog << "At line no: " << lines << " Variable is of array type: " << $1->getname()<< endl << endl;
			errlog << "At line no: " << lines << " Variable is of array type: " << $1->getname()<< endl << endl;
			error_count++;
		}
	  
		
		
		
	 }	
	 | ID LTHIRD expression RTHIRD 
	 {
	 	outlog << "At line no: " << lines << " variable : ID LTHIRD expression RTHIRD " << endl << endl;
		outlog << $1->getname() << "[" << $3->getname() << "]" << endl << endl;
		symbol_info* var_info = get_variable_info($1->getname());
		$$ = new symbol_info($1->getname() + "[" + $3->getname() + "]", "varbl");
		$$->set_is_array(var_info->get_is_array());
		$$->set_data_type(var_info->get_data_type());  // Set data type of the array

		if (!var_info->get_is_array()){
			outlog << "At line no: " << lines << " variable is not of array type : " << $1->getname()<< endl << endl;
			errlog << "At line no: " << lines << " variable is not of array type : " << $1->getname()<< endl << endl;
			error_count++;
		}
		if ($3->get_data_type()!="int"){
			outlog << "At line no: " << lines << " array index is not of integer type:" << $1->getname() << endl << endl;
			errlog << "At line no: " << lines << " array index is not of integer type:" << $1->getname() << endl << endl;
			error_count++;
		}
	 }
	 ;
	 
expression : logic_expression
	   {
	    	outlog << "At line no: " << lines << " expression : logic_expression " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "expr");
			$$->set_data_type($1->get_data_type());  // Set float flag if logic_expression is float
	   }
	   | variable ASSIGNOP logic_expression 	
	   {
	    	outlog << "At line no: " << lines << " expression : variable ASSIGNOP logic_expression " << endl << endl;
			outlog << $1->getname() << "=" << $3->getname() << endl << endl;



			if (!is_variable_declared_current_scope($3->getname())) {

				if($3->get_is_operation()){
					//pass

				}else if($3->get_is_function()){
					if ($1->get_data_type()!=$3->get_return_type()){

						outlog << "At line no: " << lines << " operation on void type " << endl << endl;
						errlog << "At line no: " << lines << " operation on void type " << endl << endl;
						error_count++;
					}
				}else if ($1->get_data_type()!=$3->get_data_type() && $3->get_is_undefined_function()==false && $1->get_is_undefined_function()==false){
					outlog << "At line no: " << lines << " Warning: Assignment of " << $3->get_data_type()<<" value into variable of "<<$1->get_data_type()<<" type" << endl << endl;
					errlog << "At line no: " << lines << " Warning: Assignment of " << $3->get_data_type()<<" value into variable of "<<$1->get_data_type()<<" type" << endl << endl;
					error_count++;
				}}

			


			$$ = new symbol_info($1->getname() + "=" + $3->getname(), "expr");
	   }
	   ;
			
logic_expression : rel_expression
	     {
	    	outlog << "At line no: " << lines << " logic_expression : rel_expression " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "lgc_expr");
			$$->set_data_type($1->get_data_type());  // Set float flag if rel_expression is float
			if ($1->get_is_function()){
				$$->set_as_function($1->get_return_type(),$1->get_parameters());
			}
			if ($1->get_is_operation()){
				$$->set_is_operation();
			}
			if ($1->get_is_undefined_function()){
				$$->set_is_undefined_function();
			}

	     }	
		 | rel_expression LOGICOP rel_expression 
		 {
	    	outlog << "At line no: " << lines << " logic_expression : rel_expression LOGICOP rel_expression " << endl << endl;
			outlog << $1->getname() << $2->getname() << $3->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + $2->getname() + $3->getname(), "lgc_expr");
			$$->set_data_type("int");
	     }	
		 ;
			
rel_expression	: simple_expression
		{
	    	outlog << "At line no: " << lines << " rel_expression : simple_expression " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "rel_expr");
			$$->set_data_type($1->get_data_type());  // Set float flag if simple_expression is float
			if ($1->get_is_function()){
				$$->set_as_function($1->get_return_type(),$1->get_parameters());
			}
			
			if ($1->get_is_operation()){
				$$->set_is_operation();
			}
			if ($1->get_is_undefined_function()){
				$$->set_is_undefined_function();
			}

	    }
		| simple_expression RELOP simple_expression
		{
	    	outlog << "At line no: " << lines << " rel_expression : simple_expression RELOP simple_expression " << endl << endl;
			outlog << $1->getname() << $2->getname() << $3->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + $2->getname() + $3->getname(), "rel_expr");
			$$->set_data_type("int");
	    }
		;
				
simple_expression : term
          {
	    	outlog << "At line no: " << lines << " simple_expression : term " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "simp_expr");
			$$->set_data_type($1->get_data_type());  // Set float flag if term is float
			if ($1->get_is_function()){
				$$->set_as_function($1->get_return_type(),$1->get_parameters());
			}

			if ($1->get_is_operation()){
				$$->set_is_operation();
			}
			if ($1->get_is_undefined_function()){
				$$->set_is_undefined_function();
			}
			
	      	}
		  | simple_expression ADDOP term 
		  {
	    	outlog << "At line no: " << lines << " simple_expression : simple_expression ADDOP term " << endl << endl;
			outlog << $1->getname() << $2->getname() << $3->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + $2->getname() + $3->getname(), "simp_expr");
			$$->set_is_operation();
	      }
		  ;
					
term :	unary_expression //term can be void because of un_expr->factor
     {
	    	outlog << "At line no: " << lines << " term : unary_expression " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "term");
			$$->set_data_type($1->get_data_type());  // Set float flag if unary_expression is float
			if ($1->get_is_function()){
				$$->set_as_function($1->get_return_type(),$1->get_parameters());
			}
			if ($1->get_is_undefined_function()){
				$$->set_is_undefined_function();
			}

			
	 }
     |  term MULOP unary_expression
     {
	    	outlog << "At line no: " << lines << " term : term MULOP unary_expression " << endl << endl;
			outlog << $1->getname() << $2->getname() << $3->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + $2->getname() + $3->getname(), "operation");
			$$->set_is_operation();

			if ($2->getname() == "/" || $2->getname() == "%"){
				if ($3->getname()=="0" && $2->getname()=="/" ){
					outlog << "At line no: " << lines << " Division by 0" << endl << endl;
					errlog << "At line no: " << lines << " Division by 0 " << endl << endl;
					error_count++;
				}
				if ($3->getname()=="0" && $2->getname()=="%" ){
					outlog << "At line no: " << lines << " Modulus by 0" << endl << endl;
					errlog << "At line no: " << lines << " Modulus by 0 " << endl << endl;
					error_count++;
				}


				if ($2->getname() == "%"){
				if ($1->get_data_type()!="int" || $3->get_data_type()!="int" ){
					outlog << "At line no: " << lines << " Modulus operator on non integer type" << endl << endl;
					errlog << "At line no: " << lines << " Modulus operator on non integer type" << endl << endl;
					error_count++;
				}}
			}


			if ($3->get_is_function() && $3->get_return_type()=="void"){
				outlog << "At line no: " << lines << " operation on "<< $3->get_return_type()<<" type" << endl << endl;
				errlog << "At line no: " << lines << " operation on "<< $3->get_return_type()<<" type" << endl << endl;
				error_count++;
			}
				
	 }
     ;

unary_expression : ADDOP unary_expression  // un_expr can be void because of factor
		 {
	    	outlog << "At line no: " << lines << " unary_expression : ADDOP unary_expression " << endl << endl;
			outlog << $1->getname() << $2->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname() + $2->getname(), "operation");
			$$->set_is_operation();

			if ($2->get_is_function() && $2->get_return_type()=="void"){
				outlog << "At line no: " << lines << " operation on "<< $2->get_return_type()<<" type" << endl << endl;
				errlog << "At line no: " << lines << " operation on "<< $2->get_return_type()<<" type" << endl << endl;
				error_count++;
			}
	     }
		 | NOT unary_expression 
		 {
	    	outlog << "At line no: " << lines << " unary_expression : NOT unary_expression " << endl << endl;
			outlog << "!" << $2->getname() << endl << endl;
			
			$$ = new symbol_info("!" + $2->getname(), "un_expr");
	     }
		 | factor 
		 {
	    	outlog << "At line no: " << lines << " unary_expression : factor " << endl << endl;
			outlog << $1->getname() << endl << endl;
			
			$$ = new symbol_info($1->getname(), "un_expr");
			$$->set_data_type($1->get_data_type()); // Set float flag if factor is float

			if ($1->get_is_function()){
				$$->set_as_function($1->get_return_type(),$1->get_parameters());
	     	}
			if ($1->get_is_undefined_function()){
				$$->set_is_undefined_function();
			}

		 }
		 ;

	
factor	: variable
    {
	    outlog << "At line no: " << lines << " factor : variable " << endl << endl;
		outlog << $1->getname() << endl << endl;
			
		$$ = new symbol_info($1->getname(), "fctr");
		$$->set_data_type($1->get_data_type()); 
	}
	| ID LPAREN argument_list RPAREN
	{
	    outlog << "At line no: " << lines << " factor : ID LPAREN argument_list RPAREN " << endl << endl;
		outlog << $1->getname() << "(" << $3->getname() << ")" << endl << endl;

		symbol_info* var_info = get_variable_info($1->getname());



		$$ = new symbol_info($1->getname() + "(" + $3->getname() + ")", "fctr");

		if (var_info==NULL){ 
			outlog << "At line no: " << lines << " Undeclared function " << $1->getname() << endl << endl;
			errlog << "At line no: " << lines << " Undeclared function " << $1->getname() << endl << endl;
			$$->set_is_undefined_function();
			error_count++;
		}else if (var_info!=NULL){
			$$->set_as_function(var_info->get_return_type(),var_info->get_parameters());
			if (current_func_params.size()!=var_info->get_parameters().size()){
				outlog << "At line no: " << lines << " Inconsistencies in number of arguments in function call : " <<  $1->getname() << endl << endl;
				errlog << "At line no: " << lines << " Inconsistencies in number of arguments in function call : " <<  $1->getname() << endl << endl;
				error_count++;
			}
			else if(current_func_params.size()==var_info->get_parameters().size()){
				for (int i=0; i<current_func_params.size(); i++){
					symbol_info* v_info = get_variable_info(current_func_params[i].first);

					if (v_info!= NULL && v_info->get_is_array()==false ){

						if (current_func_params[i].second!=var_info->get_parameters()[i].first){
							outlog << "At line no: " << lines << " argument "<< i+1 << " type mismatch in function call : " <<  $1->getname() << endl << endl;
							errlog << "At line no: " << lines << " argument "<< i+1 << " type mismatch in function call : " <<  $1->getname() << endl << endl;
							error_count++;
						}
					}else if (v_info==NULL){

						if (current_func_params[i].second!=var_info->get_parameters()[i].first && current_func_params[i].second!="array"){
							outlog << "At line no: " << lines << " argument "<< i+1 << " type mismatch in function call : " <<  $1->getname() << endl << endl;
							errlog << "At line no: " << lines << " argument "<< i+1 << " type mismatch in function call : " <<  $1->getname() << endl << endl;
							error_count++;
						}
					}
				}
			}	
		}
			

		
		current_func_params.clear(); // Clear the current function parameters after use




		

	}
	| LPAREN expression RPAREN
	{
	   	outlog << "At line no: " << lines << " factor : LPAREN expression RPAREN " << endl << endl;
		outlog << "(" << $2->getname() << ")" << endl << endl;
		
		$$ = new symbol_info("(" + $2->getname() + ")", "fctr");
	}
	| CONST_INT 
	{
	    outlog << "At line no: " << lines << " factor : CONST_INT " << endl << endl;
		outlog << $1->getname() << endl << endl;
			
		$$ = new symbol_info($1->getname(), "fctr");
		$$->set_data_type("int");
	}
	| CONST_FLOAT
	{
	    outlog << "At line no: " << lines << " factor : CONST_FLOAT " << endl << endl;
		outlog << $1->getname() << endl << endl;
		$$ = new symbol_info($1->getname(), "fctr");
		$$->set_data_type("float"); // Set float flag
	}
	| variable INCOP 
	{
	    outlog << "At line no: " << lines << " factor : variable INCOP " << endl << endl;
		outlog << $1->getname() << "++" << endl << endl;
			
		$$ = new symbol_info($1->getname() + "++", "fctr");
	}
	| variable DECOP
	{
	    outlog << "At line no: " << lines << " factor : variable DECOP " << endl << endl;
		outlog << $1->getname() << "--" << endl << endl;
			
		$$ = new symbol_info($1->getname() + "--", "fctr");
	}
	;
	
argument_list : arguments
			  {
					outlog << "At line no: " << lines << " argument_list : arguments " << endl << endl;
					outlog << $1->getname() << endl << endl;
						
					$$ = new symbol_info($1->getname(), "arg_list");
			  }
			  |
			  {
					outlog << "At line no: " << lines << " argument_list :  " << endl << endl;
					outlog << "" << endl << endl;
						
					$$ = new symbol_info("", "arg_list");
			  }
			  ;
	
arguments : arguments COMMA logic_expression
		  {
				outlog << "At line no: " << lines << " arguments : arguments COMMA logic_expression " << endl << endl;
				outlog << $1->getname() << "," << $3->getname() << endl << endl;
				if (lines==44){
					symbol_info* var_info = get_variable_info($3->getname());

				}
				pair<string, string> param($3->getname(), $3->get_data_type());
				current_func_params.push_back(param);
						
						
				$$ = new symbol_info($1->getname() + "," + $3->getname(), "arg");
		  }
	      | logic_expression
	      {
				outlog << "At line no: " << lines << " arguments : logic_expression " << endl << endl;
				outlog << $1->getname() << endl << endl;
				if (lines==44){

				}
				pair<string, string> param($1->getname(), $1->get_data_type());
				current_func_params.push_back(param);
						
				$$ = new symbol_info($1->getname(), "arg");
		  }
	      ;
 

%%

int main(int argc, char *argv[])
{
	if(argc != 2) 
	{
		cout << "Please input file name" << endl;
		return 0;
	}
	yyin = fopen(argv[1], "r");
	outlog.open("22101704_log.txt", ios::trunc);
	errlog.open("22101704_error.txt", ios::trunc);


	if(yyin == NULL)
	{
		cout << "Couldn't open file" << endl;
		return 0;
	}

	table = new symbol_table(10);  
	
	yyparse();
	
	delete table;
	
	outlog << endl << "Total lines: " << lines << endl;
	outlog << "Total errors: " << error_count << endl;

	errlog << "Total errors: " << error_count << endl;
	outlog.close();
	fclose(yyin);
	
	return 0;
}