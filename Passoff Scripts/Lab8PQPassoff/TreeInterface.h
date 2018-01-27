//YOU MAY NOT MODIFY THIS DOCUMENT

#pragma once

#include "NodeInterface.h"

using namespace std;

class TreeInterface {
public:
	TreeInterface() {}
	virtual ~TreeInterface() {}

	//Please note that the class that implements this interface must be made
	//of objects which implement the NodeInterface

	/*
	* Returns the root node for this tree
	*
	* @return the root node for this tree.
	*/
	virtual NodeInterface * getRootNode() const = 0;
};