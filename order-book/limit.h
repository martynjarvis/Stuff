/* 
  limit.h
    Represents a single limit price
*/

#ifndef limit_h
#define limit_h

#include <assert.h> 

#include "order.h"
#include "book.h"

//forward declaration
class Order;
class Book;

class Limit
{
    public:
        Limit( Order * order, Book * book );
        void Insert(Order * order);
        Limit * Remove();
        Limit * GetMin();
        Limit * GetMax();
        Limit * Succesor( );
        Limit * Predecessor( );
        Limit * parent;
        Limit * left;
        Limit * right;
        Order * head;
        Order * tail;
        Book * book;
        int volume;
        int price;
};


#endif