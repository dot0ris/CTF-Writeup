#include <algorithm>
#include "util.hpp"
#include "movement.hpp"

#define UNUSED __attribute__((unused))

std::function<std::string(Movement* const&)> Movement::getReprFunc = [](Movement* const &mv){ return mv->getRepr(); };


std::string BaseMove::getRepr() const
{
    return "\"" + escapestr(desc) + "\"";
}

std::vector<std::string> BaseMove::getStr() const
{
    return std::vector<std::string> {desc};
}

bool BaseMove::contains(const Movement *m UNUSED) const
{
    return false;
}


std::string RepetitionMove::getRepr() const
{
    return "Repetition(" + mv->getRepr() + ", " + std::to_string(repeat) + ")";
}

std::vector<std::string> RepetitionMove::getStr() const
{
    std::vector<std::string> mvvec = mv->getStr();
    std::vector<std::string> res;
    res.reserve(mvvec.size() * repeat);

    for (int i = 0; i < repeat; i++)
        res.insert(res.end(), mvvec.begin(), mvvec.end());

    return res;
}

bool RepetitionMove::contains(const Movement *m) const
{
    return mv == m || mv->contains(m);
}


std::string SequenceMove::getRepr() const
{
    return "Sequence([" + join(", ", mvs, Movement::getReprFunc) + "])";
}

std::vector<std::string> SequenceMove::getStr() const
{
    std::vector<std::string> res;

    for (auto &mv: mvs)
    {
        std::vector<std::string> mvvec = mv->getStr();
        res.insert(res.end(), mvvec.begin(), mvvec.end());
    }

    return res;
}

bool SequenceMove::contains(const Movement *m) const
{
    return std::any_of(mvs.begin(), mvs.end(), [m](const Movement *mv){ return mv == m || mv->contains(m); });
}


std::string AccumulationMove::getRepr() const
{
    return "Accumulation([" + join(", ", mvs, Movement::getReprFunc) + "])";
}

std::vector<std::string> AccumulationMove::getStr() const
{
    std::vector<std::vector<std::string>> mvsStrs;  // wow so sharp
    std::vector<std::string> res;

    for (auto &a: mvs)
        mvsStrs.push_back(a->getStr());

    for (int i = 0; i < (int)mvsStrs.size(); i++)
        for (int j = 0; j <= i; j++)
            res.insert(res.end(), mvsStrs[j].begin(), mvsStrs[j].end());
    
    return res;
}

bool AccumulationMove::contains(const Movement *m) const
{
    return std::any_of(mvs.begin(), mvs.end(), [m](const Movement *mv){ return mv == m || mv->contains(m); });
}


std::string ReversalMove::getRepr() const
{
    return "Reversal(" + mv->getRepr() + ")";
}

std::vector<std::string> ReversalMove::getStr() const
{
    std::vector<std::string> mvStrs = mv->getStr();
    std::vector<std::string> res;
    res.reserve(mvStrs.size());

    for (auto it = mvStrs.rbegin(); it <= mvStrs.rend(); it++)
    {
        std::string &cur = *it;
        res.push_back(std::move(cur));
        cur.clear();
    }

    return res;
}

bool ReversalMove::contains(const Movement *m) const
{
    return mv == m || mv->contains(m);
}


std::string RetrogradeMove::getRepr() const
{
    return "Retrograde(" + mv->getRepr() + ")";
}

std::vector<std::string> RetrogradeMove::getStr() const
{
    std::vector<std::string> mvStrs = mv->getStr();
    std::vector<std::string> res;
    res.reserve(mvStrs.size());

    for (auto it = mvStrs.rbegin(); it <= mvStrs.rend(); it++)
    {
        std::string &cur = *it;
        std::reverse(cur.begin(), cur.end());
        res.push_back(std::move(cur));
        cur.clear();
    }

    return res;
}

bool RetrogradeMove::contains(const Movement *m) const
{
    return mv == m || mv->contains(m);
}


std::string RevisedMove::getRepr() const
{
    return "Revise(" + base_mv->getRepr() + ", " +
        std::to_string(revision_at) + ", " +
        "\"" + escapestr(revise_to) + "\")";
}

std::vector<std::string> RevisedMove::getStr() const
{
    std::vector<std::string> mvStrs = base_mv->getStr();

    // again, attempt in-place replacement
    std::string &str = mvStrs.at(revision_at);
    str.replace(0, str.length(), revise_to);

    return mvStrs;
}

bool RevisedMove::contains(const Movement *m) const
{
    return base_mv == m || base_mv->contains(m);
}