#include <iostream>
#include <string>
#include <sstream>

#include "book.h"
#include "limit.h"
#include "order.h"

int main()
{

    Book * book = new Book();
    int targetSize = 200;
    
    int bestBuy = 9999999999999999;
    int bestSell = 0;
    
    while (true) {
        std::string input = "";
        getline(std::cin, input);
        std::stringstream ss(input);
        int timestamp; 
        float fPrice;
        int price; 
        int size;
        char type;
        char id;
        char sellBuy;
        if(ss>>timestamp>>type>>id){
            if (type == 'A')
            {
                assert(ss>>sellBuy>>fPrice>>size);           
                price = (int) (fPrice*100);
                bool isBid;
                if (sellBuy == 'B'){
                    isBid = true;
                }
                else if (sellBuy == 'S'){
                    isBid = false;
                }
                else{
                    assert(0);
                }
                book->AddOrder(timestamp,id,isBid,price,size);
            }
            else if (type == 'R')
            {
                assert(ss>>size);
                book->ReduceOrder(timestamp,id,size);
            }
        }
        else{
            return 0;
        }
    }
    return 0;
}


