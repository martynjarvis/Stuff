/* 
  order.h
*/

#ifndef order_h
#define order_h

#include <iostream>

#include "limit.h"

//forward declaration
class Limit;

class Order
{
    public:
        Order(int timestamp, char id, bool isBid, int price, int size);
        ~Order();
        void Append(Order * newOrder);
        int Reduce(int size);
        void repr();
        Order * next;
        Order * prev;
        int timestamp;
        int price;
        int size;
        char id;
        bool isBid;
        Limit * parentLimit;
};

#endif