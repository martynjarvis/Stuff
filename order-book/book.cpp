#include "book.h"

Book::Book()
{
    buyTree = NULL;
    sellTree = NULL;
    lowSell = NULL;
    highBuy = NULL;
}

void Book::AddOrder(int timestamp,char id, bool isBid, int price, int size)
{
    Order * order = new Order(timestamp, id, isBid, price, size);
    if (isBid){// buy order
        if (buyTree != NULL){
            buyTree->Insert(order);
            if (highBuy!=NULL){
                if (price > highBuy->price){
                    highBuy = order->parentLimit;
                }
            }
            else{
                highBuy = order->parentLimit;
            }
        }
        else{
            buyTree = new Limit(order,this);
            highBuy = order->parentLimit;
        }
    }
    else{// sell order
        if (sellTree != NULL){
            sellTree->Insert(order);
            if (lowSell!=NULL){
                if (price < lowSell->price){
                    lowSell = order->parentLimit;
                }
            }
            else{
                lowSell = order->parentLimit;
            }
        }
        else{
            sellTree = new Limit(order,this);
            lowSell = order->parentLimit;
        }
    }
    
    // update maps
    orderMap[id] = order;
    priceMap[price] = order->parentLimit;
}

void Book::ReduceOrder(int timestamp,char id, int size)
{
    Order * order = orderMap[id];
    Limit * limit = order->parentLimit;
    assert(order!=NULL);
    assert(limit!=NULL);
    
    order->Reduce(size);
    
    if (order->size <= 0){ 
        //order depleted
        int price = order->price;
        delete order;
        orderMap.erase(id);  
        
        if  (limit->volume<=0){
            // limit has been depleted
            assert(limit->volume == 0);// just checking
            // correct running min/maxes
            if (limit==lowSell){
                lowSell = limit->parent;
            }
            if (limit==highBuy){
                highBuy = limit->parent;
            }
            Limit * y = limit->Remove(); // returns node that was spliced out
            delete y;
            priceMap.erase(price);  
        }
    }
}

int Book::Quote(int required, bool buy){

    Limit * x = GetBestOffer();
    int cost = 0;
    
    while (required>0 && x != NULL)
    {
        std::cout<<required<<',';
        if (required > x->volume){
            required -= x->volume;
            cost += x->volume*x->price;  
            x = x->Succesor();
        }
        else{
            cost += required*x->price;
            required = 0;
        }
    }
        std::cout<<std::endl;
    
    if (required <= 0){
        return cost;
    }
    else{
        return -1;
    }
}

int Book::GetVolumeAtLimit(int x){
    return priceMap[x]->volume;
}

Limit * Book::GetBestBid(){
    return highBuy;
}

Limit * Book::GetBestOffer(){
    return lowSell;
}