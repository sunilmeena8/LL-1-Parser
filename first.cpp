#include <bits/stdc++.h>
using namespace std;

map<char,vector<string>> mp;

void print_set(set<char> s) {
	for(auto i: s) {
	    cout<< i<< " ";
	}
	cout<<endl;
}
//To calculate first function
set<char> first(char S,map<char,int> m) {
   set<char> s;
    m[S] = 1;
    s.insert(S);
    if(mp.find(S) == mp.end()) return s;
    s.clear();
    for(auto i: mp[S]) {
        if(i[0] == '^') s.insert(i[0]);
        else if(i[0] >= 'A' && i[0] <= 'Z') {
            if(m[i[0]] == 0) {
                m[i[0]] = 1;
                set<char> ans = first(i[0],m);
                for(auto j: ans) {
                    s.insert(j);
                }
            }
        }
        else s.insert(i[0]);
    }
    return s;
}

void check(){
    for(auto i=mp.begin();i!=mp.end();i++) {
        cout<<i->first<<" "<<i->second[0]<<endl;
    }
}

//Till Now NULL case not covered.
set<char> follow(char S,map<char,int> m) {
    set<char> s;
    //if s is a terminal
    s.insert(S);
    if(mp.find(S) == mp.end()) return s;
    s.clear();
    m[S] = 1;
    for(auto ch= mp.begin();ch!=mp.end();ch++){
    for(auto i: ch->second) {
        for(int j=0;j<i.length();j++) {
            if(i[j] == S){
                if(j<i.length()-1){
                    int flag = 0;
                    if(i[j+1]>='A' && i[j+1] <='Z') {
                        if(m[i[j+1]] == 0) {
                            m[i[j+1]] = 1;
                            map<char,int> m2 = m;
                            set<char> ans = first(i[j+1],m);
                            m=m2;
				m[i[j+1]] = 0;
                            for(auto k: ans) {
                                if(k != '^') s.insert(k);
                                else flag = 1;//if first is null then see first of next char
                            }
                        }
                        if(flag == 1){
                        	if(m[ch->first] == 0){
                               		m[ch->first] = 1;
                                	set<char> ans = follow(ch->first,m);
                       
                                	for(auto k: ans) {
                                     		s.insert(k);
                                 	}
					flag = 0;
                                }
                       }
                    }
                    else s.insert(i[j+1]);
                }
                else{
                   // cout<<ch->first<<endl;
                        //set<char> ans = follow(ch->first,m);
                    if(m[ch->first] == 0){
                        map<char,int> m2 = m;
                        set<char> ans = follow(ch->first,m);
                       
                       m=m2;
                       m[ch->first] = 1;
                        for(auto k: ans) {
                            s.insert(k);
                        }
                    }
                     
                }
            }
        }
    }
    }

 
    return s;
}//Driver function
int main() {
	mp['E'] = {"bBED","a123ExyBz","DE"};
	mp['B'] = {"wxyz"};
	mp['D'] = {"hi","ev ery"};
	map<char,int> m;
	set<char> s = first('E',m);
    print_set(s);
    s = first('D',m);
    print_set(s);
    m.clear();
    s=follow('B',m);
    print_set(s);
    m.clear();
    s=follow('D',m);
    print_set(s);
    m.clear();
    s=follow('E',m);
    print_set(s);
    check();
	
    return 0;
}
