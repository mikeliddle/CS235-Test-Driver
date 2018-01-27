#include "Huffman.h"
#include <fstream>
#include <sstream>
#include <queue>
using namespace std;

const int NUM_FILES = 4; // the total number of files to be read from

const std::string fileArray[NUM_FILES] = { "file1.txt", "file2.txt", "file3.txt", "file4.txt" }; // the string array containing the file names

																								 // This will take a string temp and a Pathfinder object and will execute an instruction from the string
																								 // no return, but writes the results of the instruction into the ofs filestream
void parse_instruction(std::string temp, std::ofstream &ofs, Huffman* aptr);

// This function is a platform independent way of reading files of various line ending types.
// It's definiton is at the bottom of the file, don't worry if you don't understand it.
namespace ta {
	std::istream& getline(std::istream& is, std::string& line);
}

int main() {
	std::ifstream ifs; // create the stream to read in from the files
	std::ofstream ofs; // create the output stream to write to an output file
	std::string temp; // used to store the current instruction
	Huffman* huffmanptr = NULL;//the Huffman object

	for (int i = 0; i < NUM_FILES; i++) {
		ifs.open(fileArray[i]); // open the file to read from
		ofs.open("out_" + fileArray[i]); // open the file to write to
		huffmanptr = new Huffman();

		if (!ifs.is_open()) { // if the file did not open, there was no such file
			std::cout << "File " << i + 1 << " could not open, please check your lab setup" << std::endl;
		}
		else {
			std::cout << "Reading file" << i + 1 << ".txt..." << std::endl;
		}

		std::cout << "Beginning out_file" << i + 1 << ".txt write" << std::endl;
		while (ta::getline(ifs, temp)) { // while there are more instructions to get,
			parse_instruction(temp, ofs, huffmanptr); // parse the instructions using the Pathfinder
		}
		std::cout << "File write complete" << std::endl << std::endl;
		if (huffmanptr != NULL) {
			delete huffmanptr;
			huffmanptr = NULL;
		}
		ifs.close();
		ofs.close();
	}
	std::cout << "end" << std::endl; // indicate that the program has successfuly executed all instructions
	return 0;
}


//a function that takes a binary tree and returns a level-order string representation of the tree
//returns a string representation of the nodes in level order
string treeToString(TreeInterface* tree);

void parse_instruction(std::string temp, std::ofstream &ofs, Huffman* aptr) {
	std::string command, expression;
	std::stringstream ss(temp);

	if (!(ss >> command)) { return; } // get command, but if string was empty, return
	if (command == "read") { // command to read in the characters from a file and creates the huffman encoding in a tree
		if (aptr->createTree(ss.str().substr(5, std::string::npos))) { // use the rest of the stringstream as createTree input
			ofs << temp << " True" << std::endl;
		}
		else {
			ofs << temp << " False" << std::endl;
		}
	}
	else if (command == "printTree") { // command to make a huffman tree out of the most recently read file
		ofs << temp << "\n" << treeToString(aptr->getTree()) << std::endl;
	}
	else if (command == "printEncoding") { // command to print the huffman encoding from the map
		map<char, string> encodings = aptr->getEncodings();
		ofs << temp << "\n";
		for (pair<char, string> p : encodings) {
			ofs << p.first << ": " << p.second << std::endl;
		}
		ofs << std::endl;
	}
	else if (command == "encode") { // command to encode a message using the huffman encoding
		ofs << temp << "\n  " << aptr->encodeMessage(ss.str().substr(7, std::string::npos)) << std::endl;
	}
	else if (command == "decode") { // command to decode an encoded huffman message 
		ofs << temp << "\n  " << aptr->decodeMessage(ss.str().substr(7, std::string::npos)) << std::endl;

	}
	else { // invalid command, wrong input file format
		std::cout << "Command: \"" << command << "\"" << std::endl;
		std::cout << "Invalid command.  Do you have the correct input file?" << std::endl;
	}
}

//a function that takes a binary tree and returns a level-order string representation of the tree
//returns a string representation of the nodes in level order
string treeToString(TreeInterface* tree) {
	queue<NodeInterface*> readQ; // used to read in the levels of the tree, contains Node*
	stringstream nodeReader_ss; // used to store the values of the nodes and the level-order sequence
	int depth = 0; // the depth of a node on the tree

	if (tree->getRootNode() == NULL) {
		return "Tree is empty";
	}

	readQ.push(tree->getRootNode()); // push the root node of the tree into the queue

	while (!readQ.empty()) { // as long as the queue has a remaining node:
		int i = readQ.size(); // store the number of nodes on this level of the tree
		nodeReader_ss << depth << ":  ";
		for (; i > 0; i--) { // for each node on this level,
			NodeInterface* nextNode = readQ.front(); // store the next node in the queue
													 //nodeReader_ss << nextNode->getCharacter() << ":" << nextNode->getFrequency() << " ";//ENABLE THIS LINE to print full tree 
			if (nextNode->getCharacter() != '\0') nodeReader_ss << nextNode->getCharacter() << ":" << nextNode->getFrequency() << " "; //DISABLE THIS LINE and enable previous line to print full tree
			if (nextNode->getLeftChild() != NULL) { // if there is a left child, push the left child into the queue
				readQ.push(nextNode->getLeftChild());
			}
			if (nextNode->getRightChild() != NULL) { // if there is a right child, push the left child into the queue
				readQ.push(nextNode->getRightChild());
			}
			readQ.pop(); // pop the node off of the queue, leaving its children in the queue
		}
		nodeReader_ss << "\n"; // push an endl into the ss to distinguish levels
		depth++;
	}

	return nodeReader_ss.str();
}






// Version of getline which does not preserve end of line characters
namespace ta {
	std::istream& getline(std::istream& in, std::string& line) {
		line.clear();

		std::istream::sentry guard(in, true); // Use a sentry to maintain the state of the stream
		std::streambuf *buffer = in.rdbuf();  // Use the stream's internal buffer directly to read characters
		int c = 0;

		while (true) { // Continue to loop until a line break if found (or end of file)
			c = buffer->sbumpc(); // Read one character
			switch (c) {
			case '\n': // Unix style, return stream for further parsing
				return in;
			case '\r': // Dos style, check for the following '\n' and advance buffer if needed
				if (buffer->sgetc() == '\n') { buffer->sbumpc(); }
				return in;
			case EOF:  // End of File, make sure that the stream gets flagged as empty
				in.setstate(std::ios::eofbit);
				return in;
			default:   // Non-linebreak character, go ahead and append the character to the line
				line.append(1, (char)c);
			}
		}
	}
}
