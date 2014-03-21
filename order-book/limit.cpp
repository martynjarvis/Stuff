#include "limit.h"

Limit::Limit( Order * order, Book * book )
{
    price = order->price;
    volume = order->size;
    parent=NULL;
    left=NULL;
    right=NULL;
    head=order;
    tail=order;  
    order->parentLimit = this;
    this->book = book;
}

Limit * Limit::Remove(){
    assert(volume==0);
    Limit * x = NULL;
    Limit * y = NULL;
    
    // determine node to splice out
    if (left==NULL || right==NULL){
        y = this;
    }
    else{
        y = this->Succesor();
    }
    
    // find non NULL child of node
    if (y->left != NULL){
        x = y->left;
    }
    else{
        x = y->right;
    }
    
    // splice out node
    if (x!=NULL && y->parent != NULL){
        x->parent = y->parent;
    }
    if (y->parent == NULL){
        if (y==book->buyTree){
            book->buyTree = x;
        }
        else if (y==book->sellTree){
            book->sellTree = x;
        }
        else{
            assert(0);//non root tree with no parent...
        }
    }
    else if (y == y->parent->left){
        y->parent->left = x;
    }
    else{
        y->parent->right = x;
    }
    
    
    if (y!=this){
        price = y->price;
        volume = y->volume;
        parent = y->parent;
        left = y->left ;
        right = y->right;
        head = y->head;
        tail = y->tail;
        book->priceMap[price]=this;
    }
    return y;
}

void Limit::Insert(Order * order){
    Limit * y = NULL;
    Limit * x = this;
    while (x != NULL)
    {
        y = x;
        if (order->price < x->price)
        {
            x = x->left;
        }
        else
        {
            x = x->right;
        }
    }
    if (y==NULL)
    {
        // tree is empty
        assert(0);
    }
    else
    {
        if (order->price < y->price)
        {
            Limit * newLimit =  new Limit(order,book);
            y->left = newLimit;
            newLimit->parent = y;
        }
        else if (order->price == y->price)
        {
            if (y->tail!=NULL)
            {
                y->tail->Append(order);
            }
            else { // empty list
                y->head=order;
                y->tail=order;
            }
            order->parentLimit = y;
            y->volume += order->size;
        }        
        else if (order->price > y->price)
        {
            Limit * newLimit =  new Limit(order,book);
            y->right = newLimit;
            newLimit->parent = y;
        }
    }
    return;
}

Limit * Limit::GetMin()
{
    Limit * x = this;
    while (x->left != NULL){
        x = x->left;
    }
    return x;    
}

Limit * Limit::GetMax()
{
    Limit * x = this;
    while (x->right != NULL){
        x = x->right;
    }
    return x;    
}

Limit * Limit::Succesor( ){  
    if (right!=NULL){
        return right->GetMin();
    }
    Limit * y = parent;
    if (y==NULL){// lone node (stump)
        return y;
    }
    Limit * x = y->right;
    while(y!=NULL && x==y->right){
        x = y;
        y = y->parent;
    }
    return y;    
}

Limit * Limit::Predecessor( ){
    if (left!=NULL){
        return left->GetMax();
    }
    Limit * y = parent;
    Limit * x = y->left;
    while(y!=NULL && x==y->left){
        x = y;
        y = y->parent;
    }
    return y;    
}

