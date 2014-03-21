#include "order.h"

Order::Order(int timestamp, char id, bool isBid, int price, int size)
{
    this->timestamp = timestamp;
    this->id = id;
    this->isBid = isBid;
    this->price = price;
    this->size = size;
    this->next = NULL;
    this->prev = NULL;
    this->parentLimit = NULL;
}

void Order::Append(Order * newOrder)
{
    Order * n = this;
    while (n->next != NULL){
        n = n->next;
    }
    n->next = newOrder;
    newOrder->prev = n;
}

int Order::Reduce(int size)
{
    this->size -= size;
    this->parentLimit->volume -= size;
    this->timestamp = timestamp;
    return this->size;
}

Order::~Order()
{
    // correct links
    if (next != NULL){
        next->prev = prev;
    }
    else{
        // I'm the tail
        parentLimit->tail = prev;
    }
    
    if (prev != NULL){
        prev->next = next;
    }
    else{
        // I'm the head
        parentLimit->head = next;
    }
    
    // did we exhaust a limit?
    if  (parentLimit->head == NULL && parentLimit->tail ==NULL){
        //delete parentLimit; // actually lets not delete it.
    }  
    
    // correct running totals
    parentLimit->volume -= size;
}

void Order::repr()
{
    std::cout<<this->id;
    if (next != NULL){
        std::cout<<'-';
        next->repr();
    }
}
