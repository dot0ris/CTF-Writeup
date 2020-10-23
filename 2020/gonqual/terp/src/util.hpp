#pragma once

#include <string>
#include <vector>
#include <functional>
#include <numeric>

template<typename T, typename A>
std::string join(std::string join_by, std::vector<T, A> const &vec, std::function<std::string(T const&)> &lambda)
{
    return vec.empty() ? "" :
        std::accumulate(vec.begin() + 1, vec.end(), lambda(vec[0]),
            [join_by, lambda](const std::string &l, T const &r){
                    return l + join_by + lambda(r);
            }
        );
}

bool isalnum(const std::string& S);
bool isid(const std::string& S);
bool getUnescString(std::stringstream &SS, std::string &res);
std::string unescapestr(const std::string& S);
std::string escapestr(const std::string& S);