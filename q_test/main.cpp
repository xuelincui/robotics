#include <iostream>
#include <vector>
#include <string>
#include <functional>
#include <unordered_map>


using namespace std;

vector<string> letterCombinations(const string& digits) {

    vector<string> result;


    return result;

}

int main() {
    string digits;
    cout << "Enter digits (2-9): ";
    cin >> digits;

    vector<string> combos = letterCombinations(digits);

    cout << "Found " << combos.size() << " combination(s):\n";
    for (const string& c : combos) {
        cout << c << '\n';
    }

    return 0;
}