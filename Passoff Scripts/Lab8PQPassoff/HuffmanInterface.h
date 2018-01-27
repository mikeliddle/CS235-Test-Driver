#pragma once
#include <iostream>
#include <string>
#include <map>
#include "TreeInterface.h"
using namespace std;

/*
WARNING: Do not modify any part of this document, including its name
*/
class HuffmanInterface
{
public:
	HuffmanInterface() {}
	virtual ~HuffmanInterface() {}

	/**
	* This method is called to generate your tree.  Returns true if the filename given was valid, else false.  Other methods
	* will be used to encode/decode the message or return the tree.
	*
	* @param filename The name of the file containing characters that should be used to create the tree
	*/
	virtual bool createTree(string filename) = 0;



	/**
	* This method is called to encode a message into 1s and 0s using the tree created by the createTree method.
	*
	* @param toEncode The message to be encoded
	*
	* @return The encoded message, or an empty string if the text could not be encoded
	*/
	virtual string encodeMessage(string toEncode) = 0;



	/**
	* This method is called to decode a message consisting of 1s and 0s back into characters using the tree that was created by the createTree method.
	*
	* @param toDecode The encoded message (1s and 0s) that should be decoded
	*
	* @return The decoded message, or an empty string if the text could not be decoded
	*/
	virtual string decodeMessage(string toDecode) = 0;

	/**
	* This method is called to return the tree created using the createTree method. It must inherit from TreeInterface.
	*
	* @return A pointer to a TreeInterface. Returns NULL if no tree has been generated.
	*/
	virtual TreeInterface * getTree() = 0;

	/**
	* This method is called to return a map that contains all of the current encodings
	* in the tree that was created by the createTree method.
	*
	* @return A map with the key = char and value = encoding.
	* I.E.
	* If your tree holds: a-01, b-00, c-1
	* Your map would look like this:
	* a->01
	* b->00
	* c->1
	*/
	virtual map<char, string> getEncodings() = 0;
};
