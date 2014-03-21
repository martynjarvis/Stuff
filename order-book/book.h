/* 
  book.h
*/

#ifndef book_h
#define book_h

#include <unordered_map>
#include <assert.h> 

#include "limit.h"
#include "order.h"

//forward declaration
class Order;
class Limit;

class Book
{
    public:
        Book();
        void AddOrder(int timestamp,char id, bool isBid, int price, int size);
        void ReduceOrder(int timestamp,char id, int size);
        Limit * GetBestOffer();
        Limit * GetBestBid();
        int GetVolumeAtLimit(int x);
        int Price(int targetSize);
        Limit * buyTree;
        Limit * sellTree;
        Limit * lowSell;
        Limit * highBuy;
        std::unordered_map <char, Order*> orderMap;
        std::unordered_map <int, Limit*> priceMap;
        Limit * buyCache;
        Limit * sellCache;
};

#endif