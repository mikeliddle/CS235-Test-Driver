//  ===================main.cpp====================//
//  Author:    Michael Liddle                      //
//  Class:     CS 236                              //
//  Project:   Datalog Interpreter                 //
//  Email:     maliddle96@gmail.com                //
//                                                 //
//  Purpose:  This program is a Datalog            //
//  Interpreter.  So far the implementation        //
//  includes a lexical analyzer(Tokenizer), a      //
//  datalog parser, and now a RDBMS.  It reads in  //
//  a datalog file(subset of prolog) and interprets//
//  the facts to be relations in the database, and //
//  the schemes to be the layout the tables will   //
//  hold with the queries being queries to the     //
//  database tables.                               //
//                                                 //
#include "Lexer.h"
#include "DatalogParser.h"
#include "Printer.h"
#include "DatabaseManager.h"

enum modes { DEBUG, PASS_OFF };

bool fileNotValid(int argC, modes mode, char* argV[])
{
	if (mode == DEBUG)
	{
		return false;
	}
	if (argC != 2)
	{
		return true;
	}
	std::ifstream testOpen;
	testOpen.open(argV[1]);
	if (testOpen.fail())
	{
		return true;
	}
	return false;
}

int main(int argC, char* argV[])
{
	//DEBUG to run in VisualStudio, PASS_OFF for command line.  
	modes mode = PASS_OFF;
	//process input arguments
	if (fileNotValid(argC, mode, argV))
	{
		/* TODO: for now I will comment this out and change the mode to DEBUG here.
		std::cout << "USAGE: " << argV[0] << " <inputFileName>" << std::endl;
		return 0;
		*/
		mode = DEBUG;
	}

	Lexer* lexicalAnalyzer = new Lexer();

	std::string filePath = mode == PASS_OFF ? std::string(argV[1]) : "OptimizationTestCases/customTest5.txt";

	if (filePath != "")
	{
		lexicalAnalyzer->analyzeFile(filePath);
		DatalogParser* parser = new DatalogParser(lexicalAnalyzer->getTokens());
		Token returnedValue = *(parser->ParseFile());
		if (returnedValue.getType() == VALID_END)
		{
			DatabaseManager* dbManager = new DatabaseManager(parser->getSchemes(), parser->getFacts());
			dbManager->applyOptimizedRules(parser->getRules());
			//dbManager->printRuleReport();
			dbManager->doQueries(parser->getQueries());
		}
		else
		{
			std::cout << "Failure!\n  " << std::endl;
			std::cout << returnedValue.toDescriptionString();
		}
		delete parser;
	}
	delete lexicalAnalyzer;
}
