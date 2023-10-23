```cpp
#include <iostream>

class A {
public:
    int x = 5;
};
class B : virtual public A {
public:
    int i = 6;
};
class C : virtual public A {
public:
    int i = 7;
};
class D : public B {

};

int main() {
    D obj;
    std::cout << obj.x << std::endl;

}```
