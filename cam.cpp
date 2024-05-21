#include <iostream>
// include library for file streams

using namespace std;
int fun(int& x)
{
		x = x + 2;
		// prints 5
		cout << x;
}
int main()
{
		int x = 3;
		fun(x);
		// prints 5，与上面不同
		cout << x;
}